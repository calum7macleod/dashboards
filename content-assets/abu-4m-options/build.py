import sys,re
BRISTOL = "--no-bristol" not in sys.argv
WAYS = "Five" if BRISTOL else "Four"
D=lambda c="#C9A84C",s=6: f'<svg class="dm" width="{s}" height="{s}" viewBox="0 0 10 10"><path d="M5 0 10 5 5 10 0 5Z" fill="{c}"/></svg>'
def conf(n,c="#C9A84C"): return '<span class="cf">'+"".join(D(c,4.6) for _ in range(n))+'</span>'
def eye(t,c="#C9A84C"): return f'<div class="eye">{D(c)}{t}</div>'
G="#9A7B2A"
PAGES=[]; TOTAL=[0]
def foot(): return '<div class="foot"><span>Abu · '+WAYS+' ways to place Đ4M · September 2026</span><span>Indicative until documents confirm · {PN} / {TOT}</span></div>'
def fn(items): return '<div class="fn">'+"".join(f'<div>{conf(c)}<span>{t}</span></div>' for t,c in items)+'</div>'
def calls(cs,cls="calls"): return f'<div class="{cls}">'+"".join(f'<div class="call"><div class="n">{a}</div><div class="l">{b}</div>{"<p>"+p+"</p>" if p else ""}</div>' for a,b,p in cs)+'</div>'
def facts(fs): return '<div class="facts">'+"".join(f'<div class="f"><div class="k">{k}</div><div class="v">{v}</div></div>' for k,v in fs)+'</div>'
def pg(cls,body): PAGES.append(f'<section class="pg {cls}">{body}{foot()}</section>')
def optpage(num,name,where,hero,heroSub,pills,h2,fs,pull,strip,notes):
    pl="".join(f'<span class="pill">{p}</span>' for p in pills)
    PAGES.append(f'''<section class="pg split"><div class="ol">{eye(f"Option {num}")}<div class="oname">{name}</div><div class="owhere">{where}</div><div class="rule"></div><div class="ohero">{hero}</div><div class="ohsub">{heroSub}</div><div class="pills">{pl}</div><div class="grow"></div><div class="pull">{pull}</div></div>
<div class="or"><h2>{h2}</h2>{facts(fs)}<div class="grow"></div>{calls(strip,"strip")}<div class="grow"></div>{notes}</div>{foot()}</section>''')
def whypage(eyebrow,h2,nums,fs,honest,notes,honest_lab="The honest line"):
    fcols="".join(f'<div class="f"><div class="k">{k}</div><div class="v">{v}</div></div>' for k,v in fs)
    pg("",f'''{eye(eyebrow,G)}<h2>{h2}</h2><div class="rule"></div>{calls(nums,"strip top")}<div class="facts two-col">{fcols}</div><div class="grow"></div><div class="honest"><span class="hl">{honest_lab}</span>{honest}</div><div class="grow"></div>{notes}''')
def paypage(eyebrow,h2,cs,table,three,notes):
    th="".join(f'<div>{t}</div>' for t in three)
    pg("",f'''{eye(eyebrow,G)}<h2>{h2}</h2><div class="rule"></div><div class="pay">{calls(cs)}{table}</div><div class="three{" four" if len(three)==4 else ""}">{th}</div><div class="grow"></div>{notes}''')
def pull(q,a): return f'<span class="pq">{q}</span><span class="pa">{a}</span>'
def tbl(head,rows,cls="",hl=None,colg=""):
    h="".join(f'<th class="{"n" if i else ""}">{c}</th>' for i,c in enumerate(head))
    r="".join(f'<tr class="{"hl" if i==hl else ""}">'+"".join(f'<td class="{"n" if j else ""}">{c}</td>' for j,c in enumerate(row))+'</tr>' for i,row in enumerate(rows))
    return f'<table class="{cls}">{colg}<tr>{h}</tr>{r}</table>'

# ---------- COVER
doors=[("01","Tara Park","Reem Island · Modon · 3-bed + maid, corner"),("02","Al Ghadeer Parks","Abu Dhabi-Dubai corridor · Aldar · townhouses and villas"),("03","Ellington, Al Yalayis 1","Near Town Square · Ellington · pre-launch townhouses"),("04","Palm Springs","Off Palm Jebel Ali · Dubai Holding · pre-launch")]
subs=["One island the banks are moving to.","One community priced for a family.","One design-led launch near Town Square.","One launch before the price sheet exists."]
if BRISTOL: doors.append(("05","The Bristol","Ramhan Island · Eagle Hills · branded apartments, pre-launch")); subs.append("One hotel-managed home on a natural island.")
co="".join(f'<div class="co"><span class="n">{n}</span><div><b>{a}</b><i>{b}</i></div></div>' for n,a,b in doors)
PAGES.append(f'''<section class="pg dark cover">{eye("Prepared for Abu · September 2026")}
<div class="cgrid"><div class="cl"><h1>{WAYS} ways<br>to place <span class="g">Đ4M</span></h1><div class="rule"></div><p class="sub">{"<br>".join(subs)}</p></div><div class="cr">{co}</div></div>
<div class="meta"><span><b>Calum MacLeod</b> · @uaecalum · +971 55 350 2699</span><span>Private options pack · every figure indicative until documents confirm</span></div></section>''')

