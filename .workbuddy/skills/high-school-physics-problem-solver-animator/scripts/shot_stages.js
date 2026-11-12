/* 分阶段画布截图 —— 覆盖「每个物理阶段的起始处」，人工看图找叠字/裁切。
 *
 * 用法：node scripts/shot_stages.js <产物.html> <输出目录> <t1> <t2> ...
 *   t 为秒；不给则用默认的关键时刻表。
 *
 * 为什么不能只用 shot_zoom.js：它固定停在 t=0，而本项目的可见缺陷
 * （标注被运动粒子压住、尺寸线被弧线横穿）**只在运动中**出现。
 * 铁律：抽样必须覆盖每个阶段的**起始**，不能只取中点与末态。
 */
const path = require('path');
const fs = require('fs');
const { chromium, exePath } = require('./chrome');

const FILE = process.argv[2];
if (!FILE) { console.error('用法: node scripts_shot_stages.js <产物.html> <输出目录> [t...]'); process.exit(2); }
const RESOLVED = path.resolve(FILE);
const BASE = path.basename(RESOLVED).replace(/\.html$/i, '');
const OUTDIR = path.resolve(process.argv[3] || path.join(path.dirname(RESOLVED), 'shots_stage'));
const TS = process.argv.slice(4).map(Number);

(async () => {
  const browser = await chromium.launch({ executablePath: exePath() });
  const page = await browser.newPage({ viewport: { width: 1500, height: 1000 }, deviceScaleFactor: 3 });
  await page.goto('file://' + RESOLVED, { waitUntil: 'load' });
  await page.waitForTimeout(6000);

  const cv = await page.$('#cv');
  const box = await page.evaluate(() => {
    const c = document.getElementById('cv');
    const r = c.getBoundingClientRect();
    return { cssW: Math.round(r.width), cssH: Math.round(r.height) };
  });
  console.log('canvas css =', JSON.stringify(box));

  if (!fs.existsSync(OUTDIR)) fs.mkdirSync(OUTDIR, { recursive: true });
  const times = TS.length ? TS : [0, 2.21, 4.4, 6.61, 9.01, 12.81, 14.21, 16.81, 20.21, 23.81, 29.01, 33.5];

  for (const tt of times) {
    await page.evaluate((v) => {
      const s = document.getElementById('slider');
      s.value = Math.round(v / 35 * 1000);
      s.dispatchEvent(new Event('input'));
    }, tt);
    await page.waitForTimeout(320);
    /* ⚠ 不能直接用 cv.screenshot()：模板 updatePanel 会 scrollIntoView 把页面
       滚到解析栏，元素截图会连带拍进上方标题栏。改为按元素在视口中的实际
       矩形做 viewport clip —— 先把画布滚到视口正中，再取其 boundingBox。 */
    await page.evaluate(() => {
      document.getElementById('cv').scrollIntoView({ block: 'center', behavior: 'instant' });
    });
    await page.waitForTimeout(250);
    const rect = await page.evaluate(() => {
      const r = document.getElementById('cv').getBoundingClientRect();
      return { x: r.x, y: r.y, width: r.width, height: r.height };
    });
    const name = `${BASE}_t${String(tt).replace('.', 'p')}.png`;
    await page.screenshot({ path: path.join(OUTDIR, name), clip: rect });
    console.log('  →', name, JSON.stringify(rect));
  }

  await Promise.race([browser.close(), new Promise(r => setTimeout(r, 5000))]);
  process.exit(0);
})().catch(e => { console.error('FAIL', e); process.exit(1); });