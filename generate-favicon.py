#!/usr/bin/env python3
"""
Rasterize favicon.svg into a multi-resolution favicon.ico.

Browsers request /favicon.ico at the site root whether or not a <link rel="icon">
points there, and some link-preview and feed bots only look for the .ico. Shipping
only favicon.svg means every one of those requests 404s.

Run from the site root after changing favicon.svg:

    python3 generate-favicon.py

Georgia is the same face the SVG asks for, so this stays visually identical to the
vector version rather than being a separate drawing.
"""

from PIL import Image, ImageDraw, ImageFont

# Mirrors favicon.svg: 64-unit viewBox, rx=12, "A" at font-size 38, baseline y=45.
VIEWBOX = 64
RENDER = 256  # render large, then let ICO downsampling do the anti-aliasing
SCALE = RENDER / VIEWBOX

INK = "#1c1813"
COPPER = "#c77b3c"
FONT = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"

ICO_SIZES = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]


def main() -> None:
    img = Image.new("RGBA", (RENDER, RENDER), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle(
        [0, 0, RENDER - 1, RENDER - 1], radius=round(12 * SCALE), fill=INK
    )
    font = ImageFont.truetype(FONT, round(38 * SCALE))
    # anchor="ms" = horizontally centered on the baseline, matching the SVG's
    # text-anchor="middle" + y=45 baseline.
    draw.text(
        (RENDER / 2, 45 * SCALE), "A", font=font, fill=COPPER, anchor="ms"
    )
    img.save("favicon.ico", sizes=ICO_SIZES)
    print(f"wrote favicon.ico ({len(ICO_SIZES)} sizes: "
          f"{', '.join(str(w) for w, _ in ICO_SIZES)})")


if __name__ == "__main__":
    main()