# ---------- WHY NOW
pg("",f'''{eye("01 · Why now",G)}<h2>Two cities, two moments.</h2><div class="rule"></div>
<div class="mkt">{eye("Abu Dhabi · the earlier-cycle market",G)}
<div class="quad why">
 <div><div class="big">+17.8<span>%</span></div><div class="lab">Residential values, past twelve months</div><p>Reem Island +22% over the same period.</p></div>
 <div><div class="big">84<span>%</span></div><div class="lab">Of all Abu Dhabi sales are off-plan</div><p>Up 156% year on year. Buyers have moved to buying the future.</p></div>
 <div><div class="big">~7<span>%</span></div><div class="lab">Cash to own a contract, day one</div><p>5% down + 2% registration. Dubai: ~14% (4% DLD + deposit).</p></div>
 <div><div class="big">6-8<span>%</span></div><div class="lab">Typical Abu Dhabi gross yield</div><p>Long-let, one cheque cycle, before costs.</p></div>
</div></div>
<div class="mkt dxb">{eye("Dubai · the correcting market",G)}
<div class="quad why three-up">
 <div><div class="big">7</div><div class="lab">Straight monthly falls in the residential index</div><p>Peak 223.2 in Dec 2025, 206.0 in Jul 2026, -2.6% year on year. Off-plan still sells at a 25% premium to ready.</p></div>
 <div><div class="big">124</div><div class="lab">Project launches, H1 2026 · 410 in H1 2025</div><p>Deferred launches now compete on launch pricing, payment plans and unit selection. The buyer holds the cards this autumn.</p></div>
 <div><div class="big">+53<span>%</span></div><div class="lab">A Costa Brava 6-bed, May 2022 to Mar 2026</div><p>Bought Đ4.74M (987 psf) in the quiet months, resold Đ7.25M. Dubai's own precedent for buying now.</p></div>
</div></div>
<div class="grow"></div>
<div class="honest"><span class="hl">The read</span>The capital sits earlier in its cycle - the run Dubai has already had is still in front of Abu Dhabi. Dubai is correcting, launches are thin, and the buyer holds the cards this autumn.</div>
<div class="grow"></div>
{fn([("ValuStrat Abu Dhabi Real Estate Review Q2-2026 (Aug 26): values, Reem Island, off-plan share; entry costs per registration conventions; yields per Tara Park deck (a method, not a promise)",3),("Dubai index: PIX via Market, Jul-26. Launch count: Cavendish Maxwell H1 2026. Costa Brava resale: DLD title deeds, Aug 26",3)])}''')

# ---------- 01 TARA PARK
optpage("01","Tara Park","Reem Island · Modon","Đ3.9<span>M</span>","3-bed + maid · corner · 2,656 sqft BUA",
 ["Đ1,468 psf","~30% under AD off-plan average","Handover 2030","ADGM jurisdiction"],
 "A corner 3-bed on the financial island, around 30% under the Abu Dhabi off-plan average.",
 [("Developer","Modon - Abu Dhabi's government-backed master developer (Hudayriyat, Reem Island)."),
  ("The unit","3-bed + maid, corner position, 2,656 sqft built-up. Đ3,900,000 = Đ1,468 psf on built-up area, against an Abu Dhabi off-plan average of Đ2,104 psf."),
  ("Jurisdiction","Reem Island sits inside the ADGM financial free zone - English common law."),
  ("Position","Directly opposite Reem Mall, with a bridge into it. Five minutes to ADGM and Al Maryah; five minutes to downtown."),
  ("The building","Resort outdoor and indoor pools, park frontage, gym, running track, co-working lounge, kids' club, hotel-grade lobby."),
  ("Handover","Anticipated 2030.")],
 pull("&ldquo;I put my own money into this building.&rdquo;","Calum MacLeod"),
 [("Đ1,468<span> psf</span>","On built-up area",""),("Đ2,104<span> psf</span>","Abu Dhabi off-plan average",""),("5<span> min</span>","To ADGM and Al Maryah","")],
 fn([("Unit and price: Calum, 23 Sep 26. Off-plan average Đ2,104 psf: ValuStrat Q2-2026 - the average is blended, the unit is on built-up area, so read the gap as indicative",2),("Developer, jurisdiction, position, building: Modon Tara Park deck and scripts, Jul-Aug 26",3),("Handover 2030: Tara Park deck, Aug 26",2)]))
names="BlackRock · State Street · PGIM · Nuveen · Capital Group · Man Group · Bain Capital · Barings · Hillhouse · Binance"
pg("",f'''{eye("01 · Tara Park · why here",G)}<h2>The ADGM engine: why Reem rents, and re-rates.</h2><div class="rule"></div>
<div class="quad">
 <div><div class="big">47,047</div><div class="lab">People now work at ADGM</div><p>Up 44% in a year.</p></div>
 <div><div class="big">13,353</div><div class="lab">Active licences</div><p>Up more than 30% in a year. The largest international financial centre in the Middle East, Africa and South Asia.</p></div>
 <div><div class="big">+57<span>%</span></div><div class="lab">Assets under management, year on year</div><p>Q1-2026 entrants alone manage $4.4tn.</p></div>
 <div><div class="big">2<span>x</span></div><div class="lab">Reem leasing activity this year</div><p>While leasing cooled across most of the emirate, Reem's more than doubled.</p></div>
</div>
<div class="grow"></div>
<div class="names">{eye("Who moved in",G)}<div class="nl">{names}</div></div>
<div class="two"><p><b>Where they sit.</b> ADGM's own reporting names its workforce on Al Maryah <i>and</i> Al Reem Islands - the jurisdiction was extended onto Reem.</p><p><b>The tenant.</b> A finance professional ten minutes from the desk. Long-let, one cheque, low turnover. That is the income case for the unit on the previous page.</p></div>
<div class="grow"></div>
{fn([("ADGM releases, Q1 2026, as cited in the Tara Park investor case (Aug 26): headcount, licences, AUM, entrants",2),("Workforce location: ADGM reporting via Tara Park deck, Aug 26",3),("Reem leasing: published 2026 research via Tara Park deck, Aug 26",2),("Tenant profile: Calum's read of the market",1)])}''')
rows=[("Booking","5%","195,000"),("Registration 2% + DARI fee","fee","78,000 + 525"),("31 Jan 2027 · Early works","5%","195,000"),("31 Jul 2027 · Main works","5%","195,000"),("31 Jan 2028 · Podium","5%","195,000"),("31 Jul 2028 · Superstructure 50%","5%","195,000"),("31 Jan 2029 · Facade 50%","5%","195,000"),("31 Jul 2029 · Fit-out 50%","5%","195,000"),("31 Jan 2030 · Completion / BCC","5%","195,000"),("Handover","60%","2,340,000")]
paypage("01 · Tara Park · what you pay, when","Đ3.9M on a 40 / 60 plan.",
 [("~Đ273,500","Day one","5% booking + 2% registration + DARI fee."),("Đ1.64<span>M</span>","To handover · 42%","Eight instalments over three years, plus registration."),("Đ195,000","Largest single payment","Never more than 5% in one go before handover.")],
 tbl(["Milestone","Share","Amount"],[(a,b,"Đ"+c) for a,b,c in rows],hl=9),
 ["<b>The 60%.</b> Mortgageable at handover for a UAE resident, subject to bank approval at the time.","<b>Income.</b> 6.5% gross on value is ~Đ250K a year at today's price - higher on handover value. Abu Dhabi long-let rents are frozen at 0% since June 2026; capital growth is unaffected.","<b>Exit.</b> Sell the contract before handover once 20% is paid, with Modon's NOC. The buyer takes over the 60%. Admin fee to confirm."],
 fn([("Modon Phase 2 payment schedule (Jul 26); registration fees per DARI sheet. Dates are Phase 2 - confirmed on the reservation form",3),("Mortgageability at handover and rent method: Tara Park deck, Aug 26",2),("Resale rule: Modon resale rules - high on the rule, admin fee to confirm",3)]))

