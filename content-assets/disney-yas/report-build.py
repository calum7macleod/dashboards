import html
CY="#1aa7c9"; GR="#c9ced3"; TX="#111"; MU="#666"
def hbar(title,sub,rows,h=None,note=None,ref=None):
    # rows: (label, value, display, accent)
    mx=max(v for _,v,_,_ in rows); x0=230; w=330; rh=36; top=58
    H=h or top+len(rows)*rh+ (26 if note else 10)
    s=f'<svg viewBox="0 0 760 {H}" width="100%" font-family="Carlito,Calibri,sans-serif" font-size="13">'
    s+=f'<text x="0" y="18" font-family="Montserrat" font-weight="700" font-size="14" fill="{TX}">{html.escape(title)}</text>'
    if sub: s+=f'<text x="0" y="38" fill="{MU}">{html.escape(sub)}</text>'
    for i,(lab,v,disp,acc) in enumerate(rows):
        y=top+i*rh; bw=max(3,v/mx*w)
        s+=f'<text x="{x0-10}" y="{y+18}" text-anchor="end" fill="{TX}">{html.escape(lab)}</text>'
        s+=f'<rect x="{x0}" y="{y}" width="{bw:.1f}" height="24" fill="{CY if acc else GR}"/>'
        s+=f'<text x="{x0+bw+8:.1f}" y="{y+17}" font-weight="700" fill="{TX}">{html.escape(disp)}</text>'
    if ref is not None:
        rx=x0+ref/mx*w; s+=f'<line x1="{rx:.1f}" y1="{top-6}" x2="{rx:.1f}" y2="{top+len(rows)*rh-6}" stroke="#555" stroke-dasharray="4 3"/>'
    if note: s+=f'<text x="0" y="{H-8}" font-size="11" fill="{MU}">{html.escape(note)}</text>'
    return s+'</svg>'
def shanghai():
    prices=[("Before","2006-07",34),("At approval","2009",177),("By opening*","2016",704)]; growth=[("Homes near Disney",162,True),("Shanghai overall",101,False)]
    s='<svg viewBox="0 0 760 330" width="92%" font-family="Carlito,Calibri,sans-serif" font-size="13">'
    s+=f'<text x="0" y="18" font-family="Montserrat" font-weight="700" font-size="14" fill="{TX}">Shanghai: homes near Disney jumped around the approval, then beat the city</text>'
    s+=f'<text x="0" y="46" font-weight="700" fill="{TX}">Homes near the site, $ per sq ft</text><text x="0" y="64" fill="{MU}">About 5 times in two to three years</text>'
    base=280; hmax=170; pmax=704
    for i,(lab,per,v) in enumerate(prices):
        x=30+i*105; ph=v/pmax*hmax
        s+=f'<rect x="{x}" y="{base-ph:.1f}" width="64" height="{ph:.1f}" fill="{CY}" fill-opacity="{0.35+i*0.32:.2f}"/>'
        s+=f'<text x="{x+32}" y="{base-ph-8:.1f}" text-anchor="middle" font-weight="700" fill="{TX}">${v}</text>'
        s+=f'<text x="{x+32}" y="{base+18}" text-anchor="middle" fill="{TX}">{lab}</text><text x="{x+32}" y="{base+34}" text-anchor="middle" fill="{MU}">{per}</text>'
    s+=f'<line x1="20" y1="{base}" x2="350" y2="{base}" stroke="#888"/>'
    s+=f'<text x="0" y="322" font-size="11" fill="{MU}">* Some projects 3km from the park. Earlier bars are area averages.</text>'
    s+=f'<text x="430" y="46" font-weight="700" fill="{TX}">Price growth, 2009-2015</text>'
    for i,(lab,p,acc) in enumerate(growth):
        y=100+i*80; gl=p/162*250
        s+=f'<text x="430" y="{y}" fill="{TX}">{lab}</text><rect x="430" y="{y+10}" width="{gl:.1f}" height="30" fill="{CY if acc else GR}"/><text x="{430+gl+8:.1f}" y="{y+31}" font-weight="700" fill="{TX}">+{p}%</text>'
    return s+'</svg>'
