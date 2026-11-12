# -*- coding: utf-8 -*-
"""生成：竖直圆环缓慢滚动多选题（AO/BO 绳张力变化）解析动画 HTML。
题图 = 动画第 0 帧（Canvas 孪生锁定）；选项 A/B/C/D 横向 2×2；解析禁微积分。"""
import io, re, os

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = os.path.join(WS, "assets", "template.html")
OUT = os.path.join(WS, "2026-09-09_竖直圆环缓慢滚动绳张力变化.html")

src = io.open(TPL, encoding="utf-8").read()

# ---------------- ① PROBLEM ----------------
problem = r'''const PROBLEM = {
  title: "",
  given: "12．（多选）一竖直放置的轻质圆环静止于水平面上，质量为 $m$ 的物体用轻绳系于圆环边缘上的 $A$、$B$ 两点，结点恰位于圆环的圆心 $O$ 点。已知物体静止时，$AO$ 绳水平，$BO$ 绳与 $AO$ 绳的夹角为 $150^{\circ}$。现使圆环沿顺时针方向缓慢滚动，在 $AO$ 绳由水平转动至竖直的过程中（　　）",

  images: [
    { src: "__CANVAS_STATIC__", caption: "题图：竖直圆环缓慢滚动，A、B 两点轻绳悬吊圆心结点处的质量 $m$（按原图几何孪生重绘，与动画同坐标）", pos: "bottom" }
  ],

  asks: [],

  // 选择题选项（A/B/C/D 四项缺一不可，横向 2×2 渲染）
  options: [
    "A. $AO$ 绳中的拉力一直增大",
    "B. $AO$ 绳中最大拉力为 $2mg$",
    "C. $BO$ 绳中的拉力先减小后增大",
    "D. $BO$ 绳中最小拉力为 $0$"
  ],

  knowledgePoints: [
    { id: "mech-equilibrium-concurrent", ch: "力学", sub: "共点力平衡", name: "共点力的平衡条件",
      formula: "$\sum F_x = 0,\; \sum F_y = 0$（平面共点力平衡时合力为零）",
      conditions: "物体受共点力作用且处于静止或匀速直线运动状态。",
      pitfalls: ["受力分析时要分清研究对象，绳的拉力只能沿绳指向绳收缩的方向",
                 "建立坐标系后，所有力必须按同一正方向列分量方程"],
      extensions: ["可推广到三力汇交、拉密定理等几何法"],
      difficulty: "基础" },
    { id: "mech-force-decomposition", ch: "力学", sub: "相互作用", name: "力的正交分解",
      formula: "$F_x = F\cos\alpha,\; F_y = F\sin\alpha$",
      conditions: "平面共点力；选定相互垂直的 x、y 轴。",
      pitfalls: ["角度 $\alpha$ 是力与坐标轴的夹角，要统一基准",
                 "分力的正负号由坐标方向决定，不能只看大小"],
      extensions: ["斜坐标系分解、平行四边形法则"],
      difficulty: "基础" },
    { id: "mech-trig-extrema", ch: "力学", sub: "数学工具", name: "三角函数的单调性与极值",
      formula: "$\cos\theta$ 在 $[0^{\circ},180^{\circ}]$ 先减后增；在 $[-90^{\circ},90^{\circ}]$ 单调",
      conditions: "高中阶段判断变力大小的常用方法。",
      pitfalls: ["注意自变量的取值范围与符号",
                 "最大/最小值常出现在区间端点或 $\cos\theta=\pm1$ 处"],
      extensions: ["可结合单位圆直观判断"],
      difficulty: "基础" },
    { id: "mech-quasistatic", ch: "力学", sub: "准静态过程", name: "缓慢过程（准静态平衡）",
      formula: "「缓慢」$\Rightarrow$ 每一时刻动能近似为零，均满足平衡条件",
      conditions: "过程进行得足够慢，可忽略动能变化与惯性效应。",
      pitfalls: ["「缓慢」不等于「匀速转动」：每个状态都是平衡态，但位置随时间变化",
                 "不要用牛顿第二定律列转动动力学方程"],
      extensions: ["缓慢移动中常用力矩平衡或共点力平衡"],
      difficulty: "基础" }
  ]
};'''

src = re.sub(r"const PROBLEM = \{[\s\S]*?\n\};", lambda m: problem, src, count=1)

