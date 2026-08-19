#!/usr/bin/env python3
"""Render the 1200x630 Open Graph card: branding, headline, credentials, portrait."""
import os, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORTRAIT = os.path.join(ROOT, "images", "_src", "joffrey-long.png")
DEST = os.path.join(ROOT, "assets", "og-image.jpg")

NAVY=(30,42,94); NAVY_D=(20,29,64); CREAM=(250,250,247); GOLD=(184,135,75)
GOLD_L=(193,150,97); LAV=(201,203,218)
SER="/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
SANS_B="/System/Library/Fonts/Supplemental/Arial Bold.ttf"
SANS="/System/Library/Fonts/Supplemental/Arial.ttf"
W,H=1200,630

def main():
    img=Image.new("RGB",(W,H),NAVY); d=ImageDraw.Draw(img)
    d.rectangle([0,0,W,9], fill=GOLD)

    # portrait, right third, faded into the navy at its left edge
    p=Image.open(PORTRAIT); p.load()
    if p.mode!="RGB":
        p=p.convert("RGBA"); bgc=Image.new("RGB",p.size,NAVY); bgc.paste(p,mask=p.split()[-1]); p=bgc
    side=min(p.width,p.height); p=p.crop(((p.width-side)//2,0,(p.width+side)//2,side))
    pw=430; p=p.resize((pw,pw), Image.LANCZOS)
    px,py=W-pw-40,(H-pw)//2
    mask=Image.new("L",(pw,pw),255); md=ImageDraw.Draw(mask)
    for i in range(90):                      # soft left edge so it sits on the navy
        md.rectangle([i,0,i,pw], fill=int(255*i/90))
    img.paste(p,(px,py),mask)

    f_eye=ImageFont.truetype(SANS_B,21); f_h=ImageFont.truetype(SER,72)
    f_sub=ImageFont.truetype(SANS,26); f_brand=ImageFont.truetype(SER,34)
    f_dom=ImageFont.truetype(SANS_B,19); f_cred=ImageFont.truetype(SANS,18)
    x=76
    d.text((x,86),"DIRECT HARD-MONEY LENDER  ·  CALIFORNIA",font=f_eye,fill=GOLD_L)
    d.text((x,136),"Got the Deal?",font=f_h,fill=CREAM)
    d.text((x,218),"Get it Closed!",font=f_h,fill=CREAM)
    d.text((x,330),"Direct hard-money lending for",font=f_sub,fill=LAV)
    d.text((x,364),"California real estate investors.",font=f_sub,fill=LAV)
    d.line([(x,432),(x+140,432)],fill=GOLD,width=3)
    d.text((x,456),"Joffrey Long",font=f_brand,fill=CREAM)
    d.text((x+2,500),"SOUTHWESTDIRECT.COM",font=f_dom,fill=GOLD_L)
    d.text((x,548),"DRE #00898122  ·  NMLS #285731  ·  43 years",font=f_cred,fill=LAV)

    img.save(DEST,"JPEG",quality=88,optimize=True,progressive=True)
    print(f"  wrote {DEST}  {img.size}  {os.path.getsize(DEST):,} bytes")
    return 0

if __name__=="__main__": sys.exit(main())
