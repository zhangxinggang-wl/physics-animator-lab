# -*- coding: utf-8 -*-
"""
生成《用位移传感器测小车速度》教学动画 HTML。
题源：红外线 + 超声波双脉冲测距（例 3）。
答案：(1) x1 = v0*t1  (2) Δx = v0*(t2-t1)，v = v0*(t2-t1)/Δt
做法：复制 assets/template.html，填充 6 个区域（PROBLEM / STEPS / VIEW+SIM / setup / drawSceneBody / readouts）。

版面预算（关键）：动画栏在 1280/1366/1600/1920 下画布 CSS 宽仅约 397/423/494/590 px，
画布高 = 0.66×宽（由框架 resize 固定），竖向空间很紧。
故画布内所有 HUD 一律用「占 H 的比例」定位（不写死像素），世界视图的 ymin/ymax 按
「上方 0.115H~0.39H 让给信息带」反算，保证 4 个宽度下都不出现叠压。
"""
import io, os, re, sys

BASE = r"C:\Users\19368\Desktop\physics-animator-lab"
TPL = os.path.join(BASE, "assets", "template.html")
OUT = os.path.join(BASE, "2026-09-22_位移传感器测小车速度_教学动画.html")

# ---------------------------------------------------------------- ① PROBLEM
PROBLEM = r'''const PROBLEM = {
  title: "",   // 原题无标题（仅有题号【例 3】），故不另拟标题
  /* 题干：与原题逐字一致 */
  given: "【例 3】如图所示是用位移传感器测小车速度的示意图，这个系统由在同一直线上且等高的 A、B 两个小盒组成，A 盒装有红外线发射器和超声波发射器，B 盒装有红外线接收器和超声波接收器，A 盒被固定在向右匀速运动的小车上，某次测量时 A 向 B 同时发射一个红外线脉冲和一个超声波脉冲，B 盒接收到红外线脉冲时开始计时，接收到超声波脉冲时停止计时，若两者的时间差为 \\(t_1\\)，空气中的声速为 \\(v_0\\)（红外线的传播时间可以忽略）。",

  /* 题图：方式② Canvas 2D 像素级重绘 + 与右栏动画孪生锁定
     （左栏题图 = drawSceneBody(0)，即右栏动画第 0 帧，几何零偏差） */
  images: [
    { src: "__CANVAS_STATIC__", caption: "题图：用位移传感器测小车速度的示意图（左栏为动画第 0 帧）", pos: "bottom" }
  ],

  options: [],

  asks: [
    "（1）求 A 第一次发射脉冲时，A 与 B 之间的距离 \\(x_1\\)；",
    "（2）经过 \\(\\Delta t\\) 时间后，A 再次同时发射一个红外线脉冲和一个超声波脉冲，此次 B 接收的时间差为 \\(t_2\\)，求 A 两次发射过程中，小车运动的距离和小车的速度。"
  ],

  knowledgePoints: [
    { id: "wave-mechanical-basics" },
    { id: "princ-modeling" },
    { id: "princ-relative-motion" }
  ]
};

'''

