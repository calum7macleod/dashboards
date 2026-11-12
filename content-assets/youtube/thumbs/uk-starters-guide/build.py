UK='''<svg viewBox="0 0 60 30" width="{w}" height="{h}" style="border-radius:8px;box-shadow:0 6px 20px rgba(0,0,0,.5)"><clipPath id="c"><rect width="60" height="30"/></clipPath><g clip-path="url(#c)"><rect width="60" height="30" fill="#012169"/><path d="M0,0 L60,30 M60,0 L0,30" stroke="#fff" stroke-width="6"/><path d="M0,0 L60,30 M60,0 L0,30" stroke="#C8102E" stroke-width="2"/><path d="M30,0 V30 M0,15 H60" stroke="#fff" stroke-width="10"/><path d="M30,0 V30 M0,15 H60" stroke="#C8102E" stroke-width="6"/></g></svg>'''
UAE='''<svg viewBox="0 0 60 30" width="{w}" height="{h}" style="border-radius:8px;box-shadow:0 6px 20px rgba(0,0,0,.5)"><rect width="60" height="30" fill="#00732F"/><rect y="10" width="60" height="10" fill="#fff"/><rect y="20" width="60" height="10" fill="#000"/><rect width="15" height="30" fill="#FF0000"/></svg>'''
CSS='''
*{margin:0;padding:0;box-sizing:border-box}
body{background:#152A1F}
.t{width:1280px;height:720px;position:relative;overflow:hidden;background:#152A1F;font-family:Carlito,Calibri,sans-serif;color:#F5EDE0}
.bg{position:absolute;inset:0;background-size:cover;background-position:center}
.dark{position:absolute;inset:0}
.face{position:absolute;bottom:-24px;right:-70px;height:720px}
.face.sm{height:600px;right:-50px}
.txt{position:absolute;left:56px;top:0;height:720px;width:760px;display:flex;flex-direction:column;justify-content:center;gap:4px}
.w{font-size:122px;font-weight:700;line-height:.94;letter-spacing:-.012em;text-transform:uppercase;text-shadow:0 4px 0 #0c1a12,0 10px 30px rgba(0,0,0,.6)}
.w.g{color:#E8C96B}
.w.md{font-size:96px}
.pill{display:inline-block;align-self:flex-start;background:#C9A84C;color:#152A1F;font-weight:700;font-size:36px;letter-spacing:.16em;padding:10px 26px 8px;border-radius:99px;margin-top:16px}
.flags{display:flex;align-items:center;gap:22px;margin-bottom:18px}
.arrow{font-size:72px;color:#E8C96B;font-weight:700;line-height:1;text-shadow:0 4px 0 #0c1a12}
.bar{position:absolute;left:0;top:0;width:14px;height:720px;background:#C9A84C}
.tag{position:absolute;left:56px;top:48px;font-size:26px;letter-spacing:.3em;text-transform:uppercase;color:#C9A84C;font-weight:700;text-shadow:0 2px 8px rgba(0,0,0,.6)}
'''
flags=lambda w,h:f'<div class="flags">{UK.format(w=w,h=h)}<span class="arrow">→</span>{UAE.format(w=w,h=h)}</div>'
T=[
 dict(name="uk-thumb-1-start-here", bg="bg-lagoon-169.jpg", shade="linear-gradient(90deg,rgba(21,42,31,.95) 0%,rgba(21,42,31,.85) 48%,rgba(21,42,31,.35) 100%)",
      body=f'<div class="txt">{flags(170,85)}<div class="w">Buying in</div><div class="w g">the UAE</div><div class="pill">START HERE</div></div>'),
 dict(name="uk-thumb-2-uk-buyers-get-wrong", bg="", shade="",
      body=f'<div class="tag">Starter\'s guide · from the UK</div><div class="txt" style="gap:0"><div class="w md">What UK</div><div class="w md">buyers get</div><div class="w g">WRONG</div></div>'),
 dict(name="uk-thumb-3-live-uk-own-dubai", bg="bg-aerial.jpg", shade="linear-gradient(90deg,rgba(21,42,31,.95) 0%,rgba(21,42,31,.82) 50%,rgba(21,42,31,.3) 100%)",
      body=f'<div class="txt" style="gap:2px">{flags(150,75)}<div class="w md">Live in the UK</div><div class="w g">Own in Dubai</div><div class="pill">BUYING OFF-PLAN FROM ABROAD</div></div>'),
]
for t in T:
    bg=f'<div class="bg" style="background-image:url({t["bg"]})"></div>' if t['bg'] else '<svg style="position:absolute;right:-160px;top:-140px;opacity:.12" width="760" height="760" viewBox="0 0 10 10"><path d="M5 0 10 5 5 10 0 5Z" fill="none" stroke="#C9A84C" stroke-width=".3"/></svg>'
    dark=f'<div class="dark" style="background:{t["shade"]}"></div>' if t['shade'] else ''
    html=f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="t">{bg}{dark}<div class="bar"></div><img class="face" src="face-cut.png">{t["body"]}</div></body></html>'
    open(t['name']+'.html','w').write(html)
print('ok')
