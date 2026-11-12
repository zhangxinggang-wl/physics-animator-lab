# -*- coding: utf-8 -*-
"""
生成《超声波测车速（位移传感器·汽车 D 与仪器 C）》教学动画 HTML。
题源：2026 教材第一章「运动的描述」【例 4】—— 高速公路上用位移传感器测车速。
已知：超声波速度 340 m/s；第一次发射脉冲后 0.2 s 收到反射波；再经 0.025 s 发射第二个脉冲；
      第二个脉冲发出后 0.25 s 收到反射波。结果均保留三位有效数字。
答案：(1) x1 = v*t1/2 = 34.0 m
      (2) Δt = t1/2 + t + t2/2 = 0.100 + 0.025 + 0.125 = 0.250 s
      (3) v = Δx/Δt = (x2 - x1)/Δt = (42.5 - 34.0)/0.250 = 34.0 m/s = 122 km/h
做法：复制 assets/template.html，填充 6 个区域（PROBLEM / STEPS / VIEW+SIM / setup / drawSceneBody / readouts）。

【与「红外线+超声波」例题的关键区别，务必看清】
本题只有超声波一种信号，且是「脉冲往返」测距：脉冲从 C 发出、到 D 反射、再回到 C，
总时间为 t1（或 t2），故「单程距离」= v·t/2（不是 v·t）。
汽车的「接收时刻」= 发射时刻 + t/2。

【版面预算】
动画栏在 1280/1366/1600/1920 视口下画布 CSS 宽仅约 397/423/494/590 px，高 = 0.66×宽（最窄约 261 px）。
故画布内所有 HUD 一律按「占画布高 H 的比例」定位（不写死像素），世界视图 ymax 按「上方信息带」
反算，保证四个宽度下均不叠压。
"""
import io, os, re, sys

BASE = r"C:\Users\19368\Desktop\physics-animator-lab"
TPL = os.path.join(BASE, "assets", "template.html")
OUT = os.path.join(BASE, "2026-09-29_超声波测车速_教学动画.html")

# ---------------------------------------------------------------- ① PROBLEM
PROBLEM = r'''const PROBLEM = {
  title: "",   // 原题为【例 4】，无独立标题；题号写进 given，不另拟标题
  /* 题干：与原题逐字一致（原题跨栏排版：左栏【例 4】起句 + 右栏续写） */
  given: "【例 4】高速公路上常用位移传感器测车速，它的原理如图所示，汽车 D 向右匀速运动，不动的仪器 C 在某一时刻发射短暂的超声波脉冲，经过 0.2 s 接收到被汽车 D 反射回来的超声波，再经过很短的一段时间 0.025 s 后又发射一个短暂的超声波脉冲，发出后经过 0.25 s 再次接收到反射回来的信号。已知超声波传播的速度为 340 m/s，结果均保留三位有效数字。则：",

  /* 题图：方式② Canvas 2D 像素级重绘 + 与右栏动画孪生锁定
     （左栏题图 = drawSceneBody(0)，即右栏动画第 0 帧，几何零偏差） */
  images: [
    { src: "__CANVAS_STATIC__", caption: "题图：用超声波位移传感器测汽车速度的原理图（左栏为动画第 0 帧）", pos: "bottom" }
  ],

  options: [],

  asks: [
    "（1）汽车第一次接收到超声波脉冲时到仪器 C 的距离为多少？",
    "（2）汽车先后两次接收到超声波脉冲的时间间隔为多少？",
    "（3）汽车行驶的速度大小为多少？"
  ],

  knowledgePoints: [
    { id: "wave-mechanical-basics" },
    { id: "princ-modeling" },
    { id: "mech-kin-uniform-accel" }
  ]
};

'''

