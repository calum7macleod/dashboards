D=lambda c="#C9A84C",s=6: f'<svg class="dm" width="{s}" height="{s}" viewBox="0 0 10 10"><path d="M5 0 10 5 5 10 0 5Z" fill="{c}"/></svg>'
def conf(n,c="#C9A84C"): return '<span class="cf">'+"".join(D(c,4.6) for _ in range(n))+'</span>'
def eye(t,d=True,c="#C9A84C"): return f'<div class="eye">{D(c) if d else ""}{t}</div>'
def foot(n,dark=False):
    return f'<div class="foot"><span>Abu · Three ways to place Đ4M · September 2026</span><span>Indicative until documents confirm · {n:02d} / 11</span></div>'
def fn(items):
    return '<div class="fn">'+"".join(f'<div>{conf(c)}<span>{t}</span></div>' for t,c in items)+'</div>'
P=[]
# 00 COVER
P.append(f'''<section class="pg dark cover">
{eye("Prepared for Abu · September 2026")}
<div class="cgrid">
 <div class="cl">
  <h1>Three ways<br>to place <span class="g">Đ4M</span></h1>
  <div class="rule"></div>
  <p class="sub">One island the banks are moving to.<br>One community priced for a family.<br>One launch before the price sheet exists.</p>
 </div>
 <div class="cr">
  <div class="co"><span class="n">01</span><div><b>Tara Park</b><i>Reem Island · Modon · 3-bed + maid, corner</i></div></div>
  <div class="co"><span class="n">02</span><div><b>Al Ghadeer Parks</b><i>Abu Dhabi-Dubai corridor · Aldar · townhouses and villas</i></div></div>
  <div class="co"><span class="n">03</span><div><b>Palm Springs</b><i>Off Palm Jebel Ali · Dubai Holding · pre-launch</i></div></div>
 </div>
</div>
<div class="meta"><span><b>Calum MacLeod</b> · @uaecalum · +971 55 350 2699</span><span>Private options pack · every figure indicative until documents confirm</span></div>
</section>''')
# 01 WHY ABU DHABI
P.append(f'''<section class="pg">
{eye("01 · Why Abu Dhabi, why now",c="#9A7B2A")}
<h2>The earlier-cycle market.</h2>
<div class="rule"></div>
<div class="quad why">
 <div><div class="big">+17.8<span>%</span></div><div class="lab">Residential values, past twelve months</div><p>Reem Island +22% over the same period.</p></div>
 <div><div class="big">84<span>%</span></div><div class="lab">Of all Abu Dhabi sales are off-plan</div><p>Up 156% year on year. Buyers have moved to buying the future.</p></div>
 <div><div class="big">~7<span>%</span></div><div class="lab">Cash to own a contract, day one</div><p>5% down + 2% registration. Dubai: ~14% (4% DLD + deposit).</p></div>
 <div><div class="big">6-8<span>%</span></div><div class="lab">Typical Abu Dhabi gross yield</div><p>Long-let, one cheque cycle, before costs.</p></div>
</div>
<div class="grow"></div>
<div class="quote"><span class="q">ValuStrat's head of research puts it plainly: the capital sits earlier in its cycle than Dubai. The run Dubai has already had is still in front of Abu Dhabi.</span></div>
<div class="grow"></div>
{fn([("ValuStrat Abu Dhabi Real Estate Review Q2-2026 (Aug 26): values, Reem Island, off-plan share, cycle position",3),("Entry costs: Abu Dhabi and Dubai registration conventions",3),("Yields: Tara Park investor deck, Aug 26 - a method, not a promise",2)])}
{foot(2)}
</section>''')
# 02 OPTION 1 TARA PARK
def optpage(n,num,name,where,hero,heroSub,pills,h2,facts,pull,notes,pn,strip=()):
    f="".join(f'<div class="f"><div class="k">{k}</div><div class="v">{v}</div></div>' for k,v in facts)
    st="".join(f'<div class="call"><div class="n">{a}</div><div class="l">{b}</div></div>' for a,b in strip)
    pl="".join(f'<span class="pill">{p}</span>' for p in pills)
    return f'''<section class="pg split">
<div class="ol">
 {eye(f"Option {num}")}
 <div class="oname">{name}</div>
 <div class="owhere">{where}</div>
 <div class="rule"></div>
 <div class="ohero">{hero}</div>
 <div class="ohsub">{heroSub}</div>
 <div class="pills">{pl}</div>
 <div class="grow"></div>
 <div class="pull">{pull}</div>
</div>
<div class="or">
 <h2>{h2}</h2>
 <div class="facts">{f}</div>
 <div class="grow"></div>
 <div class="strip">{st}</div>
 <div class="grow"></div>
 {notes}
</div>
{foot(pn)}
</section>'''
P.append(optpage(2,"01","Tara Park","Reem Island · Modon","Đ3.9<span>M</span>","3-bed + maid · corner · 2,656 sqft BUA",
 ["Đ1,468 psf","~30% under AD off-plan average","Handover 2030","ADGM jurisdiction"],
 "A corner 3-bed on the financial island, around 30% under the Abu Dhabi off-plan average.",
 [("Developer","Modon - Abu Dhabi's government-backed master developer (Hudayriyat, Reem Island)."),
  ("The unit","3-bed + maid, corner position, 2,656 sqft built-up. Đ3,900,000 = Đ1,468 psf on built-up area, against an Abu Dhabi off-plan average of Đ2,104 psf."),
  ("Jurisdiction","Reem Island sits inside the ADGM financial free zone - English common law."),
  ("Position","Directly opposite Reem Mall, with a bridge into it. Five minutes to ADGM and Al Maryah; five minutes to downtown."),
  ("The building","Resort outdoor and indoor pools, park frontage, gym, running track, co-working lounge, kids' club, hotel-grade lobby."),
  ("Handover","Anticipated 2030.")],
 f'<span class="pq">&ldquo;I put my own money into this building.&rdquo;</span><span class="pa">Calum MacLeod</span>',
 fn([("Unit and price: Calum, 23 Sep 26. Off-plan average Đ2,104 psf: ValuStrat Q2-2026 - the average is blended, the unit is on built-up area, so read the gap as indicative",2),("Developer, jurisdiction, position, building: Modon Tara Park deck and scripts, Jul-Aug 26",3),("Handover 2030: Tara Park deck, Aug 26",2)]),3,
 [("Đ1,468<span> psf</span>","On built-up area"),("Đ2,104<span> psf</span>","Abu Dhabi off-plan average"),("5<span> min</span>","To ADGM and Al Maryah")]))