# ---------- 02 AL GHADEER
optpage("02","Al Ghadeer Parks","Abu Dhabi-Dubai corridor · Aldar","<small>from</small>~Đ2.3<span>M</span>","3-bed townhouse · 4-bed villa from ~Đ3.3M · 2-bed from Đ1.9M",
 ["55 / 45 · 5% down","Handover Q2 2031","453 homes","2% registration · freehold"],
 "Đ4M buys one 4-bed villa, a 3-bed townhouse with Đ1.7M held back, or two 2-bed townhouses.",
 [("The place","Aldar. 2- and 3-bed townhouses and 4-bed villas, 453 homes at Seih Al Sedeirah on the Abu Dhabi-Dubai corridor. Manicured parks and feature lakes; tree-lined, pedestrian-first streets; private gardens and shaded terraces."),
  ("Pricing","From Đ1.9M (2-bed townhouse). 3-bed townhouse from ~Đ2.3M; 4-bed villa from ~Đ3.3M. Two 2-beds land around Đ3.8M."),
  ("The plan","55 / 45 with 5% down. Handover Q2 2031."),
  ("The last phase","Al Ghadeer Gardens New Release: 352 homes from Đ1.85M, Q4 2030. 2-bed townhouses in middle and corner configurations, two interior schemes (Light and Dark), smart-living as standard, full-height windows. Pearl 3 and Fitwel 2-star certified."),
  ("Tenure","Freehold. Registration 2%, against Dubai's 4%.")],
 pull("A family home now, a rental later.","The Đ4M angle"),
 [("453","Homes in Al Ghadeer Parks",""),("Q2 2031","Handover",""),("5<span>%</span>","Down on booking","")],
 fn([("Product, pricing, plan, handover: Metropolitan listing, Sep 26 - aggregator numbers, Aldar's sheet requested. Read every price as indicative launch pricing",1),("Previous phase specification: Metropolitan, 2026",2),("Tenure and registration: Abu Dhabi conventions",3)]))
whypage("02 · Al Ghadeer Parks · why here","Between two airports, inside a 14,000-home masterplan, after a release that sold out in 48 hours.",
 [("48<span> hrs</span>","First Al Ghadeer Gardens release sold out",""),("14,408","Homes in Aldar's Đ10bn Alghadeer masterplan",""),("16<span> min</span>","To Al Maktoum airport","")],
 [("Access","E311, E11 and E611. Al Maktoum airport 16 min, Zayed airport 30 min, Yas Island 30 min, Abu Dhabi city 40 min. Expo City, Dubai Parks and Resorts and the future Palm Jebel Ali around 20 min."),
  ("The masterplan","Đ10bn over 15 years: 1.3M sqm of residential GFA, a HARVEST community farm, lakes, running and cycling tracks, solar-lit gardens, schools, a hotel, community pools and centres."),
  ("Established","Alghadeer already had 2,000+ homes and a family base when the masterplan launched - this is an extension, not a field."),
  ("Aldar's record","Revenue up nearly half last year; three-quarters of UAE sales to foreign buyers; Đ66bn of development contracts awarded in the UAE in 2025."),
  ("Aldar on the islands","Yas Point Phase 1 sold Đ1.5bn in launch week (Jul 26). Same developer here - corridor pricing instead of island pricing."),
  ("Yield","5-6% gross per year, per the aggregator. Hold until register comps exist.")],
 "40 minutes from the city and 14,000 homes to come - this is the value-and-family door, not the scarcity door.",
 fn([("Access, yield: Metropolitan, 2026 (aggregator)",1),("Masterplan and established community: Aldar press release, Apr 2018 - old, intent-level",3),("Aldar 2025 results: AGBI, Feb 26. Yas Point launch week: Tyron pack, Aug 26",2)]))
