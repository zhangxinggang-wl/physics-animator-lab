# -*- coding: utf-8 -*-
"""由 assets/template.html 生成「铁环滚动三圈半」教学动画 HTML。

题目：水平面上 A 处放置一半径为 r 的铁环，最高点为 a，A 右侧 B 处有竖直墙面，
      墙上固定磁铁（厚度不计）。给铁环一水平速度，滚过三圈半后恰好被磁铁吸住。
      —— 正确选项 C：AB = 7πr + r。

物理要点（令 r = 1、ω = 3.5 rad/s ⇒ v = 3.5 m/s）：
  · 纯滚动 s = rθ，θ_end = 7π ⇒ s = 7πr，AB = 7πr + r ≈ 22.99r
  · a 点轨迹为旋轮线：x = rθ + r sinθ, y = r + r cosθ；转过 7π 后 a 由最高点转到最低点
  · a 点位移 = r√(49π² + 4) ≈ 22.08r（与选项 D 的 r√(49π² + 1) 不同）

注意：本文件中的 JS 代码块用 Python 原始字符串保存，因此 JS 字符串字面量里的
      LaTeX 反斜杠必须写成两个反斜杠（\\theta），否则 JS 会把 \t 当制表符吃掉。
"""
import base64
import io
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TPL = os.path.join(ROOT, "assets", "template.html")
OUT = os.path.join(ROOT, "2026-09-13_铁环滚动三圈半_教学动画.html")

# ===========================================================================
# ① PROBLEM
# ===========================================================================
PROBLEM_JS = r"""const PROBLEM = {
  title: "",   // 原题仅有题号 7.，故不另拟标题
  /* 题干：与原题逐字一致（含题号与卷面上已填的答案标记） */
  given: "7.水平面上$A$处放置有一半径为$r$的铁环，铁环的最高点为$a$，在$A$处的右侧$B$处有一竖直墙面，墙面上固定有一磁铁(厚度不计)，如图所示。现给铁环一水平速度，在水平面上滚动了三圈半后恰好被磁铁吸住，则( C )",

  /* 题图：方式① 嵌入题目原图（从整页截图中裁出图形区域后转 data URI）。
     本题原图为示意图——A、B 画得很近，而实际 AB = 7πr + r ≈ 23r，
     无法在「真实比例」下做到像素级孪生，故保留原图原貌；
     右栏动画另按真实比例绘制，比例差异已在解析中说明。 */
  images: [
    { src: "__FIG_DATA_URI__", caption: "题图：水平面上的铁环与右侧墙面上的磁铁", pos: "bottom" }
  ],

  /* 选择题：A/B/C/D 四项完整录入（模板在题图下方渲染） */
  options: [
    "A.研究铁环上$a$点的运动时，可以将铁环看成质点",
    "B.铁环运动过程中，铁环上的$a$点相对于圆心静止",
    "C.$A$、$B$间的距离等于$7\\pi r+r$",
    "D.铁环从$A$处滚动到$B$处的过程中，$a$点发生的位移大小为$r\\sqrt{1+49\\pi^{2}}$"
  ],

  asks: [],

  knowledgePoints: [
    { id: "princ-modeling" },
    { id: "princ-relative-motion" },
    { id: "princ-vector-basics" }
  ]
};"""