# ---------------------------------------------------------------- ② STEPS
STEPS = r'''const STEPS = [
  {
    q: 1,
    title: "计时原理：红外线瞬时到达，B 的计时起点就是 A 的发射时刻",
    tex: "t_{\\text{红外}} = \\frac{x}{c} \\approx 0",
    note: "红外线是电磁波，在空气中传播的速度约 $c = 3\\times10^{8}$ m/s。本题装置上 A、B 之间只有几米，红外线飞过这段距离只需 $x/c \\sim 10^{-8}$ s，比超声波的飞行时间（毫秒量级）小 5 个数量级以上，因此**红外线的传播时间可视为零**——B 盒一接收到红外线脉冲，就相当于立刻收到了 A 的发射信号。于是：B 开始计时的时刻 $\\approx$ A 发射脉冲的时刻；B 停止计时（收到超声波）与开始计时的时刻之差 $t_1$，就是**超声波在空气中的飞行时间**。这正是这套装置能够测距的关键前提。",
    basis: "电磁波与机械波的传播速度差异；理想化模型（红外线传播时间忽略不计）",
    t0: 0.00, t1: 0.45
  },
  {
    q: 1,
    title: "超声波在静止空气中匀速传播，A 与 B 的距离 x₁ = v₀t₁",
    tex: "x_{1} = v_{0} t_{1}",
    note: "超声波是机械波，它在空气中以速度 $v_0$ 匀速传播，而 $v_0$ 只由介质（空气）决定。设第一次发射时 A 与 B 的距离为 $x_1$，则这段声波从发射点飞到 B 用时 $t_1 = \\frac{x_1}{v_0}$，反解即得 $x_1 = v_0 t_1$，这就是第（1）问的答案。**易错点**：声波发出的一瞬间，发射点就已被「留在」空气中，此后声波以介质为参考系传播；A 盒虽然继续向右运动，也不会改变这段声波的飞行时间——运动的是波源，不是声波赖以传播的介质。取 $v_0 = 340$ m/s、$t_1 = 5.00$ ms 时 $x_1 = 1.70$ m。",
    basis: "机械波在均匀介质中匀速传播 $s = vt$；波速由介质决定、与波源是否运动无关",
    t0: 0.45, t1: 0.90
  },
  {
    q: 2,
    title: "经过 Δt 时间，A 前进到 Q 点再次发射，第二次测得 t₂ ⇒ x₂ = v₀t₂",
    tex: "x_{2} = v_{0} t_{2}",
    note: "两次发射相隔 $\\Delta t$，第二次发射时 A 已位于 Q 点，与 B 的距离为 $x_2$。测距原理与第一次完全相同，B 记下的时间差 $t_2$ 就是这段声波的飞行时间，所以 $x_2 = v_0 t_2$。**另一个关键点**：红外线②同样是瞬时到达 B 的，因此 B 盒记下的两次「开始计时」时刻之差，就等于两次发射的时间间隔 $\\Delta t$——这正是题目中 $\\Delta t$ 可以直接使用的理由。取 $t_2 = 7.50$ ms 时 $x_2 = 2.55$ m。",
    basis: "同一测距原理的第二次应用；红外线瞬时到达使「发射间隔 = 计时起点间隔」",
    t0: 0.90, t1: 2.90
  },
  {
    q: 2,
    title: "两次发射之间小车的位移 Δx = x₂ − x₁",
    tex: "\\Delta x = x_{2} - x_{1} = v_{0}\\,(t_{2} - t_{1})",
    note: "第一次发射时 A 在 P 点、距 B 为 $x_1$；第二次发射时 A 在 Q 点、距 B 为 $x_2$。因为 A 始终在同一条直线上向右运动，两次发射之间小车前进的距离就等于这两个距离之差：$\\Delta x = x_2 - x_1$，代入 $x_1 = v_0t_1$、$x_2 = v_0t_2$ 得 $\\Delta x = v_0(t_2 - t_1)$，这是第（2）问的第一个答案。取 $t_1 = 5.00$ ms、$t_2 = 7.50$ ms：$\\Delta x = 340\\times(7.50-5.00)\\times10^{-3} \\approx 0.85$ m。",
    basis: "同一直线上位置坐标之差即位移；$x_1 = v_0t_1$ 与 $x_2 = v_0t_2$ 的几何关系",
    t0: 2.90, t1: 3.80
  },
  {
    q: 2,
    title: "小车做匀速直线运动的速度 v = Δx / Δt",
    tex: "v = \\frac{\\Delta x}{\\Delta t} = \\frac{v_{0}\\,(t_{2} - t_{1})}{\\Delta t}",
    note: "两次发射的时间间隔为 $\\Delta t$，这段时间内小车的位移为 $\\Delta x$，由匀速直线运动的定义 $v = \\frac{\\Delta x}{\\Delta t}$ 即得 $v = \\frac{v_0(t_2-t_1)}{\\Delta t}$，这是第（2）问的第二个答案。**结果的意义**：只要测出两个时间差 $t_1$、$t_2$ 与发射间隔 $\\Delta t$，并已知声速 $v_0$，就能算出小车速度——表达式里不含 $x_1$、$x_2$ 本身，也就是说**不需要知道 A、B 的绝对位置**。取 $v_0 = 340$ m/s、$\\Delta t = 1.250$ s 时 $v = \\frac{0.850}{1.250} = 0.68$ m/s。",
    basis: "匀速直线运动 $v = \\frac{\\Delta x}{\\Delta t}$；消去中间量的思想",
    t0: 3.80, t1: 4.60
  }
];

'''

# ---------------------------------------------------------------- ③ VIEW / SIM
VIEWSIM = r'''const VIEW = { xmin: -1.05, xmax: 3.00, ymin: -0.61, ymax: 1.8208 };
const SIM  = { duration: 4.60 };
/* 说明：世界纵横比取 4.05 : 2.4308（= 4.05 × 0.60），扣除四周 36px 内边距后与画布像素
   纵横比一致（实测 1280~1920 视口下动画栏画布宽仅 395~590px，该比值在 0.597~0.61 之间），
   使 x、y 方向比例尺相等——小车车轮是正圆、超声波圆波前不失真。
   画布高 = 0.66×画布宽，竖向很紧：上方 0.115H～0.39H 固定留给「B 端接收信号时间关系」
   信息带（纯像素坐标、不占世界视图），故 ymax 取到 1.82 让场景上方留出这段空白。 */

'''

