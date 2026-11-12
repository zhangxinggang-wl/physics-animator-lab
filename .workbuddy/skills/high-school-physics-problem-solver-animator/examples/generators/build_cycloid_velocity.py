# -*- coding: utf-8 -*-
r"""
生成《配速法·摆线（旋轮线）》教学动画 HTML。

物理内核
--------
半径 R 的圆环在水平地面上做无滑滚动（纯滚动），圆心以恒定速率 v = ωR 平动。
轮缘上任一点 a 的运动 = 「随圆心的平动」+「绕圆心的匀速转动」，这就是配速法。

取 a 在 t=0 时位于最高点，滚动角 θ = ωt（= 圆转角 = 圆心前进弧角），则
    圆心：      x_c = Rθ ,      y_c = R
    轮缘点 a：  x_a = Rθ + R sinθ ,      y_a = R + R cosθ      ← 摆线参数方程
    速度分解：  v_a = v (水平，平动) + ωR (切向，绕心转动)
                a 点的切向速度方向与水平夹角为 θ，故
                v_a = 2v·|sin(θ/2)|        （θ=2πn 最高点 v=0；θ=π+2πn 最低点 v=2v）
    加速度：    转动分量恒指向圆心，大小 a = ω²R（平动速度恒定，无平动加速度分量）

数值方案：R = 0.5 m，ω = 2 rad/s → v = 1.0 m/s。
滚动 2 圈（θ: 0 → 4π，t: 0 → 2π s ≈ 6.2832 s），再留 0.9 s 定格。
水平行程 s = 4πR ≈ 6.2832 m，最高点 y = 2R = 1.0 m。

⚠ JS 字符串字面量中的 LaTeX 反斜杠必须写两个 \\，或改用 $...$ 单美元号（本脚本尽量用后者）。

⚠⚠ 重要：模板中 `const STEPS = [...]` 声明在 `/*__GLOBALS__*/` **之前**，因此 STEPS 里
     **绝对不能引用 GLOBALS 中定义的任何 const**（T_ROLL / T_END / TWO_PI 等），否则会命中
     const 的暂时性死区，抛 `ReferenceError: Cannot access 'T_ROLL' before initialization`，
     表现为整页白屏（mjx=0 / step=0）。STEPS 的 t0/t1 必须写字面数字。
"""

import io
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TPL = os.path.join(ROOT, "assets", "template.html")
OUT = os.path.join(ROOT, "2026-09-14_配速法摆线_教学动画.html")

# ---------------------------------------------------------------- 物理常数
R = 0.5           # 圆环半径 m
OMEGA = 2.0       # 角速度 rad/s
V_CM = R * OMEGA  # 圆心平动速率 1.0 m/s
T_ROLL = 4 * 3.141592653589793 / OMEGA   # 滚 2 圈用时 ≈ 6.2832 s
T_END = T_ROLL + 0.9                      # 定格 0.9 s

# ================================================================ ① 题面
PROBLEM_JS = r"""const PROBLEM = {
  title: "配速法·摆线（旋轮线）",
  tags: ["力学", "曲线运动", "运动合成与分解", "配速法", "摆线"],
  given: [
    "半径 $R = 0.5$ m 的刚性圆环在水平地面上做**无滑滚动**（纯滚动），环上标记一点 $a$；",
    "自 $t = 0$ 起，圆心 $O'$ 以恒定速率 $v = 1.0$ m/s 沿直线水平前进，圆环绕心匀速转动；",
    "$t = 0$ 时 $a$ 恰位于圆环的**最高点**，且此后圆环滚动**恰好 2 圈**（滚过的弧长等于圆心位移）。"
  ],
  asks: [
    "用「配速法」写出轮缘点 $a$ 的速度分解式，并求 $a$ 的速率 $v_a$ 随滚动角 $\\theta$ 的变化关系；",
    "求 $a$ 在最高点与最低点两处的速率，以及圆环滚动 2 圈的过程中 $a$ 的最大速率；",
    "说明 $a$ 的加速度大小与方向特征。"
  ],
  images: [
    { src: "__CANVAS_STATIC__", caption: "图 1　圆环无滑滚动，环上一点 a 的轨迹即摆线（题图 = 动画第 0 帧）" }
  ],
  knowledgePoints: [
    { id: "mech-circular-horizontal" },
    { id: "princ-relative-motion" },
    { id: "princ-vector-basics" }
  ]
};"""

