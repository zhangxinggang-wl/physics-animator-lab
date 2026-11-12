# -*- coding: utf-8 -*-
"""生成：斜面-滑轮-三物体准静态平衡多选题解析动画 HTML。
题图 = 动画第 0 帧（Canvas 孪生锁定）；选项 A/B/C/D 横向 2×2；解析禁微积分。"""
import io, re, os

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = os.path.join(WS, "assets", "template.html")
OUT = os.path.join(WS, "2026-09-09_斜面滑轮三物体准静态平衡.html")

src = io.open(TPL, encoding="utf-8").read()

# ---------------- ① PROBLEM ----------------
problem = r'''const PROBLEM = {
  title: "",
  given: "27．（多选）如图所示，倾角为 $30^{\circ}$、质量 $M=4$ kg 的斜面体 $C$ 置于粗糙水平地面上，质量 $m=3$ kg 的小物块 $B$ 放在粗糙斜面上，连接 $B$ 的轻绳与斜面平行，轻绳跨过光滑轻质定滑轮 $O$ 与质量为 $m_A=1$ kg 的物块 $A$ 相连．开始时 $A$ 静止在滑轮正下方，现对 $A$ 施加一个拉力 $F$ 使 $A$ 缓慢移动，$F$ 与连接 $A$ 的轻绳 $OA$ 的夹角始终保持 $120^{\circ}$，直至轻绳 $OA$ 水平．此过程中 $B$、$C$ 始终保持静止状态．$g$ 取 $10$ m/s²，则（　　）",

  images: [
    { src: "__CANVAS_STATIC__", caption: "题图：斜面体 $C$、物块 $B$、定滑轮 $O$ 与受拉力 $F$ 缓慢移动的物块 $A$（按原图几何孪生重绘，与动画同坐标）", pos: "bottom" }
  ],

  asks: [],

  // 选择题选项（A/B/C/D 四项缺一不可，横向 2×2 渲染）
  options: [
    "A. 开始时，$B$ 所受摩擦力大小为 $5$ N",
    "B. $OA$ 水平时，轻绳拉力为 $\\dfrac{5\sqrt{3}}{3}$ N",
    "C. $OA$ 水平时，地面对 $C$ 的支持力为 $\\left(70-\\dfrac{5\sqrt{3}}{3}\\right)$ N",
    "D. $A$ 缓慢移动过程中，轻绳拉力的最大值为 $110\sqrt{3}$ N"
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
    { id: "mech-force-friction", ch: "力学", sub: "相互作用", name: "静摩擦力",
      formula: "$f_{\text{静}} \le f_{\max} = \mu_s N$；平衡时由平衡条件求大小",
      conditions: "两接触面相对静止且有相对运动趋势。",
      pitfalls: ["静摩擦力大小不能直接用 $\mu N$ 计算，须由平衡条件或运动状态确定",
                 "方向与相对运动趋势方向相反"],
      extensions: ["斜面上物体：重力沿斜面向下的分力 $mg\sin\theta$ 常决定趋势方向"],
      difficulty: "基础" },
    { id: "mech-quasistatic", ch: "力学", sub: "准静态过程", name: "缓慢过程（准静态平衡）",
      formula: "「缓慢」$\Rightarrow$ 每一时刻动能近似为零，均满足平衡条件",
      conditions: "过程进行得足够慢，可忽略动能变化与惯性效应。",
      pitfalls: ["「缓慢」不等于「匀速移动」：每个状态都是平衡态，但位置随时间变化",
                 "不要用牛顿第二定律列转动动力学方程"],
      extensions: ["缓慢移动中常用力矩平衡或共点力平衡"],
      difficulty: "基础" }
  ]
};'''

src = re.sub(r"const PROBLEM = \{[\s\S]*?\n\};", lambda m: problem, src, count=1)

