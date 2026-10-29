import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':2048,'height':1152}); await pg.goto('file:///home/claude/yt/banner.html'); await pg.wait_for_timeout(500)
        await (await pg.query_selector('.b')).screenshot(path='YT-Banner-2048x1152.png'); await pg.close()
        pg=await b.new_page(viewport={'width':150,'height':150}); await pg.goto('file:///home/claude/yt/watermark.html'); await pg.wait_for_timeout(300)
        await (await pg.query_selector('.w')).screenshot(path='YT-Watermark-150.png',omit_background=True); await pg.close()
        await b.close()
asyncio.run(main())