# 03 ADGM
names="BlackRock · State Street · PGIM · Nuveen · Capital Group · Man Group · Bain Capital · Barings · Hillhouse · Binance"
P.append(f'''<section class="pg">
{eye("01 · The ADGM engine",c="#9A7B2A")}
<h2>Why Reem rents, and re-rates.</h2>
<div class="rule"></div>
<div class="quad">
 <div><div class="big">47,047</div><div class="lab">People now work at ADGM</div><p>Up 44% in a year.</p></div>
 <div><div class="big">13,353</div><div class="lab">Active licences</div><p>Up more than 30% in a year. The largest international financial centre in the Middle East, Africa and South Asia.</p></div>
 <div><div class="big">+57<span>%</span></div><div class="lab">Assets under management, year on year</div><p>Q1-2026 entrants alone manage $4.4tn.</p></div>
 <div><div class="big">2<span>x</span></div><div class="lab">Reem leasing activity this year</div><p>While leasing cooled across most of the emirate, Reem's more than doubled.</p></div>
</div>
<div class="grow"></div>
<div class="names">{eye("Who moved in",c="#9A7B2A")}<div class="nl">{names}</div></div>
<div class="two">
 <p><b>Where they sit.</b> ADGM's own reporting names its workforce on Al Maryah <i>and</i> Al Reem Islands - the jurisdiction was extended onto Reem.</p>
 <p><b>The tenant.</b> A finance professional ten minutes from the desk. Long-let, one cheque, low turnover. That is the income case for the building on the previous page.</p>
</div>
<div class="grow"></div>
{fn([("ADGM releases, Q1 2026, as cited in the Tara Park investor case (Aug 26): headcount, licences, AUM, entrants",2),("Workforce location: ADGM reporting via Tara Park deck, Aug 26",3),("Reem leasing: published 2026 research via Tara Park deck, Aug 26",2),("Tenant profile: Calum's read of the market",1)])}
{foot(4)}
</section>''')
# 04 TARA PAYMENT
rows=[("Booking","5%","195,000"),("Registration 2% + DARI fee","fee","78,000 + 525"),("31 Jan 2027 · Early works","5%","195,000"),("31 Jul 2027 · Main works","5%","195,000"),("31 Jan 2028 · Podium","5%","195,000"),("31 Jul 2028 · Superstructure 50%","5%","195,000"),("31 Jan 2029 · Facade 50%","5%","195,000"),("31 Jul 2029 · Fit-out 50%","5%","195,000"),("31 Jan 2030 · Completion / BCC","5%","195,000"),("Handover","60%","2,340,000")]
tr="".join(f'<tr class="{"hl" if i==9 else ""}"><td>{a}</td><td class="n">{b}</td><td class="n">Đ{c}</td></tr>' for i,(a,b,c) in enumerate(rows))
P.append(f'''<section class="pg">
{eye("01 · Tara Park · what you pay, when",c="#9A7B2A")}
<h2>Đ3.9M on a 40 / 60 plan.</h2>
<div class="rule"></div>
<div class="pay">
 <div class="calls">
  <div class="call"><div class="n">~Đ273,500</div><div class="l">Day one</div><p>5% booking + 2% registration + DARI fee.</p></div>
  <div class="call"><div class="n">Đ1.64<span>M</span></div><div class="l">To handover · 42%</div><p>Eight instalments over three years, plus registration.</p></div>
  <div class="call"><div class="n">Đ195,000</div><div class="l">Largest single payment</div><p>Never more than 5% in one go before handover.</p></div>
 </div>
 <table><tr><th>Milestone</th><th class="n">Share</th><th class="n">Amount</th></tr>{tr}</table>
</div>
<div class="three">
 <div><b>The 60%.</b> Mortgageable at handover for a UAE resident, subject to bank approval at the time.</div>
 <div><b>Income.</b> 6.5% gross on value is ~Đ250K a year at today's price - higher on handover value. Abu Dhabi long-let rents are frozen at 0% since June 2026; capital growth is unaffected.</div>
 <div><b>Exit.</b> Sell the contract before handover once 20% is paid, with Modon's NOC. The buyer takes over the 60%. Admin fee to confirm.</div>
</div>
<div class="grow"></div>
{fn([("Modon Phase 2 payment schedule (Jul 26); registration fees per DARI sheet. Dates are Phase 2 - confirmed on the reservation form",3),("Mortgageability at handover and rent method: Tara Park deck, Aug 26",2),("Resale rule: Modon resale rules - high on the rule, admin fee to confirm",3)])}
{foot(5)}
</section>''')
# 05 OPTION 2 AL GHADEER
gh_tbl='''<table class="mini"><tr><th>At price</th><th class="n">Day one (5% + 2%)</th><th class="n">Through construction (55% + fee)</th><th class="n">At handover (45%)</th></tr>
<tr><td>3-bed townhouse ~Đ2.3M</td><td class="n">~Đ161K</td><td class="n">~Đ1.31M</td><td class="n">Đ1,035,000</td></tr>
<tr><td>4-bed villa ~Đ3.3M</td><td class="n">~Đ231K</td><td class="n">~Đ1.88M</td><td class="n">Đ1,485,000</td></tr></table>'''
P.append(optpage(5,"02","Al Ghadeer Parks","Abu Dhabi-Dubai corridor · Aldar","<small>from</small>~Đ2.3<span>M</span>","3-bed townhouse · 4-bed villa from ~Đ3.3M",
 ["55 / 45 · 5% down","Handover Q2 2031","453 homes","2% registration · freehold"],
 "Đ4M buys one 4-bed villa, a 3-bed townhouse with Đ1.7M held back, or two 2-bed townhouses.",
 [("The place","2- and 3-bed townhouses and 4-bed villas across manicured parks and feature lakes. Tree-lined, pedestrian-first streets; private gardens and shaded terraces."),
  ("Access","Al Maktoum airport 16 min · Zayed airport 30 min · Yas Island 30 min · Abu Dhabi 40 min."),
  ("Demand","The previous Al Ghadeer phase followed a complete sell-out of its first release within 48 hours."),
  ("Scale","Aldar's Đ10bn Alghadeer masterplan: 14,000+ homes over 15 years with schools, a hotel and community centres."),
  ("The money",gh_tbl)],
 '<span class="pq">Phase-one pricing is the argument. A resale track record does not exist yet.</span><span class="pa">The honest line on a 2031 handover</span>',
 fn([("Product, pricing, plan, handover, access: Metropolitan listing, Sep 26 - aggregator numbers, Aldar's sheet requested. Read every price as indicative launch pricing",1),("48-hour sell-out: Metropolitan, 2026",2),("Masterplan scale: Aldar press release, Apr 2018",3)]),6,
 [("48<span> hrs</span>","Previous phase · first release sold out"),("14,000<span>+</span>","Homes in the Alghadeer masterplan"),("16<span> min</span>","To Al Maktoum airport")]))