# ===========================================================================
# ② STEPS
# ===========================================================================
STEPS_JS = r"""const STEPS = [
  {
    title: "选项 $A$：研究环上 $a$ 点的运动时能否视为质点",
    tex: "x_a = r\\theta + r\\sin\\theta,\\qquad y_a = r + r\\cos\\theta",
    note: "取 $A$ 点正上方为原点、$x$ 轴水平向右、$y$ 轴竖直向上。铁环滚过角 $\\theta$ 时环心平动 $s = r\\theta$，环上 $a$ 点（初始位于最高点）的坐标即上式的两式：水平方向随环心一起平动、竖直方向随铁环转动而起伏，其轨迹是一条旋轮线。可见环心走的是直线、$a$ 点走的是旋轮线，环上各点的运动情况互不相同，且都与半径 $r$ 直接相关。因此在研究 $a$ 点的运动时，铁环的大小和形状不能忽略，不能把它看成质点。故 A 错误。",
    basis: "质点模型的适用条件：物体的大小、形状对所研究的问题影响可忽略",
    t0: 0, t1: 1.40
  },
  {
    title: "选项 $B$：$a$ 点相对环心是否静止",
    tex: "v_{a/O} = \\omega r \\neq 0",
    note: "以环心 $O$ 为参考系，$a$ 点绕 $O$ 做半径为 $r$ 的匀速圆周运动，它与环心的相对速度大小恒为 $\\omega r$、方向沿圆环的切线，在整个滚动过程中始终不为零（会瞬时为零的是它相对地面的速度：在最高点 $v_a = 0$，在最低点 $v_a = 2v$，这与「相对环心」是两回事）。既然相对环心的速度不为零，$a$ 点相对环心就不是静止的。故 B 错误。",
    basis: "相对运动；匀速圆周运动的线速度 $v = \\omega r$",
    t0: 1.40, t1: 2.80
  },
  {
    title: "选项 $C$：纯滚动距离叠加「恰好被吸住」的几何条件",
    tex: "\\overline{AB} = 3.5 \\times 2\\pi r + r = (7\\pi + 1)r",
    note: "铁环在水平面上纯滚动（与地面无相对滑动）时，环心前进的距离等于轮缘滚过的弧长，即 $s = r\\theta$。滚过三圈半，$\\theta = 3.5 \\times 2\\pi = 7\\pi$，故环心前进 $s = 7\\pi r$。又「恰好被磁铁吸住」说明环的右缘刚好与墙面接触（磁铁厚度不计），此时环心到墙面的距离恰好等于一个半径 $r$。所以 $\\overline{AB} = 7\\pi r + r$，C 正确。",
    basis: "纯滚动（不打滑）条件：环心位移 = 轮缘滚过的弧长；「恰好接触」⇒ 环心距墙一个半径",
    t0: 2.80, t1: 6.40
  },
  {
    title: "选项 $D$：$a$ 点位移由初、末位置决定",
    tex: "\\Delta s_a = \\sqrt{(7\\pi r)^{2} + (2r)^{2}} = r\\sqrt{49\\pi^{2} + 4}",
    note: "位移只由初位置指向末位置，与路径无关。初始时 $a$ 点在环的最高点，若以 $A$ 点正上方 $r$ 处的环心初始位置为参考，则初坐标为 $(0,\\ 2r)$。铁环共转过 $7\\pi$ 弧度，而 $7\\pi = 3 \\times 2\\pi + \\pi$，即整三圈再加半圈，$a$ 点由最高点恰好转到最低点（与地面的接触点），末坐标为 $(7\\pi r,\\ 0)$。于是水平分量为 $7\\pi r$、竖直分量为 $2r$（恰好是一个直径），得 $\\Delta s_a = r\\sqrt{49\\pi^{2} + 4} \\approx 22.08r$。选项 D 给出 $r\\sqrt{49\\pi^{2} + 1}$，把竖直分量 $2r$ 误算成了 $r$，故 D 错误。",
    basis: "位移的定义：由初位置指向末位置的有向线段，大小与路径无关",
    t0: 6.40, t1: 6.92
  },
  {
    title: "结论：只有 $C$ 正确",
    tex: "\\overline{AB} = 7\\pi r + r,\\qquad \\Delta s_a = r\\sqrt{49\\pi^{2} + 4}",
    note: "A、B 两项是概念错误，D 项把竖直分量算错，只有 C 正确，故选 C。特别提醒：题图是示意图，$A$、$B$ 画得很近；右栏动画按真实比例绘制，$\\overline{AB} = 7\\pi r + r \\approx 23.0r$，所以铁环在画面中显得较小，它绕环心转动的细节请看画面上方的放大视图。",
    basis: "选择题逐项排除：A、B 为概念错误，D 为数值错误",
    t0: 6.92, t1: 7.40
  }
];"""

