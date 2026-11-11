import asyncio,os
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':794,'height':1123},device_scale_factor=2)
        await pg.goto('file:///home/claude/marina/Marina-AED5M-Guide.html'); await pg.wait_for_timeout(600)
        await pg.pdf(path='Marina-AED5M-Guide.pdf',width='210mm',height='297mm',print_background=True)
        os.makedirs('pages',exist_ok=True)
        for i,e in enumerate(await pg.query_selector_all('.pg')): await e.screenshot(path=f'pages/p{i+1}.png')
        await b.close()
asyncio.run(main())