# 06 OPTION 3 PALM SPRINGS
P.append(optpage(6,"03","Palm Springs","Off Palm Jebel Ali · Dubai Holding","~Đ4<span>M</span>","or less · 3-bed · pre-launch · not yet public",
 ["Launch in the next couple of months","First phase","4% DLD + launch plan"],
 "A 3-bed beside the Palm, before the price sheet exists.",
 [("The island","Palm Jebel Ali is twice the size of Palm Jumeirah: ~110 km of new coastline, homes for ~35,000 families, and the start of a new growth corridor under the Dubai 2040 Urban Master Plan."),
  ("Progress","Construction restarted in 2024; first properties planned for delivery Q1 2027. Nakheel has awarded Đ5bn of infrastructure contracts, including a public access road from Sheikh Zayed Road."),
  ("Price context","On the Palm itself, Nakheel's Palm Central runs from Đ2.7M (1-bed), Đ4.3M (2-bed), Đ7.5M (3-bed); townhouses from Đ14.9M; completion Sep 2030. A 3-bed at ~Đ4M beside the Palm is the value entry to the corridor."),
  ("Momentum","The June 2026 release built on the strong market response to the October 2025 release."),
  ("The position","Launch pricing, first phase, registered before the book opens.")],
 '<span class="pq">&ldquo;I&rsquo;ll have you on the list the day it opens.&rdquo;</span><span class="pa">Calum MacLeod</span>',
 fn([("Launch timing and pricing: Calum's direct conversation with Dubai Holding, 23 Sep 26 - no price sheet or payment plan exists yet",1),("Masterplan: Gulf News, Jun 2023. Palm Central pricing and momentum: The National and Nakheel, 24 Jun 26",3),("Construction restart, delivery timing, infrastructure awards: Wikipedia / Propsearch, 2026",2)]),7,
 [("2<span>x</span>","The size of Palm Jumeirah"),("~110<span> km</span>","New coastline"),("Q1 2027","First Palm Jebel Ali deliveries")]))
