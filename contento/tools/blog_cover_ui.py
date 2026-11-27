#!/usr/bin/env python3
"""Euribia Digital blog cover v3: real photo + UI cards with REAL text (rendered in Chrome).

usage: blog_cover_ui.py spec.json out.jpg [--preview]

The spec is JSON. Coordinates use a 1376x768 canvas (rendered at 2x = 2752x1536, the blog standard).
Keep everything inside x 220..1150 (the /blog grid crops to 4:3, plus a margin). The logo sits top-right, right edge at x=1150.
{
  "background": "/abs/photo.jpg",  "bg_blur": 6, "bg_dim": 0.35, "bg_pos": "center",
  "logo": "auto" | "white" | "dark",
  "elements": [
    {"type":"status",  "x":200,"y":150,"w":520, "title":"Google Search Status", "subtitle":"Класиране",
       "rows":[{"label":"…","value":"…","state":"ok|warn|bad|info"}]},
    {"type":"ranking", "x":720,"y":360,"w":420, "title":"Позиции в Google",
       "items":[{"label":"твоят-магазин.bg","delta":3}]},
    {"type":"metric",  "x":..,"y":..,"w":..,  "value":"14","label":"дни", "note":"…"},
    {"type":"bars",    "x":..,"y":..,"w":..,  "title":"…", "bars":[{"label":"Пн","value":40}], "highlight":2, "unit":""},
    {"type":"chat",    "x":..,"y":..,"w":..,  "q":"…", "a":"…", "who":"ChatGPT"},
    {"type":"notice",  "x":..,"y":..,"w":..,  "app":"Google Ads", "title":"…", "text":"…", "time":"сега"},
    {"type":"chip",    "x":..,"y":..,        "text":"…", "dot":"#bf40ff"}
  ]
}
Optional per element: "rot" (degrees, keep within ±4), "z" (stack order), "scale".
Top level "scale" (default 1.15) enlarges all elements; place x/y for the scaled size.
"""
import json, sys, os, html, subprocess, tempfile, argparse
from PIL import Image, ImageStat

CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
FONT = os.path.expanduser('~/Library/Fonts/Mulish-VariableFont_wght.ttf')
LOGO = os.path.expanduser('~/.claude/contento/assets/brand/euribia-digital-logo-{}.svg')
W, H = 1376, 768
SCALE = [1.0]  # spec "scale" (default 1.15) enlarges every element from its top-left corner
e = lambda s: html.escape(str(s))

