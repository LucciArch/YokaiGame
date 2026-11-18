// MP4 aus einer Zwischensequenz: node render.js out/prolog.html out/prolog.mp4 [fps]
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const fs = require('fs'), path = require('path');
(async () => {
  const [file, outMp4, fpsArg] = process.argv.slice(2);
  const fps = Number(fpsArg || 30);
  const px = process.env.HTTPS_PROXY || process.env.https_proxy;
  const browser = await chromium.launch(px ? { proxy: { server: px } } : {});
  const page = await (await browser.newContext({ ignoreHTTPSErrors: true, viewport: { width: 1280, height: 800 } })).newPage();
  page.on('pageerror', (e) => console.log('pageerror:', e.message));
  await page.goto('file://' + path.resolve(file));
  await page.waitForFunction(() => window.READY, null, { timeout: 30000 });
  const D = await page.evaluate(() => window.DURATION);
  // Ton
  const wav = outMp4.replace(/\.mp4$/, '.f32');
  const b64 = await page.evaluate(async (d) => {
    const r = await SOUND.renderOffline(window.scoreSound, d, 48000, { voiceover: false });
    const u8 = new Uint8Array(r.inter.buffer); let s = '';
    for (let i = 0; i < u8.length; i += 0x8000) s += String.fromCharCode.apply(null, u8.subarray(i, i + 0x8000));
    return [btoa(s), r.peak];
  }, D);
  fs.writeFileSync(wav, Buffer.from(b64[0], 'base64'));
  console.log('Ton-Spitze', b64[1].toFixed(3));
  // Bild
  const n = Math.round(D * fps);
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-i', '-',
    '-f', 'f32le', '-ar', '48000', '-ac', '2', '-i', wav,
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', outMp4]);
  ff.stderr.on('data', (d) => process.stderr.write(d));
  for (let i = 0; i < n; i++) {
    const data = await page.evaluate((tt) => { window.seek(tt); return document.getElementById('cv').toDataURL('image/jpeg', 0.93); }, i / fps);
    if (!ff.stdin.write(Buffer.from(data.split(',')[1], 'base64'))) await new Promise((r) => ff.stdin.once('drain', r));
    if (i % 90 === 0) console.log('Bild', i, '/', n);
  }
  ff.stdin.end();
  await new Promise((r) => ff.on('close', r));
  fs.unlinkSync(wav);
  await browser.close();
  console.log('fertig', outMp4, (fs.statSync(outMp4).size / 1e6).toFixed(1), 'MB');
})();