# 07 SIDE BY SIDE
sb=[("Price","Đ3.9M","~Đ2.3M","~Đ3.3M","~Đ4M or less"),("Product","3-bed + maid apartment · 2,656 sqft","Townhouse","Villa","Townhouse"),("Day one","~Đ274K","~Đ161K","~Đ231K","4% DLD + launch deposit"),("Cash to handover","~Đ1.64M · 42%","~Đ1.31M · 57%","~Đ1.88M · 57%","At launch"),("Handover","2030","Q2 2031","Q2 2031","At launch"),("Registration","2%","2%","2%","4%"),("Demand driver","ADGM workforce · long-let","Family end-users · commuters","Family end-users · commuters","Palm Jebel Ali corridor"),("Exit","Pre-handover after 20% + NOC, or hold and rent","Pre-handover per Aldar rules, or hold","Pre-handover per Aldar rules, or hold","At launch")]
tr="".join(f'<tr><td class="k">{r[0]}</td>'+"".join(f'<td>{c}</td>' for c in r[1:])+'</tr>' for r in sb)
P.append(f'''<section class="pg">
{eye("The three doors · side by side",c="#9A7B2A")}
<h2>Same Đ4M, four ways to hold it.</h2>
<div class="rule"></div>
<table class="wide"><tr><th></th><th>{D("#9A7B2A")}Tara Park corner</th><th>{D("#9A7B2A")}Al Ghadeer 3-bed TH</th><th>{D("#9A7B2A")}Al Ghadeer 4-bed villa</th><th>{D("#9A7B2A")}Palm Springs 3-bed</th></tr>{tr}</table>
<div class="grow"></div>
{fn([("All figures indicative and before selling costs. Tara Park on Modon's Phase 2 schedule; Al Ghadeer on aggregator pricing pending Aldar's sheet; Palm Springs on a pre-launch conversation",2)])}
{foot(8)}
</section>''')
# 08 RETURNS
rt=[("Tara Park · Đ3.9M","~3.5 yrs to 2030","~Đ4.78M","~Đ0.79M","~48%","~Đ5.27M","~Đ1.27M","~77%","Đ1.64M"),
    ("Al Ghadeer 3-bed · Đ2.3M","~4.7 yrs to Q2 2031","~Đ3.02M","~Đ0.66M","~51%","~Đ3.45M","~Đ1.08M","~82%","Đ1.31M"),
    ("Al Ghadeer villa · Đ3.3M","~4.7 yrs to Q2 2031","~Đ4.34M","~Đ0.95M","~51%","~Đ4.95M","~Đ1.55M","~82%","Đ1.88M")]
