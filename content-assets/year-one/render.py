import asyncio,os
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1080,'height':1350},device_scale_factor=2)
        await pg.goto('file:///home/claude/year1/milestone.html'); await pg.wait_for_timeout(500)
        os.makedirs('slides',exist_ok=True)
        for i,e in enumerate(await pg.query_selector_all('.sl')): await e.screenshot(path=f'slides/{i+1:02d}.png')
        await b.close()
asyncio.run(main())
