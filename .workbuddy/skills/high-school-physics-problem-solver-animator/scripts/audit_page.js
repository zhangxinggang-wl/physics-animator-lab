/* 产物主门禁 —— 一次跑完所有可自动化断言。
 *
 * 用法： node scripts/audit_page.js <产物.html> [输出.txt]
 *
 * 门禁项：
 *   公式     mjx-container.mjx-error = 0（可靠判据，不用裸 merror 计数）
 *   定界符   页面无裸 \( \) \[ \]
 *   交互     无 <select>（倍速必须用按钮）
 *   画布     非白像素 > 0（动画真的画出来了）
 *   解析栏   无内部滚动（完整版）
 *   动画     distinctFrames >= 5（防「动画卡死 t=0」）
 *   版面     1280/1366/1600/1920 四宽度零公式溢出、零画布空白
 *   报错     控制台与页面错误全为零
 *   单栏版   列数=1 / 画布 CSS 宽 680 / 内宽 678 / kpToggle 已删
 *
 * ⚠ 本脚本查不出「标注被裁 / 叠字」—— 那必须靠 scripts/shot_zoom.js 人工看图。
 * ⚠ 单栏版以文件名含「动画演示」判定；单栏是**从完整版抽取**而来，不另写动画代码。
 */
const path = require('path');
const url = require('url');
const fs = require('fs');
const { chromium, exePath } = require('./chrome');

const FILE = process.argv[2];
if (!FILE) {
  console.error('用法: node audit_page.js <产物.html> [输出.txt]');
  process.exit(2);
}
const OUTTXT = process.argv[3] || '';
const SINGLE = /动画演示/.test(path.basename(FILE)); // 单栏版判定

const log = [];
function P(s) { log.push(s); }

