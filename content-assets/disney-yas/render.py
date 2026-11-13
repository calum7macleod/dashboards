import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1240,'height':1754},device_scale_factor=2)
        await pg.goto('file:///home/claude/disney/cover.html'); await pg.wait_for_timeout(600)
        await (await pg.query_selector('.cv')).screenshot(path='Disney-Yas-Cover.png')
        await pg.pdf(path='Disney-Yas-Cover.pdf',width='210mm',height='297mm',print_background=True,page_ranges='1')
        await b.close()
asyncio.run(main())