# ---------------------------------------------------------------- ④ GLOBALS（含全部绘图函数，必须位于顶层）
GLOBALS = r'''/* ===== 本题物理常量与几何参数 =====
   世界坐标：x 向右、y 向上，地面取 y = 0，长度单位 m。
   物理量：声速 v₀ = 340 m/s；两次测量的时间差 t₁ = 5.00 ms、t₂ = 7.50 ms；两次发射间隔 Δt = 1.250 s。
   由此：x₁ = v₀t₁ = 1.700 m，x₂ = v₀t₂ = 2.550 m，Δx = 0.850 m，
         小车速度 v = Δx/Δt = 0.680 m/s = v₀(t₂-t₁)/Δt（两式互相校验，一致）。 */
const V0     = 340;               // 空气中的声速 v₀ (m/s)
const T1     = 5.00e-3;           // 第①次测量的时间差 t₁ (s)
const T2     = 7.50e-3;           // 第②次测量的时间差 t₂ (s)
const X1     = V0 * T1;           // 第一次发射时 A、B 的距离 x₁ = 1.700 m
const X2     = V0 * T2;           // 第二次发射时 A、B 的距离 x₂ = 2.550 m
const DX     = X2 - X1;           // 两次发射之间小车的位移 Δx = 0.850 m
const DT     = 1.25;              // 两次发射的时间间隔 Δt (s)
const VCART  = DX / DT;           // 小车速度 v = Δx/Δt = 0.680 m/s

/* 装置几何（世界坐标，m） */
const X_B    = 0;                                   // B 盒右表面（接收面）在 x = 0
const BOX_W  = 0.34, BOX_H = 0.28, BOX_Y0 = 0.26;   // 小盒宽 / 高 / 底面高度（A、B 等高）
const AXIS_H = BOX_Y0 + BOX_H / 2;                  // 两盒中心高度 0.40 m
const IR_Y   = 0.47;                                // 红外线示意高度（盒面偏上）
const US_Y   = 0.33;                                // 超声波波束轴线高度（盒面偏下）
const WHEEL_R = 0.09;                               // 小车车轮半径
const Y_DIM1 = 0.66;                                // x₁ / Δx 尺寸线高度
const Y_DIM2 = 0.80;                                // x₂ 尺寸线高度
/* HUD 竖向比例（占画布高 H 的比例）：信息带上沿 / 下沿 */
const BAND_B0 = 0.115, BAND_B1 = 0.39;

/* ===== 演示时间轴分段：动画秒 → 真实秒(τ) =====
   声波飞行只有毫秒量级，若与 Δt 段同速率，波前会一闪而过；故按段线性映射：
   声波飞行段慢放、小车前进段近似 1:1，逐段在画面信息带中标出。 */
const SEGS = [
  { t0: 0.00, t1: 0.90, r0: 0.0,     r1: T1,      name: '第①次声波飞行' },
  { t0: 0.90, t1: 2.90, r0: T1,      r1: DT,      name: '小车匀速前进' },
  { t0: 2.90, t1: 3.80, r0: DT,      r1: DT + T2, name: '第②次声波飞行' },
  { t0: 3.80, t1: 4.60, r0: DT + T2, r1: DT + T2, name: '结论定格' }
];
function segOf(t){
  for (let i = SEGS.length - 1; i >= 0; i--){ if (t >= SEGS[i].t0 - 1e-9) return i; }
  return 0;
}
function realTime(t){
  const s = SEGS[segOf(t)];
  const span = s.t1 - s.t0;
  const u = span > 1e-9 ? Math.min(1, Math.max(0, (t - s.t0) / span)) : 1;
  return s.r0 + (s.r1 - s.r0) * u;
}

/* 运动状态：画面（drawSceneBody）与数据面板（readouts）共用同一函数，
   从机制上保证「画面一套数、面板另一套数」不可能发生。 */
function stateAt(t){
  const tt  = Math.min(t, SIM.duration);
  const tau = realTime(tt);                                // 真实时刻 τ（s），以第一次发射为零点
  const xA  = X1 + VCART * tau;                            // A 盒发射面位置（匀速右移）
  return {
    tt: tt, tau: tau, xA: xA,
    r1: V0 * Math.min(tau, T1),                            // 第①次超声波波前半径
    r2: V0 * Math.max(0, Math.min(tau - DT, T2)),          // 第②次超声波波前半径
    dx: xA - X1,                                           // 相对 x₁ 的位移进度
    ir1: Math.max(0, 1 - tt / 0.26),                       // 红外线① 闪光强度（瞬时到达）
    ir2: Math.max(0, 1 - (tt - SEGS[2].t0) / 0.26),        // 红外线② 闪光强度
    phase: tau < T1 ? 0 : (tau < DT ? 1 : (tau < DT + T2 ? 2 : 3))
  };
}

/* ===== 绘图小工具（世界坐标 → 屏幕坐标，统一走 W2S） ===== */
function poly2(pts, color, w, dash){
  ctx.save();
  ctx.strokeStyle = color; ctx.lineWidth = w;
  if (dash) ctx.setLineDash(dash);
  ctx.beginPath();
  for (let i = 0; i < pts.length; i++){
    const p = W2S(pts[i][0], pts[i][1]);
    if (i) ctx.lineTo(p[0], p[1]); else ctx.moveTo(p[0], p[1]);
  }
  ctx.stroke();
  ctx.restore();
}
/* 画布标签：canvas 不渲染 LaTeX，字母下标一律用 Unicode 下标字符（x₁ / v₀ / t₂） */
function tag(x, y, str, color, size, align, plate){
  const p = W2S(x, y);
  ctx.save();
  ctx.font = 'bold ' + (size || 12) + 'px "Microsoft YaHei","PingFang SC",sans-serif';
  ctx.textAlign = align || 'left';
  if (plate){
    const tw = ctx.measureText(str).width;
    let bx = p[0] - 3;
    if (ctx.textAlign === 'center') bx = p[0] - tw / 2 - 3;
    else if (ctx.textAlign === 'right') bx = p[0] - tw - 3;
    ctx.fillStyle = 'rgba(255,255,255,0.95)';
    ctx.fillRect(bx, p[1] - (size || 12), tw + 6, (size || 12) + 7);
  }
  ctx.fillStyle = color;
  ctx.fillText(str, p[0], p[1]);
  ctx.restore();
}
function rrect(x, y, w, h, r){
  ctx.beginPath();
  ctx.moveTo(x + r, y);
  ctx.arcTo(x + w, y, x + w, y + h, r);
  ctx.arcTo(x + w, y + h, x, y + h, r);
  ctx.arcTo(x, y + h, x, y, r);
  ctx.arcTo(x, y, x + w, y, r);
  ctx.closePath();
}
function arrowHead(x1, y1, x2, y2, color, size){
  const s = size || 7, ang = Math.atan2(y2 - y1, x2 - x1);
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.moveTo(x2, y2);
  ctx.lineTo(x2 - s * Math.cos(ang - 0.38), y2 - s * Math.sin(ang - 0.38));
  ctx.lineTo(x2 - s * Math.cos(ang + 0.38), y2 - s * Math.sin(ang + 0.38));
  ctx.closePath(); ctx.fill();
}
/* 尺寸线（双箭头 + 两端界线 + 压线白底标签）；labelAtX 可把标签横向挪开以避免叠字 */
function dimLine(x1, x2, y, label, color, lw, labelAtX){
  const a = W2S(x1, y), b = W2S(x2, y);
  ctx.save();
  ctx.strokeStyle = color; ctx.lineWidth = lw || 1.3;
  ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.lineTo(b[0], b[1]); ctx.stroke();
  arrowHead(a[0], a[1], b[0], b[1], color);
  arrowHead(b[0], b[1], a[0], a[1], color);
  const t = 7;
  ctx.beginPath();
  ctx.moveTo(a[0], a[1] - t); ctx.lineTo(a[0], a[1] + t);
  ctx.moveTo(b[0], b[1] - t); ctx.lineTo(b[0], b[1] + t);
  ctx.stroke();
  ctx.font = 'bold 12px "Microsoft YaHei","PingFang SC",sans-serif';
  const tw = ctx.measureText(label).width;
  const mx = W2S(labelAtX != null ? labelAtX : (x1 + x2) / 2, y)[0], my = a[1];
  ctx.fillStyle = 'rgba(255,255,255,0.95)';
  ctx.fillRect(mx - tw / 2 - 4, my - 8, tw + 8, 16);
  ctx.fillStyle = color; ctx.textAlign = 'center';
  ctx.fillText(label, mx, my + 4);
  ctx.restore();
}
/* 小盒：实线或虚线矩形 + 居中字母 */
function boxRect(cx, cy, w, h, label, color, dashed, fill){
  const p1 = W2S(cx - w / 2, cy + h / 2), p2 = W2S(cx + w / 2, cy - h / 2);
  ctx.save();
  if (fill){ ctx.fillStyle = fill; ctx.fillRect(p1[0], p1[1], p2[0] - p1[0], p2[1] - p1[1]); }
  if (dashed) ctx.setLineDash([6, 5]);
  ctx.strokeStyle = color; ctx.lineWidth = dashed ? 1.4 : 2.0;
  ctx.strokeRect(p1[0], p1[1], p2[0] - p1[0], p2[1] - p1[1]);
  ctx.setLineDash([]);
  if (label){
    const c = W2S(cx, cy);
    ctx.fillStyle = color; ctx.font = 'italic bold 15px serif';
    ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.fillText(label, c[0], c[1] + 1);
    ctx.textAlign = 'left'; ctx.textBaseline = 'alphabetic';
  }
  ctx.restore();
}
/* 发射 / 接收器件小圆点：红 = 红外线，蓝 = 超声波 */
function nub(x, y, color){
  const p = W2S(x, y);
  ctx.save();
  ctx.beginPath(); ctx.arc(p[0], p[1], 3.6, 0, 7);
  ctx.fillStyle = color; ctx.fill();
  ctx.strokeStyle = '#fff'; ctx.lineWidth = 1; ctx.stroke();
  ctx.restore();
}

/* ===== 装置：B 盒（固定，接计算机） ===== */
function drawBUnit(){
  const a = W2S(-0.46, 0), b = W2S(0.06, BOX_Y0);      // 支架：把 B 盒架到与 A 盒等高
  ctx.save();
  ctx.fillStyle = '#e5e7eb'; ctx.fillRect(a[0], b[1], b[0] - a[0], a[1] - b[1]);
  ctx.strokeStyle = '#94a3b8'; ctx.lineWidth = 1.1;
  ctx.strokeRect(a[0], b[1], b[0] - a[0], a[1] - b[1]);
  ctx.restore();
  poly2([[-1.00, IR_Y + 0.05], [-0.42, IR_Y + 0.05], [-0.30, AXIS_H]], '#64748b', 1.6);  // 导线
  tag(-1.02, IR_Y + 0.13, '连接到计算机', '#475569', 11);
  boxRect(-0.17, AXIS_H, BOX_W, BOX_H, 'B', '#1f2937', false, '#f1f5f9');
  nub(X_B, IR_Y, '#dc2626');
  nub(X_B, US_Y, '#2563eb');
}
/* ===== 装置：小车 A（ghost = Q 处虚线残影，对应原题图中的虚线 A） ===== */
function drawCart(x, ghost){
  const col = ghost ? '#94a3b8' : '#1f2937';
  ctx.save();
  if (ghost) ctx.setLineDash([6, 5]);
  const d1 = W2S(x - 0.10, 0.18), d2 = W2S(x + 0.44, BOX_Y0);
  ctx.strokeStyle = col; ctx.lineWidth = ghost ? 1.4 : 2.0;
  ctx.strokeRect(d1[0], d1[1], d2[0] - d1[0], d2[1] - d1[1]);
  const rot = x / WHEEL_R;                              // 纯滚动：车轮转角 = 位移 / 半径
  [x + 0.02, x + 0.32].forEach(function(wx){
    const c = W2S(wx, WHEEL_R);
    ctx.beginPath(); ctx.arc(c[0], c[1], WHEEL_R * scale, 0, 7); ctx.stroke();
    if (!ghost){
      ctx.lineWidth = 1;
      for (let k = 0; k < 4; k++){
        const an = rot + k * Math.PI / 4;
        ctx.beginPath();
        ctx.moveTo(c[0] - WHEEL_R * 0.82 * scale * Math.cos(an), c[1] + WHEEL_R * 0.82 * scale * Math.sin(an));
        ctx.lineTo(c[0] + WHEEL_R * 0.82 * scale * Math.cos(an), c[1] - WHEEL_R * 0.82 * scale * Math.sin(an));
        ctx.stroke();
      }
    }
  });
  ctx.restore();
  boxRect(x + BOX_W / 2, AXIS_H, BOX_W, BOX_H, 'A', col, ghost, ghost ? null : '#f1f5f9');
  if (!ghost){ nub(x, IR_Y, '#dc2626'); nub(x, US_Y, '#2563eb'); }
}
/* ===== 超声波脉冲：以发射点为圆心向 B 扩散的球面波前（3 条波前构成波包） ===== */
function drawWave(cx, r, color, alpha){
  if (r <= 0.02 || alpha <= 0.01) return;
  ctx.save();
  /* 只画在「空气」区域：信息带下沿之上、地面之上（台面挡住下方，其余为画面边界） */
  const yTop = BAND_B1 * H, yBot = W2S(0, 0)[1] + 2;
  ctx.beginPath(); ctx.rect(0, yTop, W, Math.max(0, yBot - yTop)); ctx.clip();
  const half = 26 * Math.PI / 180, n = 30;
  for (let k = 0; k < 3; k++){
    const rr = r - k * 0.085;
    if (rr <= 0.02) continue;
    ctx.globalAlpha = alpha * (k === 0 ? 0.95 : (k === 1 ? 0.5 : 0.26));
    ctx.strokeStyle = color; ctx.lineWidth = k === 0 ? 2.4 : 1.6;
    ctx.beginPath();
    for (let i = 0; i <= n; i++){
      const a = Math.PI - half + 2 * half * i / n;
      const p = W2S(cx + rr * Math.cos(a), US_Y + rr * Math.sin(a));
      if (i) ctx.lineTo(p[0], p[1]); else ctx.moveTo(p[0], p[1]);
    }
    ctx.stroke();
  }
  /* 波束边界（细虚线）：只在发射点附近画一小段「定向波束」示意。
     长度封顶 0.42 m 且必须随波前一起「长出去」——若直接用固定长度朝 B 方向拉，
     小车驶远后这段斜虚线会横穿整个场景、压住地面附近的速度矢量 v，看起来像工程辅助线。
     故改为：长度取 min(r*0.55, 0.30)，即只在波包附近画一小段锥角示意，随波前同步前移。 */
  const lb = Math.min(r * 0.55, 0.30);
  ctx.globalAlpha = alpha * 0.42;
  ctx.strokeStyle = color; ctx.lineWidth = 1; ctx.setLineDash([4, 4]);
  const c0 = W2S(cx, US_Y);
  [-1, 1].forEach(function(sgn){
    const p = W2S(cx - lb * Math.cos(half), US_Y + sgn * lb * Math.sin(half));
    ctx.beginPath(); ctx.moveTo(c0[0], c0[1]); ctx.lineTo(p[0], p[1]); ctx.stroke();
  });
  ctx.setLineDash([]);
  ctx.restore();
}
/* ===== 红外线脉冲：瞬时到达（红色虚线 + 指向 B 的箭头） ===== */
function drawIR(st){
  function one(xFrom, alpha){
    if (alpha <= 0.01) return;
    ctx.save();
    ctx.globalAlpha = Math.min(1, alpha);
    ctx.strokeStyle = '#dc2626'; ctx.lineWidth = 2; ctx.setLineDash([7, 5]);
    const a = W2S(0, IR_Y), b = W2S(xFrom, IR_Y);
    ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.lineTo(b[0], b[1]); ctx.stroke();
    ctx.setLineDash([]);
    arrowHead(b[0], b[1], a[0], a[1], '#dc2626');
    ctx.restore();
  }
  one(X1, st.ir1);
  if (st.tau > DT - 1e-9) one(X2, st.ir2);
}

/* ===== 画布 HUD（纯像素坐标，一律按 H 的比例定位，窄画布也不叠压） ===== */
function drawBanner(st){
  const txt = st.phase === 0 ? '第①次测量 · 超声波从 P 飞向 B（t₁ 计时中）'
            : st.phase === 1 ? '小车匀速前进 · 经过 Δt 后到达 Q 点再次发射'
            : st.phase === 2 ? '第②次测量 · 超声波从 Q 飞向 B（t₂ 计时中）'
            : '结论 · Δx = x₂ − x₁ = v₀(t₂ − t₁)';
  const bg  = st.phase === 1 ? 'rgba(13,148,136,0.94)'
            : st.phase === 3 ? 'rgba(234,88,12,0.94)' : 'rgba(37,99,235,0.94)';
  ctx.save();
  ctx.font = 'bold 12px "Microsoft YaHei","PingFang SC",sans-serif';
  const tw = ctx.measureText(txt).width, bh = 22, bw = tw + 24;
  const bx = (W - bw) / 2, by = 4;
  rrect(bx, by, bw, bh, 11);
  ctx.fillStyle = bg; ctx.fill();
  ctx.fillStyle = '#fff'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  ctx.fillText(txt, W / 2, by + bh / 2 + 1);
  ctx.textAlign = 'left'; ctx.textBaseline = 'alphabetic';
  ctx.restore();
}
/* 像素坐标双箭头；below=true 时标签放到线的下方（短箭头 t₁/t₂ 用，
   否则标签白底会把箭头整条盖住），false 时标签压在线上（长箭头 Δt 用） */
function pxArrow(x1, x2, y, color, label, below){
  ctx.save();
  ctx.strokeStyle = color; ctx.lineWidth = 1.2;
  ctx.beginPath(); ctx.moveTo(x1, y); ctx.lineTo(x2, y); ctx.stroke();
  arrowHead(x2, y, x1, y, color, 6);
  arrowHead(x1, y, x2, y, color, 6);
  ctx.font = 'bold 10px "Microsoft YaHei","PingFang SC",sans-serif';
  const mx = (x1 + x2) / 2;
  if (label && below){
    ctx.fillStyle = color; ctx.textAlign = 'center';
    ctx.fillText(label, mx, y + 12);
  } else if (label){
    const tw = ctx.measureText(label).width;
    ctx.fillStyle = 'rgba(255,255,255,0.96)';
    ctx.fillRect(mx - tw / 2 - 4, y - 7, tw + 8, 14);
    ctx.fillStyle = color; ctx.textAlign = 'center';
    ctx.fillText(label, mx, y + 4);
  }
  ctx.textAlign = 'left';
  ctx.restore();
}
/* 「B 端接收信号时间关系」信息带：4 个时刻 + t₁ / Δt / t₂ 三段（示意，非等比） */
function drawTimeBand(st){
  const b0 = BAND_B0 * H, bh = (BAND_B1 - BAND_B0) * H, bx0 = 12, bx1 = W - 12;
  ctx.save();
  rrect(bx0, b0, bx1 - bx0, bh, 8);
  ctx.fillStyle = '#f8fafc'; ctx.fill();
  ctx.strokeStyle = '#e2e8f0'; ctx.lineWidth = 1; ctx.stroke();

  const rowT = b0 + bh * 0.15, rowD = b0 + bh * 0.34, rowA = b0 + bh * 0.59, rowU = b0 + bh * 0.74;

  /* 标题（左） */
  ctx.fillStyle = '#475569';
  ctx.font = 'bold 11px "Microsoft YaHei","PingFang SC",sans-serif';
  ctx.fillText('B 端接收信号的时间关系', bx0 + 10, rowT + 3);

  /* B 端计时器实时状态（右，小药丸） */
  let timerTxt, timerCol;
  if (st.tau < T1){ timerTxt = '计时①中 ' + (st.tau * 1000).toFixed(2) + ' ms'; timerCol = '#dc2626'; }
  else if (st.tau < DT){ timerTxt = '① 停止 t₁ = ' + (T1 * 1000).toFixed(2) + ' ms'; timerCol = '#2563eb'; }
  else if (st.tau < DT + T2){ timerTxt = '计时②中 ' + ((st.tau - DT) * 1000).toFixed(2) + ' ms'; timerCol = '#7c3aed'; }
  else { timerTxt = '② 停止 t₂ = ' + (T2 * 1000).toFixed(2) + ' ms'; timerCol = '#7c3aed'; }
  ctx.font = 'bold 10px "Microsoft YaHei","PingFang SC",sans-serif';
  const tw = ctx.measureText(timerTxt).width;
  if (bx1 - 10 - tw - 14 > bx0 + 10 + 150){
    rrect(bx1 - 10 - tw - 14, rowT - 9, tw + 14, 15, 7);
    ctx.fillStyle = timerCol; ctx.fill();
    ctx.fillStyle = '#fff'; ctx.fillText(timerTxt, bx1 - 10 - tw - 7, rowT + 2);
  }

  /* 时间轴与 4 个时刻 */
  const x0 = bx0 + 12, x1e = bx1 - 12, mw = x1e - x0;
  const e1 = x0 + 0.055 * mw;
  const g1 = Math.min(0.075 * mw, 48);
  const e2 = e1 + g1;
  const e3 = x0 + 0.70 * mw;
  const e4 = e3 + g1 * 1.5;                       // t₂ : t₁ = 3 : 2，段长等比
  ctx.strokeStyle = '#94a3b8'; ctx.lineWidth = 1.4;
  ctx.beginPath(); ctx.moveTo(x0, rowA); ctx.lineTo(x1e, rowA); ctx.stroke();
  function tick(x, color){
    ctx.strokeStyle = color; ctx.lineWidth = 2.4;
    ctx.beginPath(); ctx.moveTo(x, rowA - 5); ctx.lineTo(x, rowA + 5); ctx.stroke();
  }
  tick(e1, '#dc2626');
  tick(e2, st.tau >= T1 - 1e-9 ? '#2563eb' : '#cbd5e1');
  tick(e3, st.tau >= DT - 1e-9 ? '#dc2626' : '#cbd5e1');
  tick(e4, st.tau >= DT + T2 - 1e-9 ? '#7c3aed' : '#cbd5e1');

  /* Δt 段：两个「红外线到达（开始计时）」时刻之间（标签压在线上） */
  if (st.tau >= DT - 1e-9) pxArrow(e1, e3, rowD, '#0f766e', 'Δt = ' + DT.toFixed(3) + ' s（两次发射间隔）', false);
  /* t₁ / t₂ 段：开始计时 → 停止计时（标签放到线下方，保证箭头可见） */
  if (st.tau >= T1 - 1e-9) pxArrow(e1, e2, rowU, '#2563eb', 't₁ = ' + (T1 * 1000).toFixed(2) + ' ms', true);
  if (st.tau >= DT + T2 - 1e-9) pxArrow(e3, e4, rowU, '#7c3aed', 't₂ = ' + (T2 * 1000).toFixed(2) + ' ms', true);
  ctx.restore();
}
/* 底部图例：按可用宽度自动折行（自底向上），窄画布也不溢出 */
function drawLegend(){
  const items = [
    ['#2563eb', '蓝弧：第①次超声波波前'],
    ['#7c3aed', '紫弧：第②次超声波波前'],
    ['#dc2626', '红虚线：红外线（瞬时到达）'],
    ['#0f766e', '绿箭头：小车速度 v（运动方向）'],
    ['#64748b', 'x₁ = v₀t₁　x₂ = v₀t₂　Δx = x₂ − x₁（声波飞行段为慢放）']
  ];
  ctx.save();
  ctx.font = '10px "Microsoft YaHei","PingFang SC",sans-serif';
  const maxW = W - 2 * PAD, lines = [];
  let cur = [], curW = 0;
  items.forEach(function(it){
    const w = ctx.measureText(it[1]).width + 12;
    if (cur.length && curW + w > maxW){ lines.push(cur); cur = []; curW = 0; }
    cur.push([it[0], it[1], w]); curW += w;
  });
  if (cur.length) lines.push(cur);
  const use = lines.slice(0, 3);                    // 自上而下按图例顺序排列：
  use.forEach(function(ln, li){                     // 第一行在最上面，最后一行贴画布底
    const y = H - 10 - (use.length - 1 - li) * 15;
    let x = PAD;
    ln.forEach(function(seg){ ctx.fillStyle = seg[0]; ctx.fillText(seg[1], x, y); x += seg[2]; });
  });
  ctx.restore();
}

'''

