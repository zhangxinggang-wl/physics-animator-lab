/* 抽取内联 <script> 做语法自检（Windows 版：改用 vm.Script 解析，不 spawn 子进程，规避 EBUSY） */
const fs = require('fs');
const vm = require('vm');

const file = process.argv[2];
const html = fs.readFileSync(file, 'utf8');
const re = /<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/gi;
let m, i = 0, bad = 0;
while ((m = re.exec(html))) {
  i++;
  const code = m[1];
  try {
    new vm.Script(code, { filename: 'seg' + i + '.js' });
    console.log('script#' + i + ' (' + code.length + ' chars): SYNTAX OK');
  } catch (e) {
    bad++;
    console.log('script#' + i + ' (' + code.length + ' chars): SYNTAX FAIL');
    console.log(String(e.stack || e.message).slice(0, 2000));
  }
}
console.log('inline scripts checked =', i, ', fail =', bad);
process.exit(bad ? 1 : 0);
