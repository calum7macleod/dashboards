#!/usr/bin/env python3
"""render-offer.py - fill the locked offer-letter template and render PNG (2x) + PDF.
Usage: python3 render-offer.py fields.json [outdir]
fields.json: {"OWNER":"Ms. Seema","UNIT":"J519","CLUSTER":"Costa Brava","COMMUNITY":"DAMAC Lagoons",
              "DATE":"23 September 2026","PRICE":2650000,"BUYER_POSITION":"Qualified · ready to sign MOU on acceptance",
              "BROKERAGE":"White & Co Real Estate"}
AGENCY (2% flat), CONVEY (9,950 under 10M) and NET are computed. Output: <outdir>/<Owner>-<Unit>-Offer-<Price>M.png/.pdf
"""
import sys,json,os,asyncio,re
from playwright.async_api import async_playwright
f=json.load(open(sys.argv[1])); out=sys.argv[2] if len(sys.argv)>2 else "."
price=int(f["PRICE"]); agency=round(price*0.02); convey=9950 if price<10_000_000 else int(f.get("CONVEY",9950))
net=price-agency-convey
f.update(PRICE=f"{price:,}",AGENCY=f"{agency:,}",CONVEY=f"{convey:,}",NET=f"{net:,}")
tpl=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"offer-letter.html")).read()
html=re.sub(r"\{\{(\w+)\}\}",lambda m:str(f[m.group(1)]),tpl)
owner=re.sub(r"^(Mr|Ms|Mrs|Dr)\.?\s+","",f["OWNER"]).split()[0]
stem=f"{owner}-{f['UNIT']}-Offer-{price/1e6:g}M"; os.makedirs(out,exist_ok=True)
src=os.path.join(out,stem+".html"); open(src,"w").write(html)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={"width":1080,"height":1350},device_scale_factor=2)
        await pg.goto("file://"+os.path.abspath(src)); await pg.wait_for_timeout(400)
        await (await pg.query_selector(".card")).screenshot(path=os.path.join(out,stem+".png"))
        await pg.pdf(path=os.path.join(out,stem+".pdf"),width="1080px",height="1350px",print_background=True,page_ranges="1")
        await b.close()
asyncio.run(main())
print(f"Done - {stem}.png/.pdf/.html in {out} · net AED {net:,}")