paypage("02 · Al Ghadeer Parks · what you pay, when","55 / 45, with 45% only at keys.",
 [("~Đ161<span>K</span>","Day one · 3-bed townhouse","5% booking + 2% registration on ~Đ2.3M."),("~Đ231<span>K</span>","Day one · 4-bed villa","On ~Đ3.3M."),("45<span>%</span>","At handover · Q2 2031","Construction instalment dates come with Aldar's sheet.")],
 tbl(["Milestone","Share","3-bed TH ~Đ2.3M","4-bed villa ~Đ3.3M"],[("Booking","5%","Đ115,000","Đ165,000"),("Registration 2%","fee","Đ46,000","Đ66,000"),("Construction instalments (dates TBC)","50%","Đ1,150,000","Đ1,650,000"),("Handover Q2 2031","45%","Đ1,035,000","Đ1,485,000"),("Cash to handover (55% + fee)","","~Đ1,311,000","~Đ1,881,000")],hl=4),
 ["<b>Income.</b> 5-6% gross (aggregator claim) is ~Đ115-138K a year on the 3-bed, ~Đ165-198K on the villa. Hold until register comps exist.","<b>Exit.</b> Pre-handover resale per Aldar's paid threshold and NOC - rules not on file, confirm at booking. Or hold and let into a family-commuter market.","<b>The honest line.</b> A 2031 handover on the corridor: phase-one pricing is the argument; a resale track record does not exist yet."],
 fn([("Plan and prices: Metropolitan listing, Sep 26 - indicative launch pricing until Aldar's sheet lands",1),("Registration: Abu Dhabi conventions",3)]))

# ---------- 03 ELLINGTON
optpage("03","Ellington<br>Al Yalayis 1","Near Town Square · Ellington","<span class=\"pre\">~</span>Đ1,750<span> psf</span>","3-bed townhouse 2,100-2,300 sqft · targeting under Đ4M at launch",
 ["70 / 30","EOIs open · launch Q4 2026","Handover 2030-31","4% DLD"],
 "A design-led Ellington townhouse in the Al Qudra corridor, at launch pricing, before the book opens.",
 [("The project","Ellington's first full master community - apartments, townhouses and standalone villas with green areas and leisure facilities - in Al Yalayis 1, near Town Square, minutes from Mira Oasis. Access to Al Qudra Road and Emirates Road."),
  ("The launch","Q4 2026, date TBC; EOIs collected now (it had been expected Q1 2026 and slipped). 70 / 30, Ellington's house plan. Handover 2030-2031."),
  ("Sizes and psf","Townhouses: 2-bed ~1,900 sqft · 3-bed 2,100-2,300 · 4-bed ~2,700, estimated at Đ1,700-1,800 psf. Villas 3,300-4,800 sqft at Đ1,900-2,000 psf. The teaser's estimate, not a price sheet."),
  ("The money",tbl(["Derived entry on the teaser psf","Indicative"],[("2-bed townhouse ~1,900 sqft","~Đ3.23-3.42M"),("3-bed townhouse 2,100-2,300 sqft · the Đ4M fit","~Đ3.57-4.14M"),("4-bed townhouse ~2,700 sqft","~Đ4.59-4.86M")],cls="mini"))],
 pull("Calum&rsquo;s pick as the best Dubai door.","Design-led · low density · launch pricing"),
 [("Đ2.85-3.7<span>M</span>","Ready townhouses next door, sold",""),("124","Dubai launches H1 2026 · 410 a year earlier",""),("96<span>%</span>","Occupancy across Ellington's delivered projects","")],
 fn([("Project, launch timing, sizes, psf, plan: Ellington teaser via Calum, 23 Sep 26; WhiteRock, Allsopp & Allsopp - pre-launch, name and exact location TBC",2),("Derived prices: teaser psf × teaser sizes - the top of the 3-bed range breaks Đ4M",2),("Ready comps: Calum's own deals - Mira Oasis 2 #228 Đ3.7M (Dec 25), Town Square 505 Noor Townhouses Đ2.85M (Aug 26). Occupancy: Property Finder, 2026",3)]))
whypage("03 · Ellington · why here","A design-led developer with a clean handover record, moving into family product where the ready prices are already known.",
 [("2014","Founded by Robert D. Booth, former managing director of Emaar",""),("3","International Property Awards, Ellington House 2023-24",""),("Đ2.85-3.7<span>M</span>","Whole ready townhouses in the corridor, on Calum's own ledger","")],
 [("The developer","Dubai residential developer, design-focused. Delivered and launched in Palm Jumeirah, JLT, MBR City, Downtown and Emirates Hills."),
  ("Delivery","Known for on-time handover, 70/30 and post-handover plans, and a 96% occupancy rate across delivered projects."),
  ("Design record","Ellington House, Dubai Hills: best kitchen design, best show home interior, best bathroom design at the 2023-24 International Property Awards."),
  ("The claim","Across 15 recent projects, average capital growth of 50% on studios and up to 69% on 2-beds; Ellington House gross yields of 11.8-13.4%. A broker's claim - verify before it is repeated."),
  ("The move","The first master-planned townhouse and villa community, after villas at The Sanctuary and The Watercrest in MBR City (from Đ5M, 70/30). Handover timed with RTA upgrades including the Latifa bint Hamdan Street extension."),
  ("The corridor's prices","Mira Oasis 2, unit 228: sold Đ3.7M (Dec 25). Town Square, 505 Noor Townhouses: sold Đ2.85M (Aug 26). Launches across Dubai fell from 410 to 124 in a year - the deferred ones compete on price, plan and unit selection.")],
 "~Đ1,750 psf off-plan against ready neighbours trading at Đ2.85-3.7M for a whole townhouse - the entry is a premium to ready, and the launch sheet decides whether 3-beds hold under Đ4M.",
 fn([("Developer history: off-planproperties.ae, Feb 26. Delivery, occupancy, awards: Property Finder, 2026. The move, infrastructure: Allsopp & Allsopp, Bayut, 2026",2),("Growth and yield claim: Allsopp & Allsopp, 2026 - broker claim, unverified",1),("Ready comps: deals.json, Dec 25 / Aug 26. Launch count: Cavendish Maxwell H1 2026",3)]))