def payplan():
    sched=[("Booking","Nov 2026",5),("23 May","2027",10),("23 Jan","2028",10),("23 Sep","2028",10),("23 May","2029",10),("23 Jan","2030",10),("Handover","Q1 2031",45)]
    units=[("2 bedroom + maid's, from $1.06m",1061947,0.5),("3 bedroom + maid's, from $1.42m",1415929,1)]
    base=300; hmax=180; left=20; band=720/len(sched); bw=34; maxamt=1415929*0.45
    s='<svg viewBox="0 0 760 390" width="100%" font-family="Carlito,Calibri,sans-serif" font-size="12">'
    s+=f'<text x="0" y="18" font-family="Montserrat" font-weight="700" font-size="14" fill="{TX}">Canopies Sanctuary: what\'s due, and when</text><text x="0" y="38" fill="{MU}">55% before the keys, paid over three years; 45% at handover</text>'
    for j,(lab,u,op) in enumerate(units): s+=f'<rect x="{0+j*330}" y="52" width="14" height="14" fill="{CY}" fill-opacity="{op}"/><text x="{20+j*330}" y="64" fill="{TX}">{lab}</text>'
    run=0
    for i,(when,date,pct) in enumerate(sched):
        run+=pct
        for j,(lab,u,op) in enumerate(units):
            amt=u*pct/100; h=amt/maxamt*hmax; x=left+i*band+band/2-bw+j*bw
            s+=f'<rect x="{x:.1f}" y="{base-h:.1f}" width="{bw-4}" height="{h:.1f}" fill="{CY}" fill-opacity="{op}"/><text x="{x+(bw-4)/2:.1f}" y="{base-h-6:.1f}" text-anchor="middle" font-size="11" fill="{TX}">${round(amt/1000)}k</text>'
        cx=left+i*band+band/2
        s+=f'<text x="{cx:.1f}" y="{base+18}" text-anchor="middle" fill="{TX}">{pct}%</text><text x="{cx:.1f}" y="{base+36}" text-anchor="middle" fill="{MU}">{when}</text><text x="{cx:.1f}" y="{base+52}" text-anchor="middle" fill="{MU}">{date}</text><text x="{cx:.1f}" y="{base+70}" text-anchor="middle" font-size="11" fill="{MU}">{run}% paid</text>'
    s+=f'<line x1="{left}" y1="{base}" x2="{left+720}" y2="{base}" stroke="#888"/>'
    return s+'</svg>'
def fig(svg,cap): return f'<figure>{svg}<figcaption>{cap}</figcaption></figure>'
def table(head,rows,last_bold=False):
    h="".join(f'<th>{c}</th>' for c in head); r=""
    for i,row in enumerate(rows):
        b=last_bold and i==len(rows)-1
        r+='<tr>'+"".join(f'<td>{"<b>"+c+"</b>" if b else c}</td>' for c in row)+'</tr>'
    return f'<table><thead><tr>{h}</tr></thead><tbody>{r}</tbody></table>'
