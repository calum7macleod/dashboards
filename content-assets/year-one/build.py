import json,sys,os
SLIDES=[
 dict(n="01",title="First 365 Days<br>in Real Estate",big="Đ122,800,000",sub="Total sales volume  ·  40 deals",serif="$33.4M USD  ·  £25.0M GBP",line="",foot="",bg="bg3full.jpg",pos="70%",bigx=True,topdark=True,bgx="background-size:auto 100%;background-position:center;background-color:#152A1F;"),
 dict(n="02",title="Best Month",big="Đ21,300,000",sub="April 2026  ·  8 deals",serif="$5.8M USD  ·  £4.3M GBP",line="Đ10.2M and 3.3 deals a month, on average",foot="@uaecalum<span>·</span>+971 55 350 2699",bg="bg2.jpg",pos="73%",cls="up"),
 dict(n="03",title="Where",big="Dubai 33  ·  Abu Dhabi 7",sub="31 ready  ·  9 off-plan",serif="Biggest deal  Đ8,000,000  ·  Hudayriyat penthouse",line="",foot="@uaecalum<span>·</span>+971 55 350 2699",bg="bg1.jpg",pos="72%",wide=True,cls="up big3"),
]
TOT=f"{len(SLIDES):02d}"
def slide(s):
    bg=f"background-image:url('{s['bg']}');" if s['bg'] else ""
    bg+=s.get("bgx","")
    pos=s.get("pos","50%")
    return f'''<section class="sl{' topdark' if s.get('topdark') else ''} {s.get('cls','')}" style="{bg}">
  <div class="shade"></div>
  <div class="mid" style="top:{pos}">
    <div class="t">{s['title']}</div>
    <div class="rule"></div>
    <div class="big{' bigx' if s.get('bigx') else ''}{' wide' if s.get('wide') else ''}">{s['big']}</div>
    <div class="sub">{s['sub']}</div>
    {f'<div class="ser">{s["serif"]}</div>' if s['serif'] else ''}
    {f'<div class="ln">{s["line"]}</div>' if s['line'] else ''}
  </div>
  <div class="bt">{s['foot']}</div>
</section>'''
CSS='''
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#152A1F}
.sl{width:1080px;height:1350px;position:relative;overflow:hidden;color:#F5EDE0;font-family:Carlito,Calibri,sans-serif;background:#1E3D2F center/cover no-repeat;page-break-after:always}
.shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(21,42,31,.4) 0%,rgba(21,42,31,.08) 14%,rgba(21,42,31,.06) 44%,rgba(21,42,31,.66) 58%,rgba(21,42,31,.9) 70%,rgba(21,42,31,.96) 100%)}
.sl.topdark .shade{background:linear-gradient(180deg,rgba(21,42,31,.5) 0%,rgba(21,42,31,.15) 14%,rgba(21,42,31,.06) 40%,rgba(21,42,31,.66) 58%,rgba(21,42,31,.9) 70%,rgba(21,42,31,.96) 100%)}
.mid{position:absolute;left:0;right:0;top:50%;transform:translateY(-50%);text-align:center;padding:0 50px}
.t{font-family:'TeX Gyre Pagella',Palatino,serif;font-size:60px;color:#F5EDE0;line-height:1.1;text-shadow:0 2px 24px rgba(0,0,0,.45)}
.rule{width:150px;height:2px;background:#C9A84C;margin:18px auto 22px}
.big{font-family:'TeX Gyre Pagella',Palatino,serif;font-size:120px;line-height:1;color:#E8C96B;letter-spacing:-.01em;text-shadow:0 2px 28px rgba(0,0,0,.5);white-space:nowrap}
.big.bigx{font-size:134px}
.big.wide{font-size:92px}
.sub{font-size:22px;letter-spacing:.3em;text-transform:uppercase;color:#F5EDE0;margin-top:26px;font-weight:600}
.ser{font-family:'TeX Gyre Pagella',Palatino,serif;font-size:32px;color:#F5EDE0;margin-top:18px}
.ln{font-size:18px;letter-spacing:.3em;text-transform:uppercase;color:#F5EDE0;margin-top:18px;font-weight:600}
.bt{position:absolute;left:0;right:0;bottom:56px;text-align:center;font-size:16px;letter-spacing:.26em;text-transform:uppercase;color:#C9A84C;font-weight:600}
.bt span{margin:0 16px;color:#8FA898}
.sl.up .sub{font-size:26px}.sl.up .ser{font-size:38px;margin-top:20px}.sl.up .ln{font-size:22px;margin-top:22px}
.sl.big3 .sub{font-size:30px;margin-top:30px}.sl.big3 .ser{font-size:40px;margin-top:22px;color:#F5EDE0}.sl.big3 .bt{font-size:19px}
'''
html='<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Year one · milestone carousel</title><!-- Milestone carousel, 1080x1080. Set bg per slide in build.py; .ph = placeholder background until photos arrive. --><style>'+CSS+'</style></head><body>'+"".join(slide(s).replace('class="sl"','class="sl ph"') if not s['bg'] else slide(s) for s in SLIDES)+'</body></html>'
open('milestone.html','w').write(html); print(len(SLIDES),'slides')