paypage("03 · Ellington · what you pay, when","A mid-range 3-bed at Đ3.8M on 70 / 30.",
 [("Đ152<span>K</span>","DLD, day one","Plus the booking deposit - percentage set at launch."),("Đ2.81<span>M</span>","To handover · 74%","70% through construction, plus DLD."),("Đ1.14<span>M</span>","At keys · 30%","Handover 2030-2031.")],
 tbl(["Milestone","Share","Đ at 3.8M"],[("Booking (percentage set at launch)","TBC","launch deposit"),("DLD 4%","fee","Đ152,000"),("Construction instalments (milestones TBC)","70% incl. booking","Đ2,660,000"),("Handover 2030-31","30%","Đ1,140,000"),("Cash to handover (70% + DLD)","","~Đ2,812,000")],hl=4),
 ["<b>Income.</b> Dubai ready townhouses pay around 5-7% gross - ~Đ190-266K a year on Đ3.8M. Hold until Town Square and Mira Oasis rental comps are pulled.","<b>Exit.</b> Pre-handover resale once Ellington's paid threshold is met, plus NOC. Dubai developers commonly gate at 30-40% paid - confirm Ellington's at launch. Or hold and let into a family market.","<b>The honest line.</b> The 3-bed lands Đ3.57-4.14M on the teaser psf, so the top of the range breaks Đ4M. Targeting under Đ4M at launch."],
 fn([("Plan: Ellington teaser via Calum, 23 Sep 26. Booking percentage, milestones and resale threshold all set at launch",2),("Rent rail: Calum's on-camera range for Dubai ready townhouses",1),("DLD: Dubai conventions",3)]))

# ---------- 04 PALM SPRINGS
optpage("04","Palm Springs","Off Palm Jebel Ali · Dubai Holding","~Đ4<span>M</span>","or less · 3-bed townhouse · pre-launch · not yet public",
 ["Launch in the next couple of months","First phase","4% DLD + launch plan"],
 "A 3-bed townhouse beside the Palm, before the price sheet exists.",
 [("The launch","A Dubai Holding townhouse launch beside Palm Jebel Ali, expected within the next couple of months. 3-beds looking around Đ4M or less. Not yet public."),
  ("Price context","On the Palm itself, Nakheel's Palm Central runs from Đ2.7M (1-bed), Đ4.3M (2-bed), Đ7.5M (3-bed); townhouses from Đ14.9M; completion Sep 2030."),
  ("The value entry","A 3-bed townhouse at ~Đ4M beside the Palm is roughly a quarter of the on-Palm townhouse price - the entry ticket to the corridor."),
  ("Registration","Dubai 4% DLD, plus the developer's plan at launch.")],
 pull("&ldquo;I&rsquo;ll have you on the list the day it opens.&rdquo;","Calum MacLeod"),
 [("Đ14.9<span>M</span>","Townhouses on the Palm itself, from",""),("~&frac14;","The on-Palm townhouse price",""),("4<span>%</span>","DLD on registration","")],
 fn([("Launch timing and pricing: Calum's direct conversation with Dubai Holding, 23 Sep 26 - no price sheet or payment plan exists yet",1),("Palm Central pricing: The National, 24 Jun 26. Value-entry ratio derived from it",3)]))
whypage("04 · Palm Springs · why here","Dubai's next growth corridor, a government-owned master developer, and first deliveries in 2027.",
 [("2<span>x</span>","The size of Palm Jumeirah",""),("~110<span> km</span>","New coastline · homes for ~35,000 families",""),("Q1 2027","First Palm Jebel Ali deliveries","")],
 [("The island","Twice the size of Palm Jumeirah, ~110 km of new coastline, homes for ~35,000 families. Part of the Dubai 2040 Urban Master Plan - the beginning of a new growth corridor in the Jebel Ali area."),
  ("Progress","Construction restarted in 2024; first properties planned for delivery Q1 2027. Nakheel has awarded Đ5bn of infrastructure contracts, including a public access road from Sheikh Zayed Road."),
  ("The developer","Dubai Holding Real Estate is Nakheel's parent - the Palm's master developer is a government-owned group."),
  ("Proven demand","The June 2026 Palm Central release built on the strong market response to the October 2025 release. Demand on the Palm is proven before this launch opens."),
  ("Capital stacking up","Aldar and Dubai Holding expanded their joint venture to nearly 14,000 homes worth Đ38bn+, including a luxury waterfront on Palm Jebel Ali with sales from 2027. Dubai Holding has confirmed Select Group as the first private developer on the Palm.")],
 "Launch pricing, first phase, registered before the book opens.",
 fn([("Masterplan: Gulf News, Jun 2023. Nakheel parent, Palm Central momentum: The National and Nakheel, 24 Jun 26. JV and Select Group: Gulf News, 2026",3),("Construction restart, delivery timing, infrastructure awards: Wikipedia / Propsearch, 2026",2)]),honest_lab="The position")
paypage("04 · Palm Springs · what you pay, when","Nothing to model until the sheet lands. What is known:",
 [("~Đ160<span>K</span>","DLD 4% on a Đ4M ticket","Fixed."),("10-20<span>%</span>","Typical Dubai booking deposit","Plan shape set at launch."),("Q1 2027","First Palm Jebel Ali deliveries","A new launch will hand over later.")],
 tbl(["Item","Đ","Status"],[("3-bed townhouse target","~Đ4,000,000 or less","Calum / Dubai Holding, pre-launch"),("DLD 4%","~Đ160,000","fixed"),("Booking and construction instalments","set at launch","Dubai launches typically 10-20% on booking; plan shape TBC"),("Handover","TBC","first deliveries on the Palm Q1 2027; this launch will sit later")]),
 ["<b>Decide the trigger now, on shore.</b> &ldquo;If 3-beds open at or below Đ[X], I&rsquo;m in for one.&rdquo; Launches here are decided in hours.","<b>Exit.</b> Pre-handover resale per Dubai Holding's paid threshold and NOC; or hold for the corridor's build-out.","<b>The honest line.</b> Pre-launch, name and site not yet public. This page updates the day the sheet exists."],
 fn([("Target price: Calum's conversation with Dubai Holding, 23 Sep 26",1),("DLD and booking conventions: Dubai market practice",3)]))