B=[]
B.append('<h2>Why I wrote this</h2><p>Disney has opened six resorts in 70 years. Near the ones that worked, property moved most between the announcement and the opening, not after it. Disneyland Abu Dhabi was announced in May 2025 and is expected in the early 2030s, so Yas is in that window now.</p><p>Before the next phase of Yas Point launches on 26 November, I wanted to see the evidence for myself: what happened near every Disney, and where Yas stands today. Everything is in US dollars. I\'ve also kept in the parts that don\'t flatter the story, because you should see those too.</p>')
B.append('<h2>What Disney did to property</h2><p>Three resorts have the price data to show it clearly: Orlando, Shanghai and Paris.</p><p><b>Orlando.</b> Walt Disney bought 27,000 acres of Florida swamp in secret, paying under $200 an acre. Once the 1965 announcement broke, an acre nearby sold for $131,000. By the time the park opened in 1971, land was trading at up to 500 times its 1965 price.</p>'
 +fig(hbar("Orlando land: under $200 an acre, then $131,000","About 655 times as much, once Disney\'s name came out in 1965",[("Disney paid, per acre",200,"$200",False),("A nearby acre, after the news",131000,"$131,000",True)]),"The Walt Disney Company; BusinessWeek, 1971")
 +'<p><b>Shanghai.</b> The clearest before-and-after of all. Homes near the site jumped about fivefold in the two to three years around the 2009 approval, and 90 minutes after the green light a nearby plot sold for 264% of its starting price. Over 2009-2015, homes near Disney rose 162%, against 101% across Shanghai.</p>'
 +fig(shanghai(),"DTZ via Shanghai Daily (2009); China Daily (2016); South China Morning Post (2016). Yuan converted at 6.83 (2009) and 6.6 (2016) to the dollar")
 +'<p><b>Paris.</b> Chessy was a farming village when Disney arrived in 1992. Today, apartments in the two towns at Disney\'s gates sell at a 41-47% premium to the rest of the département, 34 years on.</p>'
 +fig(hbar("Paris: the towns at Disney\'s gates sell 41-47% above their region","Apartments, $ per sq ft, July 2026",[("Serris (next to Disney)",523.3,"$523  (+47%)",True),("Chessy (Disney\u2019s town)",503.9,"$504  (+41%)",True),("Seine-et-Marne average",356.9,"$357",False)],ref=356.9),"PAP / DVF registered sales, July 2026; \u20ac1 = $1.16")
 +'<p><b>The other three, in a line each:</b></p><ul><li><b>Anaheim, 1955:</b> a town of about 14,500 in 1950 had over 104,000 people by 1960, with 25 hotels around the park. The post-war boom helped; Disney accelerated it.</li><li><b>Tokyo, 1983:</b> built on land reclaimed from the sea by a local company that licenses the Disney name. The town around it nearly doubled in the decade it opened.</li><li><b>Hong Kong, 2005:</b> small, isolated, and lost money in eight of its first eleven years. I couldn\'t find any property boom around it.</li></ul>')
B.append('<h2 class="np">The pattern</h2><p>The big moves came in the years between the announcement and the opening. In Orlando and Shanghai, land and homes jumped on the news, years before a single ride ran.</p>'
 +table(["Resort","Announced","Opened","What happened nearby"],[("Anaheim","1954","1955","Town grew sevenfold in a decade"),("Orlando","1965","1971","Land from under $200 an acre to $131,000"),("Tokyo","1979","1983","Town nearly doubled in the decade it opened"),("Paris","1987","1992","Neighbouring towns trade 41-47% above their region"),("Hong Kong","1999","2005","No premium I could find"),("Shanghai","2009","2016","Homes nearby +162% against +101% for the city"),("Abu Dhabi","2025","Early 2030s","Yas is in the window now")],last_bold=True)
 +'<p>It isn\'t automatic. Hong Kong shows that Disney on its own doesn\'t move a market: size, location and the wider economy matter as much.</p>')