# ---------------- ② STEPS ----------------
steps = r'''const STEPS = [
  { q: 1, title: "缓慢滚动：每一时刻圆环处于准静态平衡",
    tex: "\sum \vec{F} = 0",
    note: "圆环沿顺时针方向「缓慢」滚动，物体 $m$ 的动能可忽略，因此 $AO$、$BO$ 两绳的张力与重力 $mg$ 在每一时刻都满足共点力平衡。选取结点 $O$ 为研究对象。",
    basis: "准静态过程的平衡条件", t0: 0, t1: 1.2 },

  { q: 1, title: "建立坐标系，用正交分解列平衡方程",
    tex: "\begin{aligned} -T_A\cos\alpha + T_B\cos(30^{\circ}-\alpha) &= 0 \\ T_A\sin\alpha + T_B\sin(30^{\circ}-\alpha) &= mg \end{aligned}",
    note: "设圆环半径为 $R$，从初始位置顺时针转过的角度为 $\alpha$（$\alpha=0$ 时 $AO$ 水平向左）。因 $\angle AOB=150^{\circ}$，$BO$ 与水平向右方向成 $30^{\circ}-\alpha$。结点 $O$ 受 $T_A$（沿 $OA$）、$T_B$（沿 $OB$）和竖直向下的 $mg$。按图示坐标列水平、竖直分量方程。",
    basis: "力的正交分解与共点力平衡", t0: 1.2, t1: 3.0 },

  { q: 1, title: "求解两绳张力随 $\alpha$ 的函数",
    tex: "T_A = 2mg\cos(30^{\circ}-\alpha),\qquad T_B = 2mg\cos\alpha",
    note: "两方程系数行列式为 $-\sin30^{\circ}=-\tfrac12$。用消元法解得 $T_A = 2mg\cos(30^{\circ}-\alpha)$、$T_B = 2mg\cos\alpha$，其中 $\alpha\in[0^{\circ},90^{\circ}]$。数值上取 $m=1\,\mathrm{kg}$、$g=10\,\mathrm{m/s^2}$，与右栏数据面板对应。",
    basis: "二元一次方程组求解（消元法/克莱姆法则）", t0: 3.0, t1: 4.5 },

  { q: 1, title: "分析 $AO$ 绳拉力：先增后减，最大为 $2mg$",
    tex: "T_A = 2mg\cos(30^{\circ}-\alpha) \Rightarrow \alpha=30^{\circ}\ \text{时}\ T_{A,\max}=2mg",
    note: "当 $\alpha$ 从 $0^{\circ}$ 增至 $90^{\circ}$ 时，$30^{\circ}-\alpha$ 从 $30^{\circ}$ 变到 $-60^{\circ}$。$\cos(30^{\circ}-\alpha)$ 在 $\alpha=30^{\circ}$ 时取最大值 $1$，故 $T_A$ 先增大后减小，最大值为 $2mg$。选项 A 错，B 对。",
    basis: "余弦函数在区间上的极值", t0: 4.5, t1: 6.0 },

  { q: 1, title: "分析 $BO$ 绳拉力：单调减小，最小为 $0$，选 B、D",
    tex: "T_B = 2mg\cos\alpha \Rightarrow \alpha=90^{\circ}\ \text{时}\ T_{B,\min}=0",
    note: "$\cos\alpha$ 在 $[0^{\circ},90^{\circ}]$ 单调减小，故 $T_B$ 一直减小；当 $AO$ 转至竖直（$\alpha=90^{\circ}$）时，$BO$ 水平，$T_B=0$。选项 C 错，D 对。综上正确选项为 B、D。",
    basis: "余弦函数的单调性", t0: 6.0, t1: 7.5 }
];'''

src = re.sub(r"const STEPS = \[[\s\S]*?\n\];", lambda m: steps, src, count=1)

# ---------------- ③ VIEW / SIM ----------------
src = re.sub(r"const VIEW = \{[^\n]*\};\nconst SIM[^\n]*\};",
             lambda m: "const VIEW = { xmin: -0.8, xmax: 4.2, ymin: -0.5, ymax: 2.7 };\nconst SIM  = { duration: 7 };",
             src, count=1)

# ---------------- ④ GLOBALS ----------------
globals_code = r'''/* 几何与物理参数（长度以圆环半径 R 为单位） */
const R = 1.0;                 // 圆环半径
const M = 1.0;                 // 物体质量，kg
const G = 10.0;                // 重力加速度，m/s²
const ALPHA_MAX = Math.PI / 2; // AO 从水平转到竖直，圆环顺时针转过 90°
function stateAt(t){
  const p = Math.min(Math.max(t / SIM.duration, 0), 1);
  const alpha = p * ALPHA_MAX;
  const Ta_over_mg = 2 * Math.cos(Math.PI/6 - alpha);
  const Tb_over_mg = 2 * Math.cos(alpha);
  const Ta = M * G * Ta_over_mg;
  const Tb = M * G * Tb_over_mg;
  return { p:p, alpha:alpha, deg:alpha*180/Math.PI,
           Ta_over_mg:Ta_over_mg, Tb_over_mg:Tb_over_mg,
           Ta:Ta, Tb:Tb };
}'''
src = src.replace("/*__GLOBALS__*/", globals_code, 1)

