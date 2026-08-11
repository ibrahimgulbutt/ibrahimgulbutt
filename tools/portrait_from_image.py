#!/usr/bin/env python3
"""Regenerate assets/portrait.txt from a photograph.

    python3 tools/portrait_from_image.py photo.jpg --crop 224 248 410 496

The defaults are tuned for a lit face against a dark background, which is the hard
case: the skin is uniformly bright, so a naive luminance ramp turns the whole face
into one solid block. Three things fix that.

  clarity   a large-radius unsharp mask lifts facial structure (eyes, nose, the
            shadow under the lip) without the halos a small radius would give
  vignette  a blurred ellipse mask kills whatever is behind the head
  levels    everything below `--floor` is crushed to pure black, so the background
            is silent instead of speckled with stray characters

Requires Pillow.
"""

import argparse
import pathlib

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAMP = " .`:;~=+r*?xnuwm#%@"


def render(path, crop, cols, floor, clarity, aspect):
    im = Image.open(path).convert("L")
    if crop:
        im = im.crop(tuple(crop))
    im = ImageOps.autocontrast(im, cutoff=1)
    im = im.filter(ImageFilter.UnsharpMask(radius=9, percent=clarity, threshold=1))

    w, h = im.size
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).ellipse((0, int(h * -0.04), w, int(h * 1.08)), fill=255)
    im = Image.composite(im, Image.new("L", (w, h), 0), mask.filter(ImageFilter.GaussianBlur(20)))

    im = im.point(lambda v: 0 if v < floor else int((v - floor) * 255 / (255 - floor)))
    im = im.resize((cols, round(h / w * cols * aspect)), Image.LANCZOS)

    n, px = len(RAMP), im.load()
    return "\n".join(
        "".join(RAMP[min(n - 1, px[x, y] * n // 256)] for x in range(im.width)).rstrip()
        for y in range(im.height)
    )


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("--crop", nargs=4, type=int, metavar=("L", "T", "R", "B"))
    ap.add_argument("--cols", type=int, default=76)
    ap.add_argument("--floor", type=int, default=74, help="below this is pure black")
    ap.add_argument("--clarity", type=int, default=105)
    ap.add_argument("--aspect", type=float, default=0.455, help="glyph height:width")
    a = ap.parse_args()

    art = render(a.image, a.crop, a.cols, a.floor, a.clarity, a.aspect)
    out = ROOT / "assets" / "portrait.txt"
    out.write_text(art + "\n", encoding="utf-8")
    print(f"wrote {out} ({max(len(r) for r in art.split(chr(10)))} cols, "
          f"{len(art.split(chr(10)))} rows)")
    print("now run: python3 tools/build.py")