B.append('<h2>Yas today</h2><p>Yas is already full of visitors without Disney, and it\'s the best-connected island to Dubai. But so far, its prices have risen with Abu Dhabi, not ahead of it.</p>'
 +'<p><b>Demand, before Disney.</b> Yas hotels averaged 85% occupancy over summer 2025. In August 2026, the year of the regional conflict, they were 92% full. August is the hottest, quietest month of the UAE\'s tourist year, and Yas fills up anyway, because its theme parks are indoors.</p>'
 +'<p><b>Visitors.</b> Yas had 44 million visits in 2025, up 16% on the year before. Abu Dhabi\'s tourism plan targets 39.3 million visitors a year to the emirate by 2030, and 50,000 hotel rooms. Yas counts every trip, residents included, so the two aren\'t like for like, but the direction is clear.</p>'
 +'<p><b>Closest to Dubai, and the rail.</b> Yas is the Abu Dhabi island nearest Dubai, about 50 minutes by road. The bigger change is the high-speed rail, now under construction, with a station on Yas: up to 350 km/h, and about 30 minutes to Dubai. One line, six stops: Reem, Saadiyat, Yas and Zayed International Airport in Abu Dhabi, then Al Maktoum Airport and Al Jaddaf in Dubai. The contractor is targeting 2031 (Etihad Rail had said 2030), the same year the Canopies Sanctuary hands over and just ahead of Disney. Dubai\'s residents and visitors end up half an hour from Yas, with Abu Dhabi\'s airport one stop away.</p>'
 +'<p><b>Since the announcement.</b> Comparing the same buildings in the year before May 2025 and the last twelve months, Yas resale prices are up 33%. Reem, Al Raha and Saadiyat moved by similar amounts. On the Shanghai pattern, the Disney premium hasn\'t shown up on Yas yet.</p>'
 +fig(hbar("Since Disney was announced, Yas has kept pace with Abu Dhabi, not pulled ahead","Resale apartment prices, same buildings: year before May 2025 against the last 12 months",[("Reem",39.4,"+39%",False),("Al Raha",38.1,"+38%",False),("Yas",33.0,"+33%",True),("Saadiyat",28.0,"+28%",False)],ref=35.2,note="Other three islands\' average: +35%"),"Abu Dhabi registered sales, my analysis: median resale price per building, 7 May 2024-6 May 2025 against Nov 2025-Oct 2026; buildings with 10+ resales in both periods")
 +'<p><b>Rental yields.</b> Yas apartments earn about 6-7% gross. That\'s in line with Dubai\'s overall average, and above Dubai\'s own leisure addresses:</p>'
 +table(["Area","Gross apartment yield"],[("Yas Island","about 6-7%"),("Dubai, all apartments","6.9%"),("Dubai Marina","5.6%"),("Downtown Dubai","5.2%"),("Palm Jumeirah","4.7%")]))
B.append('<h2 class="np">Yas Point and the Canopies Sanctuary</h2><p>Yas Point is Aldar\'s $1.63 billion masterplan on Yas\'s northern shore, one of the last undeveloped stretches of the island. Disney is confirmed for the same northern coast; its exact plot hasn\'t been published yet.</p>'
 +'<figure><img src="map.png" alt="Yas Island: Yas Point on the northern tip, next to the Disneyland Abu Dhabi site"><figcaption>Yas Island: Yas Point on the northern tip, next to the Disneyland Abu Dhabi site. Map data OpenStreetMap; Disney and Yas Point areas indicative.</figcaption></figure>'
 +'<ul><li><b>The masterplan:</b> 600,000 square metres and about 1,600 homes, with a public beach, a marina and yacht club, a 700-metre promenade and a five-star hotel</li><li><b>Nearby:</b> Yas Mall 3 minutes, the airport 10, Saadiyat 15, Dubai about 50</li><li><b>The Canopies Sanctuary:</b> the newest phase, 388 homes in three buildings, five minutes\' walk from the beach</li></ul>'
 +'<p><b>See it for yourself:</b> the Canopies Sanctuary folder from Aldar has the CGIs, factsheet, coloured floor plates and layouts, and the material board.</p>'
 +table(["Home","From","Average size","From, per sq ft"],[("Studio","$452,000","484 sq ft","about $934"),("1 bedroom","$626,000","872 sq ft","about $718"),("2 bedroom","$926,000","1,227 sq ft","about $755"),("2 bedroom + maid\'s","$1.06m","1,453 sq ft","about $731"),("3 bedroom + maid\'s","$1.42m","1,948 sq ft","about $727")])
 +'<p><b>Payment plan:</b> 5% on booking, then 10% every eight months from May 2027 to January 2030, and 45% at handover in Q1 2031. That\'s 55% before the keys.</p>'
 +fig(payplan(),"Aldar launch details, November 2026; prices are starting prices, $1 = 3.6725 dirhams")
 +'<p><b>Short-term lets.</b> Using my own nightly rates for the Canopies Sanctuary and 85% occupancy, Yas\'s hotel average last summer:</p>'
 +table(["Home","Nightly rate","Gross yield at 85%","At 60%"],[("Studio","$200","13.7%","9.7%"),("1 bedroom","$250","12.4%","8.7%"),("2 bedroom","$350","11.7%","8.3%"),("2 bedroom + maid\'s","$400","11.7%","8.2%"),("3 bedroom + maid\'s","$500","11.0%","7.7%")])
 +'<p>For context, the WB hotel on Yas averaged about $400 a night in August 2025, and a two-bedroom home on Yas let for over $1,400 a night in Grand Prix week. But these are gross, before management, licensing, service charges and furnishing, and holiday homes fill less reliably than hotels: across Abu Dhabi they average nearer 60% occupancy over a year, which is why I\'ve shown that column too.</p>'
 +'<p><b>Launch:</b> priority and international sales on 25 November, the public launch on 26 November. Appointments open on 16-17 November.</p>')
