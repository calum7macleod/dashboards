#!/usr/bin/env python3
"""Branded cost-breakdown generator - Calum MacLeod / White & Co.
Usage: python3 gen.py <price> <deposit_pct> [title] [outfile]"""
import sys, subprocess
price=float(sys.argv[1]); dep_pct=float(sys.argv[2]) if len(sys.argv)>2 else 20
title=sys.argv[3] if len(sys.argv)>3 else "3-Bed Townhouse — DAMAC Lagoons"
out=sys.argv[4] if len(sys.argv)>4 else "breakdown.pdf"
loan=price*(1-dep_pct/100); dep=price*dep_pct/100
dld=price*0.04; agency=price*0.02*1.05; conv=9950; mreg=loan*0.0025; adm1=480; adm2=190
fees=dld+agency+conv+mreg+adm1+adm2
dayone=dep+fees
f=lambda v:f"{v:,.0f}"
rows="".join([
 f'<tr><td>DLD transfer fee — 4%</td><td class="r">{f(dld)}</td></tr>',
 f'<tr><td>Agency fee — 2% + VAT</td><td class="r">{f(agency)}</td></tr>',
 f'<tr><td>Conveyancing</td><td class="r">{f(conv)}</td></tr>',
 f'<tr><td>Mortgage registration — 0.25% of loan</td><td class="r">{f(mreg)}</td></tr>',
 f'<tr><td>Trustee / admin</td><td class="r">{f(adm1)}</td></tr>',
 f'<tr><td>Knowledge / admin</td><td class="r">{f(adm2)}</td></tr>',
])
html=f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
:root{{--bg:#152A1F;--panel:#1E3D2F;--gold:#C9A84C;--lgold:#E8C96B;--cream:#F5EDE0;--muted:#8FA898;--div:#2E5A40}}
*{{box-sizing:border-box;margin:0;padding:0;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
body{{font-family:Calibri,'Segoe UI',sans-serif;color:var(--cream);background:var(--bg)}}
.page{{width:210mm;height:296mm;background:var(--bg);padding:14mm 15mm;position:relative;overflow:hidden}}
h1,h2{{font-family:'Palatino Linotype',Palatino,Georgia,serif}}
.eyebrow{{letter-spacing:4px;font-size:10px;font-weight:bold;color:var(--gold);text-transform:uppercase;text-align:center}}
h1{{font-size:25px;text-align:center;margin:3mm 0 1mm}}
.sub{{text-align:center;color:var(--muted);font-size:12px;margin-bottom:7mm}}
.strip{{display:flex;gap:4mm;margin-bottom:7mm}}
.sbox{{flex:1;background:var(--panel);border:1px solid var(--div);border-radius:10px;padding:4mm}}
.sbox .l{{font-size:8.5px;letter-spacing:2px;color:var(--muted);text-transform:uppercase}}
.sbox .v{{font-size:18px;color:var(--lgold);font-weight:700;font-family:'Palatino Linotype',serif;margin-top:1.5mm}}
.sbox .s{{font-size:9px;color:var(--muted);margin-top:1mm}}
.panel{{background:var(--panel);border:1px solid var(--div);border-radius:11px;padding:5mm 6mm;margin-bottom:6mm}}
.panel h2{{color:var(--lgold);font-size:15.5px;margin-bottom:3mm}}
table{{width:100%;border-collapse:collapse;font-size:12px}}
td{{padding:2.8mm 2mm;border-top:1px solid var(--div)}}
tr.hd td{{border-top:none;color:var(--muted);font-size:9px;letter-spacing:1.5px;text-transform:uppercase;padding-bottom:1mm}}
.r{{text-align:right}}
.tot td{{border-top:2px solid var(--gold);font-weight:bold;color:var(--lgold);font-size:13px}}
.note{{font-size:9.5px;color:var(--muted);line-height:1.6;margin-top:2.5mm}}
.say{{background:rgba(201,168,76,.1);border:1px solid var(--gold);border-radius:11px;padding:4.5mm 6mm;font-size:12.5px;line-height:1.6;color:var(--cream)}}
.foot{{position:absolute;bottom:10mm;left:15mm;right:15mm;border-top:1px solid var(--div);padding-top:3mm;display:flex;justify-content:space-between;font-size:10px;color:var(--muted)}}
.foot b{{color:var(--gold)}}
.d{{color:var(--gold)}}
</style></head><body><div class="page">
<div class="eyebrow">White &amp; Co &nbsp;·&nbsp; Calum MacLeod</div>
<h1>{title}</h1>
<div class="sub">Full cost breakdown · mortgage purchase · Đ{f(price)}</div>
<div class="strip">
 <div class="sbox"><div class="l">Purchase Price</div><div class="v">Đ {f(price)}</div><div class="s">agreed price</div></div>
 <div class="sbox"><div class="l">Cash Day One</div><div class="v">Đ {f(dayone)}</div><div class="s">deposit + all fees ({dayone/price*100:.1f}%)</div></div>
 <div class="sbox"><div class="l">Mortgage</div><div class="v">Đ {f(loan)}</div><div class="s">{100-dep_pct:.0f}% financed by bank</div></div>
</div>
<div class="panel"><h2><span class="d">◆</span> Your Money</h2>
<table>
<tr class="hd"><td>Component</td><td class="r">Amount (AED)</td></tr>
<tr><td>Deposit — {dep_pct:.0f}% of purchase price</td><td class="r">{f(dep)}</td></tr>
<tr class="hd"><td style="padding-top:3mm">Purchase costs</td><td></td></tr>
{rows}
<tr class="tot"><td>Total cash required day one</td><td class="r">{f(dayone)}</td></tr>
</table>
<div class="note">Mortgage registration is charged on the loan amount, not the price. Your bank may add an arrangement fee (typically up to 1% of the loan, sometimes waived) and a property valuation charge (≈Đ2,500–3,000) — these vary by lender and rate package, so they are quoted separately by the bank. All figures indicative until documents confirm.</div>
</div>
<div class="say">In plain terms: <b style="color:var(--lgold)">Đ{f(dayone)} gets you the keys.</b> Đ{f(dep)} of that is your equity in the property from day one — Đ{f(fees)} is the total cost of buying. The bank carries the remaining Đ{f(loan)}.</div>
<div class="foot"><div><b>Calum MacLeod</b> · White &amp; Co · DAMAC Lagoons Specialist</div><div>+971 55 350 2699 · @dubaicalum · E&amp;OE</div></div>
</div></body></html>"""
open('/tmp/bd.html','w').write(html)
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page()
    pg.goto('file:///tmp/bd.html'); pg.wait_for_timeout(400)
    pg.pdf(path=out, width='210mm', height='297mm', print_background=True, margin={'top':'0','bottom':'0','left':'0','right':'0'})
    b.close()
print('written', out)