CSS = """
@font-face{font-family:Mulish;src:url('file://%(font)s');font-weight:200 1000}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:%(W)dpx;height:%(H)dpx;overflow:hidden;font-family:Mulish,sans-serif;color:#0d0d0d}
.bg{position:absolute;inset:-%(pad)dpx;background:url('file://%(bg)s') %(pos)s/cover no-repeat;filter:blur(%(blur)dpx)}
.dim{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,%(d1).2f),rgba(0,0,0,%(d2).2f))}
.el{position:absolute}
.card{background:rgba(255,255,255,.82);backdrop-filter:blur(22px) saturate(1.3);-webkit-backdrop-filter:blur(22px) saturate(1.3);
  border:1px solid rgba(255,255,255,.75);border-radius:18px;box-shadow:0 18px 50px rgba(10,10,30,.28),0 2px 6px rgba(10,10,30,.12);padding:20px 22px}
.hd{display:flex;align-items:center;gap:10px;margin-bottom:14px}
.hd .ic{width:30px;height:30px;border-radius:9px;background:#0d0d0d;color:#fff;display:grid;place-items:center;font-weight:900;font-size:15px}
.hd b{font-size:17px;font-weight:800;letter-spacing:-.01em}.hd span{display:block;font-size:12.5px;color:#6f6f6b;font-weight:600}
.row{display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-top:1px solid rgba(0,0,0,.07);font-size:14.5px}
.row .l{color:#3a3a38;font-weight:600}.row .v{font-weight:800;display:flex;align-items:center;gap:8px}
.st{width:9px;height:9px;border-radius:50%%}
.ok{background:#16a34a}.warn{background:#f59e0b}.bad{background:#e11d48}.info{background:#2563eb}
.pill{font-size:12px;font-weight:800;padding:4px 10px;border-radius:99px}
.p-ok{background:#dcfce7;color:#166534}.p-warn{background:#fef3c7;color:#92400e}.p-bad{background:#ffe4e6;color:#9f1239}.p-info{background:#dbeafe;color:#1e40af}
.rk{display:flex;align-items:center;gap:12px;padding:9px 0;border-top:1px solid rgba(0,0,0,.07);font-size:14.5px;font-weight:700}
.rk .n{width:26px;color:#8a8a86;font-weight:800}.rk .t{flex:1}
.up{color:#16a34a;font-weight:900}.down{color:#e11d48;font-weight:900}.same{color:#8a8a86;font-weight:900}
.metric .v{font-size:76px;font-weight:900;letter-spacing:-.04em;line-height:1}.metric .lb{font-size:15px;font-weight:700;color:#3a3a38;margin-top:6px}
.metric .nt{font-size:12.5px;color:#6f6f6b;margin-top:8px;font-weight:600}
.bars{display:flex;align-items:flex-end;gap:10px;height:120px;margin-top:6px}
.bars .b{flex:1;display:flex;flex-direction:column;align-items:center;gap:6px;height:100%%;justify-content:flex-end}
.bars .bb{width:100%%;border-radius:6px 6px 3px 3px;background:#d4d4d0}.bars .hi .bb{background:#bf40ff}
.bars .bl{font-size:11.5px;color:#6f6f6b;font-weight:700}.bars .bv{font-size:12px;font-weight:800}
.chat .q{margin-left:auto;max-width:85%%;background:#0d0d0d;color:#fff;padding:11px 15px;border-radius:16px 16px 4px 16px;font-size:14.5px;font-weight:600;width:fit-content}
.chat .a{margin-top:12px;background:#f2f2f0;padding:12px 15px;border-radius:16px 16px 16px 4px;font-size:14px;line-height:1.45;font-weight:500}
.chat .who{font-size:11.5px;color:#6f6f6b;font-weight:800;margin:10px 0 4px}
.notice{display:flex;gap:12px}.notice .ic{width:38px;height:38px;border-radius:10px;background:#0d0d0d;color:#fff;display:grid;place-items:center;font-weight:900;flex:none}
.notice .top{display:flex;justify-content:space-between;font-size:12px;color:#6f6f6b;font-weight:700}.notice b{display:block;font-size:15px;margin:2px 0}.notice p{font-size:13.5px;color:#3a3a38;line-height:1.4}
.chip{display:inline-flex;align-items:center;gap:9px;background:rgba(255,255,255,.88);backdrop-filter:blur(16px);border:1px solid rgba(255,255,255,.8);
  border-radius:99px;padding:10px 18px;font-size:15px;font-weight:800;box-shadow:0 10px 30px rgba(10,10,30,.22)}
.chip i{width:9px;height:9px;border-radius:50%%;display:block}
.logo{position:absolute;top:36px;right:%(lr)dpx;width:168px}
"""