# ---------- 05 THE BRISTOL · RAMHAN ISLAND (Eagle Hills)
if BRISTOL:
    optpage("05","The Bristol","Ramhan Island · Abu Dhabi · Eagle Hills","<span class=\"h-sm\">Price TBC</span>","Hotel-branded apartments · 3-beds listed on sale, 1- and 2-beds to follow · Eagle Hills' sheet not yet public",
     ["Freehold · 2% registration","Completion Dec 2028 listed","Construction started Apr 2026","Hotel-managed rental pool"],
     "A hotel-branded residence on Abu Dhabi's last natural island, ten minutes from Yas - the lifestyle door, on the Abu Dhabi fee schedule.",
     [("The project","Eagle Hills' branded hotel-and-residence tower, the hospitality centrepiece of the Ramhan masterplan - beside marina residences, wellness and a retail promenade. Glazed facades, wide terraces, sea views from every unit."),
      ("The units","1-, 2- and 3-bed apartments as listed; 3-beds on sale now, 1- and 2-beds to follow. Sizes and prices are not published."),
      ("The plan","Not announced. Listed as 10 / 60 / 30 on the portal; the island's villas run 10 / 40 / 50. Expect a booking amount, construction-linked instalments and the balance at keys."),
      ("Timing","Construction started April 2026. Completion listed December 2028; one broker quotes a 2027 hotel opening. The sheet decides."),
      ("How you use it","A home, a holiday retreat or a managed investment: 24/7 concierge, housekeeping, in-residence dining, private beach, spa and fine dining."),
      ("The brand","The Bristol Hotels &amp; Resorts - Eagle Hills' own hotel brand: Belgrade, Tangier, Durres, Addis Ababa, and a sister tower at Emaar Beachfront in Dubai. Freehold for all nationalities.")],
     pull("The island-resort door - and it&rsquo;s in Abu Dhabi.","The position"),
     [("10<span> min</span>","To Yas Island · 15 to Saadiyat",""),("2<span>%</span>","Registration, against Dubai's 4%",""),("170","Berths in the island marina","")],
     fn([("Units, listed plan, timeline, tenure: Property Finder project page (developer-fed), Sep 26 - the same page says the official plan is unreleased; island villa plan: ramhan.ae, Apr 26",2),("Project, services, 2027 hotel opening: Top Luxury Property, Grand Reve, Top Ultra Luxury launch coverage, Mar-Sep 26. Brand addresses: the-bristol.com, Sep 26",1)]))
    whypage("05 · The Bristol · why here","A natural island with supply capped by its own shoreline, a 170-berth marina and a Ritz-Carlton Reserve - at Abu Dhabi's 2% entry.",
     [("1,800","Villas and ~900 marina residences on ~400 hectares",""),("~Đ6.9<span>M</span>","Where the island's villas start · 3-bed",""),("10<span> min</span>","To Yas · 15 to Saadiyat and the airport","")],
     [("The island","Naturally formed, between Saadiyat and Yas - bays, waterways, mangroves, private beaches. ~4 million sqm: 1,800 standalone villas, ~900 marina residences, a 170-berth marina, a 1.7 km retail promenade and a Ritz-Carlton Reserve cluster of floating villas. Early phases hand over from Q4 2026."),
      ("Access","Boat today, about 10 minutes from Sheikh Khalifa bin Zayed Road; a bridge to the mainland is under construction. Yas 10 min, Saadiyat 15, Zayed airport 15-20, downtown 25-30, Dubai about an hour on the E11."),
      ("The price ladder","Villas from ~Đ6.9M (3-bed), Đ9.2M (4-bed), Đ14M (5-bed), Đ16M (6-bed), Đ22M (7-bed). Phase 4 hands over Q3 2028; Phase 5 from Đ11M, Q2 2027. The Bristol's apartments sit below all of it - the Đ4M route onto the island."),
      ("The developer","Eagle Hills: privately held, Abu Dhabi-based, founded 2014, led by Mohamed Alabbar, founder of Emaar. Waterfront masterplans across the UAE, Bahrain, Oman, Morocco, Serbia and Ethiopia. Also delivering the Bvlgari Resort and Mansions - 90 mansions, opening 2030 - on a private island off Abu Dhabi."),
      ("Supply","The island's natural boundaries cap future supply permanently. Villa plots sit 70-100 m of water apart; the spec is private pools, direct beach or lagoon access, natural marble and timber."),
      ("Income","Abu Dhabi waterfront luxury runs 5-6% gross on comparable stock (developer-site claim). A hotel brand and island setting point to short-let - which sits outside the 0% long-let rent cap. Hold until Eagle Hills publishes the rental programme.")],
     "The island-resort door - a hotel-managed residence with a private beach, in the capital's 2% market, before the price sheet exists.",
     fn([("Island scale, promenade, Ritz-Carlton Reserve, early handovers, yield claim: ramhan.ae (developer-affiliated), Apr 26. Hectares, villa and marina counts, price ladder, Eagle Hills profile: Primo Capital, 2026",2),("Access and villa spec: Metropolitan Phase 4 listing, Aug 26. Bvlgari: Ground Floor report, Aug 26. Eagle Hills history: Wikipedia, 2026",2),("Supply commentary: Top Luxury Property blog, Sep 26",1)]),honest_lab="The position")
    paypage("05 · The Bristol · what you pay, when","Nothing to model until the sheet lands. What is known:",
     [("~Đ80<span>K</span>","Registration 2% on a Đ4M ticket","Fixed. The ceiling is Abu's budget, not a price."),("10<span>%</span>","On booking, both plan shapes","Island villas: 10 / 40 / 50. The Bristol as listed: 10 / 60 / 30."),("Dec 2028","Completion, as listed","Hotel opening quoted 2027 by one broker.")],
     tbl(["Milestone","Share","Đ at the Đ4M ceiling · 10/40/50","Đ at the Đ4M ceiling · 10/60/30"],[("Booking","10%","Đ400,000","Đ400,000"),("Registration 2%","fee","Đ80,000","Đ80,000"),("Construction instalments (milestones TBC)","40% / 60%","Đ1,600,000","Đ2,400,000"),("Handover (date per the sheet)","50% / 30%","Đ2,000,000","Đ1,200,000"),("Cash to handover (paid-in + fee)","","~Đ2,080,000 · 52%","~Đ2,880,000 · 72%")],hl=4),
     ["<b>Income.</b> Hotel-managed short-let on a private-beach island; Abu Dhabi waterfront luxury runs 5-6% gross on comparable stock (developer-site claim). Short-let sits outside the 0% long-let cap. Hold until the rental programme is published.","<b>Decide the trigger now.</b> &ldquo;If 2-beds open at or below Đ[X], I&rsquo;m in.&rdquo; Island launches allocate on the day.","<b>Exit.</b> Pre-handover resale per Eagle Hills' paid threshold and NOC; or hold as a managed asset.","<b>The honest line.</b> A branded apartment, not a townhouse; boat access until the bridge opens; no public price sheet. This page updates the day it exists."],
     fn([("Listed plan: Property Finder project page, Sep 26 (official plan unreleased). Island villa plan: ramhan.ae, Apr 26",2),("Registration: Abu Dhabi conventions. Modelled at the Đ4M ceiling - Abu's budget, not a price",3)]))

