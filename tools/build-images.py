#!/usr/bin/env python3
"""
Build responsive image derivatives for southwestdirect.com.

Reads originals from images/_src/ and writes WebP + JPEG derivatives at the
widths each image is actually displayed at, into images/.

Usage:  python3 tools/build-images.py

Any source that is missing or unreadable gets a clearly-marked "photo pending"
placeholder at the correct aspect ratio, so the preview stays reviewable.
Drop the real file into images/_src/ and re-run to replace it.
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC  = os.path.join(ROOT, "images", "_src")
OUT  = os.path.join(ROOT, "images")

CREAM = (250, 250, 247)

# slug -> (source filename, [widths], (placeholder_w, placeholder_h), label)
SPEC = {
    "joffrey-long": (
        "joffrey-long.png", [320, 640, 748], (748, 839), "Portrait of Joffrey Long"),
    "residential-rental-property": (
        "Residential-Rental-Property.webp", [400, 750], (750, 400), "Residential Rental Property"),
    "automotive-service-centers": (
        "Automotive-Service-Centers.webp", [400, 750], (750, 400), "Automotive / Service Centers"),
    "mixed-use": (
        "Mix-Use.webp", [400, 750], (750, 400), "Mixed Use Properties"),
    "industrial-warehouse": (
        "Industrial-Warehouse.webp", [400, 750], (750, 400), "Industrial / Warehouse"),
    "other-property-types": (
        "Other-Property-Types.webp", [400, 750], (750, 400), "Other Property Types"),
}


def load(path):
    """Return a fully-decoded RGB image, or None if the file is missing/corrupt."""
    if not os.path.exists(path):
        return None
    try:
        im = Image.open(path)
        im.load()                       # forces full decode; truncated files raise here
    except Exception as e:
        print(f"    ! unreadable ({e})")
        return None
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        flat = Image.new("RGB", im.size, CREAM)
        flat.paste(im, mask=im.split()[-1])
        return flat
    return im.convert("RGB")


def placeholder(w, h, label):
    im = Image.new("RGB", (w, h), (236, 232, 222))
    d = ImageDraw.Draw(im)
    step = max(18, w // 32)
    for x in range(-h, w + h, step * 2):          # diagonal hatch
        d.line([(x, 0), (x + h, h)], fill=(229, 225, 216), width=step)
    try:
        size = max(15, w // 26)
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", size)
        small = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", max(12, size - 6))
    except Exception:
        font = small = ImageFont.load_default()
    for txt, f, dy in (("PHOTO PENDING", font, -size), (label, small, size // 2)):
        bb = d.textbbox((0, 0), txt, font=f)
        d.text(((w - (bb[2] - bb[0])) / 2, (h - (bb[3] - bb[1])) / 2 + dy),
               txt, fill=(92, 86, 77), font=f)
    return im


def main():
    os.makedirs(OUT, exist_ok=True)
    made, placeheld = 0, []
    for slug, (fname, widths, ph_size, label) in SPEC.items():
        print(f"  {slug}")
        im = load(os.path.join(SRC, fname))
        if im is None:
            print(f"    -> PLACEHOLDER (source '{fname}' missing or truncated)")
            im = placeholder(*ph_size, label)
            placeheld.append((slug, fname))
        for w in widths:
            if w > im.width:
                continue                          # never upscale
            h = round(im.height * w / im.width)
            rs = im.resize((w, h), Image.LANCZOS)
            rs.save(os.path.join(OUT, f"{slug}-{w}.webp"), "WEBP", quality=82, method=6)
            rs.save(os.path.join(OUT, f"{slug}-{w}.jpg"),  "JPEG", quality=82,
                    optimize=True, progressive=True)
            made += 2
            print(f"    {w}px -> {slug}-{w}.webp + .jpg")
    print(f"\n  {made} files written to images/")
    if placeheld:
        print(f"\n  !! {len(placeheld)} PLACEHOLDER(S) — real photos still needed:")
        for slug, fname in placeheld:
            print(f"       {slug}  (expects images/_src/{fname})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