# ================================================================ ② 分步解析
STEPS_JS = r"""const STEPS = [
  { title: "① 建立描述圆环滚动的运动学量",
    tex: "$$\\theta = \\omega t,\\qquad x_{O'} = R\\theta = vt,\\qquad v = \\omega R$$",
    note: "无滑滚动是本题一切结论的出发点：**轮缘与地面接触的那一点瞬时静止**，因此圆环转过的弧长恒等于圆心前进的弧长，即 $R\\theta = v t$。这个等式把「转动量」$\\theta$ 与「平动量」$x_{O'}$ 锁死在一起，也正是下面能用一条参数方程同时写出位置与速度的原因。取地面为 $x$ 轴、$\\theta$ 为圆环滚过的弧度，$\\theta = 2\\pi$ 对应滚动 1 圈。",
    basis: "纯滚动（无滑滚动）约束 $s = R\\theta$；角量与线量关系 $v = \\omega R$",
    t0: 0.0, t1: 0.55 },

  { title: "② 位置：圆心平动叠加绕心转动，得到摆线",
    tex: "$$\\begin{cases} x_c = R\\theta \\\\ y_c = R\\end{cases}\\qquad\\Longrightarrow\\qquad \\begin{cases} x_a = R\\theta + R\\sin\\theta \\\\ y_a = R + R\\cos\\theta \\end{cases}$$",
    note: "圆心 $O'$ 只做匀速直线平动，故 $x_c = R\\theta$、$y_c = R$ 不变。轮缘点 $a$ 相对圆心始终在半径 $R$ 的圆上：由「最高点起算、顺时针积分」的几何关系可得相对位矢为 $(R\\sin\\theta,\\;R\\cos\\theta)$。把平动与转动**矢量相加**，就得到了 $a$ 的参数方程——这正是**摆线（旋轮线）**的标准形式。它是一条周期 $2\\pi R$、峰高 $2R$ 的周期曲线。",
    basis: "运动的合成：绝对位移 = 平动牵连位移 + 相对转动位移（矢量叠加）",
    t0: 0.55, t1: 1.35 },

  { title: "③ 配速法：把 a 的速度分解为「平动 + 绕心转动」",
    tex: "$$\\vec v_a = \\underbrace{\\vec v_{\\text{平}}}_{v,\\ \\text{水平向右}} + \\underbrace{\\vec v_{\\text{转}}}_{\\omega R,\\ \\text{切向}},\\qquad \\vec v_{\\text{平}} \\perp \\vec v_{\\text{切}}}$$",
    note: "配速法的全部内容就是「速度也满足矢量叠加」：$a$ 的速度 = 它跟着圆心**平动**的速度 $\\vec v_{\\text{平}}$（大小 $v = \\omega R$，方向水平向右，与圆心相同）+ 它**绕圆心转动**的速度 $\\vec v_{\\text{转}}$（大小 $\\omega R$，方向沿圆周切向）。$\\vec v_{\\text{平}}$ 与 $\\vec v_{\\text{转}}$ 与半径的关系决定了二者的夹角，也是下一问求合速率的依据。注意这两个分速度**大小恒相等**（都等于 $\\omega R$），这是配速法在滚动问题里特别简洁的原因。",
    basis: "运动的合成与分解：同一点的速度满足平行四边形定则（速度叠加原理）",
    t0: 1.35, t1: 2.40 },

  { title: "④ 求速率：两分速度夹角为 θ，得 v_a = 2v sin(θ/2)",
    tex: "$$v_a = \\sqrt{(\\omega R)^2 + (\\omega R)^2 + 2(\\omega R)^2\\cos\\theta} = 2\\omega R\\left|\\sin\\frac{\\theta}{2}\\right|$$",
    note: "把 $\\vec v_{\\text{平}}$ 与 $\\vec v_{\\text{转}}$ 画成邻边作平行四边形，对角线的长度就是 $v_a$。由余弦定理（夹角为 $\\theta$）展开：$(\\omega R)^2+(\\omega R)^2+2(\\omega R)^2\\cos\\theta$，用半角公式 $1+\\cos\\theta = 2\\cos^2(\\theta/2)$ 化简即得 $2\\omega R|\\sin(\\theta/2)|$。**这个结果说明速率只与滚动角 $\\theta$ 有关**，与「时刻」「圈数」都无关。取绝对值的意义是：合速率非负，而正弦的绝对值以 $2\\pi$ 为周期，所以每一圈的速率变化完全重复。",
    basis: "余弦定理 / 半角公式 $1+\\cos\\theta = 2\\cos^2\\frac{\\theta}{2}$；矢量合成模长公式",
    t0: 2.40, t1: 3.60 },

  { title: "⑤ 关键点验算：最高点 v = 0，最低点 v = 2v",
    tex: "$$v_{a,\\max} = 2\\omega R = 2v = 2.0\\ \\mathrm{m/s}$$",
    note: "$\\theta = 0$（最高点）：两个分速度大小相等、方向相反，合速率为 0——环上最高点**瞬时静止**，这就是无滑滚动里「最高点速度为零、与地面接触点速度也为零」之外的另一个直观结论（本题 $t=0$ 时 $a$ 恰在最高点，故 $v_a=0$）。$\\theta = \\pi$（最低点）：两个分速度**同向**（都水平向右），合速率 $= 2\\omega R = 2v = 2.0$ m/s，是全程最大值——环上该点此刻正是「瞬时向前最快」的位置。因 $|\\sin(\\theta/2)|$ 在 $\\theta = \\pi + 2k\\pi$ 处取到 1，故滚 2 圈内 $a$ **两次**达到 $2.0$ m/s。",
    basis: "把 $\\theta = 0,\\ \\pi$ 代入 $v_a = 2\\omega R|\\sin(\\theta/2)|$；矢量同向相加 / 反向相减",
    t0: 3.60, t1: 4.70 },

  { title: "⑥ 加速度：大小为 ω²R，方向恒指向圆心",
    tex: "$a_a = \\omega^2 R = 2.0\\ \\mathrm{m/s^2}$，方向始终指向圆心 $O'$。",
    note: "用同样的思路分解加速度：$a$ 的加速度 = 平动加速度 + 相对转动加速度。圆心做匀速直线运动，平动加速度为 0；相对分运动是**匀速率圆周运动**，其加速度只有向心分量，大小 $\\omega^2 R$、方向永远指向圆心。二者相加即得结论。所以 $a$ 点走的是变速率曲线运动，但**加速度大小恒定、方向始终指向环心**——速率在变、加速度大小不变，这正是摆线运动的鲜明特征。代入 $R=0.5$ m、$\\omega = 2$ rad/s：$a_a = 4 \\times 0.5 = 2.0$ m/s²。",
    basis: "匀速圆周运动的向心加速度 $a_n = \\omega^2 R$；平动加速度为 0（匀速直线）",
    t0: 4.70, t1: 6.2832 },

  { title: "⑦ 结论",
    tex: "$$v_a = 2v\\left|\\sin\\frac{\\theta}{2}\\right|,\\qquad v_{a,\\max} = 2v = 2.0\\ \\mathrm{m/s},\\qquad a_a = \\omega^2 R = 2.0\\ \\mathrm{m/s^2}$$",
    note: "配速法把「看上去很复杂的摆线运动」拆成了两个最熟悉的运动：一个匀速直线平动 + 一个匀速圆周转动。位置相加得摆线，速度相加得 $v_a = 2v|\\sin(\\theta/2)|$，加速度相加得「恒指向圆心」。滚 2 圈：圆心前进 $s = 4\\pi R \\approx 6.283$ m，$a$ 走出一条含 2 段拱的摆线，2 次瞬时静止（最高点）、2 次达 $2.0$ m/s（最低点）。",
    basis: "运动的独立性与矢量叠加原理（配速法的适用条件：平动 + 转动可分别求解再叠加）",
    t0: 6.2832, t1: 7.1832 }
];"""