# ---------------- ② STEPS ----------------
steps = r'''const STEPS = [
  { q: 1, title: "以 $A$ 为研究对象，列准静态平衡方程",
    tex: "\begin{aligned} -T\sin\varphi + F\cos(\varphi-30^{\circ}) &= 0 \\ T\cos\varphi + F\sin(\varphi-30^{\circ}) - m_A g &= 0 \end{aligned}",
    note: "设 $OA$ 与竖直向下方向夹角为 $\varphi$（$\varphi=0$ 时 $A$ 在滑轮正下方）。$T$ 沿 $A\to O$，$F$ 与 $OA$ 成 $120^{\circ}$，方向取 $\varphi-30^{\circ}$（与图示一致）。$A$ 缓慢移动，每一时刻合力为零。",
    basis: "准静态过程的共点力平衡条件", t0: 0, t1: 1.5 },

  { q: 1, title: "消去 $F$，得到轻绳张力 $T(\varphi)$",
    tex: "T(\varphi) = \frac{m_A g\cos(\varphi-30^{\circ})}{\cos30^{\circ}} = \frac{20\sqrt{3}}{3}\cos(\varphi-30^{\circ})",
    note: "由第一式得 $F = \dfrac{T\sin\varphi}{\cos(\varphi-30^{\circ})}$，代入第二式并利用 $\cos\varphi\cos(\varphi-30^{\circ})+\sin\varphi\sin(\varphi-30^{\circ})=\cos30^{\circ}$，化简即得上式。$\varphi\in[0^{\circ},90^{\circ}]$。",
    basis: "三角恒等式与共点力平衡", t0: 1.5, t1: 3.0 },

  { q: 1, title: "开始时判断 $B$ 所受摩擦力（选项 A）",
    tex: "f_B = mg\sin30^{\circ}-T_0 = 15\,\mathrm{N}-10\,\mathrm{N}=5\,\mathrm{N}",
    note: "$\varphi=0$ 时 $T_0=\dfrac{20\sqrt{3}}{3}\cos(-30^{\circ})=10$ N。对 $B$ 沿斜面列平衡：$T_0+f_B=mg\sin30^{\circ}=15$ N，故 $f_B=5$ N，方向沿斜面向上。选项 A 正确。",
    basis: "斜面上物体的平衡与静摩擦力方向判断", t0: 3.0, t1: 4.5 },

  { q: 1, title: "$OA$ 水平时判断 $T$ 与地面对 $C$ 的支持力（选项 B、C）",
    tex: "T_{90^{\circ}} = \frac{10\sqrt{3}}{3}\,\mathrm{N},\qquad N_C = 70-\frac{5\sqrt{3}}{3}\,\mathrm{N}",
    note: "$\varphi=90^{\circ}$ 时 $T=\dfrac{20\sqrt{3}}{3}\cos60^{\circ}=\dfrac{10\sqrt{3}}{3}$ N，故选项 B 的 $\dfrac{5\sqrt{3}}{3}$ N 错误。此时 $f_B=15-T=15-\dfrac{10\sqrt{3}}{3}$ N。对 $C$ 竖直方向：$N_C=Mg+N_B\cos30^{\circ}+f_B\sin30^{\circ}=40+\dfrac{45}{2}+\dfrac{15}{2}-\dfrac{5\sqrt{3}}{3}=70-\dfrac{5\sqrt{3}}{3}$ N。选项 C 正确。",
    basis: "整体法与隔离法（斜面体 $C$ 的竖直方向平衡）", t0: 4.5, t1: 6.0 },

  { q: 1, title: "张力最大值与最终结论（选项 D）",
    tex: "T_{\max}=\frac{20\sqrt{3}}{3}\,\mathrm{N}\quad(\varphi=30^{\circ})",
    note: "$\cos(\varphi-30^{\circ})$ 在 $\varphi=30^{\circ}$ 时取最大值 $1$，故 $T_{\max}=\dfrac{20\sqrt{3}}{3}$ N，远小于选项 D 的 $110\sqrt{3}$ N，D 错误。综上，正确选项为 A、C。",
    basis: "余弦函数在闭区间上的极值", t0: 6.0, t1: 7.5 }
];'''

src = re.sub(r"const STEPS = \[[\s\S]*?\n\];", lambda m: steps, src, count=1)

# ---------------- ③ VIEW / SIM ----------------
src = re.sub(r"const VIEW = \{[^\n]*\};\nconst SIM[^\n]*\};",
             lambda m: "const VIEW = { xmin: -0.6, xmax: 3.2, ymin: -0.6, ymax: 1.8 };\nconst SIM  = { duration: 7 };",
             src, count=1)

