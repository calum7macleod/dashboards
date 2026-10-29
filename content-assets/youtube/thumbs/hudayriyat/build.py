CSS='''
*{margin:0;padding:0;box-sizing:border-box}
body{background:#152A1F}
.t{width:1280px;height:720px;position:relative;overflow:hidden;background:#152A1F center/cover no-repeat;font-family:Carlito,Calibri,sans-serif;color:#F5EDE0}
.bg{position:absolute;inset:0;background-size:cover;background-position:center}
.dark{position:absolute;inset:0;background:linear-gradient(90deg,rgba(21,42,31,.94) 0%,rgba(21,42,31,.8) 50%,rgba(21,42,31,.5) 100%)}
.face{position:absolute;bottom:-20px;height:720px}
.face.l{right:-60px}
.face.r{right:-30px;height:520px}
.txt{position:absolute;display:flex;flex-direction:column;justify-content:center;gap:6px}
.w{font-size:132px;font-weight:700;line-height:.92;letter-spacing:-.01em;text-transform:uppercase;text-shadow:0 4px 0 #0c1a12,0 10px 30px rgba(0,0,0,.6)}
.w.g{color:#E8C96B}
.w.s{font-size:150px}
.pill{display:inline-block;align-self:flex-start;margin-top:18px;background:#C9A84C;color:#152A1F;font-weight:700;font-size:40px;letter-spacing:.14em;padding:10px 26px 8px;border-radius:99px}
.dm{position:absolute;opacity:.12}
.bar{position:absolute;left:0;top:0;width:14px;height:720px;background:#C9A84C}
.dm{right:auto!important;left:-120px}
'''
T=[
 dict(name="thumb-1-nobody-lives-here", bg="bg-th.jpg", dark=True, face="l",
      txt='<div class="txt" style="left:60px;top:0;height:720px;width:700px"><div class="w">Nobody</div><div class="w">lives here</div><div class="pill">$3.5BN ISLAND</div></div>'),
 dict(name="thumb-2-3-5bn-island", bg="bg-aerial.jpg", dark=False, face="r",
      txt='<div class="txt" style="left:60px;top:0;height:720px;width:820px"><div class="w" style="font-size:96px">Abu Dhabi\'s</div><div class="w g s">$3.5BN</div><div class="w">island</div></div>'),
 dict(name="thumb-3-everyone-talking", bg="", dark=False, face="l",
      txt='<div class="txt" style="left:60px;top:0;height:720px;width:700px"><div class="w" style="font-size:112px">The island</div><div class="w g" style="font-size:118px">everyone\'s</div><div class="w" style="font-size:112px">talking about</div></div>'),
]
for t in T:
    bg=f'<div class="bg" style="background-image:url({t["bg"]})"></div>' if t['bg'] else '<svg class="dm" style="right:-120px;top:-120px" width="700" height="700" viewBox="0 0 10 10"><path d="M5 0 10 5 5 10 0 5Z" fill="none" stroke="#C9A84C" stroke-width=".3"/></svg>'
    dark='<div class="dark"></div>' if t['dark'] else ('<div class="dark" style="background:linear-gradient(90deg,rgba(21,42,31,.9) 0%,rgba(21,42,31,.75) 50%,rgba(21,42,31,.25) 100%)"></div>' if t['bg'] else '')
    html=f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="t">{bg}{dark}<div class="bar"></div><img class="face {t["face"]}" src="face-cut.png">{t["txt"]}</div></body></html>'
    open(t['name']+'.html','w').write(html)
print('ok')
