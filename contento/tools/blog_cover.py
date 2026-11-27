#!/usr/bin/env python3
"""Euribia Digital blog cover compositor (locked 12.11.2026).

usage: blog_cover.py IMAGE OUT.jpg [--chip "Google Search" --chip-pos tl|bl|tr] [--logo auto|white|dark] [--preview]

- Output 2752x1536 JPG (the live blog standard). The image is cover-cropped to fill.
- Real euribia digital logo, 335 px wide, right edge 440 px from the frame edge (inside the 4:3 grid crop), top at y=150. The image prompt must keep that top-right corner empty.
  "auto" picks white or dark by the brightness under the logo.
- Optional glass topic chip (Mulish Bold, purple dot), x=440 from the edge (inside the 4:3 grid crop).
  Default is NO chip. Use it only where the image has calm space, and check it by eye.
- --preview also writes OUT_grid.jpg: the 4:3 centre crop the /blog listing shows.
"""
import sys, os, argparse
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageStat

W, H = 2752, 1536
LOGOS = {'white': '/tmp/bc/logo_white.png', 'dark': '/tmp/bc/logo_dark.png'}
LOGO_SVG = os.path.expanduser('~/.claude/contento/assets/brand/euribia-digital-logo-{}.svg')
FONT = os.path.expanduser('~/Library/Fonts/Mulish-VariableFont_wght.ttf')

def logo_png(v):
    import os, subprocess
    p = f'/tmp/bc/logo_{v}.png'
    if not os.path.exists(p):
        os.makedirs('/tmp/bc', exist_ok=True)
        html = f'/tmp/bc/l_{v}.html'
        open(html, 'w').write(f'<html><body style="margin:0;background:transparent"><img src="file://{LOGO_SVG.format(v)}" style="width:670px;display:block"></body></html>')
        subprocess.run(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--headless=new', '--disable-gpu', '--hide-scrollbars',
                        '--default-background-color=00000000', '--window-size=670,263', f'--screenshot={p}', f'file://{html}'], capture_output=True)
    return Image.open(p).convert('RGBA')

def cover_fill(im):
    s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((x, y, x + W, y + H))

def font(size, style='Bold'):
    f = ImageFont.truetype(FONT, size)
    try: f.set_variation_by_name(style)
    except Exception: pass
    return f

def main():
    a = argparse.ArgumentParser(); a.add_argument('image'); a.add_argument('out')
    a.add_argument('--chip'); a.add_argument('--chip-pos', default='tl', choices=['tl','bl','tr']); a.add_argument('--logo', default='auto'); a.add_argument('--preview', action='store_true')
    o = a.parse_args()
    base = cover_fill(Image.open(o.image).convert('RGB')).convert('RGBA')

    # logo
    lg = logo_png('white'); lw = 335; lh = round(lg.height * lw / lg.width)
    lx, ly = W - 440 - lw, 150
    v = o.logo
    if v == 'auto':
        lum = ImageStat.Stat(base.crop((lx, ly, lx + lw, ly + lh)).convert('L')).mean[0]
        v = 'dark' if lum > 150 else 'white'
    lg = logo_png(v).resize((lw, lh), Image.LANCZOS)
    base.alpha_composite(lg, (lx, ly))

    # glass chip
    if o.chip:
        f = font(40, 'Bold'); tw = f.getlength(o.chip)
        ch = 92; cw = int(tw + 46 + 22 + 50)
        cx = {'tl': 440, 'bl': 440, 'tr': W - 440 - cw}[o.chip_pos]; cy = 140 if o.chip_pos != 'bl' else 1396 - ch
        box = (cx, cy, cx + cw, cy + ch)
        mask = Image.new('L', (W, H), 0); ImageDraw.Draw(mask).rounded_rectangle(box, radius=ch // 2, fill=255)
        blurred = base.filter(ImageFilter.GaussianBlur(28))
        base = Image.composite(blurred, base, mask)
        ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
        lum = ImageStat.Stat(base.crop(box).convert('L')).mean[0]
        dark = lum > 140
        d.rounded_rectangle(box, radius=ch // 2, fill=(255, 255, 255, 120 if dark else 60), outline=(255, 255, 255, 190), width=2)
        d.ellipse((cx + 34, cy + ch // 2 - 9, cx + 52, cy + ch // 2 + 9), fill=(191, 64, 255, 255))
        d.text((cx + 68, cy + ch // 2), o.chip, font=f, fill=(13, 13, 13, 255) if dark else (255, 255, 255, 255), anchor='lm')
        base.alpha_composite(ov)

    out = base.convert('RGB'); out.save(o.out, quality=90)
    if o.preview:
        gx = (W - round(H * 4 / 3)) // 2
        out.crop((gx, 0, W - gx, H)).resize((666, 500)).save(o.out.rsplit('.', 1)[0] + '_grid.jpg', quality=85)
    print(o.out, 'logo=' + v)

if __name__ == '__main__': main()
