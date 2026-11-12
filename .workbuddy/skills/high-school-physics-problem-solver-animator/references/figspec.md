# 题图→动画图形严格一致（FIG 库）

> 本册是 `high-school-physics-problem-solver-animator` 技能的**按需加载分册**。
> 主文件 `SKILL.md` 只给工作流与门禁；细节规范在此，按阶段查阅。
> 内容自原 `SKILL.md` 第 618–834 行原样切出，未作改动。

---

### 题图→动画图形严格一致（FIG 库强制条款）

> 用户多次强调：「动画中所使用的动画图形要与试题图片中的图形完全相同」。
>   
> 为此，模板内置一套 **`FIG` 图元库**，所有动画几何元素都通过 `FIG.*` 绘制——
>   
> 与左栏题图的 SVG / 嵌入图采用**同一世界坐标**、**同一比例尺**、**同一几何元素**，
>   
> 物理上保证「题图 → 动画图形 1:1 对应」。

#### 图元清单

```js
const FIG = {
  /* —— 基础几何（题图与动画共用） —— */
  wall(x, top, bottom, opts?)            // 竖直墙壁：粗竖线 + 左侧斜线阴影
  ground(x1, x2, y, opts?)              // 水平地面：粗横线 + 下方斜线阴影
  spring(x1, x2, y, opts?)              // 水平弹簧（zigzag）：N 段折线，圈数/振幅可调
  springV(x, y1, y2, opts?)             // 竖直弹簧（zigzag）：方向竖直，圈数/振幅可调 → 与题图竖直弹簧一致
  forceArrow(x, y, dir, len, label, opts?)  // 力箭头：方向 + 长度 + 标签
  block(cx, cy, w, h, label, opts?)     // 矩形物块：中心 + 宽高 + 标签
  text(x, y, str, opts?)                // 文字标签（斜体，可选颜色）
  /* —— 力学模型图元（必须 1:1 还原） —— */
  particle(x, y, r, label, opts?)       // 质点模型：实心小圆 + 质量标注（m）
  pivot(x, y, opts?)                    // 固定铰/转轴：圆心十字（支点）
  rod(x1, y1, x2, y2, opts?)            // 直杆模型：粗实线（可双线 double）+ 两端铰点
  circleTrack(cx, cy, R, opts?)         // 竖直平面内的圆轨道模型：双圆弧轨道环（顶/底/左/右关键点）
  collisionPoint(x, y, opts?)           // 碰撞点/接触点：高亮标记 + 字母标注
  pendulum(px, py, len, angle, bobR, opts?)  // 单摆：支点+摆线+摆球（angle 自竖直向下起算）
  /* —— 恒定电流电路图元件符号（全部用 FIG.*，禁止手画矩形/折线冒充） —— */
  wire(a,b,c,d, opts?)                  // 导线：直线(x1,y1,x2,y2) 或 折线(points:[[x,y]...])
  battery(x, y, orient, opts?)          // 电源：长线+短线，orient 'h'|'v'
  resistor(x, y, orient, opts?)         // 电阻：矩形(默认,教材常见)/锯齿(style:'box'|'zigzag')
  rheostat(x, y, orient, opts?)         // 滑动变阻器：电阻体+滑片箭头+三接线柱，tap 定滑片位置
  capacitor(x, y, orient, opts?)        // 电容器：双平行板
  inductor(x, y, orient, opts?)         // 电感/线圈：半圆弧
  lamp(x, y, opts?)                     // 灯泡/用电器：圆内 X
  switchWire(x1, y1, x2, y2, opts?)     // 开关：断开/闭合(closed)
  ammeter(x, y, opts?)                  // 电流表：圆内 A
  voltmeter(x, y, opts?)                // 电压表：圆内 V
  galvanometer(x, y, opts?)             // 灵敏电流计：圆内 G
  node(x, y, opts?)                     // 导线连接点（节点实心圆点）
  /* —— 磁场 / 电场 场线（教材标准符号，位置无关，按题图实际方向绘制） —— */
  magInto(x1,x2,y1,y2,opts?)            // 磁场垂直纸面向里：区域内均匀 × 标记（紫）
  magOut(x1,x2,y1,y2,opts?)             // 磁场垂直纸面向外：区域内均匀 ⊙ 标记（紫）
  magLines(x1,x2,y1,y2,ang,opts?)       // 磁场纸面内任意方向场线：ang 弧度(0=右,π/2=上,可任意角)，带箭头平行线
  eInto(x1,x2,y1,y2,opts?)              // 电场垂直纸面向里：× 标记（蓝）
  eOut(x1,x2,y1,y2,opts?)               // 电场垂直纸面向外：⊙ 标记（蓝）
  eLines(x1,x2,y1,y2,ang,opts?)         // 电场纸面内任意方向场线：带箭头平行线
  chargePlus(x,y,opts?)                 // 正点电荷（红圆 + 十字）
  chargeMinus(x,y,opts?)                // 负点电荷（蓝圆 + 横线）
  /* —— 力学曲面 / 常见装置（圆弧面、管道、斜面等） —— */
  arcSurface(cx,cy,R,a1,a2,opts?)       // 圆弧面：世界圆心+半径+角度范围[°]；凹/凸由角度区间决定，可选实体斜线
  pipe(pts,R,opts?)                     // 管道（光滑管/弯管）：沿世界折线 pts 画空心管，管半径 R
  incline(xL,xR,yTop,yTop2,yBase,opts?) // 斜面/楔形：顶面对角(xL,yTop)-(xR,yTop2)，底边 yBase，实体在下
  /* —— 通用辅助图元（任意方向矢量 / 角度 / 滑轮 / 波 / 坐标系 / 多过程横幅） —— */
  vec(x,y,dx,dy,label,opts?)            // 通用矢量箭头：起点+分量(dx,dy)，任意方向，带标签（力/速度/加速度/洛伦兹力等）
  angleArc(cx,cy,r,a1,a2,label,opts?)   // 角度弧 + 标签（斜面角、摆角等）
  pulley(x,y,R,opts?)                   // 定滑轮：轮+轴+轮辐，可画悬挂绳 rope
  wave(x1,x2,y,amp,lambda,phase,opts?)  // 正弦波（机械波/简谐）：平衡线 y、振幅、波长、相位
  coord(xmin,xmax,ymin,ymax,opts?)      // 坐标系箭头（x/y 轴带箭头），运动学/场强分布坐标系
  processBanner(text,opts?)             // 多过程阶段横幅：画布顶部显示当前过程名（过程数=题设过程数）
};
```