# ---------------------------------------------------------------- ② STEPS
# 注意：模板用 innerHTML 渲染 note / basis，不支持 Markdown，`**...**` 会原样显示星号，
#       故这里一律直接写 <b>…</b>（main() 里的 re.sub 只是兜底，不会命中）。
STEPS = r'''const STEPS = [
  {
    q: 1,
    title: "脉冲往返测距：t₁ 是「去 + 回」的总时间，单程只有 t₁/2",
    tex: "t_{1} = \\frac{2x_{1}}{v},\\qquad x_{1} = \\frac{v\\,t_{1}}{2}",
    note: "仪器 C 在某一时刻发出一个短暂的超声波脉冲，脉冲在空气中以 340 m/s 匀速前进，碰到汽车 D 后<b>原路反射</b>回去，再被 C 接收。C 从「发射」到「接收」共经过 0.2 s，这 0.2 s 里脉冲走的是<b>一个来回</b>（去程 + 回程），所以去程（也就是 C 到车）只用了 $t_{1}/2 = 0.100$ s。<b>易错点</b>：很多人直接把 0.2 s 当成去程时间，算出 68.0 m，这是本题最常见的错误——往返测距必须除以 2。",
    basis: "机械波在均匀介质中匀速传播 $s = vt$；脉冲往返测距：总路程 = 2 × 往返距离",
    t0: 0.00, t1: 0.55
  },
  {
    q: 1,
    title: "第（1）问：第一次汽车接收到脉冲时到 C 的距离 x₁ = v t₁ / 2 = 34.0 m",
    tex: "x_{1} = \\frac{v\\,t_{1}}{2} = \\frac{340 \\times 0.2}{2}\\ \\text{m} = 34.0\\ \\text{m}",
    note: "把 $t_{1} = 0.2$ s、$v = 340$ m/s 代入 $x_{1} = \\frac{v t_{1}}{2}$，得 $x_{1} = \\frac{340\\times0.2}{2} = 34.0$ m。注意<b>「汽车接收到脉冲」的时刻</b>正是脉冲刚刚追上汽车的瞬间（即去程结束、反射发生的瞬间），此时汽车位于图中 P 点，距 C 为 34.0 m——图中 $x_{1}$ 标注的正是这一段。<b>三位有效数字</b>：34.0 的末位 0 必须写出来，写成 34 会被判为两位有效数字。",
    basis: "匀速运动位移公式；有效数字规则（本题要求三位）",
    t0: 0.55, t1: 1.05
  },
  {
    q: 2,
    title: "理清时间轴：两次「接收到脉冲」的时刻分别在哪",
    tex: "\\tau_{1} = \\frac{t_{1}}{2},\\qquad \\tau_{2} = t_{1} + t + \\frac{t_{2}}{2}",
    note: "以<b>第一次发射</b>为零点建立时间轴：$\\tau = t_{1}/2 = 0.100$ s 时脉冲追上汽车，汽车第一次接收到脉冲；$\\tau = t_{1} = 0.200$ s 时反射波回到 C，C 收到回波；题目说「再经过 0.025 s」发射第二个脉冲，故第二次发射在 $\\tau = 0.200 + 0.025 = 0.225$ s；第二个脉冲经 $t_{2}/2 = 0.125$ s 追上汽车，汽车第二次接收到脉冲的时刻为 $\\tau = 0.225 + 0.125 = 0.350$ s。<b>关键</b>：汽车「接收到脉冲」的时刻不是发射时刻，也不是 C 收到回波的时刻，而是<b>发射后 t/2</b> 的那一瞬。",
    basis: "把文字叙述翻译成时间轴；「接收到脉冲」= 发射时刻 + 单程时间 $t/2$",
    t0: 1.05, t1: 1.65
  },
  {
    q: 2,
    title: "第（2）问：前后两次接收到脉冲的时间间隔 Δt = t₁/2 + t + t₂/2 = 0.250 s",
    tex: "\\Delta t = \\frac{t_{1}}{2} + t + \\frac{t_{2}}{2} = 0.100 + 0.025 + 0.125\\ \\text{s}",
    note: "两次「汽车接收脉冲」的时刻之差就是所求间隔：$\\Delta t = \\tau_{2} - \\tau_{1} = \\left(t_{1} + t + \\frac{t_{2}}{2}\\right) - \\frac{t_{1}}{2} = \\frac{t_{1}}{2} + t + \\frac{t_{2}}{2}$。这与课本「总结提升」给出的公式完全一致（$t$ 为 C 收到第一次回波到第二次发射的间隔）。代入得 $\\Delta t = 0.100 + 0.025 + 0.125 = 0.250$ s。<b>易错点</b>：若误把两次「C 收到回波」的间隔当成 $\\Delta t$，会得到 $0.275$ s；两者的区别在于必须统一取「汽车接收到脉冲」的时刻。",
    basis: "时间轴的端点相减；课本「总结提升」公式 $\\Delta t = \\frac{t_{1}}{2} + t + \\frac{t_{2}}{2}$",
    t0: 1.65, t1: 2.15
  },
  {
    q: 3,
    title: "两次接收位置：第二次汽车位于 Q 点，x₂ = v t₂ / 2 = 42.5 m",
    tex: "x_{2} = \\frac{v\\,t_{2}}{2} = \\frac{340 \\times 0.25}{2}\\ \\text{m} = 42.5\\ \\text{m}",
    note: "第二次测距的原理与第一次完全相同（同一个「往返÷2」）：脉冲发出后 0.25 s 被汽车反射回 C，故第二次汽车接收脉冲时距 C 为 $x_{2} = \\frac{340\\times0.25}{2} = 42.5$ m，此时汽车位于图中 Q 点。于是两次接收之间汽车的位移就是 $\\Delta x = x_{2} - x_{1} = 42.5 - 34.0 = 8.5$ m。<b>看图要点</b>：图中 P、Q 是汽车的<b>两个反射位置</b>，$\\Delta x$ 标注在 P、Q 之间。",
    basis: "同一测距原理的第二次应用；同一直线上位置坐标之差即位移",
    t0: 2.15, t1: 2.70
  },
  {
    q: 3,
    title: "第（3）问：汽车速度 v = Δx / Δt = 34.0 m/s = 122 km/h",
    tex: "v_{D} = \\frac{\\Delta x}{\\Delta t} = \\frac{8.5}{0.250}\\ \\text{m/s} = 34.0\\ \\text{m/s} = 122\\ \\text{km/h}",
    note: "汽车做匀速直线运动，在 $\\Delta t = 0.250$ s 内前进 $\\Delta x = 8.5$ m，由 $v = \\frac{\\Delta x}{\\Delta t}$ 得 $v = \\frac{8.5}{0.250} = 34.0$ m/s。题目要求单位为 km/h，换算：$34.0 \\times 3.6 = 122.4$ km/h，取三位有效数字为 <b>122 km/h</b>。<b>注意</b>：$\\Delta x$ 与 $\\Delta t$ 必须<b>配对</b>——它们都对应「汽车接收第一次脉冲」到「接收第二次脉冲」这同一段时间，不能一个用汽车的接收时刻、另一个用 C 的接收时刻。",
    basis: "匀速直线运动 $v = \\frac{\\Delta x}{\\Delta t}$；单位换算 1 m/s = 3.6 km/h；有效数字三位",
    t0: 2.70, t1: 3.40
  }
];

'''

# ---------------------------------------------------------------- ③ VIEW / SIM
VIEWSIM = r'''const VIEW = { xmin: -1.10, xmax: 3.20, ymin: -0.58, ymax: 2.00 };
const SIM  = { duration: 3.40 };
/* 说明：世界纵横比取 4.30 : 2.58（= 4.30 × 0.600），扣除四周 36px 内边距后与画布像素
   纵横比一致（实测 1280~1920 视口下动画栏画布宽仅 395~590px，该比值在 0.597~0.61 之间），
   使 x、y 方向比例尺相等——超声波圆波前是正圆、车轮是正圆。
   画布高 = 0.66×画布宽，竖向很紧：上方 0.115H～0.385H 固定留给「C 端收发信号时间轴」信息带
   （纯像素坐标、不占世界视图），故世界内容（三个尺寸标注）全部压在 y ≤ 1.15 以下、ymax 取到 2.00
   让场景上方留出这段空白。 */

'''

