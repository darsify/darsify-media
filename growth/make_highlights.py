import asyncio, sys, pathlib
sys.path.insert(0, '/home/claude/darsify-media/reels/engine')
from build import ICONS
from playwright.async_api import async_playwright
OUT = pathlib.Path(__file__).parent / 'highlights'
items = [('tutors','person','#f26229'),('academies','building','#2655a3'),('schools','school','#f26229'),('how-it-works','repeat','#2655a3'),('faq','chat','#f26229')]
def page(icon, ring):
    svg = f'<svg width="300" height="300" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{ICONS[icon]}</svg>'
    return f'''<html><body style="margin:0;width:1080px;height:1920px;background:radial-gradient(70% 40% at 50% 50%,#1d3a63 0%,#0b1e30 70%);display:flex;align-items:center;justify-content:center">
<div style="width:560px;height:560px;border-radius:50%;background:{ring};display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 18px rgba(255,255,255,.08)">{svg}</div></body></html>'''
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width':1080,'height':1920})
        for name, ic, col in items:
            await pg.set_content(page(ic, col)); await pg.screenshot(path=str(OUT/f'highlight-{name}.png'))
        await b.close()
asyncio.run(main())