# ================================================================ ③ 视图
VIEW_JS = "const VIEW = { xmin: -1.25, xmax: 8.65, ymin: -0.55, ymax: 5.34 };"
SIM_JS = "const SIM  = { duration: %s };" % (repr(round(T_END, 4)))

# ================================================================ ④ 全局
GLOBALS_JS = r"""/* ---------- 物理常数（与解析完全一致） ---------- */
const R_RING = 0.5;                     // 半径 m
const OMEGA  = 2.0;                     // 角速度 rad/s
const V_CM   = R_RING * OMEGA;          // 圆心平动速率 = 1.0 m/s
const T_ROLL = 4 * Math.PI / OMEGA;     // 滚 2 圈用时 ≈ 6.2832 s
const TWO_PI = Math.PI * 2;
/* 地面每 0.5 m 一个点标记、每 1.0 m 一个刻度标签 */
const GROUND_MARKS = (function(){ const a=[]; for (let x=0; x<=7.0001; x+=0.5) a.push(x); return a; })();

/* ---------- 统一状态函数：画面与数据面板共用同一组公式 ---------- */
function stateAt(t){
  const tt = Math.min(t, T_ROLL);              // 滚动结束即定格
  const th = OMEGA * tt;                       // 滚动角（弧度）
  const cx = R_RING * th;                      // 圆心 x
  const cy = R_RING;                           // 圆心 y
  const ax = cx + R_RING * Math.sin(th);       // 轮缘点 a 的 x
  const ay = cy + R_RING * Math.cos(th);       // 轮缘点 a 的 y
  const s  = cx;                               // 圆心位移 = Rθ
  const va = 2 * V_CM * Math.abs(Math.sin(th / 2));   // 配速法合速率
  const acc = OMEGA * OMEGA * R_RING;          // 恒指向圆心的加速度
  const turn = th / TWO_PI;                    // 已滚圈数
  const frozen = t >= T_ROLL;
  return { tt, th, cx, cy, ax, ay, s, va, acc, turn, frozen };
}

/* ---------- 摆线轨迹：从 0 到 thMax 采样 ---------- */
function cycloidPts(thMax, n){
  const pts = [];
  const N = n || 240;
  for (let i = 0; i <= N; i++){
    const th = thMax * i / N;
    pts.push([R_RING*th + R_RING*Math.sin(th), R_RING + R_RING*Math.cos(th)]);
  }
  return pts;
}

/* ---------- 虚线辅助线 ---------- */
function dashed(x1,y1,x2,y2,color,dash){
  const a = W2S(x1,y1), b = W2S(x2,y2);
  ctx.save();
  ctx.strokeStyle = color; ctx.lineWidth = 1.4;
  ctx.setLineDash(dash || [5,4]);
  ctx.beginPath(); ctx.moveTo(a[0],a[1]); ctx.lineTo(b[0],b[1]); ctx.stroke();
  ctx.restore();
}

/* ---------- 右手系小坐标轴（0.62 m 长） ---------- */
function axesMini(x,y,L){
  const len = L || 0.62;
  dashed(x,y,x+len,y,'#9aa4b2',[4,3]);
  dashed(x,y,x,y+len,'#9aa4b2',[4,3]);
  FIG.vec(x,y,len,0,'',{color:'#9aa4b2', lw:1.6, head:6});
  FIG.vec(x,y,0,len,'',{color:'#9aa4b2', lw:1.6, head:6});
  FIG.text(x+len+0.05, y+0.02, 'x', {size:12, color:'#9aa4b2'});
  FIG.text(x-0.02, y+len+0.13, 'y', {size:12, color:'#9aa4b2', align:'right'});
}

/* ---------- 固定叠加说明（先铺白底让位，避免与旋转标签叠字） ---------- */
function stackNote(){
  const p = W2S(0.20, 1.17);
  const txt = '速度平行四边形：v_a = v + ωR';
  ctx.save();
  ctx.font = 'bold 13px sans-serif';
  const w = ctx.measureText(txt).width;
  ctx.fillStyle = 'rgba(255,255,255,.94)';
  ctx.fillRect(p[0]-5, p[1]-14, w+10, 20);
  ctx.strokeStyle = '#e2e8f0'; ctx.lineWidth = 1;
  ctx.strokeRect(p[0]-5, p[1]-14, w+10, 20);
  ctx.fillStyle = '#475569';
  ctx.fillText(txt, p[0], p[1]);
  ctx.restore();
}"""