# ---------------------------------------------------------------- ④ GLOBALS（含全部绘图函数，必须位于顶层）
GLOBALS = r'''/* ===== 本题物理常量与几何参数 =====
   世界坐标：x 向右、y 向上，地面取 y = 0，长度单位 m。
   物理量：超声波速度 v = 340 m/s；
           第一次发射→收到回波 t₁ = 0.20 s，第二次发射→收到回波 t₂ = 0.25 s，
           两次发射之间隔 t = 0.025 s（在 C 收到第一次回波之后）。
   由此：x₁ = v·t₁/2 = 34.0 m，x₂ = v·t₂/2 = 42.5 m，Δx = 8.5 m，
         Δt = t₁/2 + t + t₂/2 = 0.250 s，v_D = Δx/Δt = 34.0 m/s = 122 km/h。 */
const V_US   = 340;               // 超声波在空气中传播速度 (m/s)
const T1     = 0.20;              // 第一次「发射→收到回波」的时间 (s)
const T2     = 0.25;              // 第二次「发射→收到回波」的时间 (s)
const TGAP   = 0.025;             // C 收到第一次回波 → 发射第二次脉冲 的时间 (s)
const X1     = V_US * T1 / 2;     // 第一次汽车接收脉冲时距 C：x₁ = 34.0 m
const X2     = V_US * T2 / 2;     // 第二次汽车接收脉冲时距 C：x₂ = 42.5 m
const DX     = X2 - X1;           // 两次接收之间汽车位移 Δx = 8.5 m
const DT     = T1 / 2 + TGAP + T2 / 2;   // 两次接收到脉冲的时间间隔 Δt = 0.250 s
const V_CAR  = DX / DT;           // 汽车速度 v_D = Δx/Δt = 34.0 m/s（= 122.4 km/h）

/* 关键真实时刻（以第一次发射超声波为零点，单位 s） */
const TC_EMIT1 = 0.0;             // 第一次发射
const TC_RECV1 = T1 / 2;          // 0.100 : 汽车第一次接收到脉冲（反射发生，车在 P）
const TC_BACK1 = T1;              // 0.200 : C 第一次收到回波
const TC_EMIT2 = T1 + TGAP;       // 0.225 : 第二次发射
const TC_RECV2 = TC_EMIT2 + T2/2; // 0.350 : 汽车第二次接收到脉冲（反射发生，车在 Q）
const TC_BACK2 = TC_EMIT2 + T2;   // 0.475 : C 第二次收到回波

/* 装置几何（世界坐标，m）———— 布局依据原题图：
   C 在最左（矮台面上的仪器），D 向右运动；P 为第一次反射位置（在 D 起点与终点之间偏左），
   Q 为第二次反射位置（在更右处）。世界视图取很大的横向范围以容纳 x₁=34 m 与 Δx=8.5 m 的示意。 */
const X_C    = 0;                 // 仪器 C 的发射面在 x = 0
const PX1    = 1.35;              // 比例尺：把 x₁ = 34.0 m 映射到 1.35 世界单位（纯示意，非真值）
const KX     = PX1 / X1;          // 距离→世界的比例 (world/m)，全图统一
/* 汽车：左端（朝 C 的反射面）在 τ=0 时位于 S，此后以世界速度 VW 匀速右移。
   物理约束（也是「x₁、Δx 标注」的依据）：
     τ = TC_RECV1 = 0.100 s 时汽车第一次接收脉冲，此刻其反射面恰在 P（x = X_P）；
     τ = TC_RECV2 = 0.350 s 时汽车第二次接收脉冲，此刻其反射面恰在 Q（x = X_Q）。
   两时刻间隔 Δt = 0.250 s 对应真实位移 Δx = 8.5 m → 世界位移 DX·KX。
   取 VW = DX·KX/Δt，X_P = S + VW·TC_RECV1，X_Q = S + VW·TC_RECV2（自洽，无近似）。 */
const CAR_S  = 1.20;                              // 汽车 τ=0 时的左端坐标（P 左侧一点点）
const VW     = DX * KX / DT;                      // 汽车世界速度 (world/s) = 1.35
const X_P    = CAR_S + VW * TC_RECV1;             // P 点世界坐标（≈1.335）
const X_Q    = CAR_S + VW * TC_RECV2;             // Q 点世界坐标（≈1.6725）
function carLeft(tau){ return CAR_S + VW * tau; } // 汽车左端（反射面）世界坐标，匀速
const CAR_W  = 0.46;              // 汽车车身长度（世界单位，纯示意；取 < Δx 以便两车可辨）
const CAR_H  = 0.24;              // 汽车车身高度
const CAR_Y0 = 0.085;             // 车身底面高度
const WHEEL_R = 0.085;            // 车轮半径
const US_Y   = CAR_Y0 + CAR_H * 0.5;   // 超声波轴线高度（≈车身中部）
const RIG_H  = 0.48;              // 仪器 C 的本体高度
const RIG_W  = 0.40;              // 仪器 C 的本体宽度
const Y_DIM1 = 0.56;              // x₁ 尺寸线高度（紧贴车顶之上）
const Y_DIM2 = 0.73;              // Δx 尺寸线高度
const Y_DIM3 = 0.90;              // x₂ 尺寸线高度（须 < 带底世界 y：三栏最窄 397px 时为 0.972）
/* HUD 竖向比例（占画布高 H 的比例）：信息带上沿 / 下沿 */
const BAND_B0 = 0.115, BAND_B1 = 0.415;

/* ===== 演示时间轴分段：动画秒 → 真实秒(τ) =====
   脉冲飞行实际只有 0.1~0.5 s；若与「等待/结论」段同速率，波前会一闪而过。
   故按段线性映射：脉冲飞行段慢放、其余段近似 1:1，逐段在信息带中标出。 */
const SEGS = [
  { t0: 0.00, t1: 0.55, r0: 0.0,        r1: TC_RECV1, name: '脉冲①去程（慢放）' },
  { t0: 0.55, t1: 1.05, r0: TC_RECV1,   r1: TC_BACK1, name: '脉冲①回程' },
  { t0: 1.05, t1: 1.65, r0: TC_BACK1,   r1: TC_EMIT2, name: '间隔 t，发射脉冲②' },
  { t0: 1.65, t1: 2.15, r0: TC_EMIT2,   r1: TC_RECV2, name: '脉冲②去程（慢放）' },
  { t0: 2.15, t1: 3.40, r0: TC_RECV2,   r1: TC_BACK2, name: '回程 + 结论定格' }
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
  const tau = realTime(tt);                                 // 真实时刻 τ（s），以第一次发射为零点
  /* 脉冲①：去程 τ∈[0, TC_RECV1]，波前从 C 走到汽车；回程 τ∈[TC_RECV1, TC_BACK1]，波前回到 C。
     用「波前到 C 的距离」r1 单调表示：去程 r1 由 0 → X_P；回程 r1 由 X_P → 0。 */
  const r1 = tau <= TC_RECV1 ? V_US * tau
           : (tau <= TC_BACK1 ? V_US * (TC_BACK1 - tau) : 0);
  /* 脉冲②：第二次发射后同理 */
  const tau2 = tau - TC_EMIT2;
  const r2 = tau2 <= 0 ? 0
           : (tau2 <= T2 / 2 ? V_US * tau2
              : (tau2 <= T2 ? V_US * (T2 - tau2) : 0));
  return {
    tt: tt, tau: tau,
    /* 汽车左端（反射面）位置（世界坐标） */
    xLeft: carLeft(tau),
    /* 两个脉冲的「波前距 C 的距离」（世界坐标，用于画圆弧） */
    r1: r1 * KX, r2: r2 * KX,
    /* 波前是否处于「已越过汽车」的回程状态 */
    back1: tau > TC_RECV1 && tau <= TC_BACK1,
    back2: tau2 > T2 / 2 && tau2 <= T2,
    /* 闪光：脉冲到达汽车的瞬间（反射发生） */
    hit1: Math.max(0, 1 - Math.abs(tau - TC_RECV1) / 0.030),
    hit2: Math.max(0, 1 - Math.abs(tau - TC_RECV2) / 0.030),
    ghostP: tau >= TC_RECV1 - 1e-9,                        // P 处残影：第一次接收后出现（x₁ 右端界）
    ghostQ: true,                                          // Q 处残影：全程显示（末位置标记，对应原题虚线车）
    phase: tau < TC_RECV1 ? 0 : (tau < TC_EMIT2 ? 1 : (tau < TC_RECV2 ? 2 : 3))
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

/* ===== 装置：仪器 C（固定在左端；造型对照原题图：矮方盒本体 + 底座 + 朝右的换能器 + 数据线） ===== */
function drawRig(){
  ctx.save();
  /* 底座（比本体略宽的浅灰台） */
  const g1 = W2S(X_C - RIG_W * 0.62, 0.0), g2 = W2S(X_C + RIG_W * 0.62, 0.09);
  ctx.fillStyle = '#e5e7eb'; ctx.fillRect(g1[0], g1[1], g2[0] - g1[0], g2[1] - g1[1]);
  ctx.strokeStyle = '#94a3b8'; ctx.lineWidth = 1.1;
  ctx.strokeRect(g1[0], g1[1], g2[0] - g1[0], g2[1] - g1[1]);
  /* 本体（方盒，高约 0.42） */
  const b1 = W2S(X_C - RIG_W * 0.42, 0.09), b2 = W2S(X_C + RIG_W * 0.42, RIG_H);
  ctx.fillStyle = '#f1f5f9'; ctx.fillRect(b1[0], b1[1], b2[0] - b1[0], b2[1] - b1[1]);
  ctx.strokeStyle = '#334155'; ctx.lineWidth = 1.8;
  ctx.strokeRect(b1[0], b1[1], b2[0] - b1[0], b2[1] - b1[1]);
  /* 换能器（贴在本体右侧、朝右的小突起） */
  const u1 = W2S(X_C + RIG_W * 0.42, US_Y + 0.075), u2 = W2S(X_C + RIG_W * 0.42 + 0.11, US_Y - 0.075);
  ctx.fillStyle = '#1f2937';
  ctx.fillRect(u1[0], u1[1], u2[0] - u1[0], u2[1] - u1[1]);
  ctx.restore();
  /* 数据线（从本体左下引出，避免与上方尺寸线冲突） */
  poly2([[X_C - RIG_W * 0.42, RIG_H * 0.45], [X_C - 0.62, RIG_H * 0.30], [X_C - 0.70, RIG_H * 0.10]], '#64748b', 1.5);
  tag(X_C - 0.74, RIG_H * 0.06, '连接到计算机', '#475569', 10, 'left', true);
  /* C 标注（本体左侧，避免与 x₁ 尺寸线叠字） */
  tag(X_C - RIG_W * 0.42 - 0.06, US_Y + 0.05, 'C', '#1f2937', 15, 'right', true);
}

/* ===== 装置：汽车 D（ghost = P/Q 处虚线残影，对应原题图中的虚线车）
   参数 xLeft = 汽车左端（朝 C 的反射面）世界坐标。 ===== */
function drawCar(xLeft, ghost){
  const col = ghost ? '#94a3b8' : '#1f2937';
  const rot = (xLeft - (X_P - CAR_W)) / WHEEL_R * KX;   // 纯滚动：转角 = 位移 / 半径
  const yTop = CAR_Y0 + CAR_H;
  ctx.save();
  if (ghost) ctx.setLineDash([6, 5]);
  ctx.strokeStyle = col; ctx.lineWidth = ghost ? 1.4 : 2.0;
  /* 车厢主体（矩形） */
  const a = W2S(xLeft, CAR_Y0), b = W2S(xLeft + CAR_W, yTop);
  ctx.beginPath(); ctx.rect(a[0], b[1], b[0] - a[0], a[1] - b[1]);
  ctx.stroke();
  if (!ghost){ ctx.fillStyle = '#f1f5f9'; ctx.fill(); }
  /* 车顶（梯形：前低后高 → 朝右的小驾驶室） */
  const c1 = W2S(xLeft + 0.14, yTop), c2 = W2S(xLeft + 0.14, yTop + 0.13),
        c3 = W2S(xLeft + 0.42, yTop + 0.13), c4 = W2S(xLeft + 0.42, yTop);
  ctx.beginPath();
  ctx.moveTo(c1[0], c1[1]); ctx.lineTo(c2[0], c2[1]);
  ctx.lineTo(c3[0], c3[1]); ctx.lineTo(c4[0], c4[1]); ctx.closePath();
  ctx.stroke();
  if (!ghost){ ctx.fillStyle = '#e2e8f0'; ctx.fill(); }
  ctx.setLineDash([]);
  /* 车轮（两个，纯滚动辐条） */
  [xLeft + 0.14, xLeft + 0.48].forEach(function(wx){
    const c = W2S(wx, WHEEL_R);
    ctx.beginPath(); ctx.arc(c[0], c[1], WHEEL_R * scale, 0, 7);
    ctx.strokeStyle = col; ctx.lineWidth = ghost ? 1.4 : 2.0; ctx.stroke();
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
  /* 字母 D 注在车身中部（残影车不注字母，避免与活车字母叠字） */
  if (!ghost){
    const mid = W2S(xLeft + CAR_W / 2, CAR_Y0 + CAR_H * 0.5);
    ctx.save();
    ctx.fillStyle = col; ctx.font = 'italic bold 14px serif';
    ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.fillText('D', mid[0], mid[1] + 1);
    ctx.textAlign = 'left'; ctx.textBaseline = 'alphabetic';
    ctx.restore();
  }
  /* 反射面小竖线（朝 C 的一侧）—— 超声波由车左侧面反射 */
  if (!ghost){
    const f1 = W2S(xLeft, CAR_Y0 + 0.02), f2 = W2S(xLeft, CAR_Y0 + CAR_H - 0.02);
    ctx.save();
    ctx.strokeStyle = '#2563eb'; ctx.lineWidth = 2.2;
    ctx.beginPath(); ctx.moveTo(f1[0], f1[1]); ctx.lineTo(f2[0], f2[1]); ctx.stroke();
    ctx.restore();
  }
}

/* ===== 超声波脉冲「波前」：以 C 为圆心、半径为 r 的圆弧 =====
   去程：圆弧从 C 向外扩（r 增大）；回程：圆弧从汽车向 C 缩（r 减小）。
   【刻意不画「发射锥角」长虚线】—— 本项目已知坑：从 C 拉向波前两端的锥角虚线在小车驶远后
   会变成横贯场景的长斜线，看起来像多余的工程辅助线（历史上压住过 v 矢量）。
   这里改用「波前 + 少量同心残影弧」表达脉冲，去/回方向由横幅文字与时间轴说明。

   【张角与裁剪必须同时收紧】—— 本项目第二个已知坑：波前弧的顶点高度为
   US_Y + r·sin(half)。脉冲②去程 r 最大 1.687 世界单位，若 half 取 20°，
   顶点可达 y = 0.205 + 0.342×1.687 = 0.782，会越过 Δx 尺寸线（Y_DIM2 = 0.73）
   与 x₂ 尺寸线（Y_DIM3 = 0.90），弧线横穿尺寸标注 → 叠字、看不懂对应关系。
   故：① half 收到 10°，顶点最高 0.205 + 0.174×1.687 = 0.498 < Y_DIM1 = 0.56；
       ② 再加一道硬裁剪，把弧严格限制在最下方尺寸线（Y_DIM1 − 0.02）以下，
          双保险（改题后即使 half 或 Y_DIM1 变动也不会再越界）。 */
function drawFront(cx, r, color, alpha, dirSign){
  if (r <= 0.012 || alpha <= 0.01) return;
  ctx.save();
  /* 上下双向裁剪：上不过最下方尺寸线，下不到地面以下 */
  const yTop = Math.max(BAND_B1 * H, W2S(0, Y_DIM1 - 0.02)[1]);
  const yBot = W2S(0, 0)[1] + 2;
  ctx.beginPath(); ctx.rect(0, yTop, W, Math.max(0, yBot - yTop)); ctx.clip();
  const half = 10 * Math.PI / 180, n = 28;
  /* 3 条同心弧：主波前 + 两条内侧残影（体现「波包」），由外到内渐淡 */
  for (let k = 0; k < 3; k++){
    const rr = r - k * 0.075;
    if (rr <= 0.012) continue;
    ctx.globalAlpha = Math.min(1, alpha) * (k === 0 ? 0.95 : (k === 1 ? 0.45 : 0.22));
    ctx.strokeStyle = color; ctx.lineWidth = k === 0 ? 2.4 : 1.5;
    ctx.beginPath();
    for (let i = 0; i <= n; i++){
      const a = -half + 2 * half * i / n;
      const p = W2S(cx + dirSign * rr * Math.cos(a), US_Y + rr * Math.sin(a));
      if (i) ctx.lineTo(p[0], p[1]); else ctx.moveTo(p[0], p[1]);
    }
    ctx.stroke();
  }
  ctx.restore();
}
/* 反射点闪光（脉冲打到汽车的瞬间） */
function drawHit(xRef, y, alpha){
  if (alpha <= 0.02) return;
  const p = W2S(xRef, y);
  ctx.save();
  ctx.globalAlpha = Math.min(1, alpha);
  ctx.beginPath(); ctx.arc(p[0], p[1], 9, 0, 7);
  ctx.fillStyle = 'rgba(249,115,22,0.85)'; ctx.fill();
  ctx.beginPath(); ctx.arc(p[0], p[1], 5, 0, 7);
  ctx.fillStyle = '#fff'; ctx.fill();
  ctx.restore();
}

/* ===== 画布 HUD（纯像素坐标，一律按 H 的比例定位，窄画布也不叠压） ===== */
function drawBanner(st){
  const txt = st.phase === 0 ? '脉冲① 去程 · C→汽车（t₁ = 0.20 s 计时中）'
            : st.phase === 1 ? '汽车到 C 的距离 x₁ = v·t₁÷2 = 34.0 m · C 收到回波'
            : st.phase === 2 ? '隔 t = 0.025 s 发射脉冲② · C→汽车（t₂ = 0.25 s 计时中）'
            : '结论 · v = Δx/Δt = 8.5 m ÷ 0.250 s = 34.0 m/s = 122 km/h';
  const bg  = st.phase === 0 ? 'rgba(37,99,235,0.94)'
            : st.phase === 1 ? 'rgba(13,148,136,0.94)'
            : st.phase === 2 ? 'rgba(124,58,237,0.94)'
            : 'rgba(234,88,12,0.94)';
  ctx.save();
  ctx.font = 'bold 12px "Microsoft YaHei","PingFang SC",sans-serif';
  const tw = ctx.measureText(txt).width, bh = 22, bw = Math.min(W - 12, tw + 24);
  const bx = (W - bw) / 2, by = 4;
  rrect(bx, by, bw, bh, 11);
  ctx.fillStyle = bg; ctx.fill();
  ctx.fillStyle = '#fff'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  ctx.fillText(txt, W / 2, by + bh / 2 + 1);
  ctx.textAlign = 'left'; ctx.textBaseline = 'alphabetic';
  ctx.restore();
}
/* 像素坐标双箭头；below=true 时标签放到线下方（短箭头用，避免白底盖住箭头） */
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
/* 「C 端收发信号时间轴」信息带：5 个时刻 + t₁/2、t、t₂/2 三段（示意，非等比） */
function drawTimeBand(st){
  const b0 = BAND_B0 * H, bh = (BAND_B1 - BAND_B0) * H, bx0 = 12, bx1 = W - 12;
  ctx.save();
  rrect(bx0, b0, bx1 - bx0, bh, 8);
  ctx.fillStyle = '#f8fafc'; ctx.fill();
  ctx.strokeStyle = '#e2e8f0'; ctx.lineWidth = 1; ctx.stroke();

  const rowT = b0 + bh * 0.12;       // 标题 / 状态药丸（独占最上一行）
  const rowA = b0 + bh * 0.58;       // 时间轴（刻度），时刻名放在轴上方紧邻两行
  const rowD = b0 + bh * 0.90;       // Δt 汇总箭头（最下一行）

  /* 标题（左） */
  ctx.fillStyle = '#475569';
  ctx.font = 'bold 11px "Microsoft YaHei","PingFang SC",sans-serif';
  ctx.fillText('真实时间轴（以第一次发射为零点）', bx0 + 10, rowT + 3);
  /* 副题：说明 t₁ / t₂ 是往返，单程为一半 */
  ctx.font = '9px "Microsoft YaHei","PingFang SC",sans-serif';
  ctx.fillStyle = '#94a3b8';

  /* 实时状态药丸（右） */
  let timerTxt, timerCol;
  if (st.tau < TC_RECV1){ timerTxt = '脉冲①飞行 ' + (st.tau * 1000).toFixed(0) + ' ms'; timerCol = '#2563eb'; }
  else if (st.tau < TC_EMIT2){ timerTxt = '已收回波① t₁ = 0.20 s'; timerCol = '#0f766e'; }
  else if (st.tau < TC_RECV2){ timerTxt = '脉冲②飞行 ' + ((st.tau - TC_EMIT2) * 1000).toFixed(0) + ' ms'; timerCol = '#7c3aed'; }
  else { timerTxt = '已收回波② t₂ = 0.25 s'; timerCol = '#ea580c'; }
  ctx.font = 'bold 10px "Microsoft YaHei","PingFang SC",sans-serif';
  const tw = ctx.measureText(timerTxt).width;
  if (bx1 - 10 - tw - 14 > bx0 + 10 + 170){
    rrect(bx1 - 10 - tw - 14, rowT - 9, tw + 14, 15, 7);
    ctx.fillStyle = timerCol; ctx.fill();
    ctx.fillStyle = '#fff'; ctx.fillText(timerTxt, bx1 - 10 - tw - 7, rowT + 2);
  }

  /* 时间轴：5 个关键时刻，位置按真实 τ 比例（0, .1, .2, .225, .35 → 归一化到 [.02,.98]） */
  const x0 = bx0 + 14, x1e = bx1 - 14, mw = x1e - x0;
  const TAU_MAX = TC_BACK2;                                  // 0.475 s
  const fr = [0, TC_RECV1, TC_BACK1, TC_EMIT2, TC_RECV2, TC_BACK2].map(v => v / TAU_MAX);
  const e = [0, 1, 2, 3, 4].map(i => x0 + (0.03 + 0.94 * fr[i]) * mw);
  ctx.strokeStyle = '#cbd5e1'; ctx.lineWidth = 1.4;
  ctx.beginPath(); ctx.moveTo(x0, rowA); ctx.lineTo(x1e, rowA); ctx.stroke();
  const tcol = ['#334155', '#2563eb', '#0f766e', '#7c3aed', '#ea580c'];
  const tlab = ['发射①', '汽车接收①', 'C 收回波①', '发射②', '汽车接收②'];
  const ttau = [0, TC_RECV1, TC_BACK1, TC_EMIT2, TC_RECV2];
  e.forEach(function(x, i){
    const done = st.tau >= ttau[i] - 1e-9;
    ctx.strokeStyle = done ? tcol[i] : '#cbd5e1'; ctx.lineWidth = 2.6;
    ctx.beginPath(); ctx.moveTo(x, rowA - 5); ctx.lineTo(x, rowA + 5); ctx.stroke();
  });
  /* 时刻名：全部放在轴【上方】紧邻处，用 2 行垂直偏移错开（防窄画布叠字） */
  ctx.font = '9px "Microsoft YaHei","PingFang SC",sans-serif';
  ctx.textAlign = 'center';
  e.forEach(function(x, i){
    const done = st.tau >= ttau[i] - 1e-9;
    const up = (i % 2 === 0) ? 1 : 2;                       // 偶数小标在下行、奇数在上行
    const lx = Math.max(bx0 + 20, Math.min(bx1 - 20, x));   // 两端标签向内收，防越界
    ctx.fillStyle = done ? tcol[i] : '#cbd5e1';
    ctx.fillText(tlab[i], lx, rowA - 7 - (up - 1) * 11);
  });
  ctx.textAlign = 'left';

  /* Δt 汇总箭头（t₁/2 + t + t₂/2），独占最下一行 */
  pxArrow(e[0], e[4], rowD, '#7c3aed', 'Δt = t₁/2 + t + t₂/2 = 0.250 s', false);
  ctx.restore();
}
/* 底部图例：按可用宽度自动折行（自底向上），窄画布也不溢出 */
function drawLegend(){
  const items = [
    ['#2563eb', '蓝弧：脉冲①波前（去程扩 / 回程缩）'],
    ['#7c3aed', '紫弧：脉冲②波前'],
    ['#f97316', '橙点：脉冲打到汽车（反射瞬间）'],
    ['#0f766e', '绿箭头：汽车速度 v（向右）'],
    ['#94a3b8', '虚线车：P、Q 两个反射位置残影　（脉冲飞行段为慢放）']
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
  const use = lines.slice(0, 3);
  use.forEach(function(ln, li){
    const y = H - 10 - (use.length - 1 - li) * 15;
    let x = PAD;
    ln.forEach(function(seg){ ctx.fillStyle = seg[0]; ctx.fillText(seg[1], x, y); x += seg[2]; });
  });
  ctx.restore();
}

'''

