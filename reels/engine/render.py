"""Render reel.html -> frames -> reel.mp4 (+ cover.jpg).
Usage: python3 render.py out/RL-01 [stills t1,t2,...]"""
import asyncio, sys, os, json, pathlib, subprocess, shutil
from playwright.async_api import async_playwright
out = pathlib.Path(sys.argv[1]).resolve(); meta = json.loads((out / 'events.json').read_text())
FPS = 30
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--allow-file-access-from-files'])
        pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        pg.on('pageerror', lambda e: print('ERR', e))
        await pg.goto((out / 'reel.html').as_uri()); await pg.wait_for_function('window.ready===true'); await pg.wait_for_timeout(300)
        if len(sys.argv) > 2 and sys.argv[2] == 'stills':
            sd = out / 'stills'; sd.mkdir(exist_ok=True)
            for t in [float(x) for x in sys.argv[3].split(',')]:
                await pg.evaluate(f'renderFrame({t})'); await pg.screenshot(path=str(sd / f's_{t:05.2f}.jpg'), quality=70, type='jpeg')
        else:
            fd = out / 'frames'; shutil.rmtree(fd, ignore_errors=True); fd.mkdir()
            n = int(round(meta['total'] * FPS))
            for f in range(n):
                await pg.evaluate(f'renderFrame({f / FPS})'); await pg.screenshot(path=str(fd / f'f{f:04d}.jpg'), quality=92, type='jpeg')
            await pg.evaluate(f'renderFrame({meta.get("cover", 1.2)})'); await pg.screenshot(path=str(out / 'cover.jpg'), quality=90, type='jpeg')
        await b.close()
asyncio.run(main())
if not (len(sys.argv) > 2 and sys.argv[2] == 'stills'):
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-framerate', str(FPS), '-i', str(out / 'frames' / 'f%04d.jpg'), '-i', str(out / 'audio.wav'),
                    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '21', '-preset', 'medium', '-profile:v', 'high', '-r', str(FPS),
                    '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', str(out / 'reel.mp4')], check=True)
    shutil.rmtree(out / 'frames', ignore_errors=True)
    print('mp4', (out / 'reel.mp4').stat().st_size // 1024, 'KB')
