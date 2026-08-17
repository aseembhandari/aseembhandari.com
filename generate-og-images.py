#!/usr/bin/env python3
"""Generate Open Graph cards (1200x630): og/<slug>.png for every page, plus the
homepage's og-image.png at the site root.

Brand ("the CAM view", light): white ground with a fine plotting grid, an amber
press-bar, copper line work, Barlow Condensed display type and IBM Plex Mono labels —
the same system as styles.css. The homepage card carries the PCB-stator drawing.

Fonts: Barlow Condensed SemiBold and IBM Plex Mono Medium are fetched once from the
google/fonts repo into a local cache (~/Library/Caches/aseembhandari-fonts). If the
download fails, Arial Narrow / Menlo stand in.

Re-run after adding a page and add an entry to PAGES below.
"""
import math
import os
import urllib.request
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
PAPER = "#FFFFFF"
AMBER = "#E0A030"        # press-bar and eyebrow mark
COPPER = "#A0620C"       # line work — deep enough to read on white
ACC_TEXT = "#8A5D0F"     # accent text on white
INK, SOFT = "#0F151B", "#5F6A76"
OUTLINE = "#6B7684"

CACHE = os.path.expanduser("~/Library/Caches/aseembhandari-fonts")
FONT_SOURCES = {
    "display": ("BarlowCondensed-SemiBold.ttf",
                "https://github.com/google/fonts/raw/main/ofl/barlowcondensed/BarlowCondensed-SemiBold.ttf",
                "/System/Library/Fonts/Supplemental/Arial Narrow Bold.ttf"),
    "mono": ("IBMPlexMono-Medium.ttf",
             "https://github.com/google/fonts/raw/main/ofl/ibmplexmono/IBMPlexMono-Medium.ttf",
             "/System/Library/Fonts/Menlo.ttc"),
}

PAGES = [
    # slug, title, kicker
    ("home",              "Leading the shift from prototype to repeatable production.", "MANUFACTURING LEADERSHIP · NPI · MES · SPC"),
    ("blog-mes-build",    "Why we built our own MES — and shipped it to two factories.", "MES · LEADERSHIP"),
    ("blog-pilot-build",  "The pilot build is a question, not a milestone.", "NPI · PROCESS"),
    ("blog-yield-signal", "Reading a yield signal: from noise to a ranked cause list.", "YIELD · ROOT-CAUSE"),
    ("blog-spc-system",   "Building an SPC system operators actually use.", "PROCESS · DATA"),
    ("blog",              "Knowledge Hub — notes from the floor.", "ARTICLES"),
    ("work-infinitum",    "Building the line for a new kind of motor.", "INFINITUM · ELECTRIC MACHINES"),
    ("work-velodyne",     "Making precision sensors yield at volume.", "VELODYNE · LIDAR"),
    ("work-fabrinet",     "High-volume optics, held to spec.", "FABRINET · OPTICAL ASSEMBLY"),
    ("spc-tools",         "SPC & Capability Calculators.", "INTERACTIVE TOOLS"),
    ("pcbdebug",          "PCB / SMT Defect Debugger.", "INTERACTIVE TOOL"),
    ("npi-checklist",     "NPI Readiness Checklist.", "INTERACTIVE TOOL"),
]


def font_path(kind):
    name, url, fallback = FONT_SOURCES[kind]
    os.makedirs(CACHE, exist_ok=True)
    p = os.path.join(CACHE, name)
    if not os.path.exists(p):
        try:
            urllib.request.urlretrieve(url, p)
        except Exception as e:  # offline: use the closest installed face
            print(f"  ({name} download failed: {e}; using {fallback})")
            return fallback
    return p