SETUP = r'''  /* 本题运动学量全部可解析给出（stateAt 即解析解），无需数值积分。
     SIM.duration = 3.40 s，对应真实过程（真实 τ 轴）：
       0 → 0.100 s  脉冲①去程（慢放）
       0.100 → 0.200 s  脉冲①回程
       0.200 → 0.225 s  间隔 t，C 发射脉冲②
       0.225 → 0.350 s  脉冲②去程
       0.350 → 0.475 s  脉冲②回程 + 结论定格
     世界视图与 HUD 比例（BAND_B0 / BAND_B1）均为常量，绘图按 H 的比例定位。 */
'''

DRAWFRAME = r'''  const st = stateAt(t);

  /* 地面（粗横线 + 斜线阴影）—— C 的底座与汽车同在地面 */
  FIG.ground(VIEW.xmin + 0.05, VIEW.xmax - 0.05, 0, { gap: 0.16, hatchLen: 0.9, color: '#334155' });

  /* P（第一次反射位置）、Q（第二次反射位置）的竖直参考线：从地面一直拉到 x₂ 尺寸线 */
  poly2([[X_P, 0], [X_P, Y_DIM3 + 0.02]], '#94a3b8', 1.0, [4, 4]);
  poly2([[X_Q, 0], [X_Q, Y_DIM3 + 0.02]], '#94a3b8', 1.0, [4, 4]);

  /* 超声波波前：以 C 为圆心画弧，去程 r 增大、回程 r 缩小；回程时在弧上加「←回」箭头 */
  if (st.r1 > 0) drawFront(X_C, st.r1, '#2563eb', st.back1 ? 0.85 : 1, +1);
  if (st.r2 > 0) drawFront(X_C, st.r2, '#7c3aed', 1, +1);
  /* 波前方向指示：去程在弧顶画「→」，回程画「←」（贴在弧上，短小不压线） */
  function frontDir(r, color, back){
    if (r <= 0.15) return;
    const p = W2S(X_C + r, US_Y);
    const L = 14;
    if (back) arrowHead(p[0] - 2, p[1], p[0] - 2 - L, p[1], color, 7);
    else      arrowHead(p[0] + 2, p[1], p[0] + 2 + L, p[1], color, 7);
  }
  if (st.r1 > 0) frontDir(st.r1, '#2563eb', st.back1);
  if (st.r2 > 0) frontDir(st.r2, '#7c3aed', st.back2);

  /* 装置本体：仪器 C（固定）→ P、Q 残影车 → 汽车 D（实时位置）
     残影车的左端（反射面）分别落在 P、Q 上（与 drawCar 的传入语义一致） */
  drawRig();
  if (st.ghostP) drawCar(X_P, true);
  if (st.ghostQ) drawCar(X_Q, true);
  drawCar(st.xLeft, false);

  /* 反射闪光（打在汽车左端反射面上） */
  drawHit(st.xLeft, US_Y, st.hit1);
  drawHit(st.xLeft, US_Y, st.hit2);

  /* 汽车速度矢量 v（放在车正上方，随车移动；避开 Δx / x₂ 尺寸线与 Q 残影） */
  FIG.vec(st.xLeft + CAR_W * 0.5, 0.50, 0.40, 0, 'v', { color: '#0f766e', lw: 3, head: 9 });

  /* 尺寸线：x₁（C→P）、Δx（P→Q）、x₂（C→Q）—— 三层紧排，字母 P/Q 压在相应界线顶端 */
  const cX1 = st.phase <= 1 ? '#dc2626' : '#334155';
  const cDX = st.phase >= 3 ? '#ea580c' : (st.phase >= 2 ? '#0f766e' : '#64748b');
  dimLine(X_C, X_P, Y_DIM1, 'x₁', cX1, st.phase <= 1 ? 1.8 : 1.3, (X_C + X_P) / 2 - 0.05);
  dimLine(X_P, X_Q, Y_DIM2, 'Δx', cDX, st.phase >= 2 ? 1.8 : 1.3, (X_P + X_Q) / 2);
  dimLine(X_C, X_Q, Y_DIM3, 'x₂', '#7c3aed', 1.4, (X_C + X_Q) / 2 - 0.55);
  tag(X_P - 0.10, Y_DIM1 + 0.075, 'P', '#475569', 12, 'center', false);
  tag(X_Q + 0.10, Y_DIM3 - 0.075, 'Q', '#475569', 12, 'center', false);

  /* ===== 固定像素坐标 HUD：过程横幅 + 时间轴信息带 + 图例
     t=0 时不画，保证左栏题图（＝动画第 0 帧）与原题图完全一致 ===== */
  if (t > 0.002){
    drawBanner(st);
    drawTimeBand(st);
    drawLegend();
  }
'''