#### 图元清单（扩展：光学 / 热学 / 力学补充 / 电路补充 / 磁场补充 / 大学·强基）

> 2026-09 扩充：以下图元已加入 `assets/template.html` 的 `FIG.*`，与上方基础图元同坐标系、同比例尺。
>   
> 完整函数签名与零错误要点见 `references/figures_redraw_spec.md §3.1`；大学/强基知识点与图元对应关系见 `references/university_physics_reference.md`。

```js
const FIG = {
  /* —— 光学 —— */
  optAxis(x1,x2,y,opts?)               // 主光轴（虚线）
  lens(x,yt,yb,type,opts?)             // 薄透镜：type 'convex'|'concave'，可选焦距 f 标 F/2F
  mirror(x,yt,yb,type,opts?)           // 平面/球面镜：type 'plane'|'concave'|'convex'
  ray(pts,opts?)                        // 光线（折/反射折线，末端箭头）
  objArrow(x,y,h,opts?)                 // 物/像箭头（正立/倒立，虚像 dashed）
  screen(x,yt,yb,opts?)                 // 光屏
  prism(pts,opts?)                      // 棱镜（色散）
  barrier(x,y,h,slits,opts?)            // 双缝/光栅挡板
  ripple(cx,cy,R,n,opts?)               // 水波/干涉同心圆
  polarizer(x,yt,yb,opts?)              // 偏振片
  /* —— 热学 —— */
  pvAxes(vmin,vmax,pmin,pmax,opts?)     // p-V 坐标轴
  pvCurve(pts,opts?)                    // p-V 过程曲线
  gasCylinder(x,y,w,h,opts?)            // 气缸+活塞（可加活塞杆+重物）
  thermometer(x,y,len,opts?)            // 温度计（液柱比例 fill）
  utube(x,y,w,h,opts?)                  // U 形管压强计（fillL/fillR）
  heatBath(x,y,w,h,opts?)               // 热源/热库
  moleculeCloud(pts,opts?)              // 分子点云
  /* —— 力学补充 —— */
  forceParallelogram(ox,oy,v1,v2,opts?) // 力的平行四边形定则（两分力+合力）
  trajectory(pts,opts?)                 // 运动轨迹（平抛/斜抛等）
  ellipseOrbit(cx,cy,a,b,opts?)          // 椭圆轨道（开普勒，焦点恒星+行星）
  momentArm(ox,oy,px,py,fx,fy,opts?)    // 力臂（支点→力线垂足）
  com(points,opts?)                     // 质心
  /* —— 电路补充 —— */
  acSource(x,y,opts?)                    // 交流电源（圆内正弦）
  currentSource(x,y,opts?)              // 理想电流源（圆内箭头）
  transformer(x,y,opts?)                // 变压器（铁芯+原/副线圈）
  diode(x,y,opts?)                       // 二极管（flip 反向，glow=LED）
  groundSym(x,y,opts?)                   // 接地符号
  fuse(x,y,opts?)                        // 保险丝
  machine(x,y,letter,opts?)             // 电动机/发电机（圆内 M/G）
  /* —— 磁场补充 —— */
  solenoid(x1,x2,y,opts?)                // 螺线管（线圈+内部场）
  currentLoop(cx,cy,R,opts?)            // 环形电流（法向磁场）
  barMagnet(x,y,len,opts?)              // 条形磁铁（N/S+外场线）
  /* —— 大学·强基 —— */
  energyLevels(levels,transitions,opts?)// 能级图（发射↓/吸收↑）
  quantumWell(x,y,w,V0,opts?)           // 一维方势阱
  bohrOrbit(cx,cy,radii,opts?)          // 玻尔轨道
  spacetime(ox,oy,opts?)                 // 闵可夫斯基时空图（光锥）
  rigidDisk(cx,cy,R,opts?)              // 刚体转动圆盘（ω 箭头）
  axisVec(cx,cy,len,label,opts?)         // 角动量/力矩矢量
  nucleus(cx,cy,Z,N,opts?)               // 原子核（质子/中子团簇）
  streamline(pts,opts?)                 // 流体流线
};
```

