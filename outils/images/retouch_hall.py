"""Retouch of the 4x-upscaled hall photo: remove the door stop and the door notice,
then a light finishing pass (very mild contrast curve + fine sharpening).
Tone is kept close to the original: the warm glow of the lamps on the wood is the point."""
import sys
import cv2
import numpy as np

SRC = sys.argv[1] if len(sys.argv) > 1 else "hall_x4_raw.png"   # sortie de upscale.py
DST = sys.argv[2] if len(sys.argv) > 2 else "hall_hd.png"
img = cv2.imread(SRC)  # BGR
H, W = img.shape[:2]


def poly_mask(poly):
    m = np.zeros((H, W), np.uint8)
    cv2.fillPoly(m, [np.array(poly, np.int32)], 255)
    return m


def clone_patch(img, poly, dx, dy):
    """Fill `poly` with texture from the same shape shifted by (dx, dy), Poisson-blended."""
    mask = poly_mask(poly)
    M = np.float32([[1, 0, -dx], [0, 1, -dy]])
    shifted = cv2.warpAffine(img, M, (W, H), borderMode=cv2.BORDER_REFLECT)
    x, y, w, h = cv2.boundingRect(mask)
    return cv2.seamlessClone(shifted, img, mask, (x + w // 2, y + h // 2), cv2.NORMAL_CLONE)


# 1) door stop on the white marble. The black band edge runs from (1138,1500) to (1250,1732);
#    the mask stays a few px left of it so no dark pixels enter the Poisson boundary.
def band_x(y):
    return 1138 + (y - 1500) * (112 / 232)

top, bot = 1606, 1702
stop = [(1126, top), (int(band_x(top)) - 6, top), (int(band_x(bot)) - 6, bot), (1126, bot)]
img = clone_patch(img, stop, dx=-100, dy=0)

# 2) paper notice on the glass door. The glass behind it only varies across columns
#    (frame edges) and has horizontal bands, so rebuild each row by interpolating
#    between the clean pixels just left and right of the notice.
y0, y1, xl, xr = 808, 1012, 1421, 1502
f = img.astype(np.float32)
left = f[y0:y1, xl - 3:xl].mean(1)            # (rows, 3)
right = f[y0:y1, xr:xr + 3].mean(1)
left = cv2.GaussianBlur(left[:, None, :], (1, 0), sigmaX=0.1, sigmaY=1.5)[:, 0, :]
right = cv2.GaussianBlur(right[:, None, :], (1, 0), sigmaX=0.1, sigmaY=1.5)[:, 0, :]
t = np.linspace(0, 1, xr - xl)[None, :, None]
fill = left[:, None, :] * (1 - t) + right[:, None, :] * t
fill += np.random.default_rng(1).normal(0, 1.2, fill.shape)  # keep a little grain
# feathered alpha so the patch melts into its surroundings
alpha = np.zeros((y1 - y0, xr - xl), np.float32)
alpha[4:-4, 3:-3] = 1
alpha = cv2.GaussianBlur(alpha, (0, 0), 2)[..., None]
f[y0:y1, xl:xr] = f[y0:y1, xl:xr] * (1 - alpha) + fill * alpha
img = np.clip(f, 0, 255).astype(np.uint8)

# 3) very mild S-curve on luminance only
lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
L, A, B = cv2.split(lab)
x = np.arange(256, dtype=np.float32) / 255.0
curve = np.clip((x - 0.018 * np.sin(2 * np.pi * x)) * 255.0, 0, 255).astype(np.uint8)
img = cv2.cvtColor(cv2.merge([cv2.LUT(L, curve), A, B]), cv2.COLOR_LAB2BGR)

# 4) fine unsharp mask (small radius = texture of the wood grain and marble)
blur = cv2.GaussianBlur(img, (0, 0), 0.9)
img = cv2.addWeighted(img, 1.3, blur, -0.3, 0)

cv2.imwrite(DST, img)
print("done", img.shape)
