# high-school-physics-problem-solver-animator

> 把一道高中物理题（文字或截图）做成**单文件自包含的交互式教学动画 HTML**。
> 左栏原题、中栏分步解析、右栏 Canvas 2D 物理动画，题图与动画几何**孪生一致**。

## 目录结构

```
high-school-physics-problem-solver-animator/
├── SKILL.md              技能入口（总纲 + 工作流 + 门禁 + 索引，6 KB）
├── assets/
│   └── template.html     三栏页面模板（2.2 MB，内联 MathJax），框架代码勿改
├── references/           规范分册 + 六大板块公式库（按需加载，勿全量读）
├── scripts/              通用工具链（chromium 自动探测，跨机器可用）
└── examples/
    ├── README.md         选题对照表 + 改写方法
    └── generators/       14 份已交付题目的完整生成器（活案例）
```

## 依赖

| 依赖 | 版本 | 用途 | 缺失后果 |
|---|---|---|---|
| Node.js | ≥ 18 | 跑审计 / 截图脚本 | 门禁无法执行 |
| `playwright-core` | ≥ 1.40 | 无头浏览器审计 + 截图 | 门禁无法执行 |
| chromium | 任意版本 | `npx playwright install chromium` | 自动探测失败（脚本会打印已搜索路径） |
| Python | ≥ 3.9 | 跑 `build_*.py` 生成器 | 无法生成产物 |

安装：

```bash
npm i -D playwright-core
npx playwright install chromium
```

`scripts/chrome.js` 会自动探测各平台浏览器目录（Windows / macOS / Linux），
按版本号从新到旧挑选候选，**不再有硬编码版本路径**。也可用环境变量覆盖：

```bash
CHROME_DEBUG=1 node scripts/audit_page.js out.html   # 打印探测过程
PLAYWRIGHT_BROWSERS_PATH=/custom/path node ...      # 指定浏览器根目录
```

## 最小工作流

```bash
# ① 复制最接近的生成器
cp examples/generators/build_zfield_gravity.py _build/build_new.py

# ② 改写后生成产物
python _build/build_new.py

# ③ 三重验收（全部必须过）
node scripts/syntax_check.js  out.html      # 内联脚本语法
node scripts/audit_page.js    out.html      # 17 项主门禁
node scripts/audit_nosig.js   out.html      # 无署名/站外链接
node scripts/shot_zoom.js     out.html      # 3× 特写 → 人工看图 ← 不可省
```

## 为什么特写不能省

自动化门禁查不出「标注被裁切 / 文字叠字」—— 这些缺陷在像素层面完全合法。
本项目**可见缺陷几乎全部**是靠 `shot_zoom.js` 的 3× 特写人工看图发现的，
其中多例在自动化全绿的情况下漏检。因此：

**同一道题重建 / 重跑，也必须重走 3× 人工看图**，不能因为「上次过门禁」跳过。
抽样时刻要覆盖「每个物理阶段的**起始**处」，不能只取中点与末态。

详见 `references/pitfalls.md`。

## 无署名规范（强制）

产物页面**只放题目内容本身**，不含任何身份标识：

- 无页脚 `<footer>`、无署名容器（`.designer` / `.author` / `.copyright` / `.credit`）
- 无站外 `<a href="http...">` 链接、无二维码 / 微信 / QQ / 电话
- 正文无机构名，无「设计开发 / 编写 / 制作 / 出品」等署名动词
- 右栏保留「当前解析步骤与实时数据」面板即可

校验：`node scripts/audit_nosig.js <files...>`，全部归零才算通过。