SETUP = r'''  /* 本题的运动学量全部可解析给出（stateAt 即解析解），无需数值积分。
     SIM.duration = 4.60 s，对应真实过程：
       0→t₁ 声波①飞行（慢放）· t₁→Δt 小车前进 · Δt→Δt+t₂ 声波②飞行（慢放）· 末段定格结论。
     世界视图与 HUD 比例（BAND_B0 / BAND_B1）均为常量，绘图按 H 的比例定位。 */
'''

DRAWFRAME = r'''  const st = stateAt(t);

  /* 地面（粗横线 + 斜线阴影）——A、B 同在一条水平线上，等高 */
  FIG.ground(VIEW.xmin + 0.05, VIEW.xmax - 0.05, 0, { gap: 0.16, hatchLen: 0.9, color: '#334155' });

  /* 第①次发射位置 P、第二次发射位置 Q 的竖直参考线（对应原题图的 P、Q） */
  poly2([[X1, 0], [X1, Y_DIM1 - 0.02]], '#94a3b8', 1.1, [5, 5]);
  if (st.tau > DT - 1e-9) poly2([[X2, 0], [X2, Y_DIM2 - 0.02]], '#94a3b8', 1.1, [5, 5]);

  /* 超声波波前（先画，被盒体遮挡的部分由后面的装置覆盖）
     第①次测量完成后把它的波前压暗，避免末态两套圆弧在 B 附近叠得太挤 */
  drawWave(X1, st.r1, '#2563eb', st.tau <= T1 + 1e-9 ? 1 : 0.42);
  drawWave(X2, st.r2, '#7c3aed', 1);

  /* 装置本体：B 盒（固定）→ Q 处虚线残影 → A 盒（匀速右移） */
  drawBUnit();
  drawCart(X2, true);
  drawCart(st.xA, false);

  /* 红外线脉冲（红色虚线，瞬时到达 B） */
  drawIR(st);

  /* 固定文字标注（白底让位，防止与波前/尺寸线叠字） */
  tag(0.10, IR_Y + 0.075, '红外线', '#dc2626', 12, 'left', true);
  tag(0.10, US_Y - 0.115, '超声波', '#2563eb', 12, 'left', true);

  /* 小车速度矢量 v（画在车后地面附近：该处永远空着，不会与尺寸线/波前/残影叠压） */
  FIG.vec(st.xA - 0.62, 0.09, 0.30, 0, 'v', { color: '#0f766e', lw: 3, head: 9 });

  /* 尺寸线：x₁（B→P）、Δx（P→Q）、x₂（B→Q）；标签横向错开，互不叠字 */
  const cX1 = st.phase <= 1 ? '#dc2626' : '#334155';
  const cDX = st.phase >= 2 ? '#ea580c' : '#64748b';
  dimLine(X_B, X1, Y_DIM1, 'x₁', cX1, st.phase <= 1 ? 1.8 : 1.3, 0.95);
  dimLine(X1, X2, Y_DIM1, 'Δx', cDX, st.phase >= 2 ? 1.8 : 1.3, 2.15);
  dimLine(X_B, X2, Y_DIM2, 'x₂', cDX, st.phase >= 2 ? 1.8 : 1.3, 1.30);
  tag(X1, Y_DIM1 - 0.045, 'P', '#475569', 11, 'center', true);
  tag(X2, Y_DIM1 - 0.045, 'Q', '#475569', 11, 'center', true);

  /* ===== 固定像素坐标 HUD：过程横幅 + 信息带 + 图例
     t=0 时不画，保证左栏题图（＝动画第 0 帧）与原题图完全一致 ===== */
  if (t > 0.002){
    drawBanner(st);
    drawTimeBand(st);
    drawLegend();
  }
'''

