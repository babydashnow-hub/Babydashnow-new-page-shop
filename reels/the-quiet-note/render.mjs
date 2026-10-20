import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import { spawn } from 'node:child_process';
const [,, htmlPath, mode, out, times] = process.argv;
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
page.on('console', m => console.log('console:', m.text()));
page.on('pageerror', e => console.log('pageerror:', e.message));
await page.goto('file://' + htmlPath + '?render=1');
await page.evaluate(() => window.ready);
if (mode === 'stills') {
  for (const t of times.split(',')) {
    await page.evaluate(t => window.render(t), +t);
    await page.screenshot({ path: `${out}/still_${(+t).toFixed(2)}.png` });
  }
} else {
  const FPS = 30, N = 450;
  const ff = spawn('ffmpeg', ['-y', '-v', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-',
    '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo',
    '-map', '0:v', '-map', '1:a', '-shortest',
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-tune', 'film',
    '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', '-r', String(FPS), out], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let f = 0; f < N; f++) {
    await page.evaluate(t => window.render(t), f / FPS);
    const buf = await page.screenshot({ type: 'png' });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (f % 50 === 0) console.log('frame', f);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
}
await browser.close();
