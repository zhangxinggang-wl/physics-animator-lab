# physics-animator-lab

> 高中物理试题解析 + 解题过程动画生成工作区。
> 内容由 `high-school-physics-problem-solver-animator` 技能自动生成。页面**无署名、无外链**。

## 用途

输入一道物理题（文字 / 截图），输出一份**单文件自包含 HTML**：左栏原题、中栏分步解析、右栏物理动画。

## 目录

| 路径 | 说明 |
|---|---|
| `.workbuddy/skills/high-school-physics-problem-solver-animator/` | **封装好的技能包**（精简入口 + 15 册 references + 泛化工具链 + 14 份活案例） |
| `.workbuddy/skills/*.zip` | 技能包归档（约 1.0 MB），可直接分发；用户级副本已装到 `~/.workbuddy/skills/` |
| `assets/template.html` | 三栏页面模板（约 2.2 MB，内联 MathJax），**框架代码勿改** |
| `references/` | 六大板块公式参考库 + 图形重绘规范（工作区副本，与技能包同步） |
| `_build/` | 逐题构建与历史审计脚本（`build_*.py` 生成、`audit_*.js` 校验、shots_*/ 截图） |
| `.workbuddy/memory/` | 工作记忆：先读 `MEMORY.md` + 最近日期日志 |
| `SKILL.md` | **原始完整版规范**（146 KB，未拆分，便于与入口对照） |
| `*.html` | 历史产物（每题两份：`_动画演示` 单栏版 + `_教学动画` 完整版） |

> 新题请优先照**技能包**里的规范做：入口 `SKILL.md` 只 6 KB，细则按阶段查 `references/` 各分册。

## 标准流程

1. 读 `.workbuddy/skills/high-school-physics-problem-solver-animator/SKILL.md`（入口）
   + `.workbuddy/memory/MEMORY.md` + 最近日记；细则按需查该包 `references/` 各分册
2. 从技能包 `examples/generators/` 复制**题型最接近**的 `build_*.py` 到 `_build/`，改写后生成 HTML
3. 三重验收（全部必须过）：
   ```bash
   S=.workbuddy/skills/high-school-physics-problem-solver-animator
   node $S/scripts/syntax_check.js out.html    # 内联脚本语法
   node $S/scripts/audit_page.js   out.html    # 17 项主门禁
   node $S/scripts/audit_nosig.js  out.html    # 无署名/站外链接
   node $S/scripts/shot_zoom.js    out.html    # 3× 特写 → **人工看图**（不可省）
   ```
4. 产物落盘，更新记忆

> ⚠ 自动化门禁查不出「标注被裁/叠字」—— 那必须靠 `shot_zoom.js` 的 3× 特写人工看图。
> 同一道题重建也要重走这一步，不能因「上次过门禁」跳过。

## 无署名规范（强制）

页面**只放题目内容本身**，不含任何身份标识：

- 无页脚 `<footer>`
- 无署名/设计者/版权容器（`.designer` / `.author` / `.copyright` / `.credit`）
- 无任何站外 `<a href="http...">` 推广链接
- 无图元图例条（`.figlib-key`）
- 正文无学校/学院等机构名，无「设计开发 / 编写 / 制作 / 出品」等署名动词，无微信号 / 二维码 / 联系电话

右栏保留「当前解析步骤与实时数据」数据面板即可。
校验：`node .workbuddy/skills/high-school-physics-problem-solver-animator/scripts/audit_nosig.js <files...>`，
全部条目归零才算通过。