READOUTS = r'''  const st = stateAt(t);
  /* 读数与解析逐项对应：t₁/x₁ 按「声波已飞行的时间」增长到 t₁/x₁；
     t₂ 在第二次发射后才开始累计；x₂/Δx 取「发射瞬间」的两盒距离（不含声波飞行期
     间小车又前进的那几毫米），故末态严格等于解析给出的 x₂ = 2.550 m、Δx = 0.850 m。 */
  const t1Run = Math.min(st.tau, T1);
  const t2Run = Math.max(0, Math.min(st.tau - DT, T2));
  const x2At  = X1 + VCART * Math.min(st.tau, DT);
  return [
    ["演示时刻 $t$", st.tt.toFixed(2), "s"],
    ["真实时刻 $\\tau$", (st.tau * 1000).toFixed(1), "ms"],
    ["第①次时间差 $t_{1}$", (t1Run * 1000).toFixed(2), "ms"],
    ["第①次测距 $x_{1}=v_{0}t_{1}$", (t1Run * V0).toFixed(3), "m"],
    ["第②次时间差 $t_{2}$", (t2Run * 1000).toFixed(2), "ms"],
    ["第②次测距 $x_{2}=v_{0}t_{2}$", x2At.toFixed(3), "m"],
    ["两次发射间位移 $\\Delta x$", VCART * Math.min(st.tau, DT) > 0 ? (x2At - t1Run * V0).toFixed(3) : "0.000", "m"],
    ["小车速度 $v=\\frac{v_{0}(t_{2}-t_{1})}{\\Delta t}$", VCART.toFixed(3), "m/s"]
  ];
'''


