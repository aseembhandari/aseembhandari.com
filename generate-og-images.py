#!/usr/bin/env python3
"""Generate per-page Open Graph cards (1200x630) into og/.

Brand: warm paper bg, near-black ink, copper accent. Uses Georgia/Menlo
(closest installed cousins of Fraunces / IBM Plex Mono). Re-run after
adding a page and add an entry to PAGES below.
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
PAPER, INK, COPPER, SOFT = "#f6f2ea", "#1c1813", "#a8591c", "#5f5a52"

SERIF = "/System/Library/Fonts/Supplemental/Georgia.ttf"
SERIF_I = "/System/Library/Fonts/Supplemental/Georgia Italic.ttf"
MONO = "/System/Library/Fonts/Menlo.ttc"

PAGES = [
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


def card(slug, title, kicker):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 14], fill=COPPER)  # masthead press-bar
    mono_s = ImageFont.truetype(MONO, 26)
    mono_xs = ImageFont.truetype(MONO, 22)

    d.text((90, 96), kicker, font=mono_s, fill=COPPER)
    d.line([90, 148, 210, 148], fill=COPPER, width=3)

    size = 84
    while size > 44:
        serif = ImageFont.truetype(SERIF, size)
        lines = wrap(d, title, serif, W - 180)
        if len(lines) <= 3:
            break
        size -= 6
    y = 190
    for ln in lines:
        d.text((86, y), ln, font=serif, fill=INK)
        y += int(size * 1.18)

    d.line([90, H - 110, W - 90, H - 110], fill="#e6dfd2", width=2)
    d.text((90, H - 84), "ASEEM BHANDARI", font=mono_s, fill=INK)
    right = "aseembhandari.com"
    d.text((W - 90 - d.textlength(right, font=mono_xs), H - 80), right, font=mono_xs, fill=SOFT)

    img.save(f"og/{slug}.png", optimize=True)
    print(f"og/{slug}.png")


if __name__ == "__main__":
    os.makedirs("og", exist_ok=True)
    for slug, title, kicker in PAGES:
        card(slug, title, kicker)
