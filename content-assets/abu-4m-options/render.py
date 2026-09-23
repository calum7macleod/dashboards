import asyncio,os,sys
from playwright.async_api import async_playwright
names=["Abu-4M-Options-Sep26","Abu-4M-Options-Sep26-four-doors"]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for nm in names:
            pg=await b.new_page(viewport={'width':1123,'height':794},device_scale_factor=2)
            await pg.goto('file:///home/claude/abu/'+nm+'.html'); await pg.wait_for_timeout(600)
            await pg.pdf(path=nm+'.pdf',width='297mm',height='210mm',print_background=True)
            d='pages' if nm==names[0] else 'pages4'; os.makedirs(d,exist_ok=True)
            for i,e in enumerate(await pg.query_selector_all('.pg')): await e.screenshot(path=f'{d}/p{i+1:02d}.png')
            await pg.close()
        await b.close()
asyncio.run(main())
