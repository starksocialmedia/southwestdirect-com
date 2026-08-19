#!/usr/bin/env python3
"""
Generate assets/joffrey-long.vcf with the portrait embedded as base64.

Usage:  python3 tools/build-vcard.py

iOS Contacts is unreliable about fetching a remote PHOTO;VALUE=uri at import
time, so the image is embedded directly. That is also why the source is
downscaled hard: the whole .vcf has to stay small enough to hand around.
"""
import base64, io, os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "images", "_src", "joffrey-long.png")
DEST = os.path.join(ROOT, "assets", "joffrey-long.vcf")

PHONE = "+18186351777"
EMAIL = "info@asksw.com"
PHOTO_PX = 400
JPEG_QUALITY = 85
# Square crop window on the source, chosen to sit the face near the centre of
# the frame — iOS masks contact photos to a circle, so edges get eaten.
CROP_TOP = 20


def portrait_b64():
    im = Image.open(SRC)
    im.load()
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        flat = Image.new("RGB", im.size, (255, 255, 255))
        flat.paste(im, mask=im.split()[-1])
        im = flat
    else:
        im = im.convert("RGB")

    side = min(im.width, im.height - CROP_TOP)
    left = (im.width - side) // 2
    im = im.crop((left, CROP_TOP, left + side, CROP_TOP + side))
    im = im.resize((PHOTO_PX, PHOTO_PX), Image.LANCZOS)

    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=False)
    raw = buf.getvalue()
    print(f"  portrait: {PHOTO_PX}x{PHOTO_PX} JPEG q{JPEG_QUALITY}, {len(raw):,} bytes")
    return base64.b64encode(raw).decode("ascii"), len(raw)


def fold(line):
    """RFC 2426 folding: 75 octets per line, continuations begin with one space.

    Counted in octets, not characters, and never split inside a multi-byte
    UTF-8 sequence — the NOTE field carries middle dots.
    """
    out, first = [], True
    while line:
        limit = 75 if first else 74
        take = len(line)
        while len(line[:take].encode("utf-8")) > limit:
            take -= 1
        out.append(line[:take] if first else " " + line[:take])
        line = line[take:]
        first = False
    return out


def main():
    b64, raw_len = portrait_b64()

    props = [
        "BEGIN:VCARD",
        "VERSION:3.0",
        "FN:Joffrey Long",
        "N:Long;Joffrey;;;",
        "PHOTO;ENCODING=b;TYPE=JPEG:" + b64,
        "ORG:Southwest Bancorp",
        "TITLE:Direct Hard-Money Lender",
        f"TEL;TYPE=WORK,VOICE:{PHONE}",
        f"EMAIL;TYPE=WORK:{EMAIL}",
        "ADR;TYPE=WORK:;;5151 California Ave STE 100;Irvine;CA;92617-3205;USA",
        "URL:https://southwestdirect.com",
        "NOTE:California DRE Broker License 00525142 · NMLS 207202 · 43 years hard-money lending",
        "END:VCARD",
    ]

    lines = []
    for prop in props:
        lines += fold(prop)

    with open(DEST, "w", encoding="utf-8", newline="") as f:
        f.write("\r\n".join(lines) + "\r\n")

    size = os.path.getsize(DEST)
    print(f"  wrote {DEST}")
    print(f"  base64: {len(b64):,} chars, {len(lines)} folded lines total")
    print(f"  total .vcf: {size:,} bytes ({size/1024:.1f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