B.append('<h2>What it could mean for Yas</h2><p>This is an illustration from the one comparable case, not a forecast. Shanghai is the only Disney with price data both next to the park and across the whole city, and by opening, homes near Disney ended about 30% above where the city\'s growth alone would have taken them.</p><ul><li><b>Yas\'s top new buildings today:</b> about $720-800 per sq ft</li><li><b>With a Shanghai-style 30% premium:</b> about $940-1,040 per sq ft, in today\'s money, before any general market growth</li><li><b>On Hong Kong\'s path:</b> no premium at all</li></ul><p>That upper figure isn\'t a stretch: Saadiyat\'s newest launches already sell at $940-1,060 per sq ft.</p>')
B.append('<h2>What could go wrong</h2><ul><li><b>Yas hasn\'t beaten the market yet.</b> Since the announcement it has moved with Reem, Al Raha and Saadiyat, not ahead of them. The premium may come, or may be smaller than Shanghai\'s.</li><li><b>Supply.</b> Around 7,700 homes are under construction on Yas, more than on any other Abu Dhabi island.</li><li><b>Handover waves.</b> When many units hand over at once, resale prices can pause for a while. Yas Point will hand over a large phase in one go too.</li><li><b>No opening date.</b> Disney\'s own estimate is one to two years to design and four to six to build, which points to the early 2030s. Timelines slip.</li><li><b>Shanghai cooled.</b> The frenzy around the 2009 approval later settled back to the city\'s average growth.</li><li><b>It isn\'t automatic.</b> Hong Kong had Disney and no premium.</li></ul>')
B.append('<h2>How to secure a unit</h2><p>If you want one, timing matters: the best units go to whoever submits first, so I\'d submit the moment the system opens.</p><ol><li>Tell me which home you want and your budget.</li><li>Send me your documents.</li><li>I upload them to Aldar\'s portal, and we secure the unit with the 5% booking payment.</li></ol><p><b>Still a maybe? Submit anyway.</b> Getting your documents in early keeps your place for the best units, and nothing is paid until you decide to go ahead. We look at what\'s available together, and if it isn\'t right, you simply don\'t book.</p><p>Appointments open on 16-17 November, ahead of the launch on 25-26 November.</p>')
B.append('<h2 class="np">Sources</h2><ul class="src"><li><b>Abu Dhabi prices, Yas and Saadiyat analysis:</b> registered sales data for Abu Dhabi, January 2019 to October 2026 (126,500 transactions), my own analysis; whole-unit residential sales only</li><li><b>Orlando:</b> The Walt Disney Company; BusinessWeek, 11 September 1971</li><li><b>Shanghai:</b> China Daily, November 2009; Shanghai Daily / DTZ; South China Morning Post, 2016; China Daily, July 2016; Mingtiandi / Savills</li><li><b>Paris:</b> PAP / DVF, Chessy and Serris, July 2026</li><li><b>Anaheim, Tokyo, Hong Kong:</b> City of Anaheim; Oriental Land Co.; Japanese census via Urayasu; Attractions Management</li><li><b>Disneyland Abu Dhabi:</b> The National</li><li><b>Yas hotels:</b> Miral, via Gulf News and Arabian Business</li><li><b>High-speed rail:</b> Gulf News; 2031 target: AGBI, August 2026</li><li><b>Yields:</b> Cavendish Maxwell H1 2026; Engel &amp; V\u00f6lkers, August 2026; Bayut H1 2026</li><li><b>Yas Point and the Canopies Sanctuary:</b> Aldar launch details, November 2026; WAM</li><li><b>Yas visits and Abu Dhabi\'s 2030 targets:</b> WAM; The National</li><li><b>Short-term rates:</b> nightly rates are my own assumptions; WB hotel rate from Miral via Gulf News</li><li><b>Holiday homes:</b> Grand Prix week rate from Gulf News; Abu Dhabi holiday-home occupancy from Airbtics</li><li><b>Map:</b> OpenStreetMap; Disney and Yas Point areas drawn from local plans and indicative only</li><li><b>Currency:</b> $1 = 3.6725 dirhams; \u20ac1 = $1.16; 6.83 yuan to the dollar in 2009 and 6.6 in 2016</li></ul>')
CSS='''
@font-face{font-family:Montserrat;src:url(Montserrat.ttf);font-weight:100 900}
@page{size:210mm 297mm;margin:20mm 22mm 22mm}
@page cover{margin:0}
*{box-sizing:border-box}
html,body{margin:0;background:#fff}
body{font-family:Carlito,Calibri,sans-serif;font-size:11pt;line-height:1.5;color:#111}
.cover{page:cover;width:210mm;height:297mm;page-break-after:always;overflow:hidden;margin:0}
.cover img{width:210mm;height:297mm;display:block}
.doc{padding:0}
.doc h1{font-family:Montserrat;font-weight:800;font-size:22pt;line-height:1.15;margin:0 0 2mm;color:#111}
.doc .by{font-size:10pt;color:#666;margin:0 0 8mm;padding-bottom:4mm;border-bottom:2px solid #111}
.doc h2{font-family:Montserrat;font-weight:700;font-size:14pt;margin:9mm 0 3mm;color:#111;page-break-after:avoid}
.doc h2:first-of-type{margin-top:0}
.doc h2.np{page-break-before:always;break-before:page;margin-top:0}
p{margin:0 0 3.2mm}
ul,ol{margin:0 0 3.5mm 5mm;padding:0}li{margin:0 0 1.6mm}
table{width:100%;border-collapse:collapse;margin:2mm 0 5mm;font-size:10.5pt;page-break-inside:avoid}
th{padding-top:1.6mm}
th{text-align:left;font-family:Montserrat;font-weight:700;font-size:9pt;padding:2mm 2mm 2mm 0;border-bottom:1.5px solid #111}
td{padding:1.7mm 2mm 1.7mm 0;border-bottom:1px solid #d9dde2;vertical-align:top}
figure{margin:3mm 0 6mm;page-break-inside:avoid;break-inside:avoid;display:block}figure svg{display:block}figure img{width:100%;display:block;border:1px solid #e3e6ea}
figcaption{font-size:9pt;color:#666;margin-top:1.5mm}
.mapslot{border:1px dashed #9aa4ad;border-radius:2mm;padding:14mm 8mm;text-align:center;color:#666;font-size:10.5pt;margin:2mm 0 5mm;page-break-inside:avoid}
.mapslot span{display:block;font-size:9pt;margin-top:2mm}
ul.src{font-size:9.5pt}ul.src li{margin-bottom:1.2mm}
.foot{position:fixed;bottom:9mm;left:22mm;right:22mm;font-size:8.5pt;color:#888;display:flex;justify-content:space-between;border-top:1px solid #e3e6ea;padding-top:1.5mm}
'''
body='<div class="doc"><h1>Disney Is Coming To Yas Island - Here\'s What It Did Everywhere Else</h1><div class="by">Calum MacLeod · 13 November 2026</div>'+"".join(B)+'</div>'
open('report.html','w').write(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Disney Is Coming To Yas Island</title><style>{CSS}</style></head><body>{body}</body></html>')
print('ok')
