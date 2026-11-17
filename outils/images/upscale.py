"""Real-ESRGAN x4plus upscaling on CPU with ncnn, tiled with overlap."""
import os, sys, time
import numpy as np
import ncnn
from PIL import Image

# Poids du modèle (non versionnés) : realesrgan-x4plus.param / .bin, format ncnn
MODEL = os.environ.get("REALESRGAN_MODEL", "models/realesrgan-x4plus")
SCALE = 4


def make_net(threads=2):
    net = ncnn.Net()
    net.opt.use_vulkan_compute = False
    net.opt.num_threads = threads
    net.opt.use_fp16_storage = False
    net.opt.use_fp16_arithmetic = False
    net.load_param(MODEL + ".param")
    net.load_model(MODEL + ".bin")
    return net


def run_tile(net, tile):
    # tile: HxWx3 float32 in 0..1 -> CHW
    chw = np.ascontiguousarray(tile.transpose(2, 0, 1))
    ex = net.create_extractor()
    ex.input("data", ncnn.Mat(chw))
    _, out = ex.extract("output")
    return np.array(out).transpose(1, 2, 0)


def upscale(src, dst, tile=192, pad=16):
    img = np.asarray(Image.open(src).convert("RGB")).astype(np.float32) / 255.0
    h, w, _ = img.shape
    out = np.zeros((h * SCALE, w * SCALE, 3), np.float32)
    net = make_net()
    t0 = time.time()
    ys = list(range(0, h, tile))
    xs = list(range(0, w, tile))
    n = len(ys) * len(xs)
    k = 0
    for y in ys:
        for x in xs:
            y0, x0 = max(y - pad, 0), max(x - pad, 0)
            y1, x1 = min(y + tile + pad, h), min(x + tile + pad, w)
            res = run_tile(net, img[y0:y1, x0:x1])
            # crop the padding back off
            cy0, cx0 = (y - y0) * SCALE, (x - x0) * SCALE
            th, tw = (min(y + tile, h) - y) * SCALE, (min(x + tile, w) - x) * SCALE
            out[y * SCALE:y * SCALE + th, x * SCALE:x * SCALE + tw] = res[cy0:cy0 + th, cx0:cx0 + tw]
            k += 1
            print(f"tile {k}/{n}  {time.time() - t0:.0f}s", flush=True)
    out = (np.clip(out, 0, 1) * 255.0 + 0.5).astype(np.uint8)
    Image.fromarray(out).save(dst)
    print("saved", dst, out.shape, f"{time.time() - t0:.0f}s")


if __name__ == "__main__":
    upscale(sys.argv[1], sys.argv[2], *(int(a) for a in sys.argv[3:]))