def replace_span(s, start_anchor, end_anchor, new_text):
    i = s.find(start_anchor)
    if i < 0:
        raise SystemExit("找不到起始锚点: " + start_anchor[:40])
    j = s.find(end_anchor, i)
    if j < 0:
        raise SystemExit("找不到结束锚点: " + end_anchor[:40])
    return s[:i] + new_text + s[j:]


def main():
    with io.open(TPL, "r", encoding="utf-8") as f:
        s = f.read()

    # ① PROBLEM
    s = replace_span(s, "const PROBLEM = {", "/* 选项由 PROBLEM.options 提供", PROBLEM)
    # ② STEPS
    #   注意：模板用 innerHTML 渲染 note / basis，不支持 Markdown，
    #   写成 **加粗** 会在页面上原样显示两个星号 —— 统一转成 <b>…</b>。
    steps_src = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", STEPS)
    n_bold = len(re.findall(r"<b>", steps_src))
    s = replace_span(s, "const STEPS = [", "\n\n/* ===", steps_src)
    if n_bold == 0:
        raise SystemExit("STEPS 中未发现任何 <b> 强调，检查 ** 转换是否生效")
    print("note/basis 强调标记已转换为 <b>：%d 处" % n_bold)
    # ③ VIEW / SIM
    old_vs = "const VIEW = { xmin: -1, xmax: 11, ymin: -1, ymax: 7 };\nconst SIM  = { duration: 4 };"
    if old_vs not in s:
        raise SystemExit("VIEW/SIM 锚点未找到")
    s = s.replace(old_vs, VIEWSIM.rstrip("\n"), 1)
    # ④ 全局常量 + 全部绘图/HUD 函数（GLOBALS 在 setup() 之外，保证是顶层函数）
    s = s.replace("/*__GLOBALS__*/", GLOBALS.rstrip("\n"), 1)
    # ⑤ setup
    s = s.replace("/*__SETUP__*/", SETUP.rstrip("\n"), 1)
    # ⑥ 逐帧绘制
    s = s.replace("/*__DRAWFRAME__*/", DRAWFRAME.rstrip("\n"), 1)
    # ⑦ 实时数据
    s = s.replace("/*__READOUTS__*/", READOUTS.rstrip("\n"), 1)
    # 标题
    s = s.replace("<title>高中物理试题 · 分步解析与动画演示</title>",
                  "<title>用位移传感器测小车速度 · 分步解析与动画演示</title>", 1)

    for mk in ("__GLOBALS__", "__SETUP__", "__DRAWFRAME__", "__READOUTS__"):
        if mk in s:
            raise SystemExit("标记未替换: " + mk)

    with io.open(OUT, "w", encoding="utf-8") as f:
        f.write(s)

    # ===== 探针自检：关键字符串必须在产出文件中（缺一即报） =====
    probes = [
        "const V0     = 340", "function stateAt(t)", "function drawWave(",
        "function drawTimeBand(st)", "function drawBanner(st)", "function dimLine(",
        "function drawLegend()", "function drawCart(x, ghost)",
        "x_{1} = v_{0} t_{1}", r"\\Delta x = x_{2} - x_{1} = v_{0}\\,(t_{2} - t_{1})",
        r"v = \\frac{\\Delta x}{\\Delta t}", "drawIR(st)", "drawCart(X2, true)",
        "__CANVAS_STATIC__", "const BAND_B0 = 0.115",
        # HUD 函数必须是顶层声明（行首无缩进）
        "\nfunction drawBanner(st){", "\nfunction drawTimeBand(st){",
        "\nfunction drawLegend(){", "\nfunction drawWave(cx, r, color, alpha){",
    ]
    with io.open(OUT, "r", encoding="utf-8") as f:
        out = f.read()
    miss = 0
    for p in probes:
        ok = p in out
        if not ok:
            miss += 1
        print(("FOUND   " if ok else "MISSING ") + repr(p))
    if miss:
        print("!! 探针自检失败，共 %d 项" % miss)
        sys.exit(1)

    print("OK -> " + OUT)
    print("size = %.2f MB" % (os.path.getsize(OUT) / 1048576.0))


if __name__ == "__main__":
    main()
