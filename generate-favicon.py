#!/usr/bin/env python3
"""
Rasterize favicon.svg into a multi-resolution favicon.ico.

Browsers request /favicon.ico at the site root whether or not a <link rel="icon">
points there, and some link-preview and feed bots only look for the .ico. Shipping
only favicon.svg means every one of those requests 404s.

Run from the site root after changing favicon.svg:

    python3 generate-favicon.py

The mark is pure geometry (a PCB stator seen from above: copper ring, eight coil
spokes, centre bore) so this draws the same shapes as the SVG — no font involved.
"""

import math
from PIL import Image, ImageDraw

VIEWBOX = 64
RENDER = 256  # render large, then let ICO downsampling do the anti-aliasing
S = RENDER / VIEWBOX

SLATE = "#0F151B"
AMBER = "#E0A030"

ICO_SIZES = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]


def ring(draw, cx, cy, r, width, fill):
    w = width / 2
    draw.ellipse([cx - r - w, cy - r - w, cx + r + w, cy + r + w], outline=fill, width=max(1, round(width)))


def main() -> None:
    img = Image.new("RGBA", (RENDER, RENDER), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, RENDER - 1, RENDER - 1], radius=round(8 * S), fill=SLATE)
    cx = cy = 32 * S
    ring(d, cx, cy, 22 * S, 3 * S, AMBER)          # outer copper ring
    ring(d, cx, cy, 6 * S, 2.5 * S, AMBER)         # centre bore
    for k in range(8):                              # eight coil spokes, radius 13 → 22 units
        a = math.radians(k * 45)
        x0, y0 = cx + math.cos(a) * 13 * S, cy + math.sin(a) * 13 * S
        x1, y1 = cx + math.cos(a) * 22 * S, cy + math.sin(a) * 22 * S
        d.line([x0, y0, x1, y1], fill=AMBER, width=round(3 * S))
    img.save("favicon.ico", sizes=ICO_SIZES)
    print(f"wrote favicon.ico ({len(ICO_SIZES)} sizes: {', '.join(str(w) for w, _ in ICO_SIZES)})")


if __name__ == "__main__":
    main()
