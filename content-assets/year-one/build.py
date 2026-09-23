import json,sys,os
SLIDES=[
 dict(n="01",title="One Year Today",big="Đ122,800,000",sub="Sold in my first 12 months in real estate",serif="$33.4M USD  ·  £25.0M GBP",line="23 Sep 2025 - 23 Sep 2026  ·  40 deals",bg="bg3.jpg",pos="70%",bigx=True,topdark=True),
 dict(n="02",title="Best Month",big="Đ21,300,000",sub="April 2026  ·  8 deals",serif="$5.8M USD  ·  £4.3M GBP",line="11 straight months with a signing",bg="bg2.jpg",pos="73%",noav=True),
 dict(n="03",title="The Shape of It",big="Đ13M  →  Đ37M",sub="First 100 days  →  last 100 days",serif="4 deals became 11",line="Dubai 33  ·  Abu Dhabi 7  ·  29 in DAMAC Lagoons",bg="bg1.jpg",pos="72%",noav=True),
]
TOT=f"{len(SLIDES):02d}"
def slide(s):
    bg=f"background-image:url('{s['bg']}');" if s['bg'] else ""
    pos=s.get("pos","50%")
    return f'''<section class="sl{' topdark' if s.get('topdark') else ''}" style="{bg}">
  <div class="shade"></div>
  <div class="tl"><div class="who">Calum MacLeod<span>·</span>@uaecalum</div><div class="mark"><svg width="12" height="12" viewBox="0 0 10 10"><path d="M5 0 10 5 5 10 0 5Z" fill="#C9A84C"/></svg><i></i></div></div>
  <div class="tr"><div class="pill">Milestone</div><div class="ct">{s['n']} / {TOT}</div></div>
  <div class="mid" style="top:{pos}">
    <div class="t">{s['title']}</div>
    <div class="rule"></div>
    <div class="big{' bigx' if s.get('bigx') else ''}">{s['big']}</div>
    <div class="sub">{s['sub']}</div>
    {f'<div class="ser">{s["serif"]}</div>' if s['serif'] else ''}
    <div class="ln">{s['line']}</div>
  </div>
  {"" if s.get("noav") else '<div class="bl"><img src="avatar.png"><div><b>Calum MacLeod</b><i>@uaecalum</i></div></div>'}
  <div class="br">+971 55 350 2699</div>
</section>'''
CSS='''
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#152A1F}
.sl{width:1080px;height:1350px;position:relative;overflow:hidden;color:#F5EDE0;font-family:Carlito,Calibri,sans-serif;background:#1E3D2F center/cover no-repeat;page-break-after:always}
.sl.ph{background:radial-gradient(ellipse at 50% 40%,#2E5A40 0%,#1E3D2F 45%,#152A1F 100%)}
.shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(21,42,31,.6) 0%,rgba(21,42,31,.1) 18%,rgba(21,42,31,.06) 44%,rgba(21,42,31,.66) 58%,rgba(21,42,31,.9) 70%,rgba(21,42,31,.96) 100%)}
.sl.topdark .shade{background:linear-gradient(180deg,rgba(21,42,31,.82) 0%,rgba(21,42,31,.45) 16%,rgba(21,42,31,.1) 30%,rgba(21,42,31,.06) 44%,rgba(21,42,31,.66) 58%,rgba(21,42,31,.9) 70%,rgba(21,42,31,.96) 100%)}
.tl{position:absolute;left:78px;top:88px}
.who{font-size:20px;letter-spacing:.32em;text-transform:uppercase;color:#E8C96B;font-weight:600}
.who span{margin:0 18px;color:#C9A84C}
.mark{display:flex;align-items:center;gap:14px;margin-top:22px}
.mark i{display:block;width:240px;height:2px;background:#C9A84C}
.tr{position:absolute;right:82px;top:82px;text-align:center}
.pill{display:inline-block;background:#C9A84C;color:#152A1F;font-size:21px;font-weight:700;letter-spacing:.3em;text-transform:uppercase;padding:18px 52px 16px;border-radius:40px 40px 40px 6px;padding-left:58px}
.ct{font-size:16px;letter-spacing:.3em;color:#F5EDE0;margin-top:22px;font-weight:600}
.mid{position:absolute;left:0;right:0;top:50%;transform:translateY(-50%);text-align:center;padding:0 60px}
.t{font-family:'TeX Gyre Pagella',Palatino,serif;font-size:60px;color:#F5EDE0;letter-spacing:.005em;line-height:1.05;text-shadow:0 2px 24px rgba(0,0,0,.45)}
.rule{width:150px;height:2px;background:#C9A84C;margin:14px auto 18px}
.big.bigx{font-size:128px}
.big{font-family:'TeX Gyre Pagella',Palatino,serif;font-size:108px;line-height:1;color:#E8C96B;letter-spacing:-.01em;text-shadow:0 2px 28px rgba(0,0,0,.5);white-space:nowrap}
.sub{font-size:21px;letter-spacing:.32em;text-transform:uppercase;color:#F5EDE0;margin-top:20px;font-weight:600}
.ser{font-family:'TeX Gyre Pagella',Palatino,serif;font-size:32px;color:#F5EDE0;margin-top:16px}
.ln{font-size:18px;letter-spacing:.3em;text-transform:uppercase;color:#F5EDE0;margin-top:16px;font-weight:600}
.bl{position:absolute;left:78px;bottom:78px;display:flex;align-items:center;gap:18px}
.bl img{width:82px;height:82px;border-radius:50%;border:2px solid #C9A84C}
.bl b{display:block;font-size:22px;font-weight:700}.bl i{display:block;font-style:normal;font-size:18px;color:#C9A84C;margin-top:4px}
.br{position:absolute;right:82px;bottom:62px;font-size:18px;letter-spacing:.06em;color:#F5EDE0}
'''
html='<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Year one · milestone carousel</title><!-- Milestone carousel, 1080x1080. Set bg per slide in build.py; .ph = placeholder background until photos arrive. --><style>'+CSS+'</style></head><body>'+"".join(slide(s).replace('class="sl"','class="sl ph"') if not s['bg'] else slide(s) for s in SLIDES)+'</body></html>'
open('milestone.html','w').write(html); print(len(SLIDES),'slides')
