# 项目长期记忆（physics-animator-lab）

> 规范入口 = Skill 包 `.workbuddy/skills/high-school-physics-problem-solver-animator/`。
> **写生成器前必读 `references/pitfalls.md`**（单题细坑都在那）；选题先查 `examples/README.md`，**复制最接近的一份改写，绝不从零写**。本文件只留索引与跨题通用铁律。

## 产物与流水线

- 单文件自包含 HTML（`assets/template.html` 填 6 区域）；单栏版用抽取脚本生成，绝不另写。
- 流水线：`build_*.py`（FOUND/MISSING 探针 + 反斜杠硬门禁）→ `syntax_check.js` → `audit_page.js` → `audit_nosig.js` → `shot_stages`（按物理阶段抽帧，**人工看图不可省**）。
- 门禁：mjx-error=0、无裸定界符/`<select>`、canvas 非白、解析栏无滚动、四宽零溢出、零报错、首帧四要素、distinctFrames≥5；单栏另查列数=1、内宽678、kpToggle=0。
- note/title/basis 禁裸 `<``>` ⇒ `\lt` `\gt`；canvas/HUD 文案用 Unicode 下标。
- ⚠ 自动门禁查不出标注被裁/叠字 ⇒ 可见缺陷 100% 靠人工看图（多时刻）。

## 渲染铁律（详见 pitfalls.md）

- WBOX 映射「绘图带」，每帧开头 ensureView() 反解 VIEW；帧内引用常量放 GLOBALS_JS（放 DRAW_JS 顶部 TDZ 首帧崩）。
- 世界/像素原语两套隔离；圆弧一律世界坐标采样折线 arcW，别用 ctx.arc。
- 静态 VIEW 必须按画布宽保持宽高比（`yrange/xrange=(0.66cw−72)/(cw−72)` 类），否则变形。
- 白底 wtBox 会挖掉穿过的线 ⇒ 避字处用无底 wt/halo；标签偏移沿法向；同一锚点最多两支箭头；图例不泄露答案。
- **骑行字母标签在密集轨迹带必被弧线压住 ⇒ 双粒子题删骑行字母，靠颜色+图例区分**（2026山东18 实测）。
- Python 注入 JS 用 .replace()+lambda；改生成器一次一条 Edit；shot_stages 除数动态读 SIM.duration。

## 单栏抽取五条

1. `#cv{width:680px}` 被 .col padding+边框压成 678 ⇒ 栏宽上限 706。
2. tune 块 `#cv{width:5xx}` 是 ID 选择器 ⇒ 必须同步改。
3. `.wrap` 外壳保留；kpToggle+kpDrawer 整块删。
4. extra CSS 包 `<style>` 再插 `</head>`。
5. 多 style 页锚点用 `</style>\n</head>`；「只标注不运动」段做 sp 渐进呈现。

## 分段引擎

- SEGS 按轨迹原始顺序；arc/hold 注入 `v` 字段；lin 公式含 `(sg.y0||0)` 且两处一致 + 始/终点断言；段间连续性 assert。
- 双粒子闭式：各写 aState3/bState3（绝对 s = s0+sT·sp），轨迹分别采样绘制。

## 题型索引（结论详见当日日志/pitfalls.md；生成器都在 `_build/build_*.py`）

2011福建22 摆线｜2014天津12 同步加速器｜2016浙江25 扇形回旋｜2021广东14 花瓣｜2021湖南13 磁聚焦｜2022江苏15 交变电场｜2023江苏16 霍耳推进｜2023山东17 方形电场+外围磁场｜2023重庆15 加速器（首例分镜头相机）｜2024新课标26 速度空间（圆顺时针270°）｜2024海南19 三区域磁场｜2025重庆14 荧光屏打点｜2025贵州15 yOz 分区磁场｜2026山东17 旋转叶片｜
**2026山东18 速度选择器+交替半圆漂移**：B₀=E/v、B₁=mv/(qh)、t=29πm/(60qB)、M=17m/10、x₁=34mv/(15qB)；相遇条件 10j−17k=12 ⇒ (j,k)=(8,4)；b 速率是 v 非 v′（OCR 易误读）；a 的 +y 穿越点 (12+7j)mv/(30qB)、b 的 (12+7k)Mv/(30qB)。抽取 `extract_2026sd18_single.py`、单栏审计 `audit_anim_sd18.js`、截图 `shot_stages_sd18.js`（滑杆除数动态读 SIM.duration）。

## 用户偏好

中文注释、可直接运行、单文件完整交付；沟通简洁直接，先结论后过程。
**交付后必须 present_files 打开 HTML 预览**。
