import asyncio,os
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1123,'height':794},device_scale_factor=2)
        await pg.goto('file:///home/claude/abu/Abu-4M-Three-Options-Sep26.html'); await pg.wait_for_timeout(600)
        await pg.pdf(path='Abu-4M-Three-Options-Sep26.pdf',width='297mm',height='210mm',print_background=True)
        os.makedirs('pages',exist_ok=True)
        for i,e in enumerate(await pg.query_selector_all('.pg')): await e.screenshot(path=f'pages/p{i+1:02d}.png')
        await b.close()
asyncio.run(main())