# ================================================================ ⑤ 初始化
SETUP_JS = r"""/* 本场景无需额外初始化（所有量由 stateAt 按 t 推出） */
  bindDrag();
  function bindDrag(){
    const cvEl = document.getElementById('cv');
    let dragging = false;
    cvEl.style.cursor = 'ew-resize';
    cvEl.addEventListener('pointerdown', function(e){
      dragging = true; cvEl.setPointerCapture(e.pointerId); apply(e);
    });
    cvEl.addEventListener('pointermove', function(e){ if (dragging) apply(e); });
    cvEl.addEventListener('pointerup', function(e){ dragging = false; });
    function apply(e){
      const rect = cvEl.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width;
      window.__setProgress(x);
    }
  }"""

# ================================================================ ⑥ 逐帧绘制
DRAW_JS = r"""  const st  = stateAt(t);
  const th  = st.th;
  const cO  = W2S(st.cx, st.cy);          // 圆心
  const cA  = W2S(st.ax, st.ay);          // 轮缘点 a
  const rpx = R_RING * scale;
  const deg = th * 180 / Math.PI;         // 世界系（向上为正）角度，可直接喂给 angleArc
  const START_DEG = 90;                   // a 在 t=0 时的方位角（最高点）

  /* ===== ① 背景层：地面 + 点标记 ===== */
  FIG.ground(-0.2, 7.15, 0, {gap: 0.16, hatchLen: 0.9});
  ctx.save();
  ctx.fillStyle = '#cbd5e1';
  for (let i = 0; i < GROUND_MARKS.length; i++){
    const mx = GROUND_MARKS[i], p = W2S(mx, 0);
    const big = Math.abs(mx - Math.round(mx)) < 1e-6;
    ctx.beginPath();
    ctx.arc(p[0], p[1], big ? 2.6 : 1.6, 0, TWO_PI);
    ctx.fill();
  }
  ctx.restore();
  FIG.text(3.68, -0.33, '地面（无滑滚动）', {size: 12, color: '#94a3b8', align: 'center'});
  FIG.text(3.68, 0.14, '水平轴 x /m', {size: 12, color: '#94a3b8', align: 'center'});

  /* ===== ② 轨迹层：完整摆线（浅灰虚线）+ 已走过部分（实线蓝） ===== */
  FIG.trajectory(cycloidPts(TWO_PI * 2), {color: '#cbd5e1', lw: 1.6, dash: [5, 4]});
  if (th > 0.02) FIG.trajectory(cycloidPts(th), {color: '#2563eb', lw: 2});
  FIG.text(6.55, 0.40, '摆线（旋轮线）', {size: 12, color: '#2563eb'});

  /* ===== ③ 圆环本体 ===== */
  ctx.strokeStyle = '#1e3a8a'; ctx.lineWidth = 2.6;
  ctx.beginPath(); ctx.arc(cO[0], cO[1], rpx, 0, TWO_PI); ctx.stroke();
  /* 半径虚线 O'a */
  if (th > 0.03) dashed(st.cx, st.cy, st.ax, st.ay, '#93a3b8', [4, 3]);
  /* 环上两条十字辐条（随环转动，直观显示 θ） */
  ctx.save();
  ctx.strokeStyle = '#c7d2fe'; ctx.lineWidth = 2;
  for (let k = 0; k < 2; k++){
    const a = (START_DEG - deg + k * 180) * Math.PI / 180;
    ctx.beginPath(); ctx.moveTo(cO[0], cO[1]);
    ctx.lineTo(cO[0] + rpx * Math.cos(a), cO[1] - rpx * Math.sin(a));
    ctx.stroke();
  }
  ctx.restore();
  FIG.particle(st.cx, st.cy, 0.055, '', {color: '#1e3a8a'});
  FIG.text(st.cx - 0.09, st.cy + 0.06, "O'", {size: 13, color: '#1e3a8a', align: 'right'});
  /* 轮缘点 a */
  ctx.fillStyle = '#dc2626';
  ctx.beginPath(); ctx.arc(cA[0], cA[1], 6, 0, TWO_PI); ctx.fill();
  ctx.strokeStyle = '#fff'; ctx.lineWidth = 1.6; ctx.stroke();
  FIG.text(st.ax + 0.10, st.ay - 0.10, 'a', {size: 15, color: '#dc2626'});
  /* 接触点 P（瞬时静止） */
  if (th > 0.05){
    const cP = W2S(st.cx, 0);
    ctx.fillStyle = '#94a3b8';
    ctx.beginPath(); ctx.arc(cP[0], cP[1], 3.4, 0, TWO_PI); ctx.fill();
    FIG.text(st.cx + 0.02, -0.20, 'P（接触点，瞬时静止）', {size: 11, color: '#94a3b8'});
  }

  /* ===== ④ 滚动角 θ 弧 ===== */
  FIG.angleArc(st.cx, st.cy, 0.30, 0, 90, '', {color: '#93a3b8'});
  FIG.angleArc(st.cx, st.cy, 0.30, 90 - deg, 90, '', {color: '#b45309'});
  FIG.text(st.cx + 0.40, st.cy + 0.36, 'θ = ωt', {size: 13, color: '#b45309'});

  /* ===== ⑤ 速度分解（配速法核心） ===== */
  const vp = [V_CM, 0];                                            // 平动分速度 v
  const vt = [V_CM * Math.cos(th), -V_CM * Math.sin(th)];           // 转动分速度 ωR（切向）
  const vr = [vp[0] + vt[0], vp[1] + vt[1]];                        // 合速度 v_a

  /* 平行四边形（虚线，先画，位于矢量下方） */
  ctx.save();
  ctx.strokeStyle = '#a5b4fc'; ctx.lineWidth = 1.4; ctx.setLineDash([4, 3]);
  ctx.beginPath();
  ctx.moveTo(cA[0], cA[1]);
  ctx.lineTo(cA[0] + vt[0] * scale, cA[1] - vt[1] * scale);
  ctx.lineTo(cA[0] + vr[0] * scale, cA[1] - vr[1] * scale);
  ctx.stroke();
  ctx.restore();
  /* 平动分速度 v 的平移到 a 的辅助虚线 */
  dashed(st.ax, st.ay, st.ax + vp[0], st.ay, '#c7d2fe', [3, 3]);

  const vrLen = Math.hypot(vr[0], vr[1]);
  /* 转动分速度 ωR（橙色） */
  if (V_CM * scale > 12){
    FIG.vec(st.ax, st.ay, vt[0], vt[1], '', {color: '#ea580c', lw: 3, head: 9});
    const midT = W2S(st.ax + vt[0]*0.5, st.ay + vt[1]*0.5);
    FIG.text(st.ax + vt[0] + (vt[0] >= 0 ? 0.08 : -0.08),
             st.ay + vt[1] + (vt[1] >= 0 ? 0.16 : -0.16),
             'ωR', {size: 13, color: '#ea580c', align: vt[0] >= 0 ? 'left' : 'right'});
  }
  /* 平动分速度 v（绿色） */
  if (V_CM * scale > 12){
    FIG.vec(st.ax, st.ay, vp[0], 0, '', {color: '#059669', lw: 3, head: 9});
    FIG.text(st.ax + vp[0] + 0.08, st.ay - 0.10, 'v', {size: 13, color: '#059669'});
  }
  /* 合速度 v_a（红色，像素长度足够才画标签） */
  if (vrLen * scale > 14){
    FIG.vec(st.ax, st.ay, vr[0], vr[1], '', {color: '#dc2626', lw: 3.4, head: 11});
    FIG.text(st.ax + vr[0] + (vr[0] >= 0 ? 0.10 : -0.10),
             st.ay + vr[1] + (vr[1] >= 0 ? 0.20 : -0.16),
             'v_a', {size: 15, color: '#dc2626', align: vr[0] >= 0 ? 'left' : 'right'});
  }
  stackNote();

  /* ===== ⑥ 固定叠加视图：t=0 的「ωR + v = 0」几何证明 ===== */
  const dx0 = cA[0] + Math.max(1.10, rpx * 1.25 + 0.40);
  const dy0 = cA[1] - rpx * 0.32;
  ctx.fillStyle = '#f8fafc';
  ctx.strokeStyle = '#e2e8f0'; ctx.lineWidth = 1.2;
  ctx.beginPath();
  ctx.roundRect(dx0 - 8, dy0 - 44, 152, 66, 8);
  ctx.fill(); ctx.stroke();
  ctx.fillStyle = '#64748b'; ctx.font = 'bold 11.5px sans-serif';
  ctx.fillText("t = 0（第 0 帧）", dx0, dy0 - 28);
  ctx.fillText("a 在最高点：", dx0, dy0 - 12);
  ctx.font = 'bold 12.5px sans-serif';
  ctx.fillStyle = '#059669'; ctx.fillText("v", dx0, dy0 + 6);
  ctx.fillStyle = '#64748b'; ctx.fillText("（向右） +", dx0 + 10, dy0 + 6);
  ctx.fillStyle = '#ea580c'; ctx.fillText("ωR", dx0 + 62, dy0 + 6);
  ctx.fillStyle = '#64748b'; ctx.fillText("（向左）", dx0 + 88, dy0 + 6);
  ctx.fillStyle = '#dc2626'; ctx.font = 'bold 13px sans-serif';
  ctx.fillText("= 0　瞬时静止", dx0, dy0 + 24);

  /* ===== ⑦ 右上角 θ / 圈数读数 ===== */
  const bw = 118, bh = 52, bx = cv.clientWidth - bw - 10, by = 10;
  ctx.fillStyle = 'rgba(255,255,255,.92)';
  ctx.strokeStyle = '#e2e8f0'; ctx.lineWidth = 1;
  ctx.beginPath(); ctx.roundRect(bx, by, bw, bh, 8); ctx.fill(); ctx.stroke();
  ctx.fillStyle = '#b45309'; ctx.font = 'bold 13px monospace';
  ctx.fillText('θ = ' + (th / Math.PI).toFixed(2) + 'π', bx + 10, by + 20);
  ctx.fillStyle = '#1e3a8a';
  ctx.fillText('n = ' + st.turn.toFixed(2) + ' 圈', bx + 10, by + 38);
  if (st.frozen){
    ctx.fillStyle = '#94a3b8'; ctx.font = 'bold 11px sans-serif';
    ctx.fillText('（已定格）', bx + 10, by + 52);
  }

  /* ===== ⑧ 画面图例 ===== */
  const lx = W2S(-1.10, 4.62), ly = lx[1];
  const legend = [
    ['#dc2626', 'v_a = v + ωR　配速法合速度'],
    ['#059669', 'v = ωR　圆心平动分速度'],
    ['#ea580c', 'ωR　绕心转动分速度'],
    ['#2563eb', '摆线轨迹（已走过）']
  ];
  ctx.font = 'bold 11.5px sans-serif';
  for (let i = 0; i < legend.length; i++){
    const yy = ly + i * 17;
    ctx.strokeStyle = legend[i][0]; ctx.lineWidth = 2.6;
    ctx.beginPath(); ctx.moveTo(lx[0], yy - 4); ctx.lineTo(lx[0] + 16, yy - 4); ctx.stroke();
    ctx.fillStyle = '#475569';
    ctx.fillText(legend[i][1], lx[0] + 22, yy);
  }"""

