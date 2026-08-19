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
import os, sys, json
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
        "Residential-Rental-Property.jpg", [400, 750, 1100], (750, 400), "Residential Rental Property"),
    "automotive-service-centers": (
        "Automotive-Service-Centers.webp", [400, 750, 1100], (750, 400), "Automotive / Service Centers"),
    "mixed-use": (
        "Mix-Use.webp", [400, 750, 1100], (750, 400), "Mixed Use Properties"),
    "industrial-warehouse": (
        "Industrial-Warehouse.webp", [400, 750, 1100], (750, 400), "Industrial / Warehouse"),
    "other-property-types": (
        "Other-Property-Types.webp", [400, 750, 1100], (750, 400), "Other Property Types"),
    # Full-bleed coastal band that sits between the contact section and the footer.
    # The design's own asset for this was an AI illustration and was pulled, so this
    # placeholders until a licensed photo lands in images/_src/.
    "california-band": (
        "california-band.jpg", [768, 1280, 1920], (1920, 320), "California coastline"),
}

# Slugs that must render a "PHOTO PENDING" placeholder even though a source file
# exists, because the source itself is unusable. Remove the entry and drop the
# real photo into images/_src/ to restore it.
FORCE_PLACEHOLDER = {
    # (empty) — v2 of the design replaced the broken Residential photo.
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
        # Scale off the smaller dimension so a short, very wide band does not
        # get billboard-sized lettering.
        size = max(15, min(w, h * 2) // 26)
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
    made, placeheld, manifest = 0, [], {}
    for slug, (fname, widths, ph_size, label) in SPEC.items():
        print(f"  {slug}")
        if slug in FORCE_PLACEHOLDER:
            print(f"    -> PLACEHOLDER (forced): {FORCE_PLACEHOLDER[slug]}")
            im = None
        else:
            im = load(os.path.join(SRC, fname))
        is_placeholder = im is None
        if is_placeholder:
            if slug not in FORCE_PLACEHOLDER:
                print(f"    -> PLACEHOLDER (source '{fname}' missing or truncated)")
            im = placeholder(*ph_size, label)
            placeheld.append((slug, fname))
        built = []
        for w in widths:
            if w > im.width:
                continue                          # never upscale
            h = round(im.height * w / im.width)
            rs = im.resize((w, h), Image.LANCZOS)
            rs.save(os.path.join(OUT, f"{slug}-{w}.webp"), "WEBP", quality=82, method=6)
            rs.save(os.path.join(OUT, f"{slug}-{w}.jpg"),  "JPEG", quality=82,
                    optimize=True, progressive=True)
            made += 2
            built.append([w, h])
            print(f"    {w}px -> {slug}-{w}.webp + .jpg")
        manifest[slug] = {
            "widths":      [w for w, _ in built],
            "intrinsic":   built[-1] if built else list(ph_size),
            "placeholder": is_placeholder,
            "label":       label,
        }
    with open(os.path.join(OUT, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2, sort_keys=True)
        f.write("\n")
    print(f"\n  {made} files written to images/  (+ manifest.json)")
    if placeheld:
        print(f"\n  !! {len(placeheld)} PLACEHOLDER(S) — real photos still needed:")
        for slug, fname in placeheld:
            print(f"       {slug}  (expects images/_src/{fname})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
