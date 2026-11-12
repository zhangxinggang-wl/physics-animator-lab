/* 画布多时刻高清截图 —— 常规看图（判断整体布局、轨迹形状、配色）。
 *
 * 用法： node scripts/shot_canvas.js <产物.html> [输出目录] [时刻...]
 *   时刻为滑块值 0~1000，省略时用默认四档（首帧 / 早段 / 中段 / 末态）。
 *   例： node scripts/shot_canvas.js out.html shots 0 300 650 1000
 *
 * 默认 dpr=3，输出 *_c000.png / *_c300.png …（前缀取产物名）。
 *
 * ⚠ 本脚本看的是**整体**。标注被裁 / 叠字这类缺陷要看 scripts/shot_zoom.js 的 3× 特写。
 */
const path = require('path');
const fs = require('fs');
const { chromium, exePath } = require('./chrome');

const FILE = process.argv[2];
if (!FILE) {
  console.error('用法: node shot_canvas.js <产物.html> [输出目录] [时刻...]');
  process.exit(2);
}
const RESOLVED = path.resolve(FILE);
const BASE = path.basename(RESOLVED).replace(/\.html$/i, '');
const OUTDIR = path.resolve(process.argv[3] || path.join(path.dirname(RESOLVED), 'shots'));
const MOMENTS = process.argv.slice(4).map(Number);
const TIMES = MOMENTS.length ? MOMENTS : [0, 300, 650, 1000];

if (!fs.existsSync(OUTDIR)) fs.mkdirSync(OUTDIR, { recursive: true });

(async () => {
  const browser = await chromium.launch({ executablePath: exePath() });
  const page = await browser.newPage({ viewport: { width: 1500, height: 1000 }, deviceScaleFactor: 3 });
  await page.goto('file://' + RESOLVED, { waitUntil: 'load' });
  await page.waitForTimeout(6000); // 等 MathJax 稳定

  const cv = await page.$('#cv');
  const box = await page.evaluate(() => {
    const c = document.getElementById('cv');
    const r = c.getBoundingClientRect();
    return { cssW: Math.round(r.width), cssH: Math.round(r.height), W: c.width, H: c.height, dpr: window.devicePixelRatio };
  });
  console.log('canvas box =', JSON.stringify(box));

  for (const v of TIMES) {
    await page.evaluate((val) => {
      const s = document.getElementById('slider');
      s.value = val;
      s.dispatchEvent(new Event('input'));
    }, v);
    await page.waitForTimeout(450);
    const name = `${BASE}_c${String(v).padStart(4, '0')}.png`;
    if (cv) await cv.screenshot({ path: path.join(OUTDIR, name) });
    console.log('  →', name);
  }
  await Promise.race([browser.close(), new Promise(r => setTimeout(r, 5000))]);
  process.exit(0);
})().catch(e => { console.error('FAIL', e); process.exit(1); });