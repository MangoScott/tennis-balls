// Renders thumbnail.html to a 1280x720 PNG (YouTube's recommended thumbnail size).
// Usage: node render.js
const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  await page.goto('file://' + path.join(__dirname, 'thumbnail.html'));
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: path.join(__dirname, 'thumbnail.png') });
  await browser.close();
})();
