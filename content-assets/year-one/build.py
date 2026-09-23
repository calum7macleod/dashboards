import json,sys,os
SLIDES=[
 dict(n="01",title="One Year Today",big="Đ122,800,000",sub="Sold in my first 12 months in real estate",serif="$33.4M USD  ·  £25.0M GBP",line="23 Sep 2025 - 23 Sep 2026  ·  40 deals",bg="bg3.jpg",pos="68%",bigx=True,topdark=True,bgx="background-size:118%;background-position:center bottom;"),
 dict(n="02",title="Best Month",big="Đ21,300,000",sub="April 2026  ·  8 deals",serif="$5.8M USD  ·  £4.3M GBP",line="Đ10.2M and 3.3 deals a month, on average",bg="bg2.jpg",pos="73%"),
 dict(n="03",title="Where They Sold",big="Dubai 33  ·  Abu Dhabi 7",sub="29 in DAMAC Lagoons  ·  31 ready  ·  9 off-plan",serif="Costa Brava  ·  Malta  ·  Portofino  ·  Tara Park  ·  Reem  ·  Hudayriyat",line="Biggest: Đ8M penthouse, Hudayriyat",bg="bg1.jpg",pos="72%",wide=True),
]
TOT=f"{len(SLIDES):02d}"
def slide(s):
    bg=f"background-image:url('{s['bg']}');" if s['bg'] else ""
    bg+=s.get("bgx","")
    pos=s.get("pos","50%")
    return f'''<section class="sl{' topdark' if s.get('topdark') else ''}" style="{bg}">
  <div class="shade"></div>
  <div class="tl">Calum MacLeod<span>·</span>@uaecalum</div>
  <div class="mid" style="top:{pos}">
    <div class="eye"><svg width="9" height="9" viewBox="0 0 10 10"><path d="M5 0 10 5 5 10 0 5Z" fill="#C9A84C"/></svg>Milestone<span>·</span>{s['n']} / {TOT}</div>
    <div class="t">{s['title']}</div>
    <div class="rule"></div>
    <div class="big{' bigx' if s.get('bigx') else ''}{' wide' if s.get('wide') else ''}">{s['big']}</div>
    <div class="sub">{s['sub']}</div>
    {f'<div class="ser">{s["serif"]}</div>' if s['serif'] else ''}
    <div class="ln">{s['line']}</div>
  </div>
  <div class="bt">@uaecalum<span>·</span>+971 55 350 2699</div>
</section>'''
CSS='''
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#152A1F}
.sl{width:1080px;height:1350px;position:relative;overflow:hidden;color:#F5EDE0;font-family:Carlito,Calibri,sans-serif;background:#1E3D2F center/cover no-repeat;page-break-after:always}
.shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(21,42,31,.55) 0%,rgba(21,42,31,.1) 16%,rgba(21,42,31,.06) 44%,rgba(21,42,31,.66) 58%,rgba(21,42,31,.9) 70%,rgba(21,42,31,.96) 100%)}
.sl.topdark .shade{background:linear-gradient(180deg,rgba(21,42,31,.8) 0%,rgba(21,42,31,.4) 16%,rgba(21,42,31,.1) 30%,rgba(21,42,31,.06) 44%,rgba(21,42,31,.66) 58%,rgba(21,42,31,.9) 70%,rgba(21,42,31,.96) 100%)}
.tl{position:absolute;left:0;right:0;top:64px;text-align:center;font-size:16px;letter-spacing:.32em;text-transform:uppercase;color:#E8C96B;font-weight:600}
.tl span,.bt span{margin:0 16px;color:#C9A84C}
.mid{position:absolute;left:0;right:0;top:50%;transform:translateY(-50%);text-align:center;padding:0 50px}
.eye{font-size:15px;letter-spacing:.34em;text-transform:uppercase;color:#C9A84C;font-weight:700;margin-bottom:22px}
.eye svg{margin-right:14px;vertical-align:1px}.eye span{margin:0 14px;font-weight:400}
.t{font-family:'TeX Gyre Pagella',Palatino,serif;font-size:60px;color:#F5EDE0;line-height:1.05;text-shadow:0 2px 24px rgba(0,0,0,.45)}
.rule{width:150px;height:2px;background:#C9A84C;margin:16px auto 20px}
.big{font-family:'TeX Gyre Pagella',Palatino,serif;font-size:120px;line-height:1;color:#E8C96B;letter-spacing:-.01em;text-shadow:0 2px 28px rgba(0,0,0,.5);white-space:nowrap}
.big.bigx{font-size:134px}
.big.wide{font-size:92px}
.sub{font-size:22px;letter-spacing:.3em;text-transform:uppercase;color:#F5EDE0;margin-top:26px;font-weight:600}
.ser{font-family:'TeX Gyre Pagella',Palatino,serif;font-size:32px;color:#F5EDE0;margin-top:18px}
.ln{font-size:18px;letter-spacing:.3em;text-transform:uppercase;color:#F5EDE0;margin-top:18px;font-weight:600}
.bt{position:absolute;left:0;right:0;bottom:56px;text-align:center;font-size:15px;letter-spacing:.24em;text-transform:uppercase;color:#8FA898;font-weight:600}
'''
html='<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Year one · milestone carousel</title><!-- Milestone carousel, 1080x1080. Set bg per slide in build.py; .ph = placeholder background until photos arrive. --><style>'+CSS+'</style></head><body>'+"".join(slide(s).replace('class="sl"','class="sl ph"') if not s['bg'] else slide(s) for s in SLIDES)+'</body></html>'
open('milestone.html','w').write(html); print(len(SLIDES),'slides')
