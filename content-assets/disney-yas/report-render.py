import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':794,'height':1123})
        await pg.goto('file:///home/claude/disney/report/report.html'); await pg.wait_for_timeout(800)
        await pg.pdf(path='Disney-Yas-Island-Report.pdf',width='210mm',height='297mm',print_background=True,display_header_footer=True,header_template='<div></div>',footer_template='<div style="width:100%;font-size:8px;color:#888;padding:0 22mm;display:flex;justify-content:space-between;font-family:Carlito,sans-serif"><span>Disney Is Coming To Yas Island · Calum MacLeod</span><span class="pageNumber"></span></div>',prefer_css_page_size=True)
        await b.close()
asyncio.run(main())