# ===========================================================================
# ③ VIEW / SIM
# ===========================================================================
VIEW_JS = "const VIEW = { xmin: -1.5, xmax: 24.3, ymin: -2.6, ymax: 12.73 };"
SIM_JS = "const SIM  = { duration: 7.40 };"

# ===========================================================================
# ④ GLOBALS（无 LaTeX，无反斜杠）
# ===========================================================================
GLOBALS_JS = r"""
/* =========================================================================
   本题物理参数与几何（世界坐标：x 向右、y 向上，地面取 y = 0）
   —— 长度以铁环半径 r 为单位，令 r = 1，所有结论可直接按比例读出。
   纯滚动（不打滑）⇒ 环心位移 s = rθ；取 ω = 3.5 rad/s ⇒ v = ωr = 3.5 m/s，
   滚过三圈半（θ = 7π）用时 T = 7π/ω = 2π ≈ 6.283 s。
   ========================================================================= */
const R_RING  = 1.0;                             // 铁环半径 r
const OMEGA   = 3.5;                             // 角速度 ω (rad/s)
const V_CM    = OMEGA * R_RING;                  // 环心平动速度 v = ωr (m/s)
const TURNS   = 3.5;                             // 滚动圈数
const TH_END  = 2 * Math.PI * TURNS;             // 总转角 θ_end = 7π (rad)
const S_END   = R_RING * TH_END;                 // 环心滚过的距离 s = 7πr
const XB_WALL = S_END + R_RING;                  // A、B 间距 AB = 7πr + r
const T_ROLL  = TH_END / OMEGA;                  // 滚动总时长 = 2π s
const DS_A    = Math.hypot(S_END, 2 * R_RING);   // a 点位移 = r√(49π²+4)
const AN_A    = OMEGA * OMEGA * R_RING;          // a 点向心加速度 ω²r (m/s²)
const Y_WALL  = 3.4, Y_MAG = 2.9;                // 墙面 / 磁铁的绘图高度（按原图比例）
const A_X0 = 0, A_Y0 = 2 * R_RING;               // a 点初位置（环的最高点）

/* 运动状态：画面 drawSceneBody 与数据面板 readouts 共用同一函数，
   从机制上杜绝「画面一套数、面板另一套数」。t ≥ T_ROLL 时定格于末状态。 */
function stateAt(t){
  const tt = Math.min(t, T_ROLL);
  const th = OMEGA * tt;                            // θ(t) = ωt
  const s  = R_RING * th;                           // 环心位移 s(t) = rθ
  const cx = s, cy = R_RING;                        // 环心坐标 (rθ, r)
  const ax = cx + R_RING * Math.sin(th);            // a 点：旋轮线
  const ay = cy + R_RING * Math.cos(th);
  const va = 2 * V_CM * Math.abs(Math.sin(th / 2)); // a 点速率 = 2v·|sin(θ/2)|
  return {
    tt: tt, th: th, s: s, cx: cx, cy: cy, ax: ax, ay: ay,
    turns: th / (2 * Math.PI),                      // 已转过的圈数 n
    va: va,                                         // a 点速率 v_a
    dsa: Math.hypot(ax - A_X0, ay - A_Y0),          // a 点位移（初位置 → 当前位置）
    frozen: t >= T_ROLL
  };
}

/* 旋轮线轨迹（世界坐标，可选虚线；随滚动生长） */
function traceCycloid(thMax, color, dash){
  if (thMax < 0.02) return;
  const n = Math.max(2, Math.round(1000 * thMax / TH_END));
  ctx.save();
  ctx.strokeStyle = color; ctx.lineWidth = 1.6;
  if (dash) ctx.setLineDash(dash);
  ctx.beginPath();
  for (let i = 0; i <= n; i++){
    const th = thMax * i / n;
    const p = W2S(R_RING * th + R_RING * Math.sin(th), R_RING + R_RING * Math.cos(th));
    if (i) ctx.lineTo(p[0], p[1]); else ctx.moveTo(p[0], p[1]);
  }
  ctx.stroke();
  ctx.restore();
}

/* 双箭头尺寸线（世界坐标，横向） */
function dimLine(x1, x2, y, color, label, labelBelow){
  const a = W2S(x1, y), b = W2S(x2, y);
  ctx.save();
  ctx.strokeStyle = color; ctx.fillStyle = color; ctx.lineWidth = 1.6;
  ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.lineTo(b[0], b[1]); ctx.stroke();
  function head(px, py, dir){
    ctx.beginPath(); ctx.moveTo(px, py);
    ctx.lineTo(px + dir * 9, py - 4.5); ctx.lineTo(px + dir * 9, py + 4.5);
    ctx.closePath(); ctx.fill();
  }
  head(a[0], a[1], 1); head(b[0], b[1], -1);
  if (label){
    ctx.font = 'bold 12px sans-serif'; ctx.textAlign = 'center';
    ctx.fillText(label, (a[0] + b[0]) / 2, a[1] + (labelBelow ? 14 : -6));
  }
  ctx.restore();
}

/* 顶部实时角度显示器：θ(t) 同时给出度与弧度（[GREEK_VARIABLE] 强制） */
function drawHUD(st){
  const deg = st.th * 180 / Math.PI;
  ctx.save();
  ctx.textAlign = 'left'; ctx.font = 'bold 13px sans-serif'; ctx.fillStyle = '#1d4ed8';
  ctx.fillText('铁环纯滚动 → 恰被磁铁吸住', 10, 19);
  ctx.textAlign = 'right'; ctx.font = 'bold 13px sans-serif'; ctx.fillStyle = '#b45309';
  ctx.fillText('θ(t) = ' + deg.toFixed(1) + '° = ' + st.th.toFixed(3) + ' rad', W - 10, 19);
  ctx.font = 'bold 12px sans-serif'; ctx.fillStyle = '#475569';
  ctx.fillText('n = ' + st.turns.toFixed(2) + ' 圈      s = rθ = ' + st.s.toFixed(2) + ' m', W - 10, 36);
  if (st.frozen){
    ctx.textAlign = 'left'; ctx.fillStyle = '#dc2626'; ctx.font = 'bold 12px sans-serif';
    ctx.fillText('末态：a 恰好转到最低点（即与地面的接触点）', 10, 56);
  }
  ctx.restore();
}

/* 放大视图：把铁环放大到固定像素尺寸，展示 a 点绕环心的匀速圆周运动 */
function drawZoom(st){
  const mx = W / 2, my = 114, MR = 50;
  ctx.save();
  /* 说明文字（放在圆环左侧固定位置；下方以底衬白底遮住可能与之重叠的
     「v = ωr」标签——a 转到左上方时两者会相撞，白底相当于给文字让位） */
  ctx.fillStyle = '#64748b'; ctx.font = '11px sans-serif'; ctx.textAlign = 'right';
  const zx1 = mx - MR - 12;
  ctx.fillStyle = 'rgba(255,255,255,0.94)';
  ctx.fillRect(zx1 - 122, my - 22, 128, 40);
  ctx.fillStyle = '#64748b';
  ctx.fillText('放大视图', zx1, my - 6);
  ctx.fillText('a 点绕环心匀速转动', zx1, my + 10);
  /* 环 */
  ctx.strokeStyle = '#1d4ed8'; ctx.lineWidth = 2.2;
  ctx.beginPath(); ctx.arc(mx, my, MR, 0, 7); ctx.stroke();
  /* 转动前的参照半径（竖直向上，虚线） */
  ctx.strokeStyle = '#cbd5e1'; ctx.lineWidth = 1; ctx.setLineDash([4, 3]);
  ctx.beginPath(); ctx.moveTo(mx, my); ctx.lineTo(mx, my - MR); ctx.stroke();
  ctx.setLineDash([]);
  /* 已转过的角 θ 的圆弧（自正上方起、顺时针，最多画满一圈） */
  const RARC = MR * 0.40, phMax = Math.min(st.th, 2 * Math.PI);
  if (phMax > 0.03){
    const n = Math.max(2, Math.round(80 * phMax / (2 * Math.PI)));
    ctx.strokeStyle = '#f59e0b'; ctx.lineWidth = 2;
    ctx.beginPath();
    for (let i = 0; i <= n; i++){
      const ph = phMax * i / n;
      const px = mx + RARC * Math.sin(ph), py = my - RARC * Math.cos(ph);
      if (i) ctx.lineTo(px, py); else ctx.moveTo(px, py);
    }
    ctx.stroke();
    const phl = phMax / 2;
    ctx.fillStyle = '#b45309'; ctx.font = 'italic bold 13px serif'; ctx.textAlign = 'center';
    ctx.fillText('θ', mx + RARC * 1.55 * Math.sin(phl), my - RARC * 1.55 * Math.cos(phl) + 4);
  }
  /* 半径线 O → a 与环心 O */
  const axm = mx + MR * Math.sin(st.th), aym = my - MR * Math.cos(st.th);
  ctx.strokeStyle = 'rgba(220,38,38,.8)'; ctx.lineWidth = 1.6;
  ctx.beginPath(); ctx.moveTo(mx, my); ctx.lineTo(axm, aym); ctx.stroke();
  ctx.fillStyle = '#1d4ed8'; ctx.beginPath(); ctx.arc(mx, my, 2.6, 0, 7); ctx.fill();
  ctx.font = 'italic bold 13px serif'; ctx.textAlign = 'left';
  ctx.fillText('O', mx + 5, my + 15);
  /* a 点及其相对速度矢量（切向，大小恒为 ωr ⇒ 箭头长度恒定，正比于标量） */
  ctx.fillStyle = '#dc2626'; ctx.beginPath(); ctx.arc(axm, aym, 4.2, 0, 7); ctx.fill();
  ctx.font = 'italic bold 14px serif'; ctx.textAlign = 'center';
  ctx.fillText('a', mx + (MR + 14) * Math.sin(st.th), my - (MR + 14) * Math.cos(st.th) + 5);
  const VL = 24, vdx = Math.cos(st.th) * VL, vdy = Math.sin(st.th) * VL;
  ctx.strokeStyle = '#dc2626'; ctx.fillStyle = '#dc2626'; ctx.lineWidth = 2;
  ctx.beginPath(); ctx.moveTo(axm, aym); ctx.lineTo(axm + vdx, aym + vdy); ctx.stroke();
  const angv = Math.atan2(vdy, vdx), HL = 9;
  ctx.beginPath(); ctx.moveTo(axm + vdx, aym + vdy);
  ctx.lineTo(axm + vdx - HL * Math.cos(angv - 0.42), aym + vdy - HL * Math.sin(angv - 0.42));
  ctx.lineTo(axm + vdx - HL * Math.cos(angv + 0.42), aym + vdy - HL * Math.sin(angv + 0.42));
  ctx.closePath(); ctx.fill();
  ctx.font = 'italic bold 12px serif';
  ctx.textAlign = vdx >= 0 ? 'left' : 'right';
  /* 标签放到矢量末端、沿箭头方向再外推一点，避免箭头三角与文字相叠 */
  ctx.fillText('v = ωr', axm + vdx + (vdx >= 0 ? 7 : -7), aym + vdy + (vdy >= 0 ? 13 : -6));
  /* 向心加速度矢量（指向环心，大小恒为 ω²r） */
  const AL = 17, adx = -Math.sin(st.th) * AL, ady = Math.cos(st.th) * AL;
  ctx.strokeStyle = '#0891b2'; ctx.fillStyle = '#0891b2'; ctx.lineWidth = 1.8;
  ctx.beginPath(); ctx.moveTo(axm, aym); ctx.lineTo(axm + adx, aym + ady); ctx.stroke();
  const anga = Math.atan2(ady, adx);
  ctx.beginPath(); ctx.moveTo(axm + adx, aym + ady);
  ctx.lineTo(axm + adx - 7 * Math.cos(anga - 0.42), aym + ady - 7 * Math.sin(anga - 0.42));
  ctx.lineTo(axm + adx - 7 * Math.cos(anga + 0.42), aym + ady - 7 * Math.sin(anga + 0.42));
  ctx.closePath(); ctx.fill();
  ctx.font = 'italic bold 11px serif'; ctx.textAlign = 'center';
  ctx.fillText('向心加速度 ω²r', mx, my + MR + 31);
  ctx.restore();
}
"""

