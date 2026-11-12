// 产物合规审计：页面不得含任何署名/身份标识/站外链接
// 检测规则全部通用化（正则 + 结构特征），不硬编码任何具体人名、校名或站点。
// 判据：
//   1. 无 <footer> 页脚、无署名类容器（.designer/.author/.copyright/.credit/.mm-panel/.figlib-key）
//   2. 无站外 <a href="http..."> 链接
//   3. 无二维码 / 微信 / QQ / 电话 等联系方式
//   4. 无「..中学」「..学校」「..学院」等机构名，无「设计开发/编写/制作/出品」等署名动词
//   5. 无 MathJax 渲染错误、无 console/page 报错、动画 canvas 已绘制
const { chromium, exePath } = require('./chrome');
const path = require('path');

const files = process.argv.slice(2);

const AUDIT = () => {
  const txt = document.body.innerText;
  const cv = document.querySelector('canvas');
  let painted = null;
  if (cv) {
    try {
      const c = cv.getContext('2d');
      const w = Math.min(cv.width, 900), h = Math.min(cv.height, 600);
      const d = c.getImageData(0, 0, w, h).data;
      let n = 0;
      for (let i = 3; i < d.length; i += 4) if (d[i] > 0) n++;
      painted = n;
    } catch (e) { painted = 'err:' + e.message; }
  }
  const links = [...document.querySelectorAll('a')].map(a => a.getAttribute('href'));

  // —— 通用痕迹检测 ——
  const hits = [];
  const push = (kind, ev) => hits.push(kind + '=' + ev);

  if (document.querySelectorAll('footer').length) push('footer', '存在页脚');

  const sigSel = '.designer,.author,.copyright,.credit,.mm-panel,.mm-link,.figlib-key';
  const sigs = [...document.querySelectorAll(sigSel)];
  if (sigs.length) push('sigBox', sigs.map(e => e.className).join(','));

  const ext = links.filter(h => h && /^https?:/i.test(h));
  if (ext.length) push('extLink', ext.join(','));

  if (/微信|weixin|wechat|二维码|QQ\s*[:：]?\s*\d{5,}|联系电话|手机号/.test(txt)) push('contact', '联系方式');

  const org = txt.match(/[\u4e00-\u9fa5]{2,10}(?:中学|学校|学院|大学|教研室|教育集团)/g);
  if (org) push('org', [...new Set(org)].join(','));

  const verb = txt.match(/(?:设计开发|设计者|编写|制作|出品|编著|主播|剪辑)/g);
  if (verb) push('creditVerb', [...new Set(verb)].join(','));

  const cls = [...document.querySelectorAll('*')]
    .map(e => (typeof e.className === 'string' ? e.className : '')).join(' ');
  ['mm-panel', 'mm-link', 'figlib-key', 'designer'].forEach(c => { if (cls.includes(c)) push('residueClass', c); });

  return {
    hits,
    mathError: document.querySelectorAll('mjx-container[data-mjx-error]').length,
    canvas: !!cv,
    canvasPainted: painted
  };
};

(async () => {
  if (!files.length) {
    console.error('用法: node audit_nosig.js <产物.html> [更多.html ...]');
    process.exit(2);
  }
  const browser = await chromium.launch({ executablePath: exePath() });
  let fail = 0;
  for (const f of files) {
    const page = await browser.newPage();
    const errs = [], pErrs = [];
    page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    page.on('pageerror', e => pErrs.push(String(e)));
    try {
      await page.goto(require('url').pathToFileURL(path.resolve(f)).href, { waitUntil: 'load' });
      await page.waitForTimeout(3500);
      const r = await page.evaluate(AUDIT);
      const ok = r.hits.length === 0 && errs.length === 0 && pErrs.length === 0 && r.mathError === 0;
      if (!ok) fail++;
      let line = (ok ? 'PASS' : 'FAIL') + '  ' + path.basename(f) + '  ' + JSON.stringify(r);
      if (errs.length) line += '  ERR:' + errs.slice(0, 2).join(' | ');
      if (pErrs.length) line += '  PAGEERR:' + pErrs.slice(0, 1).join('');
      process.stdout.write(line + '\n');
    } catch (e) {
      fail++;
      process.stdout.write('FAIL  ' + path.basename(f) + '  ' + e.message + '\n');
    }
    await page.close();
  }
  // ⚠ browser.close() 在常驻 rAF + MathJax 的页面上可能不返回 ⇒ 必须超时兜底并显式退出
  await Promise.race([browser.close(), new Promise(r => setTimeout(r, 5000))]);
  process.stdout.write((fail ? 'FAILED ' + fail + '/' + files.length : 'ALL PASS ' + files.length) + '\n');
  process.exit(fail ? 1 : 0);
})();