tr="".join(f'<tr><td class="k">{r[0]}<span class="s">{r[1]} · cash deployed {r[8]}</span></td><td class="n">{r[2]}</td><td class="n">{r[3]}</td><td class="n b">{r[4]}</td><td class="n sep">{r[5]}</td><td class="n">{r[6]}</td><td class="n b">{r[7]}</td></tr>' for r in rt)
P.append(f'''<section class="pg">
{eye("Illustrative returns · exit at handover",c="#9A7B2A")}
<h2>One growth assumption, applied to every door.</h2>
<div class="rule"></div>
<table class="wide ret"><colgroup><col style="width:58mm"><col><col><col><col><col><col></colgroup>
<tr><th></th><th colspan="3" class="grp">At 6% a year</th><th colspan="3" class="grp sep">At 9% a year · half of Abu Dhabi's recent pace</th></tr>
<tr><th></th><th class="n">Value</th><th class="n">Gain</th><th class="n">On cash</th><th class="n sep">Value</th><th class="n">Gain</th><th class="n">On cash</th></tr>
{tr}
<tr><td class="k">Palm Springs</td><td colspan="6" class="mutd">Modelled after the price sheet lands.</td></tr>
</table>
<p class="method">Gain is after 2% agency on exit, before other costs. Return on cash = gain over cash deployed before handover (paid-in plus 2% registration).</p>
<div class="grow"></div>
<div class="rail">{D("#9A7B2A")}Growth cases are illustrative, not forecasts. Abu Dhabi's last twelve months were +17.8%. The register decides.</div>
<div style="height:10mm"></div>
{foot(9)}
</section>''')
# 09 NEXT STEP
P.append(f'''<section class="pg dark next">
{eye("Next step")}
<h2 class="xl">Fifteen minutes decides the lens.</h2>
<div class="rule"></div>
<div class="lens">
 <div><span class="ln">01</span><b>Long-let income on Reem</b><i>Tara Park · I hold the unit</i></div>
 <div><span class="ln">02</span><b>A family home on the corridor</b><i>Al Ghadeer Parks · I request Aldar's sheet</i></div>
 <div><span class="ln">03</span><b>First-phase Dubai</b><i>Palm Springs · I register you the day it opens</i></div>
</div>
<p class="then">Then I hold the unit, request Aldar's sheet, and register you for Palm Springs the day it opens.</p>
<div class="grow"></div>
<div class="cta">
 <a class="btn fill" href="https://wa.me/971553502699?text=Calum%20-%20read%20the%20%C4%904M%20pack">WhatsApp Calum</a>
 <a class="btn line" href="tel:+971553502699">Call +971 55 350 2699</a>
 <span class="ig">@uaecalum</span>
</div>
<div class="meta"><span><b>Calum MacLeod</b> · Abu Dhabi and Dubai</span><span>Private options pack · September 2026</span></div>
</section>''')
# 10 SOURCES
src=[("ValuStrat Abu Dhabi Real Estate Review Q2-2026","on file: content-assets/research/ · Aug 2026"),
     ("ADGM releases, Q1 2026","as cited in the Tara Park investor case · Aug 2026"),
     ("Modon Phase 2 payment schedule and DARI fee sheet","Jul 2026"),
     ("Aldar - Alghadeer masterplan release","Apr 2018 · Al Ghadeer Parks listing via Metropolitan, Sep 2026, indicative"),
     ("Nakheel / Dubai Holding - Palm Central release","24 Jun 2026 · Gulf News masterplan approval, Jun 2023"),
     ("Palm Springs","Dubai Holding, direct conversation with Calum · Sep 2026")]
