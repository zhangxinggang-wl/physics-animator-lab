/* 整页高清截图 —— 看三栏整体版式、公式渲染、知识点卡片布局。
 *
 * 用法： node scripts/shot_full.js <产物.html> [输出目录]
 * 默认 dpr=2、viewport 1700×1100（解析栏在 1280px 最紧，四宽度已在 audit_page.js 覆盖）。
 */
const path = require('path');
const fs = require('fs');
const { chromium, exePath } = require('./chrome');

const FILE = process.argv[2];
if (!FILE) {
  console.error('用法: node shot_full.js <产物.html> [输出目录]');
  process.exit(2);
}
const RESOLVED = path.resolve(FILE);
const BASE = path.basename(RESOLVED).replace(/\.html$/i, '');
const OUTDIR = path.resolve(process.argv[3] || path.join(path.dirname(RESOLVED), 'shots'));
if (!fs.existsSync(OUTDIR)) fs.mkdirSync(OUTDIR, { recursive: true });

(async () => {
  const browser = await chromium.launch({ executablePath: exePath() });
  const page = await browser.newPage({ viewport: { width: 1700, height: 1100 }, deviceScaleFactor: 2 });
  await page.goto('file://' + RESOLVED, { waitUntil: 'load' });
  await page.waitForTimeout(6000);
  const name = `${BASE}_full.png`;
  await page.screenshot({ path: path.join(OUTDIR, name), fullPage: true });
  console.log('  →', name, '（整页，注意这是真实像素；裁剪换算比例 s = 图宽/1700）');
  await Promise.race([browser.close(), new Promise(r => setTimeout(r, 5000))]);
  process.exit(0);
})().catch(e => { console.error('FAIL', e); process.exit(1); });