# ---------------- ④ GLOBALS ----------------
globals_code = r'''/* 几何与物理参数（长度以米为单位，力以 N 为单位） */
const M_C = 4.0;      // 斜面体 C 质量，kg
const M_B = 3.0;      // 物块 B 质量，kg
const M_A = 1.0;      // 物块 A 质量，kg
const G   = 10.0;     // 重力加速度，m/s²
const THETA = 30 * Math.PI / 180; // 斜面倾角
const XB  = 1.8;      // 斜面底边水平长度
const HW  = XB * Math.tan(THETA); // 斜面高度（精确 30°）
const SB  = 0.7;      // B 沿斜面距底端距离
const DO  = 1.2;      // B 到滑轮 O 的绳长
const L_OA = 0.7;     // 绳 OA 长度
const KF  = 0.035;    // 力矢量比例尺（世界长度 / N）

// 固定几何点
const Bx0 = SB * Math.cos(THETA), By0 = SB * Math.sin(THETA);
const Ox = Bx0 + DO * Math.cos(THETA), Oy = By0 + DO * Math.sin(THETA);

function stateAt(t){
  const p = Math.min(Math.max(t / SIM.duration, 0), 1);
  const phi = p * Math.PI / 2;                 // φ: 0 → 90°
  const T = (20 * Math.sqrt(3) / 3) * Math.cos(phi - Math.PI/6); // 绳张力
  const F = (T * Math.sin(phi)) / Math.cos(phi - Math.PI/6);     // 拉力 F
  const fB = M_B * G * Math.sin(THETA) - T;    // B 所受静摩擦（沿斜面向上）
  const NB = M_B * G * Math.cos(THETA);        // 斜面对 B 的支持力
  const NC = M_C * G + NB * Math.cos(THETA) + fB * Math.sin(THETA); // 地面对 C 支持力
  const Ax = Ox + L_OA * Math.sin(phi), Ay = Oy - L_OA * Math.cos(phi);
  return { p:p, phi:phi, deg:phi*180/Math.PI, T:T, F:F, fB:fB, NB:NB, NC:NC, Ax:Ax, Ay:Ay };
}

// 预计算 A 的轨迹点（圆弧），用于轨迹追踪
window.traj = [];
for (let i = 0; i <= 60; i++){
  const ph = (i / 60) * Math.PI / 2;
  window.traj.push([Ox + L_OA * Math.sin(ph), Oy - L_OA * Math.cos(ph)]);
}'''
src = src.replace("/*__GLOBALS__*/", globals_code, 1)

# ---------------- ⑤ SETUP ----------------
src = src.replace("/*__SETUP__*/",
                  "// 轨迹点已在全局预计算为 window.traj，无需额外初始化", 1)