# ===========================================================================
# ⑤ SETUP
# ===========================================================================
SETUP_JS = r"""
  /* 无需预计算：旋轮线与各物理量均在 stateAt() 与各绘制函数中由同一组公式实时给出，
     保证「画面 = 解析」。此处只做一次性自检（控制台可查 window.__RING）。 */
  window.__RING = {
    r: R_RING, omega: OMEGA, v: V_CM,
    theta_end: TH_END, turns: TURNS,
    s_end: S_END, s_end_check: 7 * Math.PI,
    AB: XB_WALL, AB_check: 7 * Math.PI + 1,
    T_roll: T_ROLL,
    dsA: DS_A, dsA_check: Math.sqrt(49 * Math.PI * Math.PI + 4),
    dsA_optionD: Math.sqrt(49 * Math.PI * Math.PI + 1),
    an: AN_A
  };"""

# ===========================================================================
# ⑥ DRAWFRAME
# ===========================================================================
DRAW_JS = r"""
  const st = stateAt(t), th = st.th;

  /* ---------- 背景层：地面、墙面、磁铁、A/B 标记（固定不动） ---------- */
  FIG.ground(-1.4, XB_WALL, 0, { gap: 0.85, hatchLen: 3, color: '#334155' });
  /* 电磁铁：厚度不计 ⇒ 紧贴墙面的薄片（先画，墙线压在它右缘上才清晰） */
  (function(){
    const p1 = W2S(XB_WALL - 0.36, Y_MAG), p2 = W2S(XB_WALL, 0.06);
    ctx.fillStyle = '#9ca3af';
    ctx.fillRect(p1[0], p1[1], p2[0] - p1[0], p2[1] - p1[1]);
    ctx.strokeStyle = '#6b7280'; ctx.lineWidth = 1;
    ctx.strokeRect(p1[0], p1[1], p2[0] - p1[0], p2[1] - p1[1]);
  })();
  /* 墙面：整段竖线；只在磁铁之上露出的一小段加阴影，用于示意「固定墙」 */
  FIG.wall(XB_WALL, 0, Y_WALL, { hatchLen: 0, color: '#334155' });
  FIG.wall(XB_WALL, Y_MAG, Y_WALL, { gap: 0.34, hatchLen: 2.2, color: '#334155' });
  FIG.text(0, -1.05, 'A', { size: 14, align: 'center' });
  FIG.text(XB_WALL, -1.05, 'B', { size: 14, align: 'center' });

  /* ---------- a 点的旋轮线轨迹（随滚动生长） ---------- */
  traceCycloid(th, '#cbd5e1', [5, 4]);

  /* ---------- a 点的位移矢量：初位置 → 当前位置（与路径无关） ---------- */
  const p0 = W2S(A_X0, A_Y0), pa = W2S(st.ax, st.ay);
  if (Math.hypot(pa[0] - p0[0], pa[1] - p0[1]) > 14){
    ctx.save();
    ctx.strokeStyle = '#7c3aed'; ctx.fillStyle = '#7c3aed'; ctx.lineWidth = 2.4;
    ctx.beginPath(); ctx.moveTo(p0[0], p0[1]); ctx.lineTo(pa[0], pa[1]); ctx.stroke();
    const ang = Math.atan2(pa[1] - p0[1], pa[0] - p0[0]);
    ctx.beginPath(); ctx.moveTo(pa[0], pa[1]);
    ctx.lineTo(pa[0] - 11 * Math.cos(ang - 0.42), pa[1] - 11 * Math.sin(ang - 0.42));
    ctx.lineTo(pa[0] - 11 * Math.cos(ang + 0.42), pa[1] - 11 * Math.sin(ang + 0.42));
    ctx.closePath(); ctx.fill();
    ctx.beginPath(); ctx.arc(p0[0], p0[1], 3.2, 0, 7); ctx.fill();
    ctx.font = 'bold italic 13px serif'; ctx.textAlign = 'center';
    ctx.fillText('Δs_a', p0[0] + (pa[0] - p0[0]) * 0.32, p0[1] + (pa[1] - p0[1]) * 0.32 - 8);
    ctx.restore();
  }

  /* ---------- 尺寸线：s = rθ(t)（随滚动生长，蓝）+ r（橙） ⇒ AB = s + r ---------- */
  const yDim = -1.85;
  [0, XB_WALL].forEach(function(x){   /* 尺寸界线：自 A/B 标注下方拉到尺寸线下方 */
    const a1 = W2S(x, -1.40), b1 = W2S(x, yDim - 0.24);
    ctx.save(); ctx.strokeStyle = '#94a3b8'; ctx.lineWidth = 1; ctx.setLineDash([4, 3]);
    ctx.beginPath(); ctx.moveTo(a1[0], a1[1]); ctx.lineTo(b1[0], b1[1]); ctx.stroke();
    ctx.restore();
  });
  if (st.s > 0.06) dimLine(0, st.s, yDim, '#2563eb', 's = rθ(t) = ' + st.s.toFixed(2) + ' m');
  if (st.frozen){
    dimLine(S_END, XB_WALL, yDim, '#ea580c', 'r', true);
    const mid = W2S(XB_WALL / 2, yDim - 0.72);
    ctx.save();
    ctx.fillStyle = '#0f172a'; ctx.font = 'bold 12px sans-serif'; ctx.textAlign = 'center';
    ctx.fillText('AB = s + r = 7πr + r', mid[0], mid[1]);
    ctx.restore();
  }

  /* ---------- 铁环本体（环 + 环心 O + 半径线 + a 点） ---------- */
  const c = W2S(st.cx, st.cy);
  ctx.save();
  ctx.strokeStyle = '#1d4ed8'; ctx.lineWidth = 2.6;
  ctx.beginPath(); ctx.arc(c[0], c[1], R_RING * scale, 0, 7); ctx.stroke();
  ctx.strokeStyle = 'rgba(220,38,38,.7)'; ctx.lineWidth = 1.4; ctx.setLineDash([3, 3]);
  ctx.beginPath(); ctx.moveTo(c[0], c[1]); ctx.lineTo(pa[0], pa[1]); ctx.stroke();
  ctx.setLineDash([]);
  ctx.fillStyle = '#1d4ed8'; ctx.beginPath(); ctx.arc(c[0], c[1], 2.6, 0, 7); ctx.fill();
  ctx.fillStyle = '#dc2626'; ctx.beginPath(); ctx.arc(pa[0], pa[1], 4.2, 0, 7); ctx.fill();
  ctx.restore();
  FIG.text(st.ax, st.ay + 0.42, 'a', { size: 14, align: 'center', color: '#dc2626' });

  /* ---------- 顶部实时角度显示器 θ(t) 与放大视图 ---------- */
  drawHUD(st);
  drawZoom(st);
"""