(async () => {
  const browser = await chromium.launch({ executablePath: exePath() });
  const page = await browser.newPage({ viewport: { width: 1600, height: 1000 }, deviceScaleFactor: 2 });
  const consoleErrors = [], pageErrors = [];
  page.on('console', m => { if (m.type() === 'error') consoleErrors.push(m.text()); });
  page.on('pageerror', e => pageErrors.push(String(e)));
  await page.goto(url.pathToFileURL(path.resolve(FILE)).href, { waitUntil: 'load' });

  // 等 MathJax 稳定：连续 6 次采样数量不变且零 error（固定 3.5s 会假阴性）
  let prev = -1, stable = 0, mjxN = 0;
  for (let i = 0; i < 80; i++) {
    const r = await page.evaluate(() => ({
      n: document.querySelectorAll('mjx-container').length,
      e: document.querySelectorAll('mjx-container.mjx-error, mjx-container[data-mjx-error]').length
    }));
    mjxN = r.n;
    if (r.n === prev && r.e === 0) stable++; else stable = 0;
    prev = r.n;
    if (stable >= 6) break;
    await page.waitForTimeout(250);
  }
  P('mjx-container = ' + mjxN + ' (stable>=6, error=0)');

  const res = await page.evaluate(() => {
    const out = {};
    out.mjxError = document.querySelectorAll('mjx-container.mjx-error, mjx-container[data-mjx-error]').length;
    out.merror = document.querySelectorAll('merror').length; // 仅作参考，不作判据
    out.bareDelim = (document.body.innerText.match(/\\\(|\\\)|\\\[|\\\]/g) || []).length;
    out.selectTag = document.querySelectorAll('select').length;
    const ac = document.querySelector('.col-analysis');
    out.analysisScroll = ac ? ac.scrollHeight - ac.clientHeight : -1;
    const cv = document.getElementById('cv');
    const d = cv.getContext('2d').getImageData(0, 0, cv.width, cv.height).data;
    let n = 0; for (let i = 0; i < d.length; i += 4) if (!(d[i] === 255 && d[i+1] === 255 && d[i+2] === 255)) n++;
    out.animPx = n;
    const r = cv.getBoundingClientRect();
    out.cvCssW = Math.round(r.width); out.cvCssH = Math.round(r.height);
    out.cvInnerW = cv.clientWidth;
    out.colCount = document.querySelectorAll('.wrap > section.col').length;
    out.dpr = window.devicePixelRatio;
    out.figPx = 0;
    const figC = document.querySelector('#problemBody canvas.fig-canvas');
    if (figC) {
      const fd = figC.getContext('2d').getImageData(0, 0, figC.width, figC.height).data;
      let fn = 0; for (let i = 0; i < fd.length; i += 4) if (!(fd[i]===255&&fd[i+1]===255&&fd[i+2]===255)) fn++;
      out.figPx = fn;
    }
    out.kpToggle = document.getElementById('kpToggle') ? 1 : 0;
    return out;
  });

  // 动画播放：抽 8 帧统计 distinctFrames（专防「动画卡死 t=0」）
  let distinct = 0;
  try {
    await page.evaluate(() => { const s = document.getElementById('slider'); s.value = 0; s.dispatchEvent(new Event('input')); });
    await page.evaluate(() => { document.getElementById('play').click(); });
    const urls = [];
    for (let i = 0; i < 8; i++) {
      await page.waitForTimeout(420);
      urls.push(await page.evaluate(() => document.getElementById('cv').toDataURL()));
    }
    distinct = new Set(urls).size;
  } catch (e) { P('play err: ' + e); }
  P('distinctFrames = ' + distinct);

  // 首帧四要素分区非白像素（横幅 / HUD / 图例 / 画面主体）
  await page.evaluate(() => { const s = document.getElementById('slider'); s.value = 0; s.dispatchEvent(new Event('input')); });
  await page.waitForTimeout(500);
  const zones = await page.evaluate(() => {
    const cv = document.getElementById('cv');
    const d = cv.getContext('2d').getImageData(0, 0, cv.width, cv.height).data;
    const W = cv.width, H = cv.height;
    const box = {
      banner: [0, 0, W, Math.round(H * 0.11)],
      hud:    [0, 0, W, Math.round(H * 0.30)],
      legend: [0, Math.round(H * 0.85), W, H],
      middle: [0, Math.round(H * 0.25), W, Math.round(H * 0.80)]
    };
    const out = {};
    for (const k in box) {
      const [x0, y0, x1, y1] = box[k];
      let n = 0;
      for (let y = y0; y < y1; y++) for (let x = x0; x < x1; x++) {
        const i = (y * W + x) * 4;
        if (!(d[i] === 255 && d[i+1] === 255 && d[i+2] === 255)) n++;
      }
      out[k] = n;
    }
    return out;
  });

  // 四宽度版面
  const widths = [];
  for (const w of [1280, 1366, 1600, 1920]) {
    const p2 = await browser.newPage({ viewport: { width: w, height: 900 } });
    const errs = [];
    p2.on('pageerror', e => errs.push(String(e)));
    p2.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    await p2.goto(url.pathToFileURL(path.resolve(FILE)).href, { waitUntil: 'load' });
    await p2.waitForTimeout(3500);
    const r = await p2.evaluate(() => {
      let texOver = 0;
      document.querySelectorAll('.step .tex').forEach(e => { if (e.scrollWidth - e.clientWidth > 1) texOver++; });
      const ac = document.querySelector('.col-analysis');
      const cv = document.getElementById('cv');
      const d = cv.getContext('2d').getImageData(0, 0, cv.width, cv.height).data;
      let n = 0; for (let i = 0; i < d.length; i += 4) if (!(d[i]===255&&d[i+1]===255&&d[i+2]===255)) n++;
      // 单栏动画版无 .col-analysis —— 必须容 null，否则整脚本崩在此
      return {
        texOverflow: texOver,
        analysisScroll: ac ? ac.scrollHeight - ac.clientHeight : -1,
        mjxError: document.querySelectorAll('mjx-container.mjx-error').length,
        animPx: n
      };
    });
    widths.push({ width: w, ...r, errors: errs.slice(0, 3) });
    await p2.close();
  }

  P('');
  P('=== 门禁 ===');
  const gate = [];
  gate.push(['mjx-error=0', res.mjxError === 0, res.mjxError]);
  gate.push(['merror=0', res.merror === 0, res.merror]);
  gate.push(['无裸定界符', res.bareDelim === 0, res.bareDelim]);
  gate.push(['无 <select>', res.selectTag === 0, res.selectTag]);
  gate.push(['画布非白像素>0', res.animPx > 0, res.animPx]);
  if (SINGLE) {
    gate.push(['题图已移除', res.figPx === 0, res.figPx]);
    gate.push(['解析栏已移除', res.analysisScroll === -1, res.analysisScroll]);
  } else {
    gate.push(['题图非白像素>0', res.figPx > 0, res.figPx]);
    gate.push(['解析栏无内部滚动', res.analysisScroll <= 1, res.analysisScroll]);
  }
  gate.push(['distinctFrames>=5', distinct >= 5, distinct]);
  gate.push(['四宽度零溢出', widths.every(w => w.texOverflow === 0), JSON.stringify(widths.map(w => w.texOverflow))]);
  if (!SINGLE) gate.push(['四宽度解析栏无滚动', widths.every(w => w.analysisScroll <= 1), JSON.stringify(widths.map(w => w.analysisScroll))]);
  gate.push(['四宽度画布有内容', widths.every(w => w.animPx > 0), JSON.stringify(widths.map(w => w.animPx))]);
  gate.push(['零控制台/页面报错', consoleErrors.length === 0 && pageErrors.length === 0,
             JSON.stringify({ consoleErrors: consoleErrors.slice(0, 5), pageErrors: pageErrors.slice(0, 5) })]);
  gate.push(['四宽度零报错', widths.every(w => w.errors.length === 0), JSON.stringify(widths.map(w => w.errors))]);

  // 首帧四要素分区：专防「让位判断没放开导致首屏缺一半元素」
  for (const k of ['banner', 'hud', 'legend', 'middle']) {
    gate.push(['首帧 ' + k + ' 非空', zones[k] > 0, zones[k]]);
  }

  // 单栏版专属
  if (SINGLE) {
    gate.push(['单栏：列数=1', res.colCount === 1, res.colCount]);
    gate.push(['单栏：画布 CSS 宽 680', res.cvCssW === 680, res.cvCssW]);
    gate.push(['单栏：画布内宽 678', res.cvInnerW === 678, res.cvInnerW]);
    gate.push(['单栏：kpToggle 已删', res.kpToggle === 0, res.kpToggle]);
  }

  for (const [name, ok, v] of gate) P((ok ? 'PASS  ' : 'FAIL  ') + name + '  →  ' + v);
  P('');
  P('zones(首帧) = ' + JSON.stringify(zones));
  P('canvas css = ' + res.cvCssW + 'x' + res.cvCssH + ' dpr=' + res.dpr);
  P('widths = ' + JSON.stringify(widths));

  await Promise.race([browser.close(), new Promise(r => setTimeout(r, 5000))]);
  const txt = log.join('\n');
  console.log(txt);
  if (OUTTXT) fs.writeFileSync(OUTTXT, txt, 'utf8');
  process.exit(gate.some(g => !g[1]) ? 1 : 0);
})().catch(e => {
  console.log(log.join('\n'));
  console.error('FAIL', e);
  process.exit(2);
});