#### 使用约定（生成页面时必须遵守）

- **同一坐标系**：动画视图坐标 `VIEW = {xmin, xmax, ymin, ymax}` 直接复刻左栏题图的几何范围；题图 SVG 中物块/墙/地/弹簧的坐标投影后应与 `FIG.*` 调用的世界坐标**完全一致**（如墙在 `x = -2`，则动画中 `FIG.wall(-2, ...)`）。
- **同一比例尺**：`FIG.spring` 的 zigzag 振幅 / `FIG.wall` 的阴影斜线长度都按 `scale` 自动调整，避免动画中的弹簧被拉长或压缩。
- **禁止混用**：动画中**禁止**直接用 `drawRect` / `drawArrow` 画与题图相同的元素——必须走 `FIG.*`，否则比例/几何可能与题图不一致。
- **页面图例**：模板**不渲染**右下角「图元」配色小条（`.figlib-key` 及 `renderFiglibLegend` 已从模板移除），右栏动画区不再显示图例条。

#### ⚠ 比例尺与纵横比（生成前必算，否则圆变成椭圆、轮子陷进地面）

- **画布尺寸固定为 1 : 0.66**：`resize()` 中 `cv.height = cv.clientWidth * 0.66`，且 `scale = (W - 2*PAD) / (VIEW.xmax - VIEW.xmin)`（`PAD = 36`、`W/H` 为 CSS 像素）。
- **x、y 比例尺一致的条件（车轮/圆轨道/圆必须是正圆的唯一依据）**：
  `(VIEW.xmax - VIEW.xmin) / (VIEW.ymax - VIEW.ymin) = (W - 2*PAD) / (H - 2*PAD)`。
  由于 `H = 0.66·W`，近似为 `yrange ≈ 0.594 · xrange`（**不是** `0.66·xrange`——`PAD` 会吃掉一部分，直接用 0.66 会让纵向比例尺偏小约 10%，`ctx.arc` 画出的车轮会「陷进地面」、气门芯/质点的相对半径失真）。
  实测：1500px 视口下 `W ≈ 443`，此时 `xrange = 2.84` 对应 `yrange = 1.687`（2.84 × 220.38 / 371）。
