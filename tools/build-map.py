#!/usr/bin/env python3
"""
Render a static map of the office location by stitching OpenStreetMap tiles.

Usage:  python3 tools/build-map.py

Writes images/_src/office-map.png. Run tools/build-images.py afterwards to
produce the WebP/JPEG derivatives the page actually serves.

Replaces the interactive OSM iframe, which captured the scroll wheel over the
Contact section. A single business location does not need pan/zoom on the page;
the image links out to OpenStreetMap for anyone who wants directions.

OSM tile policy: this fetches ~20 tiles once, with a descriptive User-Agent, and
the required attribution is burned into the image and repeated as page text.
"""
import math, os, sys, urllib.request
from PIL import Image, ImageDraw, ImageFont

# Geocoded from "5151 California Ave, Irvine, CA 92617" via OSM Nominatim.
# The design's original marker sat ~1.7km north-east of the actual address.
LAT, LON, ZOOM = 33.64074, -117.85386, 16
OUT_W, OUT_H = 1040, 760
TILE = 256
UA = "SouthwestDirect-static-map/1.0 (nathan@starksocial.com)"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(ROOT, "images", "_src", "office-map.png")

NAVY = (30, 42, 94)
CREAM = (250, 250, 247)


def deg2px(lat, lon, z):
    n = 2.0 ** z * TILE
    x = (lon + 180.0) / 360.0 * n
    lat_r = math.radians(lat)
    y = (1.0 - math.asinh(math.tan(lat_r)) / math.pi) / 2.0 * n
    return x, y


def fetch(z, x, y):
    url = f"https://tile.openstreetmap.org/{z}/{x}/{y}.png"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return Image.open(__import__("io").BytesIO(r.read())).convert("RGB")


def main():
    cx, cy = deg2px(LAT, LON, ZOOM)
    left, top = cx - OUT_W / 2, cy - OUT_H / 2
    x0, y0 = int(left // TILE), int(top // TILE)
    x1, y1 = int((left + OUT_W) // TILE), int((top + OUT_H) // TILE)

    canvas = Image.new("RGB", ((x1 - x0 + 1) * TILE, (y1 - y0 + 1) * TILE), (233, 229, 220))
    count = 0
    for tx in range(x0, x1 + 1):
        for ty in range(y0, y1 + 1):
            try:
                canvas.paste(fetch(ZOOM, tx, ty), ((tx - x0) * TILE, (ty - y0) * TILE))
                count += 1
            except Exception as e:
                print(f"    ! tile {ZOOM}/{tx}/{ty} failed: {e}")
    print(f"  {count} tiles fetched at z{ZOOM}")

    ox, oy = int(left - x0 * TILE), int(top - y0 * TILE)
    img = canvas.crop((ox, oy, ox + OUT_W, oy + OUT_H))

    # marker pin at the exact office coordinate (dead centre)
    d = ImageDraw.Draw(img, "RGBA")
    mx, my = OUT_W // 2, OUT_H // 2
    r, stem = 17, 22
    d.polygon([(mx - 9, my + 6), (mx + 9, my + 6), (mx, my + stem)], fill=NAVY + (255,))
    d.ellipse([mx - r - 2, my - r - 2, mx + r + 2, my + r + 2], fill=CREAM + (255,))
    d.ellipse([mx - r, my - r, mx + r, my + r], fill=NAVY + (255,))
    d.ellipse([mx - 6, my - 6, mx + 6, my + 6], fill=CREAM + (255,))

    # required attribution, burned in
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 15)
    except Exception:
        font = ImageFont.load_default()
    txt = "© OpenStreetMap contributors"
    bb = d.textbbox((0, 0), txt, font=font)
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    d.rectangle([OUT_W - w - 18, OUT_H - h - 16, OUT_W, OUT_H], fill=(255, 255, 255, 200))
    d.text((OUT_W - w - 9, OUT_H - h - 11), txt, fill=(60, 60, 60), font=font)

    os.makedirs(os.path.dirname(DEST), exist_ok=True)
    img.save(DEST, "PNG", optimize=True)
    print(f"  wrote {DEST}  {img.size}  {os.path.getsize(DEST):,} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
