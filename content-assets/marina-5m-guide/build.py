D=lambda c="#C9A84C",s=6: f'<svg class="dm" width="{s}" height="{s}" viewBox="0 0 10 10"><path d="M5 0 10 5 5 10 0 5Z" fill="{c}"/></svg>'
G="#9A7B2A"
def eye(t,c="#C9A84C"): return f'<div class="eye">{D(c)}{t}</div>'
def foot(n): return f'<div class="foot"><span>Marina · Abu Dhabi and Dubai · November 2026</span><span>Indicative · {n} / 3</span></div>'
def tbl(head,rows,cls="",hl=None):
    h="".join(f'<th>{c}</th>' for c in head)
    r="".join(f'<tr class="{"hl" if i==hl else ""}">'+"".join(f'<td>{c}</td>' for c in row)+'</tr>' for i,row in enumerate(rows))
    return f'<table class="{cls}"><tr>{h}</tr>{r}</table>'
P=[]
# PAGE 1
P.append(f'''<section class="pg">
<div class="band">
  {eye("Prepared for Marina · November 2026")}
  <h1>Abu Dhabi and Dubai:<br>a clear guide for your AED 5M</h1>
  <p class="lead">There's a lot of noise about the UAE property market right now, and much of it contradicts itself. This guide cuts it down to what actually matters for your budget: how the two cities compare, what protects your money, and which homes make sense.</p>
</div>
<div class="body">
<h2>The short version</h2>
<ul class="dia">
 <li>Both cities are safe, regulated places to buy. Which one suits you depends on what you want the home to do for you.</li>
 <li><b>Dubai</b> is the bigger, more established market, with more choice and more homes being completed right now.</li>
 <li><b>Abu Dhabi</b> is earlier in its story: more people arriving than homes being built, and payment plans that ask for less money before you receive the keys.</li>
</ul>
<h2>What's happening in each market</h2>
{tbl(["","Abu Dhabi","Dubai"],[
 ("Home sales, first half of 2026","Up 178% on last year","Down 16% on last year"),
 ("New homes coming","Around 37,000 over the next four years","Around 27,300 completed in one quarter this year"),
 ("People arriving","Around 288,000 in a year - roughly 18 for every new home sold","Roughly 2 for every new home sold"),
 ("Rents","Up 17% in a year, 21% on the islands","Steadying, with some prices easing 5-7%"),
 ("Paid before you get the keys","Usually 35-50%","Usually 60-80%"),
 ("Who stands behind the developers","The government's sovereign funds, around US$1.9 trillion","Dubai's government holding company, Dubai Holding")],cls="cmp")}
<div class="two">
 <div><h2>What protects your money - in both cities</h2>
  <div class="prot"><b>Escrow.</b> Your payments go into a regulated account, not to the developer, and are released only as construction progresses and is verified.</div>
  <div class="prot"><b>Government-backed developers.</b> Every developer in this guide is owned or majority-owned by the state.</div>
  <div class="prot"><b>Staged payments.</b> You never pay the full price up front - you pay in steps as the building goes up.</div>
  <div class="prot"><b>Registered ownership.</b> Your purchase is recorded with the government land registry from day one.</div>
 </div>
 <div><h2>Five terms, in plain English</h2>
  <div class="term"><b>Off-plan</b> - buying a home before it's finished, usually at a lower price.</div>
  <div class="term"><b>Payment plan (e.g. 40/60)</b> - 40% paid during construction, 60% when you receive the keys.</div>
  <div class="term"><b>Handover</b> - the day the home is finished and yours to use or rent.</div>
  <div class="term"><b>Cancellation unit</b> - a home released back to the developer and offered again, often the only way into a project that has sold out.</div>
  <div class="term"><b>Escrow</b> - the protected account your payments sit in while the building goes up.</div>
 </div>
</div>
<div class="src">Sources: Cavendish Maxwell H1 2026 · Knight Frank · SCAD · ADREC H1 2026 · Savills Q2 2026. Figures indicative, November 2026.</div>
</div>{foot(1)}</section>''')
# PAGE 2
P.append(f'''<section class="pg">
<div class="body top">
{eye("Your options in Abu Dhabi",G)}
<h1 class="dk">Five homes that fit your budget, each suited to a different priority.</h1>
{tbl(["Home","Where","What you get","Price","Paid before keys","Ready"],[
 ("<b>Tara Park</b><i>Modon</i>","Reem Island, opposite Reem Mall, 5 minutes from the financial district","3-bed apartment, ~2,000-2,500 sq ft","~AED 3.6-3.7m","40%","Late 2029 - mid 2030"),
 ("<b>Muheira</b><i>Modon</i>","Waterfront on Reem Island","3-bed apartment, ~1,950-2,000 sq ft","AED 3.3-4.3m","50%","Late 2028 - mid 2029"),
 ("<b>Bashayer</b><i>Modon</i>","Hudayriyat Island, on the beach","2-bed ~1,400-1,600 sq ft, or 3-bed ~2,000 sq ft","2-bed AED 3.05-4.1m · 3-bed from ~AED 3.6m","50%","2029"),
 ("<b>The Canopies, Yas Point</b><i>Aldar</i>","Yas Island waterfront","2-bed + maid's room ~1,500 sq ft","AED 4.2m","To be confirmed","To be confirmed"),
 ("<b>Manchester City Yas Residences</b><i>Ohana</i>","Yas Canal","3-bed townhouse ~2,230 sq ft","AED 4.25m","35%","Late 2029")],cls="opts")}
<div class="note"><b>A note on availability.</b> Tara Park, Muheira, Bashayer and Manchester City Yas Residences all sold out at launch. For these, we'd be securing a cancellation unit, so availability and exact price are confirmed home by home. The Canopies is still selling directly.</div>
<h2>Which suits you</h2>
<div class="suits">
 <div><span class="k">If rental income matters most</span><b>Tara Park.</b> Its tenants are the professionals working in Abu Dhabi's financial district, which grew 34% in a year. It's also the best value per square foot. I bought a 2-bedroom here myself in April.</div>
 <div><span class="k">If you'd like the keys sooner</span><b>Muheira.</b> Ready up to two years earlier than most of the others, on the water.</div>
 <div><span class="k">If it's a home you'd love to live in</span><b>Bashayer.</b> A beachfront apartment on Abu Dhabi's flagship island, with the surf park, beach and cycle tracks already open.</div>
 <div><span class="k">If you want a house rather than an apartment</span><b>Manchester City Yas Residences.</b> A townhouse with its own garage, and the lowest amount to pay before handover.</div>
 <div><span class="k">If Yas Island is the draw</span><b>The Canopies.</b> Prime waterfront from Aldar, Abu Dhabi's best-known developer.</div>
</div>
<div class="call"><b>Or two homes instead of one.</b> AED 5m also covers two 2-bedroom apartments at Tara Park, around AED 2.4-2.7m each. Two rents, and the freedom to sell one without selling both.</div>
<div class="src">Prices from developer releases and current listings, November 2026. Indicative and subject to availability.</div>
</div>{foot(2)}</section>''')
# PAGE 3
P.append(f'''<section class="pg">
<div class="body top">
{eye("The Dubai option, and where I'd start",G)}
<h1 class="dk">Palm Springs - Nakheel, Jebel Ali</h1>
<p class="p">Dubai's newest family community, launched on 9 November next to Palm Jebel Ali: 977 townhouses and villas for around 50,000 residents.</p>
<div class="facts">
 <div><span class="k">3-bed townhouse</span>2,326 sq ft from AED 3.8m</div>
 <div><span class="k">Payment plan 60/40</span>10% on booking, 50% in six payments between April 2027 and May 2029, 40% when you receive the keys - AED 2.28m before handover on a 3-bed</div>
 <div><span class="k">Ready</span>October 2030</div>
 <div><span class="k">Why people like it</span>Nakheel's name, and more space for the money than anything else in this guide</div>
 <div><span class="k">What to weigh up</span>More money paid before handover, a later finish, and a brand-new area in a city completing more homes than it has in years</div>
</div>
<p class="p">There are other good options in Dubai beyond Palm Springs, and I'm happy to share them. But as the numbers on the first page show, Abu Dhabi is probably the safer investment right now.</p>
<h2>Three good homes at around AED 4m, side by side</h2>
{tbl(["","Palm Springs · Dubai","Man City Yas · Abu Dhabi","Bashayer · Abu Dhabi"],[
 ("What you get","3-bed townhouse, 2,326 sq ft","3-bed townhouse, ~2,230 sq ft","3-bed beachfront apartment, ~2,000 sq ft"),
 ("Price","AED 3.8m","AED 4.25m","from ~AED 3.6m"),
 ("Price per sq ft","~AED 1,630","~AED 1,910","~AED 1,760"),
 ("Paid before keys","AED 2.28m (60%)","AED 1.49m (35%)","AED 1.8m (50%)"),
 ("Ready","October 2030","Late 2029","2029"),
 ("What's there today","A new masterplan","Ferrari World, Yas Mall, the F1 circuit","Surf park, velodrome, beach - all open")],cls="cmp three")}
<div class="call big"><span class="k">Where I'd start</span>Palm Springs gives you the most space for your money, and it's a good product. But if I were in your position, I'd start in Abu Dhabi. You'd keep up to AED 800,000 more in your pocket until the keys arrive, the home would be ready around a year sooner, and you'd be buying in a market where far more people are arriving than homes are being built. Dubai is a strong market too - it's simply at a different stage, with a lot of new supply arriving at the same time.</div>
<h2>What happens next</h2>
<div class="steps">
 <div><b>1</b>Meet and discuss what you'd like the property to do for you</div>
 <div><b>2</b>Get the actual unit details on the ones we like - availability, exact prices, floor plans</div>
 <div><b>3</b>Decide from there whether it makes sense</div>
</div>
<div class="sig"><b>Calum MacLeod</b> · +971 55 350 2699</div>
<div class="src">Prices and figures indicative as of November 2026, based on developer releases, regulator data and current listings (Palm Springs: Nakheel launch pack, 9 November 2026); subject to availability and change. Not financial advice.</div>
</div>{foot(3)}</section>''')
CSS='''
@page{size:210mm 297mm;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#152A1F;-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{font-family:Carlito,Calibri,sans-serif;font-size:9.6pt;line-height:1.42;color:#152A1F}
.pg{width:210mm;height:297mm;position:relative;overflow:hidden;page-break-after:always;background:#F5EDE0;display:flex;flex-direction:column}
.band{background:#152A1F;color:#F5EDE0;padding:11mm 16mm 8mm}
.body{padding:6mm 16mm 10mm;flex:1}.body.top{padding-top:14mm}
.dm{display:inline-block;vertical-align:.1em;margin-right:2.4mm}
.eye{font-size:7pt;font-weight:700;letter-spacing:.3em;text-transform:uppercase;color:#C9A84C}
h1{font-family:'TeX Gyre Pagella',Palatino,serif;font-weight:400;font-size:22pt;line-height:1.1;margin-top:3mm;letter-spacing:-.005em}
h1.dk{color:#152A1F;font-size:18pt;margin-bottom:4mm}
.lead{font-size:9.6pt;line-height:1.45;color:#cfd8d0;margin-top:3mm;max-width:165mm}
h2{font-family:'TeX Gyre Pagella',Palatino,serif;font-weight:400;font-size:13pt;margin:4mm 0 1.6mm;color:#152A1F}
h2:first-child{margin-top:0}
ul.dia{list-style:none}ul.dia li{position:relative;padding-left:5mm;margin:1.2mm 0}
ul.dia li:before{content:"";position:absolute;left:0;top:.42em;width:2.2mm;height:2.2mm;background:#C9A84C;transform:rotate(45deg)}
table{width:100%;border-collapse:collapse;font-size:8.8pt;margin-top:1.5mm}
th{font-size:6.6pt;letter-spacing:.14em;text-transform:uppercase;text-align:left;color:#9A7B2A;font-weight:700;padding:1.4mm 2mm 1.4mm 0;border-bottom:.4mm solid #C9A84C;vertical-align:bottom}
td{padding:1.6mm 2.5mm 1.6mm 0;border-bottom:.2mm solid #d9cfbd;vertical-align:top;color:#2b4034;line-height:1.35}
td:first-child{font-weight:700;color:#152A1F}
table.cmp td:first-child{width:38mm}
table.cmp.three td:first-child{width:30mm}
table.opts{font-size:8.6pt}table.opts td{padding:2mm 2mm 2mm 0}
table.opts td i{display:block;font-style:normal;font-weight:400;color:#9A7B2A;font-size:7pt;letter-spacing:.1em;text-transform:uppercase;margin-top:.5mm}
.two{display:grid;grid-template-columns:1fr 1fr;gap:9mm;margin-top:1mm}
.prot,.term{font-size:8.8pt;line-height:1.4;color:#2b4034;padding:1.3mm 0;border-bottom:.2mm solid #d9cfbd}
.prot:last-child,.term:last-child{border-bottom:0}
.prot b,.term b{color:#152A1F}
.src{font-size:7pt;color:#5d7266;margin-top:3.5mm;line-height:1.45}
.note{margin-top:4mm;background:#152A1F;color:#F5EDE0;border-radius:3mm;padding:4mm 5mm;font-size:9.4pt;line-height:1.45}
.note b{color:#E8C96B}
.suits div{padding:2mm 0;border-bottom:.2mm solid #d9cfbd;font-size:9.4pt;line-height:1.45;color:#2b4034}
.suits div:last-child{border-bottom:0}
.suits .k,.facts .k,.call .k{display:block;font-size:6.8pt;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:#9A7B2A;margin-bottom:.6mm}
.suits b,.facts b{color:#152A1F}
.call{margin-top:5mm;border-left:.8mm solid #C9A84C;padding:1.5mm 0 1.5mm 5mm;font-size:9.6pt;line-height:1.5;color:#2b4034}
.call b{color:#152A1F}
.call.big{font-family:'TeX Gyre Pagella',Palatino,serif;font-size:10.6pt;line-height:1.42;color:#152A1F;margin-top:4.5mm}
.call.big .k{font-family:Carlito,sans-serif;margin-bottom:1.5mm}
.p{font-size:9.6pt;line-height:1.45;color:#2b4034;margin:1.5mm 0 2.5mm}
.facts div{padding:1.5mm 0;border-bottom:.2mm solid #d9cfbd;font-size:9pt;line-height:1.45;color:#2b4034}
.facts div:last-child{border-bottom:0}
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:6mm;margin-top:2mm}
.steps div{border-top:.5mm solid #C9A84C;padding-top:2mm;font-size:8.8pt;line-height:1.4;color:#2b4034}
.steps b{display:block;font-family:'TeX Gyre Pagella',Palatino,serif;font-size:16pt;color:#9A7B2A;line-height:1;margin-bottom:1.5mm}
.sig{margin-top:4.5mm;font-size:10pt;color:#152A1F;letter-spacing:.02em}.sig b{font-family:'TeX Gyre Pagella',Palatino,serif;font-size:13pt}
.foot{position:absolute;left:16mm;right:16mm;bottom:7mm;display:flex;justify-content:space-between;font-size:6.4pt;letter-spacing:.14em;text-transform:uppercase;color:#5d7266;border-top:.25mm solid #d9cfbd;padding-top:2mm;font-weight:700}
'''
open('Marina-AED5M-Guide.html','w').write(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Marina · Abu Dhabi and Dubai · AED 5M guide</title><!-- Client guide, A4 portrait x3. Fonts: TeX Gyre Pagella + Carlito (placeholders). Generated by build.py --><style>{CSS}</style></head><body>{"".join(P)}</body></html>')
print('ok')