- **`VIEW` 只约束世界范围，不干扰顶栏**：过程横幅（`FIG.processBanner`）与 `θ(t)` 显示器都画在**像素坐标**的画布顶部；若场景较高（如自行车、斜面），应把 `ymin` 往下压、给顶部留出 ~90px 的空白带，并把**实时角度 HUD 放在横幅下一行**（横幅 y≈8–37px、HUD y≈40–82px），否则两者会互相压字。
- **⚠️ 画布上「按像素定位」的一切（横幅/HUD/图例）必须取 CSS 像素，取 `ctx.canvas.width` 会整块画到画布外**（2026-09-23 实测，模板级 bug 已修）：
  `resize()` 里执行了 `ctx.setTransform(ratio,0,0,ratio,0,0)`（`ratio = devicePixelRatio`），
  之后**所有绘制坐标按 CSS 像素解释**；而 `ctx.canvas.width/height` 是**设备像素**（2× 屏即翻倍）。
  故 `(W - bw)/2` 会按 2 倍偏移居中 ⇒ **横幅只露左半截、右下角 HUD 整块消失**。
  **只在 dpr ≥ 2 的屏幕上暴露，dpr=1 时完全正常**——极易被误判成「没写这个图元」。
  正确写法：
  ```js
  const r = ctx.canvas.getBoundingClientRect();
  const Wp = (r && r.width)  ? r.width  : ctx.canvas.width;
  const Hp = (r && r.height) ? r.height : ctx.canvas.height;
  ```
  用 `getBoundingClientRect()` 而非全局 `W/H`，因为此类函数可能被左栏题图画布复用
  （`drawStaticGraph` 里临时把全局 `ctx` 指向题图画布，此时全局 `W/H` 是动画画布的尺寸、会取错）。
  新增 HUD/横幅后**先 grep 一遍 `ctx.canvas.width`**，命中就要改。
- **`FIG.ground` / `FIG.wall` 的 `hatchLen` 是世界长度×1.25**：实现为 `sh = hatchLen * scale / 8`（像素）。默认 `hatchLen:10` 在 `scale≈28`（大场景）时约 35px 尚可，但在 `scale≈130`（小场景、`xrange` 仅几米）时会画出上百像素的巨型阴影斜线。**小场景必须显式传小值**：如 `{gap:0.16, hatchLen:0.7}`（地面）、`{hatchLen:2, gap:6}`（竖直墙）。
- **短矢量不要用 `FIG.vec` 的自动标签**：`FIG.vec` 在**末端 1.12 倍**处放标签，而世界坐标下的短矢量（如 `uRel*0.070`，仅几像素）会把标签正好压在物块中心的字号标签上。
  对策：`FIG.vec(x,y,dx,dy,'',{...})` 只画箭头，标签在 `drawLabels()` 里按「垂直于矢量、朝外」方向手动外推（如沿圆弧外法线推 0.26 世界单位）。
- **零矢量与图形题图的干净性**：`FIG.vec` 即使 `dx=dy=0` 也会在起点画一个箭头三角，故**生长型矢量必须按「像素长度 > 10~12px」设阈值**再绘；题目原图没有的解题辅助元素（轨迹、分位移、角度弧、图例、HUD）应统一放在 `if (t > 0.002){ ... }` 里绘制，使 `drawSceneBody(0)`（＝左栏题图）与原题图逐线一致。
- **旋转矢量上的标签必须避开「活动禁区」**（放大视图/圆轨道类图元高频踩坑）：矢量末端位置随 `θ` 转圈，若标签写死在固定偏移（如末端 `+(4, +4)`），当矢量转到其他象限时会与旁边的固定说明文字、圆环或箭头三角叠字。两条对策，能同时用最好：
  1. **白底让位**：在固定说明文字下先铺一块 `rgba(255,255,255,0.94)` 矩形（略大于文字），再写文字——旋转标签路过时"沉"到底下，视觉仍可读，且无需改文字位置。
  2. **标签随矢量方向外推**：偏移量拆成法向/切向两项，按矢量朝向取符号，例如
     `fillText(label, ex + (dx>=0?7:-7), ey + (dy>=0?13:-6))`（`(dx,dy)` 为矢量像素分量），
     使标签始终落在箭头"外侧"而不是压在箭头上。
  **仅靠自动化门禁查不出这类叠字**，必须用 `shot_canvas.js`（`deviceScaleFactor:3`）在**多个 t 值**（至少 0、0.4、0.7、1.0）下截图人工核对——单看末态正常不代表中段正常。

#### ⚠ 竖向预算：HUD 一律按 H 的比例定位（窄画布必踩）

- **动画栏实际画布宽度远小于视口宽**：`.col-animation{flex:1.3 1 340px}`，实测 1280 / 1366 / 1600 / 1920 视口下
  `cv.clientWidth` 仅约 **395 / 423 / 494 / 590 px**，而画布高恒为 `0.66×宽` → 最窄时只有 **261 px 高**。