# ---------------- ⑥ DRAWFRAME ----------------
draw_code = r'''  const st = stateAt(t);
  const phi = st.phi, deg = st.deg;

  clearBg();
  FIG.ground(-0.5, 3.0, 0, {});

  /* 坐标系 */
  FIG.coord(-0.4, 2.6, -0.4, 1.6, { labels: ['x', 'y'], color: '#94a3b8' });

  /* 斜面体 C（三角形） */
  FIG.incline(0, XB, 0, HW, 0, { fill: '#e2e8f0', hatch: true, color: '#1f2937' });
  FIG.text(XB - 0.12, 0.18, "C", { size: 15, color: '#0f172a' });

  /* 物块 B：随斜面旋转的矩形 */
  ctx.save();
  const [bsx, bsy] = W2S(Bx0, By0);
  ctx.translate(bsx, bsy);
  ctx.rotate(-THETA); // 画布坐标 y 向下，故取负
  const wb = 0.35 * scale, hb = 0.22 * scale;
  ctx.fillStyle = '#f1f5f9'; ctx.strokeStyle = '#1f2937'; ctx.lineWidth = 1.8;
  ctx.fillRect(-wb/2, -hb/2, wb, hb); ctx.strokeRect(-wb/2, -hb/2, wb, hb);
  ctx.fillStyle = '#0f172a'; ctx.font = 'italic bold 14px serif'; ctx.textAlign = 'center';
  ctx.fillText("B", 0, 5); ctx.textAlign = 'left';
  ctx.restore();

  /* 轨迹：A 的圆弧路径（浅灰虚线） */
  ctx.save(); ctx.strokeStyle = '#94a3b8'; ctx.lineWidth = 1.6; ctx.setLineDash([6, 5]);
  ctx.beginPath();
  window.traj.forEach(function(pt, i){ const s = W2S(pt[0], pt[1]); i ? ctx.lineTo(s[0], s[1]) : ctx.moveTo(s[0], s[1]); });
  ctx.stroke(); ctx.restore();

  /* 滑轮 O */
  FIG.pulley(Ox, Oy, 0.09, {});
  FIG.text(Ox + 0.08, Oy + 0.10, "O", { size: 15 });

  /* 绳：B → O → A */
  drawLine(Bx0, By0, Ox, Oy, '#475569', 1.6);
  drawLine(Ox, Oy, st.Ax, st.Ay, '#475569', 1.6);

  /* 物块 A */
  FIG.block(st.Ax, st.Ay, 0.26, 0.26, "A", { fill: '#f8fafc', border: '#1f2937', lw: 1.8 });

  /* 120° 角弧（F 与 OA 之间） */
  const angOA = 90 + deg; // OA 方向（A→O）在世界坐标中的角度
  const angF  = deg - 30; // F 方向
  FIG.angleArc(st.Ax, st.Ay, 0.28, Math.min(angOA, angF), Math.max(angOA, angF), "120°", { color: '#7c3aed' });

  /* A 上的力矢量 */
  FIG.vec(st.Ax, st.Ay, -st.T * KF * Math.sin(phi), st.T * KF * Math.cos(phi), "T", { color: '#2563eb', lw: 2.6, head: 9 });
  FIG.vec(st.Ax, st.Ay, st.F * KF * Math.cos(phi - Math.PI/6), st.F * KF * Math.sin(phi - Math.PI/6), "F", { color: '#dc2626', lw: 2.8, head: 9 });
  FIG.vec(st.Ax, st.Ay, 0, -M_A * G * KF, "m_A g", { color: '#059669', lw: 2.4, head: 9 });

  /* B 上的力矢量 */
  FIG.vec(Bx0, By0, st.T * KF * Math.cos(THETA), st.T * KF * Math.sin(THETA), "T", { color: '#2563eb', lw: 2.4, head: 9 });
  FIG.vec(Bx0, By0, -st.fB * KF * Math.sin(THETA), st.fB * KF * Math.cos(THETA), "N", { color: '#7c2d12', lw: 2.2, head: 9 });
  FIG.vec(Bx0, By0, st.fB * KF * Math.cos(THETA), st.fB * KF * Math.sin(THETA), "f", { color: '#d97706', lw: 2.4, head: 9 });
  FIG.vec(Bx0, By0, 0, -M_B * G * KF, "mg", { color: '#059669', lw: 2.4, head: 9 });

  /* 斜面角标注 */
  FIG.angleArc(0, 0, 0.42, 0, 30, "30°", { color: '#0f172a' });

  /* 实时角度与阶段显示器 */
  ctx.fillStyle = '#0f172a'; ctx.font = '12.5px sans-serif'; ctx.textAlign = 'right';
  ctx.fillText('\u03c6(t) = ' + deg.toFixed(1) + '\u00b0 = ' + phi.toFixed(3) + ' rad', W - 10, 18);
  ctx.textAlign = 'left';'''
src = src.replace("/*__DRAWFRAME__*/", draw_code, 1)

# ---------------- ⑦ READOUTS ----------------
readouts_code = r'''  const st = stateAt(t);
  return [
    ["$\\varphi(t)$", st.deg.toFixed(1), "\u00b0"],
    ["$\\varphi(t)$", st.phi.toFixed(3), "rad"],
    ["$T$", st.T.toFixed(2), "N"],
    ["$F$", st.F.toFixed(2), "N"],
    ["$f_B$", st.fB.toFixed(2), "N"],
    ["$N_B$", st.NB.toFixed(2), "N"],
    ["$N_C$", st.NC.toFixed(2), "N"]
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
