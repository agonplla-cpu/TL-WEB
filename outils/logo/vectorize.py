import os, sys
import numpy as np, potrace
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'logo_raster.png')
OUTDIR = sys.argv[2] if len(sys.argv) > 2 else '.'
im = np.asarray(Image.open(SRC).convert('L')).astype(np.float32)
im = im[:, 7:1174]                      # crop to ink bbox horizontally
# smooth slightly then threshold at mid-grey for accurate edges
from PIL import ImageFilter
pil = Image.fromarray(im.astype(np.uint8)).resize((im.shape[1]*3, im.shape[0]*3), Image.BICUBIC).filter(ImageFilter.GaussianBlur(2.4))
a = np.asarray(pil).astype(np.float32)
bm = potrace.Bitmap(a)  # values > 127.5 = background
path = bm.trace(turdsize=20, turnpolicy=potrace.POTRACE_TURNPOLICY_MINORITY, alphamax=1.1, opticurve=True, opttolerance=0.8)
W, H = a.shape[1], a.shape[0]
s = 1/3
def f(p): return f"{p.x*s:.2f},{p.y*s:.2f}"
d = []
for curve in path:
    d.append("M" + f(curve.start_point))
    for seg in curve.segments:
        if seg.is_corner:
            d.append("L" + f(seg.c) + "L" + f(seg.end_point))
        else:
            d.append("C" + f(seg.c1) + " " + f(seg.c2) + " " + f(seg.end_point))
    d.append("Z")
D = "".join(d)
w, h = W*s, H*s
svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" role="img" aria-label="TL Propreté"><path fill="#092094" fill-rule="evenodd" d="{D}"/></svg>'
open(os.path.join(OUTDIR,'tl-logo-full.svg'),'w').write(svg)
print(len(path), 'curves', len(svg), 'bytes', w, h)

# split monogram (TL) and wordmark (TL PROPRETÉ)
mono, word = [], []
def bbox(curve):
    pts=[curve.start_point]+[seg.end_point for seg in curve.segments]
    return min(p.y for p in pts)*s, max(p.y for p in pts)*s
def dcurve(curve):
    out=["M"+f(curve.start_point)]
    for seg in curve.segments:
        out.append(("L"+f(seg.c)+"L"+f(seg.end_point)) if seg.is_corner else ("C"+f(seg.c1)+" "+f(seg.c2)+" "+f(seg.end_point)))
    return "".join(out)+"Z"
allpts=[]
for c in path:
    y0,y1=bbox(c)
    (mono if y1<1530 else word).append(c)
import re
def write(curves,name,pad=4):
    D="".join(dcurve(c) for c in curves)
    nums=[float(v) for v in re.findall(r'-?\d+\.?\d*',D)]
    xs,ys=nums[0::2],nums[1::2]
    x0,y0,x1,y1=min(xs)-pad,min(ys)-pad,max(xs)+pad,max(ys)+pad
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.1f} {y0:.1f} {x1-x0:.1f} {y1-y0:.1f}" role="img" aria-label="TL Propreté"><path fill="#092094" fill-rule="evenodd" d="{D}"/></svg>'
    open(name,'w').write(svg); print(name,len(curves),'curves',f'{x1-x0:.0f}x{y1-y0:.0f}')
write(mono,os.path.join(OUTDIR,'tl-monogram.svg'))
write(word,os.path.join(OUTDIR,'tl-wordmark.svg'))