# ================================================================ ⑦ 数据面板
READOUTS_JS = r"""  const st = stateAt(t);
  return [
    ["滚动角 $\\theta$",       (st.th / Math.PI).toFixed(2) + "π", "rad"],
    ["已滚圈数 $n$",           st.turn.toFixed(2), "圈"],
    ["圆心位移 $s = R\\theta$", st.s.toFixed(3), "m"],
    ["圆心速率 $v$",           st.va >= 0 ? V_CM.toFixed(1) : "", "m/s"],
    ["平动分速度 $v$",         V_CM.toFixed(2), "m/s"],
    ["转动分速度 $\\omega R$",  (OMEGA * R_RING).toFixed(2), "m/s"],
    ["a 点速率 $v_a$",          st.va.toFixed(2), "m/s"],
    ["a 点加速度 $a_a$",        st.acc.toFixed(1), "m/s²"],
    ["摆线峰高 $2R$",           (2 * R_RING).toFixed(1), "m"],
    ["摆线周期 $2\\pi R$",      (TWO_PI * R_RING).toFixed(3), "m"]
  ];"""


def build_fig_data_uri():
    """本题走 Canvas 孪生锁定（__CANVAS_STATIC__），不需要外部位图。"""
    return None


def main():
    with io.open(TPL, encoding="utf-8") as f:
        out = f.read()

    # ---------- ① PROBLEM ----------
    pat = re.compile(r"const PROBLEM = \{.*?\n\};", re.S)
    hits = pat.findall(out)
    assert len(hits) == 1, "PROBLEM anchor not unique: %d" % len(hits)
    out = pat.sub(lambda m: PROBLEM_JS, out, count=1)

    # ---------- ② STEPS ----------
    pat = re.compile(r"const STEPS = \[.*?\n\];", re.S)
    hits = pat.findall(out)
    assert len(hits) == 1, "STEPS anchor not unique: %d" % len(hits)
    out = pat.sub(lambda m: STEPS_JS, out, count=1)

    # ---------- ③ VIEW / SIM ----------
    old_view = "const VIEW = { xmin: -1, xmax: 11, ymin: -1, ymax: 7 };"
    old_sim = "const SIM  = { duration: 4 };"
    assert out.count(old_view) == 1, "VIEW anchor not unique"
    assert out.count(old_sim) == 1, "SIM anchor not unique"
    out = out.replace(old_view, VIEW_JS).replace(old_sim, SIM_JS)

    # ---------- ④~⑦ 四个 token ----------
    for token, repl, name in (
        ("/*__GLOBALS__*/", GLOBALS_JS, "GLOBALS"),
        ("/*__SETUP__*/", SETUP_JS, "SETUP"),
        ("/*__DRAWFRAME__*/", DRAW_JS, "DRAWFRAME"),
        ("/*__READOUTS__*/", READOUTS_JS, "READOUTS"),
    ):
        cnt = out.count(token)
        assert cnt == 1, "%s token count = %d" % (name, cnt)
        out = out.replace(token, repl)

    # ---------- 题图尺寸覆写：孪生锁定画布按 2:1 呈现（与画布比例一致，不裁切） ----------
    css_add = (
        "\n  /* 配速法摆线：题图用孪生锁定画布，按画布本身比例放大显示 */\n"
        "  .fig-canvas{max-width:430px;max-height:215px}\n"
        "  .fig:has(.fig-canvas){max-width:100%}\n"
    )
    assert out.count("</style>") == 1
    out = out.replace("</style>", css_add + "</style>", 1)

    with io.open(OUT, "w", encoding="utf-8") as f:
        f.write(out)

    # ---------- 探针自检 ----------
    probes = [
        ("配速法·摆线（旋轮线）", "题目标题"),
        ("mech-circular-horizontal", "知识点 id 1"),
        ("princ-relative-motion", "知识点 id 2"),
        ("__CANVAS_STATIC__", "孪生锁定占位"),
        ("function stateAt(t)", "GLOBALS.stateAt"),
        ("function cycloidPts(", "GLOBALS.cycloidPts"),
        ("function stackNote(", "GLOBALS.stackNote"),
        ("const st  = stateAt(t);", "DRAW 入口"),
        ("FIG.trajectory(cycloidPts(TWO_PI * 2)", "完整摆线"),
        ("= 0　瞬时静止", "t=0 叠加说明"),
        ("a 点速率", "数据面板"),
        ("bindDrag", "画布拖拽"),
        ("x_a = R\\\\theta + R\\\\sin\\\\theta", "参数方程"),
        ("t0: 6.2832", "末步 t0 字面量"),
    ]
    print("=" * 56)
    for key, label in probes:
        print("[%s] %s  ->  %s" % ("FOUND" if key in out else "MISSING", label, key[:44]))
    # 死区自检：STEPS 的字面量里不得出现 GLOBALS 的 const 名（用 python 变量在构建期注入）
    steps_zone = STEPS_JS
    for bad in ("T_ROLL", "T_END", "TWO_PI", "V_CM", "OMEGA", "R_RING", "GROUND_MARKS"):
        if re.search(r"\b" + bad + r"\b", steps_zone):
            print("[!!! FATAL] STEPS 引用了 GLOBALS 常量 %s —— 会命中 const 死区，必须改为字面数字" % bad)
    print("STEPS 死区自检完成（以上无 FATAL 即通过）")
    print("=" * 56)
    print("输出：%s  (%.1f KB)" % (OUT, len(out.encode("utf-8")) / 1024.0))


if __name__ == "__main__":
    main()