READOUTS = r'''  const st = stateAt(t);
  /* 读数与解析逐项对应，全部取自同一个 stateAt：
     · x₁ 在「脉冲①去程」期间按 v·τ 增长，τ 到达 TC_RECV1 = 0.100 s 时严格 = 34.0 m；
     · x₂ 在汽车第二次接收到脉冲的瞬间（τ = TC_RECV2）确定，= 42.5 m；
     · Δx = x₂ − x₁ 与 Δt = t₁/2 + t + t₂/2 只在两次接收都完成后才给出（末值 8.5 m、0.250 s）。 */
  const t1Run = Math.min(st.tau, TC_BACK1) * 1000;                       // 到 C 收回波① 为止计满 200 ms
  const x1Run = Math.min(st.tau, TC_RECV1) * V_US;                       // 去程实时 x₁（末值 34.0）
  const t2Run = Math.max(0, Math.min(st.tau - TC_EMIT2, T2)) * 1000;     // 到 C 收回波② 为止计满 250 ms
  const done2 = st.tau >= TC_RECV2 - 1e-9;
  const x2Run = done2 ? X2 : 0;
  const dxRun = done2 ? DX : 0;
  const dtRun = done2 ? DT : 0;
  return [
    ["演示时刻 $t$", st.tt.toFixed(2), "s"],
    ["真实时刻 $\\tau$", (st.tau * 1000).toFixed(0), "ms"],
    ["脉冲①往返时间 $t_{1}$", t1Run.toFixed(0), "ms"],
    ["第一次距离 $x_{1}=\\frac{v\\,t_{1}}{2}$", x1Run.toFixed(1), "m"],
    ["脉冲②往返时间 $t_{2}$", t2Run.toFixed(0), "ms"],
    ["第二次距离 $x_{2}=\\frac{v\\,t_{2}}{2}$", done2 ? x2Run.toFixed(1) : "—", "m"],
    ["两次位移 $\\Delta x=x_{2}-x_{1}$", done2 ? dxRun.toFixed(1) : "—", "m"],
    ["时间间隔 $\\Delta t=\\frac{t_{1}}{2}+t+\\frac{t_{2}}{2}$", done2 ? dtRun.toFixed(3) : "—", "s"],
    ["汽车速度 $v_{D}=\\frac{\\Delta x}{\\Delta t}$", done2 ? (V_CAR * 3.6).toFixed(0) : "—", "km/h"]
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
    # ② STEPS（**兜底转 <b>**）
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
    # ④ GLOBALS
    s = s.replace("/*__GLOBALS__*/", GLOBALS.rstrip("\n"), 1)
    # ⑤ setup
    s = s.replace("/*__SETUP__*/", SETUP.rstrip("\n"), 1)
    # ⑥ drawFrame
    s = s.replace("/*__DRAWFRAME__*/", DRAWFRAME.rstrip("\n"), 1)
    # ⑦ readouts
    s = s.replace("/*__READOUTS__*/", READOUTS.rstrip("\n"), 1)
    # 标题
    s = s.replace("<title>高中物理试题 · 分步解析与动画演示</title>",
                  "<title>超声波测车速（位移传感器）· 分步解析与动画演示</title>", 1)

    for mk in ("__GLOBALS__", "__SETUP__", "__DRAWFRAME__", "__READOUTS__"):
        if mk in s:
            raise SystemExit("标记未替换: " + mk)

    with io.open(OUT, "w", encoding="utf-8") as f:
        f.write(s)

    # ===== 探针自检 =====
    probes = [
        "const V_US   = 340", "function stateAt(t)", "function drawFront(",
        "function drawTimeBand(st)", "function drawBanner(st)", "function dimLine(",
        "function drawLegend()", "function drawCar(xLeft, ghost)", "function drawRig(",
        "function carLeft(tau)", "function realTime(t)",
        r"x_{1} = \\frac{v\\,t_{1}}{2}", r"\\Delta x = x_{2} - x_{1}",
        r"v_{D} = \\frac{\\Delta x}{\\Delta t}",
        "drawRig()", "drawCar(X_P, true)", "drawCar(X_Q, true)",
        "__CANVAS_STATIC__", "const BAND_B0 = 0.115",
        "\nfunction drawBanner(st){", "\nfunction drawTimeBand(st){",
        "\nfunction drawLegend(){", "\nfunction drawFront(cx, r, color, alpha, dirSign){",
        "\nfunction carLeft(tau){",
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
