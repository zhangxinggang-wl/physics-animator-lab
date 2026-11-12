/* chromium 可执行文件自动探测 —— 消除各脚本里硬编码的版本号路径。
 *
 * 背景：原先每个审计/截图脚本都写死
 *   .../ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-win64/...
 * 浏览器一升级，所有脚本同时失效（且报错信息指向"文件不存在"，看不出真因）。
 *
 * 用法：
 *   const { chromium, exePath } = require('./chrome');
 *   const browser = await chromium.launch({ executablePath: exePath() });
 */
const fs = require('fs');
const path = require('path');
const os = require('os');

/** 常见安装根目录，按优先级排列。 */
function roots() {
  if (process.env.PLAYWRIGHT_BROWSERS_PATH) return [process.env.PLAYWRIGHT_BROWSERS_PATH];
  const home = os.homedir();
  if (process.platform === 'win32') {
    return [path.join(home, 'AppData', 'Local', 'ms-playwright')];
  }
  if (process.platform === 'darwin') {
    return [path.join(home, 'Library', 'Caches', 'ms-playwright')];
  }
  return [path.join(home, '.cache', 'ms-playwright')];
}

/** 在一个根目录下找出所有可用的 chromium 可执行文件（版本号倒序 = 新的优先）。 */
function scanRoot(root) {
  if (!fs.existsSync(root)) return [];
  const hits = [];
  for (const dir of fs.readdirSync(root)) {
    // 只看 chromium 家族，跳过 firefox / webkit
    if (!/^chromium/i.test(dir)) continue;
    const base = path.join(root, dir);
    const cands =
      process.platform === 'win32'
        ? [
            path.join(base, 'chrome-headless-shell-win64', 'chrome-headless-shell.exe'),
            path.join(base, 'chrome-win', 'chrome.exe'),
            path.join(base, 'chrome-win64', 'chrome.exe'),
          ]
        : process.platform === 'darwin'
        ? [
            path.join(base, 'chrome-headless-shell-mac', 'chrome-headless-shell'),
            path.join(base, 'chrome-mac', 'Chromium.app', 'Contents', 'MacOS', 'Chromium'),
          ]
        : [
            path.join(base, 'chrome-headless-shell-linux64', 'chrome-headless-shell'),
            path.join(base, 'chrome-linux', 'chrome'),
          ];
    for (const c of cands) {
      if (fs.existsSync(c)) {
        // 从目录名尾部抽版本号（chromium_headless_shell-1248 → 1248）
        const m = dir.match(/-(\d+)(\.\d+)*$/);
        hits.push({ path: c, ver: m ? parseFloat(m[1]) : 0, dir });
      }
    }
  }
  hits.sort((a, b) => b.ver - a.ver);
  return hits;
}

let cached = null;

/**
 * 返回可用的 chromium 可执行文件路径。
 * 找不到时抛出**可操作的**错误信息（而不是让 playwright 报 "file not found"）。
 */
function exePath() {
  if (cached) return cached;
  const all = [];
  for (const r of roots()) all.push(...scanRoot(r));
  if (!all.length) {
    throw new Error(
      '未找到 chromium。\n' +
      '  已搜索：\n' +
      roots().map(r => '    - ' + r).join('\n') +
      '\n  解决办法（二选一）：\n' +
      '    1) 运行  npx playwright install chromium\n' +
      '    2) 或设置环境变量 PLAYWRIGHT_BROWSERS_PATH 指向浏览器目录\n' +
      '  临时覆盖：环境变量 CHROME_PATH=<chrome.exe 全路径>'
    );
  }
  cached = all[0].path;
  if (process.env.CHROME_DEBUG) {
    console.log('[chrome] 使用', cached);
    console.log('[chrome] 候选', all.map(h => h.ver + ' ' + h.path).join(' | '));
  }
  return cached;
}

/** 列出全部候选（排障用）。 */
function listAll() {
  const all = [];
  for (const r of roots()) all.push(...scanRoot(r));
  return all;
}

/**
 * playwright-core 可能装在工作区也可能装在用户级，逐个尝试 require。
 * 封装成 Skill 后目录会换位置，不能只依赖 ../node_modules。
 */
function loadPlaywright() {
  const tried = [];
  const froms = [__dirname, process.cwd()];
  // 逐级向上找（包可能被放在 .workbuddy/skills/<name>/ 或更深）
  let up = __dirname;
  for (let i = 0; i < 6; i++) {
    up = path.dirname(up);
    if (up === path.dirname(up)) break;
    froms.push(up);
  }
  // 已知的常用工作区根（存在 node_modules 就直接用）
  for (const guess of WORKSPACE_GUESSES) {
    if (fs.existsSync(path.join(guess, 'node_modules'))) froms.push(guess);
  }
  const seen = new Set();
  for (const name of ['playwright-core', 'playwright']) {
    for (const from of froms) {
      if (seen.has(from)) continue;
      seen.add(from);
      try {
        const p = require(require.resolve(name, { paths: [from] }));
        if (p && p.chromium) return p;
      } catch (e) {
        tried.push(name + ' @ ' + from);
      }
    }
  }
  throw new Error(
    '未找到 playwright-core。已尝试：\n  ' + tried.join('\n  ') +
    '\n解决办法：\n' +
    '  · 在本技能目录下执行  npm i playwright-core\n' +
    '  · 或在生成产物的工作区里安装（脚本会自动向上查找 node_modules）\n' +
    '  · 确保浏览器已安装：npx playwright install chromium'
  );
}

/** 常见工作区根目录（含 node_modules 时优先）。 */
const WORKSPACE_GUESSES = [
  process.env.PHYSICS_LAB_ROOT,
  path.join(os.homedir(), 'Desktop', 'physics-animator-lab'),
  path.join(process.cwd(), 'node_modules', '..'),
].filter(Boolean);

const chromium = loadPlaywright().chromium;

module.exports = { chromium, exePath, listAll, roots };