def wrap(draw, text, font, max_w):
    lines, line = [], ""
    for word in text.split():
        trial = (line + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w:
            line = trial
        else:
            lines.append(line)
            line = word
    lines.append(line)
    return lines


def stator(img, cx, cy, R, alpha=255):
    """Top-copper of a PCB stator: 12 coil sectors of nested loops, vias, bore, outline."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    amber = (160, 98, 12, alpha)      # COPPER
    outline = (107, 118, 132, alpha)  # OUTLINE
    N, loops = 12, 8
    r_out0, r_in0, step = R * 205 / 260, R * 84 / 260, R * 6.4 / 260

    def pt(r, a):
        t = math.radians(a)
        return (cx + r * math.cos(t), cy + r * math.sin(t))

    def arc_pts(r, a0, a1, n=14):
        return [pt(r, a0 + (a1 - a0) * i / n) for i in range(n + 1)]

    for i in range(N):
        a0 = -90 + i * 360 / N
        for k in range(loops):
            ro, ri = r_out0 - k * step, r_in0 + k * step * 0.5
            hwo, hwi = 13.4 - k * 1.32, 10.6 - k * 1.02
            pts = arc_pts(ro, a0 - hwo, a0 + hwo) + arc_pts(ri, a0 + hwi, a0 - hwi)
            d.line(pts + [pts[0]], fill=amber, width=2)
        x, y = pt(r_out0 - 2.6, a0 - 13.4 + .85)
        d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=amber)
        x, y = pt(r_in0 + loops * step * .5 + 2.5, a0)
        d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=amber)
    for r in (r_out0 + 14 * R / 260, 52 * R / 260):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=outline, width=2)
    for j in range(6):
        x, y = pt(66 * R / 260, -90 + j * 60 + 30)
        rr = 4.5 * R / 260
        d.ellipse([x - rr, y - rr, x + rr, y + rr], outline=outline, width=2)
    img.alpha_composite(layer)
    return img


def card(slug, title, kicker, display, mono):
    img = Image.new("RGBA", (W, H), PAPER)
    # plotting grid, fading in from the left
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    for x in range(0, W, 44):
        gd.line([x, 0, x, H], fill=(15, 21, 27, 255))
    for y in range(0, H, 44):
        gd.line([0, y, W, y], fill=(15, 21, 27, 255))
    fade = Image.linear_gradient("L").rotate(-90, expand=True).resize((W, H)).point(lambda v: 5 + v * 12 // 255)
    g.putalpha(Image.composite(fade, Image.new("L", (W, H), 0), g.getchannel("A")))
    img.alpha_composite(g)

    d = ImageDraw.Draw(img)
    home = slug == "home"
    if home:
        stator(img, W - 250, H // 2 + 10, 240)
        d = ImageDraw.Draw(img)
    else:
        stator(img, W - 112, 196, 100, alpha=78)
        d = ImageDraw.Draw(img)

    d.rectangle([0, 0, W, 8], fill=AMBER)                       # amber press-bar
    mono_s = ImageFont.truetype(mono, 24)
    mono_xs = ImageFont.truetype(mono, 21)
    d.rectangle([90, 100, 104, 114], fill=AMBER)                # eyebrow mark
    d.text((122, 96), kicker, font=mono_s, fill=ACC_TEXT)

    max_w = (W - 600) if home else (W - 330)
    size = 96
    while size > 48:
        f = ImageFont.truetype(display, size)
        lines = wrap(d, title, f, max_w)
        if len(lines) <= 3 and 160 + len(lines) * size <= H - 130:
            break
        size -= 4
    y = 160
    for ln in lines:
        d.text((88, y), ln, font=f, fill=INK)
        y += int(size * 1.0)

    d.line([90, H - 104, W - 90, H - 104], fill=(15, 21, 27, 38), width=1)
    d.text((90, H - 78), "ASEEM BHANDARI", font=mono_s, fill=INK)
    right = "aseembhandari.com"
    d.text((W - 90 - d.textlength(right, font=mono_xs), H - 75), right, font=mono_xs, fill=SOFT)

    out = "og-image.png" if home else f"og/{slug}.png"
    img.convert("RGB").save(out, optimize=True)
    print(out)


if __name__ == "__main__":
    os.makedirs("og", exist_ok=True)
    display, mono = font_path("display"), font_path("mono")
    for slug, title, kicker in PAGES:
        card(slug, title, kicker, display, mono)
