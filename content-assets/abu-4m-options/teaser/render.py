import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1080,'height':1350},device_scale_factor=2)
        await pg.goto('file:///home/claude/teaser/Abu-4M-Teaser-Sep26.html'); await pg.wait_for_timeout(500)
        await (await pg.query_selector('.card')).screenshot(path='Abu-4M-Teaser-Sep26.png')
        await pg.pdf(path='Abu-4M-Teaser-Sep26.pdf',width='1080px',height='1350px',print_background=True,page_ranges='1')
        await b.close()
asyncio.run(main())