- **任何 HUD（信息带、计时器、图例、横幅）都不得写死像素高度**：写死 110px 的信息带会在窄画布下
  直接压住世界场景的尺寸线。正确做法：
  1. 给 HUD 划一条**比例带**，如信息带 `[0.115H, 0.39H]`，内部各行位置写成 `b0 + bh * 系数`；
  2. 由「`0.39H` 对应多高的世界坐标」反算 `VIEW.ymax`，保证场景最高的一条标注（如最上面的尺寸线）
     落在 `0.39H` 之下——四宽度都要验算，最窄宽度是约束方；
  3. 用 `clip()` 把物理图元限制在「HUD 下沿 ~ 地面」之间的空气区域（如波前圆弧），
     避免图元窜进 HUD。
- **纵横比系数要按「实际画布内宽」算，不要背一个固定值**：正圆条件为
  `yrange / xrange = (0.66·W内 − 2·PAD) / (W内 − 2·PAD)`（`PAD = 36`）。
  - **三栏完整版**：画布内宽随视口在 **395~590px** 间变（对应系数 0.594~0.613），取 **0.60** 全局最稳，
    车轮/圆波前的纵横比误差 < 2.5%；
  - **单栏动画页**：画布 CSS 定宽 680px ⇒ 内宽（扣 1px 边框）恒为 **678**，系数取 **0.6196**
    （`yrange = 4.05 × 0.6196 = 2.5094`、`ymax = 1.8994`），此时两向比例尺精确相等（149.6296 px/m）。
  - 判据：`ctx.arc(px,py,r*scale)` 画的圆**不受影响**；会被拉成椭圆的是**用 `W2S` 逐点描出的圆弧**
    ——超声波圆波前、连杆轨迹、圆弧轨道都属于后者，务必验算。
- **横向也要留白**：`HUD` 里所有定宽内容（如「计时器状态」药丸、图例）必须**先 `measureText` 再判断
  是否有余量**，放不下就不画或折行；图例按可用宽度自底向上折行时记住把行序倒过来
  （`y = H - 10 - (n - 1 - li) * 15`），否则读起来是反的。

#### ⚠ 脚本组织：HUD 函数必须放在 `GLOBALS`（顶层）

- `/*__DRAWFRAME__*/`、`/*__READOUTS__*/` 都位于**函数体内**（`drawSceneBody(t)`、`readouts(t)`）。
  把 `drawBanner / drawTimeBand / drawWave` 这类辅助函数追加在 `/*__READOUTS__*/` 之后，
  它们就只在 `readouts` 内部可见 → 播放时 `ReferenceError: drawTimeBand is not defined`，
  而且 `loop()` 中 `render()` 抛错后 `requestAnimationFrame` 不再排期，**动画会直接卡死在 t = 0**
  （门禁症状：`distinctFrames = 1`、上一步/下一步点不动、`pageerror` 出现 ReferenceError）。
  正确落点：`/*__GLOBALS__*/`（在 `function setup()` 之前，属顶层）。
  生成器末尾建议加探针断言 `"\nfunction drawTimeBand(st){" in out`（行首无缩进 = 顶层声明）。
- **`note` / `basis` 由模板以 `innerHTML` 渲染，不支持 Markdown**：写成 `**加粗**` 会在页面上
  **原样显示两个星号**。一律写 `<b>…</b>`；可在生成器里加
  `STEPS = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", STEPS)` 兜底并打印转换处数。
- **像素坐标短箭头不要用压线白底标签**：`t₁ = 5.00 ms` 这类短段（约 26px）标签宽约 55px，
  白底会把箭头整条盖掉。短箭头把标签放到**线下方**（`y + 12`），长箭头（如 `Δt = 1.250 s`）才用压线标签。
- **读数必须与解析逐项对齐（末态尤其）**：若某读数是"当前实时量"（如"当前 A 到 B 的距离"），
  它会在声波回程期间继续缓慢变化（本题第二次声波飞行 7.5 ms 内小车又走 5 mm，读出 2.555 而答案是 2.550）。
  应改为**按「测量瞬间」取值**（`x₂ = x₁ + v·min(τ, Δt)`），使末态读数严格等于解析答案。

#### 违规判定（QA）

同一题的两份截图（左栏题图 + 右栏动画暂停态），如果存在以下任一差异，即视为「图-动画不一致」：

- 物块大小、间距、相对位置不同；
- 弹簧长度 / 圈数差异；
- 墙、地面缺失或斜线阴影方向错误；
- 力箭头长度 / 方向错误；
- 标注字母（A/B/C/F）位置错位。

修正方法：在 `drawFrame` 中用 `FIG.*` 重画所有图元，使其几何与左栏题图 SVG 一致。

---