sl="".join(f'<div class="f"><div class="v"><b>{a}</b><span class="s">{b}</span></div></div>' for a,b in src)
P.append(f'''<section class="pg">
{eye("Sources and the small print",c="#9A7B2A")}
<h2>Where every number came from.</h2>
<div class="rule"></div>
<div class="srcgrid">
 <div class="facts src">{sl}</div>
 <div class="key">
  {eye("How to read the marks",c="#9A7B2A")}
  <div class="kr">{conf(3)}<span><b>Documented.</b> A published report, a developer sheet, a signed rule.</span></div>
  <div class="kr">{conf(2)}<span><b>Reported.</b> Developer material or research cited second-hand; a method, not a document.</span></div>
  <div class="kr">{conf(1)}<span><b>Early.</b> Aggregator pricing, a pre-launch conversation, a market read. Confirm before you rely on it.</span></div>
  <p class="disc">Figures indicative until reservation documents confirm · before selling costs · growth cases illustrative · not financial advice · E&amp;OE. Prepared privately for Abu by Calum MacLeod, September 2026.</p>
 </div>
</div>
<div class="grow"></div>
{foot(11)}
</section>''')
CSS='''
@page{size:297mm 210mm;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#152A1F;-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{font-family:Carlito,Calibri,sans-serif;font-size:9.4pt;line-height:1.5;color:#152A1F}
.pg{--mut:#5d7266;--ln:#d9cfbd;width:297mm;height:210mm;padding:15mm 18mm 13mm;position:relative;overflow:hidden;page-break-after:always;display:flex;flex-direction:column;background:#F5EDE0}
.pg.dark{--mut:#8FA898;--ln:#2E5A40;background:#152A1F;color:#F5EDE0}
.dm{display:inline-block;vertical-align:.1em}
.eye{font-size:7.2pt;font-weight:700;letter-spacing:.3em;text-transform:uppercase;color:#C9A84C;line-height:1.4}
.eye .dm{margin-right:2.6mm;vertical-align:.05em}
.pg:not(.dark) .eye{color:#9A7B2A}
h1{font-family:'TeX Gyre Pagella',Palatino,serif;font-weight:400;font-size:58pt;line-height:.96;letter-spacing:-.01em}
h1 .g{color:#E8C96B}
h2{font-family:'TeX Gyre Pagella',Palatino,serif;font-weight:400;font-size:24pt;line-height:1.1;letter-spacing:-.005em;margin-top:4mm;max-width:210mm}
h2.xl{font-size:36pt;max-width:180mm}
.rule{width:16mm;height:.5mm;background:#C9A84C;margin:5mm 0 6mm}
.grow{flex:1}
.foot{position:absolute;left:18mm;right:18mm;bottom:7mm;display:flex;justify-content:space-between;font-size:6.2pt;letter-spacing:.14em;text-transform:uppercase;color:var(--mut);border-top:.25mm solid var(--ln);padding-top:2mm;font-weight:700}
.meta{display:flex;justify-content:space-between;font-size:7.4pt;letter-spacing:.06em;color:#8FA898;border-top:.25mm solid #2E5A40;padding-top:3mm}
.meta b{color:#F5EDE0;font-weight:700}
/* cover */
.cgrid{display:flex;flex:1;align-items:flex-end;gap:14mm;padding-bottom:10mm}
.cl{flex:1.25}.cr{flex:1;border-left:.25mm solid #2E5A40;padding-left:10mm;padding-bottom:2mm}
.sub{font-family:'TeX Gyre Pagella',Palatino,serif;font-style:italic;font-size:13.5pt;line-height:1.35;color:#F5EDE0;max-width:140mm}
.co{display:flex;gap:5mm;align-items:baseline;padding:4mm 0;border-bottom:.2mm solid #2E5A40}
.co:last-child{border-bottom:0}
.co .n{font-family:'TeX Gyre Pagella',Palatino,serif;font-size:19pt;color:#C9A84C;width:12mm}
.co b{display:block;font-size:12.5pt;font-weight:700}.co i{display:block;font-style:normal;font-size:8pt;color:#8FA898;letter-spacing:.03em;margin-top:.5mm}
.cover h1{margin-top:8mm}
/* numbers */
.trio,.quad{display:grid;grid-template-columns:repeat(3,1fr);gap:12mm;margin-top:2mm}
.quad{grid-template-columns:repeat(4,1fr);gap:9mm}
.quad.why{margin-top:8mm}.quad.why .big{font-size:56pt}.quad.why .lab{margin-top:5mm}.quad.why p{font-size:10.6pt}
.big{font-family:'TeX Gyre Pagella',Palatino,serif;font-size:50pt;line-height:1;letter-spacing:-.02em;font-variant-numeric:lining-nums}
.big span{font-size:.5em;color:#9A7B2A;letter-spacing:0}
.quad .big{font-size:40pt}
.lab{font-size:6.8pt;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:#9A7B2A;margin:3mm 0 2mm;line-height:1.45}
.trio p,.quad p{font-size:10pt;line-height:1.5;color:#2b4034}
.quote{margin-top:0;margin-bottom:6mm;border-left:.6mm solid #C9A84C;padding:2mm 0 2mm 7mm;max-width:232mm}
.quote .q{font-family:'TeX Gyre Pagella',Palatino,serif;font-style:italic;font-size:19pt;line-height:1.35}
.line{margin-top:6mm;font-size:9.4pt;color:#2b4034}
.names{margin-top:9mm}
.nl{font-family:'TeX Gyre Pagella',Palatino,serif;font-size:13.5pt;line-height:1.5;margin-top:2.5mm;letter-spacing:.005em}
.two{display:grid;grid-template-columns:1fr 1fr;gap:12mm;margin-top:7mm}
.two p{font-size:10.2pt;line-height:1.5;color:#2b4034}.two b,.three b{color:#152A1F}
/* footnotes */
.fn{margin-top:5mm;font-size:6.4pt;line-height:1.5;color:var(--mut)}
.fn div{display:flex;gap:2.2mm;align-items:baseline;padding:.6mm 0}
.cf{white-space:nowrap;width:8mm;flex:none;display:inline-flex;gap:.6mm}
/* option split */
.split{padding:0;flex-direction:row}
.ol{width:96mm;background:#1E3D2F;color:#F5EDE0;padding:15mm 12mm 16mm 18mm;display:flex;flex-direction:column;--mut:#8FA898}
.or{flex:1;padding:15mm 18mm 16mm 14mm;display:flex;flex-direction:column}
.split .foot{left:18mm;right:18mm}
.split .foot span:first-child{color:#8FA898}
.oname{font-family:'TeX Gyre Pagella',Palatino,serif;font-size:27pt;line-height:1.05;margin-top:5mm}
.owhere{font-size:8.2pt;letter-spacing:.1em;text-transform:uppercase;color:#8FA898;margin-top:2mm;font-weight:700}
.ol .rule{margin:5mm 0}
.ohero{font-family:'TeX Gyre Pagella',Palatino,serif;font-size:44pt;line-height:1;color:#E8C96B;letter-spacing:-.02em}
.ohero span{font-size:.55em;color:#C9A84C}
.ohero small{display:block;font-family:Carlito,sans-serif;font-size:8pt;letter-spacing:.24em;text-transform:uppercase;color:#C9A84C;font-weight:700;margin-bottom:2mm;letter-spacing:.24em}
.ohsub{font-size:9pt;color:#F5EDE0;margin-top:2.5mm;line-height:1.45}
.pills{margin-top:5mm}
.pill{display:inline-block;font-size:6.6pt;letter-spacing:.12em;text-transform:uppercase;font-weight:700;color:#152A1F;background:#C9A84C;padding:1.1mm 3mm .9mm;border-radius:99px;margin:0 1.5mm 1.8mm 0;line-height:1.3}
.pull{border-top:.25mm solid #2E5A40;padding-top:5mm}
.pq{display:block;font-family:'TeX Gyre Pagella',Palatino,serif;font-style:italic;font-size:14pt;line-height:1.3;color:#E8C96B}
.pa{display:block;font-size:6.8pt;letter-spacing:.2em;text-transform:uppercase;color:#8FA898;margin-top:3mm;font-weight:700}
.or h2{margin-top:0;font-size:22pt;max-width:165mm}
.strip{display:grid;grid-template-columns:repeat(3,1fr);gap:8mm;margin:4mm 0 2mm}
.strip .call .n{font-size:21pt}
.strip .call .l{margin-bottom:0}
.facts{margin-top:6mm}
.f{display:grid;grid-template-columns:27mm 1fr;gap:4mm;padding:3.4mm 0;border-bottom:.2mm solid var(--ln);align-items:baseline}
.f:last-child{border-bottom:0}
.f .k{font-size:6.6pt;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:#9A7B2A;padding-top:.6mm}
.f .v{font-size:10.2pt;line-height:1.45;color:#2b4034}
/* tables */
table{width:100%;border-collapse:collapse;font-size:8.6pt;font-variant-numeric:tabular-nums lining-nums}
th{font-size:6.4pt;letter-spacing:.16em;text-transform:uppercase;text-align:left;color:#9A7B2A;font-weight:700;padding:1.8mm 2mm 1.8mm 0;border-bottom:.4mm solid #C9A84C;vertical-align:bottom;line-height:1.4}
th .dm{margin-right:1.6mm}
td{padding:2.1mm 2mm 2.1mm 0;border-bottom:.2mm solid var(--ln);vertical-align:top;color:#2b4034;line-height:1.4}
td.n,th.n{text-align:right;padding-right:0}
tr.hl td{font-weight:700;color:#152A1F;border-bottom:none}
td.k{font-weight:700;color:#152A1F;width:34mm}
table.mini{margin-top:1mm;font-size:7.6pt}table.mini th{font-size:5.8pt;padding:1mm 1.5mm 1mm 0}table.mini td{padding:1.4mm 1.5mm 1.4mm 0}
table.wide{margin-top:2mm;font-size:10pt}table.wide td{padding:3.2mm 3mm 3.2mm 0}
.ret td{padding:4mm 3mm 4mm 0}
.ret th.grp{text-align:center;font-size:7pt;color:#152A1F}
.ret .sep{border-left:.25mm solid var(--ln);padding-left:4mm}
.ret td.b{font-weight:700;color:#9A7B2A;font-size:12.5pt;font-family:'TeX Gyre Pagella',Palatino,serif}
.ret td.k{width:auto;font-size:10.5pt}
.ret .s{display:block;font-weight:400;font-size:7pt;color:var(--mut);letter-spacing:.02em}
.ret .mutd{color:var(--mut);font-style:italic}
.method{font-size:7.6pt;color:var(--mut);margin-top:4mm;line-height:1.5}
.rail{margin-top:7mm;font-family:'TeX Gyre Pagella',Palatino,serif;font-style:italic;font-size:12.5pt;line-height:1.35;border-top:.25mm solid var(--ln);border-bottom:.25mm solid var(--ln);padding:4mm 0}
.rail .dm{margin-right:3mm;vertical-align:.15em}
/* payment page */
.pay{display:grid;grid-template-columns:70mm 1fr;gap:16mm;align-items:start}
.calls{display:flex;flex-direction:column;gap:6mm;padding-top:1mm}
.call{border-left:.6mm solid #C9A84C;padding-left:5mm}
.call .n{font-family:'TeX Gyre Pagella',Palatino,serif;font-size:23pt;line-height:1;letter-spacing:-.01em}
.call .n span{font-size:.55em;color:#9A7B2A}
.call .l{font-size:6.6pt;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:#9A7B2A;margin:1.6mm 0 1mm}
.call p{font-size:8.4pt;color:#2b4034;line-height:1.4}
.pay table{font-size:9.2pt}.pay td{padding:1.9mm 2mm 1.9mm 0}
.three{display:grid;grid-template-columns:repeat(3,1fr);gap:9mm;margin-top:8mm;font-size:9.4pt;line-height:1.45;color:#2b4034}
/* next */
.next h2{margin-top:6mm}
.lens{display:grid;grid-template-columns:repeat(3,1fr);gap:8mm;margin-top:4mm}
.lens div{border-top:.25mm solid #2E5A40;padding-top:5mm}
.lens .ln{display:block;font-family:'TeX Gyre Pagella',Palatino,serif;font-size:26pt;color:#C9A84C;line-height:1}
.then{font-family:'TeX Gyre Pagella',Palatino,serif;font-style:italic;font-size:15pt;line-height:1.4;color:#F5EDE0;margin-top:14mm;max-width:190mm}
.lens b{display:block;font-size:15pt;font-weight:700;margin-top:2mm;line-height:1.25}
.lens i{display:block;font-style:normal;font-size:9.4pt;color:#8FA898;margin-top:1.5mm;letter-spacing:.03em}
.cta{display:flex;align-items:center;gap:6mm;margin-bottom:10mm}
.btn{display:inline-block;padding:4.2mm 9mm;border:.4mm solid #C9A84C;border-radius:99px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;font-size:8pt;text-decoration:none;line-height:1}
.btn.fill{background:#C9A84C;color:#152A1F}.btn.line{color:#E8C96B}
.ig{font-size:8pt;letter-spacing:.14em;color:#8FA898;font-weight:700;margin-left:2mm}
/* sources */
.srcgrid{display:grid;grid-template-columns:1.15fr 1fr;gap:16mm;margin-top:2mm}
.facts.src .f{grid-template-columns:1fr}
.facts.src .s{display:block;font-size:8.2pt;color:var(--mut);margin-top:.4mm}
.key .kr{display:flex;gap:3mm;align-items:baseline;font-size:9.6pt;line-height:1.45;color:#2b4034;padding:2.4mm 0;border-bottom:.2mm solid var(--ln)}
.key .cf{width:8mm}
.key .eye{margin-bottom:2mm}
.disc{margin-top:6mm;font-size:7.2pt;line-height:1.55;color:var(--mut)}
'''
html=f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Abu · Three ways to place Đ4M · September 2026</title><!-- Source for content-assets/abu-4m-options/. Fonts: TeX Gyre Pagella + Carlito (the template placeholders until brand fonts are locked). Render: python3 render.py -> A4 landscape PDF + page PNGs. --><style>{CSS}</style></head><body>{"".join(P)}</body></html>'
open('Abu-4M-Three-Options-Sep26.html','w').write(html)
print("pages",len(P))
