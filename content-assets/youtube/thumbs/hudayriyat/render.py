import asyncio,glob
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for f in sorted(glob.glob('thumb-*.html')):
            pg=await b.new_page(viewport={'width':1280,'height':720}); await pg.goto('file:///home/claude/thumbs/'+f); await pg.wait_for_timeout(400)
            await (await pg.query_selector('.t')).screenshot(path=f.replace('.html','.png')); await pg.close()
        await b.close()
asyncio.run(main())
