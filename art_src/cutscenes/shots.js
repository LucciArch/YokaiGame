// Standbilder zur Kontrolle: node shots.js out/prolog.html 1,3,5 /pfad/ausgabe-prefix
const { chromium } = require('playwright');
(async () => {
  const [file, times, prefix] = process.argv.slice(2);
  const px = process.env.HTTPS_PROXY || process.env.https_proxy;
  const browser = await chromium.launch(px ? { proxy: { server: px } } : {});
  const page = await (await browser.newContext({ ignoreHTTPSErrors: true, viewport: { width: 1280, height: 800 } })).newPage();
  page.on('console', (m) => { if (m.type() === 'error') console.log('console:', m.text()); });
  page.on('pageerror', (e) => console.log('pageerror:', e.message));
  await page.goto('file://' + require('path').resolve(file));
  await page.waitForFunction(() => window.READY, null, { timeout: 30000 });
  console.log('fonts:', await page.evaluate(() => document.fonts.check('72px "IM Fell English"')));
  for (const t of times.split(',').map(Number)) {
    const ms = await page.evaluate((tt) => { const a = performance.now(); window.seek(tt); return performance.now() - a; }, t);
    const data = await page.evaluate(() => document.getElementById('cv').toDataURL('image/jpeg', 0.85));
    require('fs').writeFileSync(`${prefix}_${t}.jpg`, Buffer.from(data.split(',')[1], 'base64'));
    console.log('t', t, 'ms', ms.toFixed(0));
  }
  await browser.close();
})();