# ---------- SIDE BY SIDE
cols=["Tara Park corner","Al Ghadeer 3-bed TH","Al Ghadeer 4-bed villa","Ellington 3-bed TH","Palm Springs 3-bed"]+(["The Bristol, Ramhan Island"] if BRISTOL else [])
sb=[("Price","Đ3.9M","~Đ2.3M","~Đ3.3M","~Đ3.6-4.1M","~Đ4M or less","TBC · not public"),
    ("Product","3-bed + maid apartment · 2,656 sqft","Townhouse","Villa","Townhouse · 2,100-2,300 sqft","Townhouse","Branded apartment · hotel-managed · sizes TBC"),
    ("Day one","~Đ274K","~Đ161K","~Đ231K","Launch deposit + Đ152K DLD","4% DLD + launch deposit","10% + 2% registration"),
    ("Cash to handover","~Đ1.64M · 42%","~Đ1.31M · 57%","~Đ1.88M · 57%","~Đ2.81M · 74%","At launch","~52-72% · plan TBC"),
    ("Handover","2030","Q2 2031","Q2 2031","2030-31","At launch","Dec 2028 listed · hotel 2027"),
    ("Registration","2%","2%","2%","4%","4%","2%"),
    ("Demand driver","ADGM workforce · long-let","Family end-users · commuters","Family end-users · commuters","Family end-users · Al Qudra corridor","Palm Jebel Ali corridor","Island resort short-let · capped supply"),
    ("Exit","Pre-handover after 20% + NOC, or hold and rent","Pre-handover per Aldar rules, or hold","Pre-handover per Aldar rules, or hold","Pre-handover per Ellington threshold, or hold","At launch","Pre-handover per Eagle Hills threshold, or hold")]
n=len(cols)+1
tr="".join(f'<tr><td class="k">{r[0]}</td>'+"".join(f'<td>{c}</td>' for c in r[1:n])+'</tr>' for r in sb)
th="".join(f'<th>{D(G)}{c}</th>' for c in cols)
pg("",f'''{eye("The doors · side by side",G)}<h2>Same Đ4M, {"six" if BRISTOL else "five"} ways to hold it.</h2><div class="rule"></div>
<table class="wide sbs"><colgroup><col style="width:30mm">{"".join("<col>" for _ in cols)}</colgroup><tr><th></th>{th}</tr>{tr}</table><div class="grow"></div>
{fn([("All figures indicative and before selling costs. Tara Park on Modon's Phase 2 schedule; Al Ghadeer on aggregator pricing pending Aldar's sheet; Ellington on the teaser psf; Palm Springs on a pre-launch conversation"+("; The Bristol on a listed plan pending Eagle Hills' price sheet" if BRISTOL else ""),2)])}''')

# ---------- RETURNS
rt=[("Tara Park · Đ3.9M","~3.5 yrs to 2030","~Đ4.78M","~Đ0.79M","~48%","~Đ5.27M","~Đ1.27M","~77%","Đ1.64M"),
    ("Al Ghadeer 3-bed · Đ2.3M","~4.7 yrs to Q2 2031","~Đ3.02M","~Đ0.66M","~51%","~Đ3.45M","~Đ1.08M","~82%","Đ1.31M"),
    ("Al Ghadeer villa · Đ3.3M","~4.7 yrs to Q2 2031","~Đ4.34M","~Đ0.95M","~51%","~Đ4.95M","~Đ1.55M","~82%","Đ1.88M"),
    ("Ellington 3-bed · Đ3.8M","~4.5 yrs to 2030-31","~Đ4.94M","~Đ1.04M","~37%","~Đ5.60M","~Đ1.69M","~60%","Đ2.81M")]
pending=["Palm Springs"]+(["The Bristol, Ramhan Island"] if BRISTOL else [])
tr="".join(f'<tr><td class="k">{r[0]}<span class="s">{r[1]} · cash deployed {r[8]}</span></td><td class="n">{r[2]}</td><td class="n">{r[3]}</td><td class="n b">{r[4]}</td><td class="n sep">{r[5]}</td><td class="n">{r[6]}</td><td class="n b">{r[7]}</td></tr>' for r in rt)
pg("",f'''{eye("Illustrative returns · exit at handover",G)}<h2>One growth assumption, applied to every door.</h2><div class="rule"></div>
<table class="wide ret"><colgroup><col style="width:58mm"><col><col><col><col><col><col></colgroup>
<tr><th></th><th colspan="3" class="grp">At 6% a year</th><th colspan="3" class="grp sep">At 9% a year · half of Abu Dhabi's recent pace</th></tr>
<tr><th></th><th class="n">Value</th><th class="n">Gain</th><th class="n">On cash</th><th class="n sep">Value</th><th class="n">Gain</th><th class="n">On cash</th></tr>{tr}
{"".join(f'<tr><td class="k">{p}</td><td colspan="6" class="mutd">Modelled after the price sheet lands.</td></tr>' for p in pending)}</table>
<p class="method">Gain is after 2% agency on exit, before other costs. Return on cash = gain over cash deployed before handover (paid-in plus registration). The Dubai door funds more of the price before keys, which is why its return on cash sits lower at the same growth rate.</p>
<div class="grow"></div><div class="rail">{D(G)}Growth cases are illustrative, not forecasts. Abu Dhabi's last twelve months were +17.8%. The register decides.</div><div style="height:8mm"></div>''')

