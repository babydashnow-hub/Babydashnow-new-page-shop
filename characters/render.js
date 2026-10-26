// Rend une page HTML de planche en PNG avec Playwright.
// Usage : node characters/render.js <entrée.html> <sortie.png> <largeur> <hauteur>
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const [input, output, w = '1200', h = '1600'] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: +w, height: +h } });
  await page.goto('file://' + path.resolve(input));
  await page.screenshot({ path: output, fullPage: true });
  await browser.close();
})();
