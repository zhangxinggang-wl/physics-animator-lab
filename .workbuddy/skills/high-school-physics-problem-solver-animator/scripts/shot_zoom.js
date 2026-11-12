/* 画布 3× 特写截图 —— **人工看图的主力**，专查「标注被裁 / 叠字 / 越界」。
 *
 * 用法： node scripts/shot_zoom.js <产物.html> [输出目录] [x0 y0 x1 y1 ...]
 *   区域参数是**画布 CSS 像素**的 4 元组，可给多组（每组一张图）。
 *   省略区域时自动切 3×3 九宫格（覆盖全画布，足够抓大多数缺陷）。
 *   例： node scripts/shot_zoom.js out.html shots 0 0 240 120
 *
 * 为什么必须这一步：
 *   自动化门禁（audit_page.js）查不出标注被裁或叠字 —— 那些缺陷在像素层面
 *   完全合法。本项目**可见缺陷几乎全部**是靠这里的特写图人工发现的。
 *
 * 特写清单（按经验，容易出问题的地方优先看）：
 *   □ 画布顶端 1/4（HUD 与横幅区：文字被下沿裁切）
 *   □ 画布底缘（尺寸线与图例：图例单行重叠、文字压轴）
 *   □ 几何体所在区域（粒子扫过固定标注 ⇒ 叠字）
 *   □ 每个物理阶段的**起始**时刻（不是中点、不是末态）
 */
const path = require('path');
const fs = require('fs');
const { chromium, exePath } = require('./chrome');

const FILE = process.argv[2];
if (!FILE) {
  console.error('用法: node shot_zoom.js <产物.html> [输出目录] [x0 y0 x1 y1 ...]');
  process.exit(2);
}
const RESOLVED = path.resolve(FILE);
const BASE = path.basename(RESOLVED).replace(/\.html$/i, '');
const OUTDIR = path.resolve(process.argv[3] || path.join(path.dirname(RESOLVED), 'shots_zoom'));
const nums = process.argv.slice(4).map(Number);

// 未给区域 ⇒ 九宫格；给了 ⇒ 按每 4 个一组
let regions = [];
if (nums.length && nums.length % 4 === 0) {
  for (let i = 0; i < nums.length; i += 4) regions.push(nums.slice(i, i + 4));
} else if (nums.length) {
  console.error('区域参数必须是 4 的倍数（x0 y0 x1 y1）；已忽略，改用九宫格。');
}

if (!fs.existsSync(OUTDIR)) fs.mkdirSync(OUTDIR, { recursive: true });

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

  if (!regions.length) {
    const W = box.cssW, H = box.cssH;
    for (let r = 0; r < 3; r++) for (let c = 0; c < 3; c++) {
      regions.push([
        Math.round((W / 3) * c), Math.round((H / 3) * r),
        Math.round((W / 3) * (c + 1)), Math.round((H / 3) * (r + 1))
      ]);
    }
    console.log('未指定区域 ⇒ 使用 3×3 九宫格');
  }

  // 停到首帧再截（特写看的是静态版面问题）
  await page.evaluate(() => { const s = document.getElementById('slider'); s.value = 0; s.dispatchEvent(new Event('input')); });
  await page.waitForTimeout(500);

  regions.forEach(([x0, y0, x1, y1], i) => {
    const name = `${BASE}_z${String(i).padStart(2, '0')}_${x0}_${y0}.png`;
    cv.screenshot({ path: path.join(OUTDIR, name), clip: { x: x0, y: y0, width: x1 - x0, height: y1 - y0 } })
      .then(() => console.log('  →', name))
      .catch(e => console.error('  FAIL', name, e.message));
  });

  // 等所有截图落盘再退出
  await page.waitForTimeout(2500);
  await Promise.race([browser.close(), new Promise(r => setTimeout(r, 5000))]);
  process.exit(0);
})().catch(e => { console.error('FAIL', e); process.exit(1); });