def el_html(x):
    t = x.get('type'); st = f"left:{x.get('x',0)}px;top:{x.get('y',0)}px;" + (f"width:{x['w']}px;" if x.get('w') else '') \
        + f"transform-origin:top left;transform:rotate({x.get('rot',0)}deg) scale({x.get('scale', SCALE[0])});" + (f"z-index:{x['z']};" if x.get('z') else '')
    if t == 'chip':
        return f'<div class="el chip" style="{st}"><i style="background:{e(x.get("dot","#bf40ff"))}"></i>{e(x["text"])}</div>'
    def head(title, sub='', ic=None):
        sb = '<span>%s</span>' % e(sub) if sub else ''
        return '<div class="hd"><div class="ic">%s</div><div><b>%s</b>%s</div></div>' % (e(ic or (title or '•')[0]), e(title), sb)
    if t == 'status':
        def val(r):
            st_ = r.get('state', 'info')
            if r.get('pill'):
                return '<span class="pill p-%s">%s</span>' % (st_, e(r['value']))
            dot = '<i class="st %s"></i>' % r['state'] if r.get('state') else ''
            return dot + e(r['value'])
        rows = ''.join('<div class="row"><span class="l">%s</span><span class="v">%s</span></div>' % (e(r['label']), val(r)) for r in x.get('rows', []))
        return f'<div class="el card" style="{st}">{head(x.get("title",""), x.get("subtitle",""), x.get("icon"))}{rows}</div>'
    if t == 'ranking':
        def d(v):
            v = int(v or 0)
            return f'<span class="up">▲ {v}</span>' if v > 0 else f'<span class="down">▼ {-v}</span>' if v < 0 else '<span class="same">–</span>'
        rows = ''.join(f'<div class="rk"><span class="n">{i+1}</span><span class="t">{e(r["label"])}</span>{d(r.get("delta"))}</div>' for i, r in enumerate(x.get('items', [])))
        return f'<div class="el card" style="{st}">{head(x.get("title",""), x.get("subtitle",""), x.get("icon"))}{rows}</div>'
    if t == 'metric':
        nt = '<div class="nt">%s</div>' % e(x['note']) if x.get('note') else ''
        return '<div class="el card metric" style="%s"><div class="v" style="color:%s">%s</div><div class="lb">%s</div>%s</div>' % (st, e(x.get('color', '#0d0d0d')), e(x['value']), e(x.get('label', '')), nt)
    if t == 'bars':
        mx = max([b['value'] for b in x['bars']] or [1]); hi = x.get('highlight')
        bs = ''.join('<div class="b %s"><span class="bv">%s</span><div class="bb" style="height:%d%%"></div><span class="bl">%s</span></div>' % ('hi' if i == hi else '', e(b.get('show', str(b['value']) + x.get('unit', ''))), max(4, round(b['value'] / mx * 88)), e(b['label'])) for i, b in enumerate(x['bars']))
        return f'<div class="el card" style="{st}">{head(x.get("title",""), x.get("subtitle",""), x.get("icon"))}<div class="bars">{bs}</div></div>'
    if t == 'chat':
        return f'<div class="el card chat" style="{st}"><div class="q">{e(x["q"])}</div><div class="who">{e(x.get("who","AI"))}</div><div class="a">{e(x["a"])}</div></div>'
    if t == 'notice':
        return f'<div class="el card notice" style="{st}"><div class="ic">{e(x.get("icon",(x.get("app") or "•")[0]))}</div><div style="flex:1"><div class="top"><span>{e(x.get("app",""))}</span><span>{e(x.get("time",""))}</span></div><b>{e(x.get("title",""))}</b><p>{e(x.get("text",""))}</p></div></div>'
    raise SystemExit(f'unknown element type {t}')

def shoot(html_path, png, w, h):
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=2',
                    f'--window-size={w},{h}', '--virtual-time-budget=3000', f'--screenshot={png}', f'file://{html_path}'], capture_output=True)

def main():
    a = argparse.ArgumentParser(); a.add_argument('spec'); a.add_argument('out'); a.add_argument('--preview', action='store_true'); o = a.parse_args()
    s = json.load(open(o.spec)); bg = os.path.abspath(s['background']); SCALE[0] = float(s.get('scale', 1.15))
    blur = int(s.get('bg_blur', 6)); dim = float(s.get('bg_dim', .3))
    # logo colour from the background brightness under it
    v = s.get('logo', 'auto')
    if v == 'auto':
        im = Image.open(bg).convert('L'); sc = max(W / im.width, H / im.height); im = im.resize((round(im.width*sc), round(im.height*sc)))
        ox, oy = (im.width - W)//2, (im.height - H)//2
        lum = ImageStat.Stat(im.crop((ox+1150-168, oy+36, ox+1150, oy+100))).mean[0] * (1 - dim)
        v = 'dark' if lum > 150 else 'white'
    css = CSS % dict(font=FONT, W=W, H=H, bg=bg, pos=s.get('bg_pos', 'center'), blur=blur, pad=blur*3, d1=dim*.8, d2=dim*1.2, lr=W-1150)
    body = '<div class="bg"></div><div class="dim"></div>' + ''.join(el_html(x) for x in s['elements']) + f'<img class="logo" src="file://{LOGO.format(v)}">'
    tmp = tempfile.mkdtemp(); hp = os.path.join(tmp, 'c.html'); open(hp, 'w').write(f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{body}</body></html>')
    png = os.path.join(tmp, 'c.png'); shoot(hp, png, W, H)
    im = Image.open(png).convert('RGB')
    if im.size != (W*2, H*2): im = im.resize((W*2, H*2))
    im.save(o.out, quality=92)
    if o.preview:
        gx = (W*2 - round(H*2*4/3))//2
        im.crop((gx, 0, W*2-gx, H*2)).resize((666, 500)).save(o.out.rsplit('.',1)[0] + '_grid.jpg', quality=85)
    print(o.out, 'logo=' + v)

if __name__ == '__main__': main()