# ---------------- ⑤ SETUP ----------------
src = src.replace("/*__SETUP__*/",
                  "// 状态全部由全局 stateAt(t) 实时给出，无需预计算", 1)

# ---------------- ⑥ DRAWFRAME ----------------
draw_code = r'''  const st = stateAt(t);
  const alpha = st.alpha, deg = st.deg;

  /* 圆环中心 O 的世界坐标（无滑滚动：向右移动 R·α） */
  const Ox = R + R * alpha;
  const Oy = R;

  /* A、B 两点方向（AO、BO 为从 O 指向环边缘的半径） */
  const ax = -Math.cos(alpha), ay = Math.sin(alpha);
  const bx = Math.cos(Math.PI/6 - alpha), by = Math.sin(Math.PI/6 - alpha);
  const Ax = Ox + R * ax, Ay = Oy + R * ay;
  const Bx = Ox + R * bx, By = Oy + R * by;

  /* 悬挂物块位置（O 正下方） */
  const mx = Ox, my = Oy - 0.32;

  /* 绘制 */
  clearBg();
  FIG.ground(-0.6, 4.4, 0, {});
  FIG.circleTrack(Ox, Oy, R, { color: '#1f2937', thickness: 0.07 });

  /* 轻绳 AO、BO 及悬挂线 */
  drawLine(Ox, Oy, Ax, Ay, '#334155', 1.6);
  drawLine(Ox, Oy, Bx, By, '#334155', 1.6);
  drawLine(Ox, Oy, mx, my + 0.11, '#334155', 1.6);

  /* 物块 m */
  const [msx, msy] = W2S(mx, my);
  const wp = 0.22 * scale, hp = 0.22 * scale;
  ctx.fillStyle = '#e2e8f0'; ctx.strokeStyle = '#1f2937'; ctx.lineWidth = 1.6;
  ctx.fillRect(msx - wp/2, msy - hp/2, wp, hp);
  ctx.strokeRect(msx - wp/2, msy - hp/2, wp, hp);

  /* 点 A、B、O */
  drawPoint(Ax, Ay, '#1f2937', 3.5);
  drawPoint(Bx, By, '#1f2937', 3.5);
  drawPoint(Ox, Oy, '#1f2937', 3.5);

  /* 字母标注 */
  drawText(Ax - 0.14, Ay, 'A', '#0f172a', 14, 'right');
  drawText(Bx + 0.10, By + 0.06, 'B', '#0f172a', 14, 'left');
  drawText(Ox + 0.10, Oy + 0.10, 'O', '#0f172a', 14, 'left');
  drawText(mx + 0.12, my, 'm', '#0f172a', 14, 'left');

  /* 实时角度显示器 */
  ctx.fillStyle = '#0f172a'; ctx.font = '12.5px sans-serif'; ctx.textAlign = 'right';
  ctx.fillText('\u03b1(t) = ' + deg.toFixed(1) + '\u00b0 = ' + alpha.toFixed(3) + ' rad', W - 10, 18);
  ctx.textAlign = 'left';'''
src = src.replace("/*__DRAWFRAME__*/", draw_code, 1)

# ---------------- ⑦ READOUTS ----------------
readouts_code = r'''  const st = stateAt(t);
  return [
    ["$\\alpha(t)$", st.deg.toFixed(1), "\u00b0"],
    ["$\\alpha(t)$", st.alpha.toFixed(3), "rad"],
    ["$T_A/mg$", st.Ta_over_mg.toFixed(3), ""],
    ["$T_B/mg$", st.Tb_over_mg.toFixed(3), ""],
    ["$T_A$", st.Ta.toFixed(2), "N"],
    ["$T_B$", st.Tb.toFixed(2), "N"]
  ];'''
src = src.replace("/*__READOUTS__*/", readouts_code, 1)

# ---------------- ⑧ 选项横向 2×2 覆写 ----------------
opt_override = (
    "<style id=\"opt-horizontal-override\">\n"
    "  /* 本页左栏较窄，选项改为 2×2 横排网格，文本可换行 */\n"
    "  .options{display:grid;grid-template-columns:1fr 1fr;column-gap:18px;row-gap:3px;margin:8px 0 6px}\n"
    "  .opt{font-size:13px;line-height:1.7;white-space:normal;min-width:0}\n"
    "</style>\n"
)
src = src.replace("</head>", opt_override + "</head>", 1)

io.open(OUT, "w", encoding="utf-8").write(src)
print("written:", OUT, os.path.getsize(OUT), "bytes")