# ---------- NEXT STEP
lens=[("01","Long-let income on Reem","Tara Park · I hold the unit"),("02","A family home on the corridor","Al Ghadeer Parks · I request Aldar's sheet"),("03","A design-led launch near Town Square","Ellington · I lodge the EOI"),("04","First-phase Palm Jebel Ali","Palm Springs · I register you the day it opens")]
if BRISTOL: lens.append(("05","A hotel-managed home on a natural island","The Bristol, Ramhan · I get Eagle Hills' sheet the moment it is released"))
ld="".join(f'<div><span class="ln">{n}</span><b>{a}</b><i>{b}</i></div>' for n,a,b in lens)
PAGES.append(f'''<section class="pg dark next">{eye("Next step")}<h2 class="xl">Fifteen minutes decides the lens.</h2><div class="rule"></div>
<div class="lens l{len(lens)}">{ld}</div>
<p class="then">Then I hold the unit, request Aldar's sheet, lodge the Ellington EOI{", register you for Palm Springs the day it opens, and get Eagle Hills' Bristol sheet the moment it is released." if BRISTOL else ", and register you for Palm Springs the day it opens."}</p>
<div class="grow"></div>
<div class="cta"><a class="btn fill" href="https://wa.me/971553502699?text=Calum%20-%20read%20the%20%C4%904M%20pack">WhatsApp Calum</a><a class="btn line" href="tel:+971553502699">Call +971 55 350 2699</a><span class="ig">@uaecalum</span></div>
<div class="meta"><span><b>Calum MacLeod</b> · Abu Dhabi and Dubai</span><span>Private options pack · September 2026</span></div></section>''')

# ---------- SOURCES
src=[("ValuStrat Abu Dhabi Real Estate Review Q2-2026","on file: content-assets/research/ · Aug 2026"),
     ("Dubai market","PIX residential index Jul-26 (Market) · Cavendish Maxwell H1 2026 launch count · DLD title deeds (film kit, Aug 26)"),
     ("ADGM releases, Q1 2026","as cited in the Tara Park investor case · Aug 2026"),
     ("Modon Phase 2 payment schedule and DARI fee sheet","Jul 2026"),
     ("Aldar","Alghadeer masterplan release (Apr 2018) · Al Ghadeer Parks and Gardens listings via Metropolitan (2026, indicative) · AGBI on Aldar's 2025 results (Feb 2026)"),
     ("Ellington","Launch teaser via Calum (23 Sep 2026) · Allsopp &amp; Allsopp, Property Finder, WhiteRock, Bayut developer pages (2026)"),
     ("Nakheel / Dubai Holding","Palm Central release (24 Jun 2026) · Gulf News masterplan approval (Jun 2023), Aldar-Dubai Holding JV and Select Group announcements (2026)"),
     ("Palm Springs","Dubai Holding, direct conversation with Calum · Sep 2026")]
if BRISTOL: src.append(("Eagle Hills / Ramhan Island","ramhan.ae (Apr 2026) · Property Finder project page (Sep 2026) · Metropolitan Phase 4 listing (Aug 2026) · Primo Capital, Top Luxury Property, Top Ultra Luxury and Grand Reve launch coverage of The Bristol (Mar-Sep 2026) · the-bristol.com · Eagle Hills press (Apr 2026) · Bvlgari Ramhan from the Ground Floor report (Aug 2026) - no price sheet yet"))
sl="".join(f'<div class="f"><div class="v"><b>{a}</b><span class="s">{b}</span></div></div>' for a,b in src)
pg("",f'''{eye("Sources and the small print",G)}<h2>Where every number came from.</h2><div class="rule"></div>
<div class="srcgrid"><div class="facts src">{sl}</div><div class="key">{eye("How to read the marks",G)}
<div class="kr">{conf(3)}<span><b>Documented.</b> A published report, a developer sheet, a signed rule, a title deed.</span></div>
<div class="kr">{conf(2)}<span><b>Reported.</b> Developer material or research cited second-hand; a method, not a document.</span></div>
<div class="kr">{conf(1)}<span><b>Early.</b> Aggregator pricing, a pre-launch conversation, a broker claim, a market read. Confirm before you rely on it.</span></div>
<p class="disc">Figures indicative until reservation documents confirm · before selling costs · growth cases illustrative · not financial advice · E&amp;OE. Prepared privately for Abu by Calum MacLeod, September 2026.</p></div></div><div class="grow"></div>''')

CSS=open('style.css').read()
tot=len(PAGES)
body="".join(p.replace("{PN}",f"{i+1:02d}").replace("{TOT}",str(tot)) for i,p in enumerate(PAGES))
name="Abu-4M-Options-Sep26"+("" if BRISTOL else "-four-doors")
open(name+'.html','w').write(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Abu · {WAYS} ways to place Đ4M · September 2026</title><!-- Source for content-assets/abu-4m-options/. Generated by build.py (flag --no-bristol for the four-door cut). Fonts: TeX Gyre Pagella + Carlito (template placeholders until brand fonts are locked). --><style>{CSS}</style></head><body>{body}</body></html>')
print(name,"pages",tot)
