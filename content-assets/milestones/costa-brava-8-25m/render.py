import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1080,'height':1350},device_scale_factor=2)
        await pg.goto('file:///home/claude/cb825/CostaBrava-8.25M.html'); await pg.wait_for_timeout(500)
        await (await pg.query_selector('.sl')).screenshot(path='CostaBrava-8.25M.png'); await b.close()
asyncio.run(main())