# ===========================================================================
# ⑦ READOUTS
# ===========================================================================
READOUTS_JS = r"""
  const st = stateAt(t);
  const deg = st.th * 180 / Math.PI;
  return [
    ["$t$", "s"],
    ["$\\theta(t)$（度）", deg.toFixed(1), "°"],
    ["$\\theta(t)$（弧度）", st.th.toFixed(3), "rad"],
    ["$n$ 转过的圈数", st.turns.toFixed(2), "圈"],
    ["$s$ 环心位移", st.s.toFixed(2), "m"],
    ["$v_a$ $a$ 点速率", st.va.toFixed(2), "m/s"],
    ["$a_n$ 向心加速度", AN_A.toFixed(2), "m/s²"],
    ["$\\Delta s_a$ 位移大小", st.dsa.toFixed(2), "m"],
    ["$\\overline{AB}$", XB_WALL.toFixed(2), "m"]
  ];
"""


def build_fig_data_uri():
    """把裁好的题图 PNG 转成 data URI（纯标准库）。"""
    fig = os.path.join(HERE, "_fig_crop.png")
    if not os.path.exists(fig):
        raise SystemExit("missing %s" % fig)
    with open(fig, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode("ascii")


def main():
    tpl = io.open(TPL, encoding="utf-8").read()
    fig_uri = build_fig_data_uri()
    out = tpl

    # --- ① PROBLEM ---
    pat = re.compile(r"const PROBLEM = \{.*?\n\};", re.S)
    assert len(pat.findall(out)) == 1, "PROBLEM anchor not unique"
    out = pat.sub(lambda m: PROBLEM_JS.replace("__FIG_DATA_URI__", fig_uri), out, count=1)

    # --- ② STEPS ---
    pat = re.compile(r"const STEPS = \[.*?\n\];", re.S)
    assert len(pat.findall(out)) == 1, "STEPS anchor not unique"
    out = pat.sub(lambda m: STEPS_JS, out, count=1)

    # --- ③ VIEW / SIM ---
    old_view = "const VIEW = { xmin: -1, xmax: 11, ymin: -1, ymax: 7 };"
    old_sim = "const SIM  = { duration: 4 };"
    assert out.count(old_view) == 1 and out.count(old_sim) == 1, "VIEW/SIM anchor"
    out = out.replace(old_view, VIEW_JS).replace(old_sim, SIM_JS)

    # --- ④⑤⑥⑦ 占位符 ---
    for token, repl, name in (
        ("/*__GLOBALS__*/", GLOBALS_JS, "GLOBALS"),
        ("/*__SETUP__*/", SETUP_JS, "SETUP"),
        ("/*__DRAWFRAME__*/", DRAW_JS, "DRAWFRAME"),
        ("/*__READOUTS__*/", READOUTS_JS, "READOUTS"),
    ):
        assert out.count(token) == 1, "%s token count != 1" % name
        out = out.replace(token, repl)

    # --- ⑧ 题图尺寸覆写（本题原图是「宽扁」示意图，把显示上限适度放大以便看清；
    #        仅覆写 max-width/max-height，不改模板的居中与不铺满写法） ---
    css_anchor = "</style>"
    assert out.count(css_anchor) == 1, "</style> anchor not unique"
    out = out.replace(
        css_anchor,
        "  /* 本题题图是「宽扁」示意图（原图 480×146），放大显示上限以便看清 */\n"
        "  .fig img{max-width:300px;max-height:200px}\n" + css_anchor, 1)

    # --- ⑨ 关键内容自检（防止编辑丢失） ---
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(out)
    print("OK -> %s (%d bytes)" % (OUT, len(out.encode("utf-8"))))
    for probe in ("Y_WALL  = 3.4", "恰好转到最低点", "labelBelow", "mx - MR - 12",
                  "0.32", "max-width:300px"):
        print("  probe %-22s : %s" % (probe, "FOUND" if probe in out else "*** MISSING ***"))


if __name__ == "__main__":
    main()
