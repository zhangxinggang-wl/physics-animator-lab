# -*- coding: utf-8 -*-
"""生成《匀强电场 + 重力 + 分区磁场复合场》教学动画单文件 HTML。

【物理量纲约定】画布世界单位取 R1 = v^2/g，故
    z0 = 2v^2/(5g) = 0.4 R1,   P = (16v^2/(5g), 0) = (3.2 R1, 0)

【答案】
  (1) qE = mg  ⇒  E = mg/q ；第一次过 z=z0 平面的 x = 4v^2/(5g) = 0.8 R1
  (2) 令 r2 = R2/R1 = (k-2)/k，k = 相切点序号；时间最短取 k=3
      ⇒ r2 = 1/3，B2 = 3mg/(qv)
      t_min = [2π + 4·arccos(3/5)]·v/g ≈ 9.9924 v/g
  (3) 电场改沿 +y：F_B = qvB1 ẑ = mg ẑ 抵消重力，净力 qE ŷ
      ⇒ x = vt，y = gt²/2，z = 0  ⇒  y = gx²/(2v²)，z = 0
"""
import os
import math
import re as _re
import io as _io

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = os.path.join(ROOT, 'assets', 'template.html')
OUT = os.path.join(ROOT, '2026-10-13_电场重力分区磁场复合场_教学动画.html')

# ============================================================
# 一、物理参数（世界单位 = R1 = v^2/g）
# ============================================================
A = math.acos(0.6)                 # 0.927295218 rad = 53.130102°
A_DEG = math.degrees(A)            # 53.130102
B_SWEEP = 2 * math.pi - 2 * A      # 4.428592 rad = 253.739796°
C_SWEEP = 2 * A                    # 1.854590 rad = 106.260204°
R2 = 1.0 / 3.0                     # r2 = R2/R1
K_TAN = 3                          # 相切点序号（k=2 时 r2=0 退化，k≥3）
Z0 = 0.4
XP = 3.2
X_TAN1 = 1.6 * (1 - R2)            # 1.066667
X_TAN2 = 2 * 1.6 * (1 - R2)        # 2.133333
assert abs(X_TAN1 - 16.0 / 15.0) < 1e-12
assert abs(X_TAN2 - 32.0 / 15.0) < 1e-12
assert abs(3 * 1.6 * (1 - R2) - XP) < 1e-12

_A_II0 = math.radians(-36.8698976)  # 区域Ⅱ 段起始角
_A_I1 = math.pi + math.radians(36.8698976)   # 区域Ⅰ 段（完整）起始角 = 216.869898°

# 7 段轨迹：区域Ⅰ 首段 → Ⅱ → Ⅰ → Ⅱ → Ⅰ → Ⅱ → Ⅰ（末段止于 P）
SEGS = [
    dict(reg='I',  R=1.0,       cx=0.0,       cz=1.0, a0=math.radians(-90.0), sweep=A),
    dict(reg='II', R=R2,        cx=0.8 - 0.8 * R2, cz=Z0 + 0.6 * R2, a0=_A_II0, sweep=B_SWEEP),
    dict(reg='I',  R=1.0,       cx=X_TAN1,    cz=1.0, a0=_A_I1, sweep=C_SWEEP),
    dict(reg='II', R=R2,        cx=1.6,       cz=Z0 + 0.6 * R2, a0=_A_II0, sweep=B_SWEEP),
    dict(reg='I',  R=1.0,       cx=X_TAN2,    cz=1.0, a0=_A_I1, sweep=C_SWEEP),
    dict(reg='II', R=R2,        cx=2.4 + 0.8 - 0.8 * R2, cz=Z0 + 0.6 * R2, a0=_A_II0, sweep=B_SWEEP),
    dict(reg='I',  R=1.0,       cx=XP,        cz=1.0, a0=_A_I1, sweep=A),
]
for _s in SEGS:
    _s['len'] = _s['R'] * _s['sweep']          # 以 R1 为单位的弧长（= 时间 × v / R1）
TAU = [0.0]
for _s in SEGS:
    TAU.append(TAU[-1] + _s['len'])
T_TOTAL = TAU[-1]
assert abs(T_TOTAL - (2 * math.pi + 4 * A)) < 1e-12, T_TOTAL   # = 9.992366179

# 时间轴分段（秒）
T_Q1 = 4.0
T_A = 8.0
T_B = 13.0
T_ATP = 18.0                # 到达 P 的时刻（第(3)问画面尚未开始）
T_C = 18.6
T_END = 24.0

# ============================================================
# 二、题面
# ============================================================
PROBLEM_TITLE = '电磁复合场（电场 + 重力 + 分区磁场）'
PROBLEM_GIVEN = (
    '如图所示，在 \\(xOz\\) 平面内存在方向竖直向上的匀强电场，'
    '电场强度大小为 \\(E\\)。'
    '以 \\(z=z_0\\) 为界，\\(z\\leqslant z_0\\) 的区域Ⅰ与 \\(z>z_0\\) 的区域Ⅱ中'
    '均存在方向垂直纸面向里的匀强磁场，磁感应强度大小分别为 \\(B_1\\) 和 \\(B_2\\)。'
    '一带正电荷的粒子，质量为 \\(m\\)、电荷量为 \\(q\\)，以速率 \\(v\\) '
    '从 \\(O\\) 点沿 \\(x\\) 轴正方向射出，在区域Ⅰ、Ⅱ中均做匀速圆周运动，'
    '且恰好能经过 \\(x\\) 轴上的 \\(P\\) 点。已知 \\(z_0=\\dfrac{2v^2}{5g}\\)，'
    '\\(B_1=\\dfrac{mg}{qv}\\)，\\(\\dfrac{16v^2}{5g}\\) 为 \\(P\\) 点的横坐标。'
    '重力加速度为 \\(g\\)。'
)
PROBLEM_ASKS = [
    '求电场强度 \\(E\\) 的大小，以及粒子第一次经过 \\(z=z_0\\) 平面时的位置对应的 \\(x\\) 坐标值；',
    '求粒子从 \\(O\\) 点运动到 \\(P\\) 点的运动时间最短时，区域Ⅱ中磁感应强度的大小 \\(B_2\\)；',
    '若仅将匀强电场的方向改为沿 \\(y\\) 轴正方向，粒子仍以速率 \\(v\\) 从 \\(O\\) 点沿 \\(x\\) 轴正方向射出，'
    '求该粒子的轨迹方程。',
]
KNOWLEDGE_IDS = [
    'em-lorentz-force',
    'em-cyclotron',
    'em-electric-field',
    'em-field-superposition',
]

# ============================================================
# 三、分步解析
# ============================================================
STEPS = [
    dict(q=1, title='匀速圆周 ⇒ 电场力与重力平衡', t0=0.0, t1=2.0,
         tex=r'F_E=mg\quad\Rightarrow\quad E=\dfrac{mg}{q}',
         note='粒子在两个区域内都做<b>匀速</b>圆周运动，说明合力始终与速度垂直、大小恒定。'
              '在竖直方向上，合力为 \\(qE-mg\\)；若 \\(qE\\neq mg\\)，'
              '当速度转到与竖直方向不垂直时，\\(qE-mg\\) 就会出现沿速度切向的分量，'
              '速率将发生变化，与「匀速」矛盾。故必须有 \\(qE=mg\\)，'
              '即 \\(E=\\dfrac{mg}{q}\\)。此时竖直方向受力平衡，'
              '合力只剩洛伦兹力 \\(qvB\\)，恰好充当向心力。',
         basis='匀速圆周运动条件（合力恒垂直于速度）'),
    dict(q=1, title='区域Ⅰ 半径：洛伦兹力提供向心力', t0=1.6, t1=3.0,
         tex=r'qvB_1=\dfrac{mv^{2}}{R_1}\quad\Rightarrow\quad R_1=\dfrac{mv}{qB_1}=\dfrac{v^{2}}{g}',
         note='由 \\(B_1=\\dfrac{mg}{qv}\\) 得 '
              '\\(R_1=\\dfrac{mv}{q\\cdot mg/(qv)}=\\dfrac{v^{2}}{g}\\)。'
              '粒子在 \\(O\\) 点速度沿 \\(+x\\)，磁场垂直纸面向里，由左手定则洛伦兹力沿 \\(+z\\)，'
              '故区域Ⅰ 内轨迹圆的圆心在 \\(O\\) 点正上方 \\((0,\\,R_1)\\)。'
              '于是圆周方程可写成参数式 \\(x=R_1\\sin\\theta\\)，\\(z=R_1(1-\\cos\\theta)\\)。',
         basis='洛伦兹力提供向心力 + 左手定则定圆心'),
    dict(q=1, title='第一次穿过界面 z = z₀ 的位置', t0=2.6, t1=4.2,
         tex=r'z_0=0.4R_1\Rightarrow\cos\theta_A=0.6,\ \sin\theta_A=0.8'
             r'\quad\Rightarrow\quad x=\dfrac{4v^{2}}{5g}',
         note='令 \\(z=z_0=\\dfrac{2v^2}{5g}=0.4R_1\\)，代入参数式得 '
              '\\(\\cos\\theta_A=1-\\dfrac{z_0}{R_1}=0.6\\)，故 '
              '\\(\\sin\\theta_A=0.8\\)，\\(\\theta_A=\\arccos 0.6\\approx53.13^{\\circ}\\)。'
              '于是第一次经过界面的位置横坐标 '
              '\\(x=R_1\\sin\\theta_A=0.8R_1=\\dfrac{4v^2}{5g}\\)。'
              '该点速度方向为 \\((\\cos\\theta_A,\\ \\sin\\theta_A)=(0.6,\\ 0.8)\\)。',
         basis='圆周参数式 + 三角函数精确值'),
    dict(q=2, title='区域Ⅱ 内圆弧：转角 2π − 2θ_A，横移 −1.6r₂', t0=4.0, t1=6.2,
         tex=r'\Delta\theta_{\mathrm{II}}=2\pi-2\arccos 0.6=253.74^{\circ},'
             r'\quad \Delta x_{\mathrm{II}}=-1.6r_2',
         note='粒子以速度 \\((0.6,\\ 0.8)\\) 进入区域Ⅱ，'
              '半径 \\(R_2=r_2R_1\\)，圆心在该点左上方 \\((-0.8r_2,\\ +0.6r_2)\\) 处。'
              '进入时速度方向角为 \\(-36.87^{\\circ}\\)；'
              '再次回到界面 \\(z=z_0\\) 时对应 \\(216.87^{\\circ}\\)，'
              '故在区域Ⅱ 内转过 \\(253.74^{\\circ}=2\\pi-2\\theta_A\\)，为<b>劣弧</b>。'
              '出射点横坐标 \\(x=0.8-1.6r_2\\)，速度方向 \\((0.6,\\ -0.8)\\)。',
         basis='圆周几何 + 界面上两点等高'),
    dict(q=2, title='回到区域Ⅰ：圆弧恰与 x 轴相切', t0=6.2, t1=8.4,
         tex=r'O_1=\big(0.8-1.6r_2+0.8,\ z_0+0.6R_1\big),'
             r'\quad z_{\min}=z_0+0.6R_1-R_1=0',
         note='以速度 \\((0.6,\\ -0.8)\\) 重返区域Ⅰ（半径 \\(R_1\\)，洛伦兹力仍指向左上），'
              '圆心为入射点 \\((0.8-1.6r_2,\\ 0.4)\\) 加上 \\(R_1(-v_z,\\ v_x)=(0.8,\\ 0.6)\\)，'
              '即圆心纵坐标 \\(z_0+0.6R_1=1.0R_1\\)。'
              '于是这段圆弧的最低点恰好落在 \\(z=1.0R_1-R_1=0\\) 上，'
              '即<b>与 \\(x\\) 轴相切</b>——这正是题给 \\(z_0=0.4R_1\\) 的设计意图。'
              '第 \\(k\\) 个相切点的横坐标为 \\(x_k=1.6k(1-r_2)\\)。',
         basis='圆心位置 + 几何相切条件'),
    dict(q=2, title='相切点递推：令 x_k = 3.2 解出 r₂', t0=8.4, t1=11.5,
         tex=r'1.6k\left(1-r_2\right)=\dfrac{16v^2}{5g}\Big/ R_1=3.2'
             r'\quad\Rightarrow\quad r_2=\dfrac{k-2}{k}',
         note='每经历「区域Ⅱ 一段 + 区域Ⅰ 一段」，横坐标净前进 '
              '\\(1.6-1.6r_2=1.6(1-r_2)\\)。'
              '要使轨迹恰好过 \\(P\\)，必须让某个相切点落在 \\(x=3.2R_1\\) 上：'
              '\\(1.6k(1-r_2)=3.2\\)，解得 '
              '\\(r_2=\\dfrac{k-2}{k}=\\dfrac{B_1}{B_2}\\)，'
              '即 \\(B_2=\\dfrac{k}{k-2}B_1=\\dfrac{k}{k-2}\\cdot\\dfrac{mg}{qv}\\)。'
              '\\(k=2\\) 时 \\(r_2=0\\)（\\(B_2\\to\\infty\\)，退化），故 \\(k\\geqslant 3\\)。',
         basis='分段递推关系 + 周期性'),
    dict(q=2, title='时间最短：k = 3，B₂ = 3mg/(qv)', t0=11.5, t1=18.2,
         tex=r't=\Big[2k\arccos\tfrac35+(k-2)\big(2\pi-2\arccos\tfrac35\big)\Big]'
             r'\dfrac{v}{g}\ \Rightarrow\ B_2=\dfrac{3mg}{qv}',
         note='圆弧时间 \\(t=R\\Delta\\theta/v\\)。从 \\(O\\) 到第 \\(k\\) 个相切点，'
              '区域Ⅰ 内共转过 \\(2k\\theta_A\\)（首末各半段），区域Ⅱ 内共转过 '
              '\\(k\\cdot 2\\pi-2k\\theta_A\\)。代入 \\(r_2=\\dfrac{k-2}{k}\\) 得 '
              '\\(t=\\big[2k\\arccos 0.6+(k-2)(2\\pi-2\\arccos 0.6)\\big]\\dfrac{v}{g}\\)。'
              '该式随 \\(k\\) 单调递增（\\(k=3\\) 时约 \\(9.99\\dfrac{v}{g}\\)，'
              '\\(k=4\\) 时约 \\(16.28\\dfrac{v}{g}\\)），故最短对应 \\(k=3\\)：'
              '\\(r_2=\\dfrac13\\)，\\(\\boxed{B_2=\\dfrac{3mg}{qv}}\\)，'
              '此时 \\(t_{\\min}=\\big[2\\pi+4\\arccos 0.6\\big]\\dfrac{v}{g}'
              '\\approx9.99\\dfrac{v}{g}\\)。',
         basis='圆弧时间公式 + 单调性比较'),
    dict(q=3, title='磁场力恰好抵消重力', t0=18.0, t1=20.2,
         tex=r'F_B=qvB_1\hat{z}=mg\hat{z}=G\quad\Rightarrow\quad F_{\text{合}}=qE\hat{y}',
         note='电场改为沿 \\(+y\\) 后，重力 \\(mg\\hat{z}\\) 仍在。'
              '粒子速度沿 \\(+x\\)、磁场沿 \\(+y\\)，洛伦兹力 \\(qvB_1\\hat{z}\\) 沿 \\(+z\\)，'
              '而 \\(qvB_1=mg\\)，二者<b>大小相等、方向相反</b>，恰好抵消。'
              '所以竖直方向净力为零，粒子始终保持 \\(v_z=0\\)，一直待在区域Ⅰ（\\(z=0 \\lt z_0\\)）内，'
              '不会跨界面。剩下唯一的合力是 \\(qE\\hat{y}=mg\\hat{y}\\)。',
         basis='洛伦兹力公式 + 平衡条件'),
    dict(q=3, title='只沿 y 方向做匀加速平抛', t0=20.2, t1=22.2,
         tex=r'a=\dfrac{qE}{m}\hat{y}=g\hat{y},\quad x=vt,\quad y=\dfrac{1}{2}gt^{2},'
             r'\quad z=0',
         note='注意：速度一旦出现 \\(y\\) 分量，\\(v_y\\hat{y}\\times B\\hat{y}=0\\)，'
              '磁场力仍只有 \\(qvB_1\\hat{z}\\)，所以 \\(x\\) 方向速度恒为 \\(v\\)，'
              '竖直方向净加速度恒为 \\(g\\)。'
              '这正是平抛运动：\\(x\\) 方向匀速、\\(y\\) 方向匀加速，'
              '且 \\(z\\equiv 0\\)。',
         basis='牛顿第二定律 + 分方向独立性'),
    dict(q=3, title='消去时间得轨迹方程', t0=22.2, t1=24.0,
         tex=r'\boxed{\ y=\dfrac{gx^{2}}{2v^{2}},\qquad z=0\ }',
         note='由 \\(x=vt\\) 得 \\(t=\\dfrac{x}{v}\\)，代入 '
              '\\(y=\\dfrac{1}{2}gt^{2}\\) 得 '
              '\\(y=\\dfrac{gx^{2}}{2v^{2}}\\)；又 \\(z\\equiv 0\\)。'
              '所以轨迹是 \\(xOy\\) 平面内一条<b>开口沿 \\(+y\\) 的抛物线</b>，'
              '过原点、顶点在原点、以 \\(x\\) 轴为对称轴。',
         basis='平抛运动的标准轨迹'),
]

# ============================================================
# 四、视图 / 横幅
# ============================================================
VIEW = dict(xmin=-0.42, xmax=3.62, ymin=-0.80, ymax=1.63)

TIMELINE = [
    (0.00, T_Q1, '第(1)问  匀速圆周 ⇒ 电场力与重力平衡'),
    (T_Q1, T_A, '第(2)问  进入区域Ⅱ：转过 253.74°，横移 −1.6r₂'),
    (T_A, T_B, '第(2)问  区域Ⅰ 内圆弧恰与 x 轴相切'),
    (T_B, T_C, '第(2)问  相切点递推：r₂ = (k−2)/k'),
    (T_C, T_END, '第(3)问  电场沿 +y：抛物线 y = gx²/(2v²)'),
]

# ============================================================
# 五、动画 JS
# ============================================================
GLOBALS_JS = r"""
/* =========================================================================
   本题全局：物理参数、分段圆弧几何、时间↔相位换算
   ---------------------------------------------------------------------------
   【长度单位】取 R1 = v^2/g 为 1，故 z0 = 0.4，P = (3.2, 0)，r2 = R2/R1 = 1/3。
   【角度】  θ_A = arccos(3/5) = 53.130102°
             区域Ⅰ 首段弧   转角 θ_A
             区域Ⅱ 每一段弧 转角 2π − 2θ_A = 253.739796°
             区域Ⅰ 后续弧   转角 2θ_A = 106.260204°，末段只取 θ_A（止于 P）
   【时间】  τ = 路程 / R1（单位：R1/v），圆弧时间 = R·Δθ/v
   ========================================================================= */
const PAR = {
  A: %(A).6f,            /* arccos(0.6) */
  Adeg: %(Ad).4f,         /* 53.130102 */
  Bsweep: %(Bs).6f,       /* 2π − 2A */
  Csweep: %(Cs).6f,      /* 2A */
  r2: %(r2).6f,          /* R2/R1 = 1/3 */
  B2: %(B2).4f,          /* B2/B1 = 3 */
  z0: %(z0).4f,
  XP: %(xp).4f,
  xTan1: %(xt1).6f,
  xTan2: %(xt2).6f,
  T: %(Ttot).6f         /* t_min / (R1/v) = 9.992363 */
};

/* 7 段圆弧：{ reg 区域, R 半径, cx, cz 圆心, a0 起始角(rad), sweep 转角(rad), len 弧长 } */
const SEGS = [
%(SEGS)s
];
const TAU = [0.0];
for (let i = 0; i < SEGS.length; i++) TAU.push(TAU[i] + SEGS[i].len);
const T_TOTAL = TAU[TAU.length - 1];

/* 画布几何（世界单位） */
const GEO = {
  pr: 0.048,          /* 粒子世界半径 */
  xTan1: PAR.xTan1,
  xTan2: PAR.xTan2
};

/* ---- 时间轴分段（秒） ---- */
const TT = { q1: %(q1).2f, a: %(ta).2f, b: %(tb).2f, atp: %(atp).2f, c: %(tc).2f, end: %(te).2f };

/* ---- 由显示时间 t 求归一化时间 τ（单位 R1/v） ---- */
function tauOf(t){
  if (t < TT.q1) return t / TT.q1 * TAU[1];
  if (t < TT.a)   return TAU[1] + (t - TT.q1) / (TT.a - TT.q1) * (TAU[3] - TAU[1]);
  if (t < TT.b)   return TAU[3] + (t - TT.a)   / (TT.b - TT.a)   * (TAU[5] - TAU[3]);
  if (t < TT.c)   return TAU[5] + (t - TT.b)   / (TT.c - TT.b)   * (TAU[7] - TAU[5]);
  return TAU[7];
}
/* 由 τ 找当前所在段 */
function segOf(tau){
  for (let i = 0; i < SEGS.length; i++){
    if (tau < TAU[i + 1] - 1e-9) return i;
  }
  return SEGS.length - 1;
}
/* 第 i 段圆弧上，行走比例 f∈[0,1] 处的位置与速度方向（逆时针） */
function segPos(i, f){
  const s = SEGS[i];
  const th = s.a0 + s.sweep * f;
  return {
    x: s.cx + s.R * Math.cos(th),
    z: s.cz + s.R * Math.sin(th),
    vx: -Math.sin(th),
    vz: Math.cos(th),
    th: th
  };
}
/* 完整折线的采样点（供磁场符号避让与浅色底轨使用）。
   每段的采样起点下标记入 off，便于把 τ 映射到采样下标。 */
const PATH_STEP = 0.035;
const FULL_PATH = [];
const PATH_OFF = [];
for (let i = 0; i < SEGS.length; i++){
  const s = SEGS[i];
  PATH_OFF.push(FULL_PATH.length);
  const n = Math.max(8, Math.ceil(s.len / PATH_STEP));
  for (let k = 0; k <= n; k++){
    const p = segPos(i, k / n);
    FULL_PATH.push([p.x, p.z]);
  }
}
/* ⚠ 必须补哨兵：最后一段 i = SEGS.length-1 时 pathIndexOf 会取 PATH_OFF[i+1]，
   若数组只有 SEGS.length 项则得到 undefined ⇒ 返回 NaN ⇒ 红色已走轨迹整段消失 */
PATH_OFF.push(FULL_PATH.length);
/* τ → FULL_PATH 中最后已到达的采样下标（含） */
function pathIndexOf(tau){
  if (tau <= 0) return 0;
  for (let i = 0; i < SEGS.length; i++){
    if (tau < TAU[i + 1] - 1e-9){
      const f = Math.max(0, Math.min(1, (tau - TAU[i]) / SEGS[i].len));
      const a = PATH_OFF[i], b = PATH_OFF[i + 1];
      return Math.min(FULL_PATH.length - 1, a + Math.round(f * (b - a)));
    }
  }
  return FULL_PATH.length - 1;
}

/* ---- 显示时间 t → 状态 ---- */
function stateAt(t){
  const st = { phase: 'q1', tau: 0, seg: 0, frac: 0,
               x: 0, z: 0, vx: 1, vz: 0, cx: 0, cz: 1, reg: 'I', R: 1,
               segDone: 0, atP: false, tHat: 0 };
  /* 第(3)问：抛物线（平抛），x 匀速、y 匀加速。
     ⚠ 行程不能太长：HUD 占住画布顶部约 86px 且居中（bx≈100px 到 415px），
       若粒子终态 y 太高就会躲进 HUD 后面消失。
       取 x: 0 → 1.62（与曲线同 XMAX），y = x²/2 ⇒ y_max = 1.31，
       在视窗上界 2.62 下换算约 165px，安全低于 HUD 下沿（≈128px）之上但 x 已 >1.6，
       粒子落在 HUD 右侧的空白区。 */
  if (t >= TT.c){
    /* 第(3)问：抛物线（平抛），x 匀速、y 匀加速 */
    st.phase = 'q3';
    const f = Math.min(1, Math.max(0, (t - TT.c) / (TT.end - TT.c)));
    const xx = 1.62 * f;
    st.tHat = f * 4.0;
    st.x = xx; st.z = 0;
    st.vx = 1; st.vz = xx;          /* ∝ (1, x)，即 (v, gt) */
    return st;
  }
  st.tau = tauOf(t);
  st.tHat = st.tau;
  const i = segOf(st.tau);
  const f = (st.tau - TAU[i]) / (TAU[i + 1] - TAU[i]);
  const p = segPos(i, Math.max(0, Math.min(1, f)));
  st.phase = (t < TT.q1) ? 'q1' : 'q2';
  st.seg = i; st.frac = f; st.reg = SEGS[i].reg; st.R = SEGS[i].R;
  st.cx = SEGS[i].cx; st.cz = SEGS[i].cz;
  st.x = p.x; st.z = p.z; st.vx = p.vx; st.vz = p.vz;
  st.segDone = 0;
  for (let k = 0; k < i; k++) st.segDone++;
  st.atP = (t >= TT.atp - 1e-6);
  return st;
}

/* 第(3)问已改为整屏画面（见 drawParabolaScene），故无需内嵌小图映射函数 */
""" % dict(
    A=A, Ad=A_DEG, Bs=B_SWEEP, Cs=C_SWEEP, r2=R2, B2=1.0 / R2,
    z0=Z0, xp=XP, xt1=X_TAN1, xt2=X_TAN2, Ttot=T_TOTAL,
    q1=T_Q1, ta=T_A, tb=T_B, atp=T_ATP, tc=T_C, te=T_END,
    SEGS=''.join(
        "  { reg: '%s', R: %.9f, cx: %.9f, cz: %.9f, a0: %.9f, sweep: %.9f, len: %.9f },\n"
        % (s['reg'], s['R'], s['cx'], s['cz'], s['a0'], s['sweep'], s['len'])
        for s in SEGS).rstrip('\n'),
)

SETUP_JS = """
/* 本题无需额外 setup：全部几何与时间换算已在全局完成 */
"""

HELPERS_JS = r"""
/* =========================================================================
   绘图辅助（全部声明在 GLOBALS 区，即顶层作用域）
   ⚠ 拿画布尺寸必须用 CSS 像素（getBoundingClientRect），不能用 ctx.canvas.width。
   ========================================================================= */

/* ---- 引线标注：文字放在空白处，细点线连回目标点 ---- */
function leadLabel(tx, ty, lx, ly, txt, color, opts){
  opts = opts || {};
  const c = opts.color || color || '#0f172a';
  const p = W2S(tx, ty), q = W2S(lx, ly);
  ctx.save();
  ctx.strokeStyle = opts.line || '#94a3b8';
  ctx.lineWidth = 1;
  ctx.setLineDash([2.5, 2.5]);
  ctx.beginPath(); ctx.moveTo(p[0], p[1]); ctx.lineTo(q[0], q[1]); ctx.stroke();
  ctx.setLineDash([]);
  ctx.beginPath(); ctx.arc(p[0], p[1], 2.2, 0, 7);
  ctx.fillStyle = c; ctx.fill();
  ctx.font = (opts.italic === false ? '' : 'italic ') + 'bold ' + (opts.size || 13) + 'px serif';
  ctx.textAlign = opts.align || 'center';
  ctx.lineWidth = 3.4; ctx.strokeStyle = 'rgba(255,255,255,0.94)';
  ctx.strokeText(txt, q[0], q[1]);
  ctx.fillStyle = c; ctx.fillText(txt, q[0], q[1]);
  ctx.textAlign = 'left';
  ctx.restore();
}

/* ---- 带白底衬托的小标签（dy / dx 为屏幕像素偏移） ---- */
function haloTag(x, y, txt, color, dy, dx){
  const p = W2S(x, y);
  ctx.save();
  ctx.font = 'italic bold 13px serif';
  ctx.textAlign = dx ? 'left' : 'center';
  const ox = p[0] + (dx || 0);
  ctx.lineWidth = 3.6; ctx.strokeStyle = 'rgba(255,255,255,0.95)';
  ctx.strokeText(txt, ox, p[1] + dy);
  ctx.fillStyle = color; ctx.fillText(txt, ox, p[1] + dy);
  ctx.textAlign = 'left';
  ctx.restore();
}

/* ---- 白底衬托的普通文字（可覆盖浅色虚线轨迹，不影响可读性） ---- */
function haloText(x, y, txt, color, opts){
  opts = opts || {};
  const p = W2S(x, y);
  ctx.save();
  ctx.font = (opts.bold === false ? '' : 'bold ') + (opts.size || 12) + 'px ' +
             (opts.serif ? 'serif' : 'sans-serif');
  ctx.textAlign = opts.align || 'left';
  ctx.lineWidth = 3.8; ctx.strokeStyle = 'rgba(255,255,255,0.95)';
  ctx.strokeText(txt, p[0], p[1]);
  ctx.fillStyle = color; ctx.fillText(txt, p[0], p[1]);
  ctx.textAlign = 'left';
  ctx.restore();
}

/* ---- 圆心标记：空心小十字 ---- */
function centerMark(cx, cz){
  const p = W2S(cx, cz);
  ctx.save();
  ctx.strokeStyle = '#64748b'; ctx.lineWidth = 1.2;
  ctx.beginPath();
  ctx.moveTo(p[0] - 5, p[1]); ctx.lineTo(p[0] + 5, p[1]);
  ctx.moveTo(p[0], p[1] - 5); ctx.lineTo(p[0], p[1] + 5);
  ctx.stroke();
  ctx.restore();
}
/* 圆心名（带白底让位） */
function centerName(cx, cz, txt, dx, dz){
  const q = W2S(cx + (dx || 0), cz - 0.055 + (dz || 0));
  ctx.save();
  ctx.font = 'italic bold 12px serif';
  ctx.textAlign = (dx != null && dx !== 0) ? 'right' : 'center';
  ctx.lineWidth = 3.4; ctx.strokeStyle = 'rgba(255,255,255,0.94)';
  ctx.strokeText(txt, q[0], q[1]);
  ctx.fillStyle = '#64748b';
  ctx.fillText(txt, q[0], q[1]);
  ctx.textAlign = 'left';
  ctx.restore();
}

/* ---- 世界坐标小箭头 ---- */
function wArrow(x1, z1, x2, z2, color, lw, head){
  const a = W2S(x1, z1), b = W2S(x2, z2);
  ctx.save();
  ctx.strokeStyle = color; ctx.fillStyle = color; ctx.lineWidth = lw || 2.2;
  ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.lineTo(b[0], b[1]); ctx.stroke();
  const ang = Math.atan2(b[1] - a[1], b[0] - a[0]);
  const hd = head || 8;
  ctx.beginPath();
  ctx.moveTo(b[0], b[1]);
  ctx.lineTo(b[0] - hd * Math.cos(ang - 0.42), b[1] - hd * Math.sin(ang - 0.42));
  ctx.lineTo(b[0] - hd * Math.cos(ang + 0.42), b[1] - hd * Math.sin(ang + 0.42));
  ctx.closePath(); ctx.fill();
  ctx.restore();
}

/* ---- 尺寸线（世界坐标，双端短竖线 + 居中标注） ---- */
function dimLine(x1, x2, zw, txt, color, labelDz){
  const a = W2S(x1, zw), b = W2S(x2, zw);
  ctx.save();
  ctx.strokeStyle = color || '#475569'; ctx.lineWidth = 1.2;
  ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.lineTo(b[0], b[1]); ctx.stroke();
  const tk = 5;
  ctx.beginPath();
  ctx.moveTo(a[0], a[1] - tk); ctx.lineTo(a[0], a[1] + tk);
  ctx.moveTo(b[0], b[1] - tk); ctx.lineTo(b[0], b[1] + tk);
  ctx.stroke();
  const q = W2S((x1 + x2) / 2, zw + (labelDz != null ? labelDz : 0.09));
  ctx.font = 'italic bold 12px serif';
  ctx.textAlign = 'center';
  ctx.lineWidth = 3.6; ctx.strokeStyle = 'rgba(255,255,255,0.94)';
  ctx.strokeText(txt, q[0], q[1]);
  ctx.fillStyle = color || '#475569';
  ctx.fillText(txt, q[0], q[1]);
  ctx.textAlign = 'left';
  ctx.restore();
}

/* 磁场 ⊗ 符号的避让区：每项 [x0, x1, z0, z1]。
   ⚠ 必须声明在全局（GLOBALS）区：drawSceneBody 是函数体，
     在其中声明 const 会被 drawFields 调用时命中 TDZ ⇒ ReferenceError ⇒ 整帧中断。 */
const FIELD_AVOID = [
  [-0.45, -0.17, -0.58, 0.72],   /* E 箭头及其 E / 电场方向 标注 */
  [2.05, 2.70, 0.53, 0.67],      /* 区域Ⅱ（B₂） */
  [2.20, 3.60, 0.42, 0.56],      /* z = z₀ 界面标注（右上） */
  [-0.10, 0.86, -0.54, -0.36],   /* 区域Ⅰ（B₁） */
  [1.70, 3.00, 0.48, 0.64],      /* 区域Ⅱ（B₂） */
  [0.90, 2.14, 0.64, 0.86],      /* x = 4v²/(5g) 引线标注 */
  [-0.50, 3.70, -0.72, -0.28],    /* 底部两条尺寸线及其文字带（横跨全宽） */
  [2.26, 3.00, 0.46, 0.60]        /* 区域Ⅱ 圆心 O₂ 名（右侧那颗） */
];

/* ---- 顶部信息盒（CSS 像素定位） ---- */
function drawHud(st){
  const _r = ctx.canvas.getBoundingClientRect();
  const Wp = (_r && _r.width) ? _r.width : ctx.canvas.width;
  const Hp = (_r && _r.height) ? _r.height : ctx.canvas.height;
  if (Wp < 340) return;
  const k = Math.max(0.62, Math.min(1, Wp / 520));
  const lines = hudLines(st);
  const bw = Math.min(Wp - 14, 372 * k), bh = (18 + lines.length * 17) * k;
  const bx = (Wp - bw) / 2, by = 42 * k;
  ctx.save();
  ctx.fillStyle = '#ffffff';   /* 纯白不透明：否则底下的引线标注会隐约透出 */
  ctx.strokeStyle = '#cbd5e1'; ctx.lineWidth = 1.2;
  ctx.fillRect(bx, by, bw, bh); ctx.strokeRect(bx, by, bw, bh);
  ctx.fillStyle = '#1d4ed8'; ctx.font = 'bold ' + (12.5 * k).toFixed(1) + 'px sans-serif';
  ctx.fillText(lines[0], bx + 9 * k, by + 17 * k);
  ctx.fillStyle = '#0f172a'; ctx.font = (11.4 * k).toFixed(1) + 'px sans-serif';
  for (let i = 1; i < lines.length; i++){
    ctx.fillText(lines[i], bx + 9 * k, by + (17 + i * 17) * k);
  }
  ctx.restore();

  /* 底部图例：4 项 2 列 × 2 行，整块落在画布下边距内（不遮挡绘图区）。
     ⚠ 第(3)问画面已换成 xOy 平抛坐标系，磁场分区不再出现，
       图例必须随之切换，否则会指向画面里根本不存在的元素。 */
  const lw = Math.min(Wp - 14, 340 * k), lh = 34 * k;
  const lx = (Wp - lw) / 2, lyy = Hp - lh - 5 * k;
  ctx.save();
  ctx.fillStyle = 'rgba(255,255,255,0.94)';
  ctx.strokeStyle = '#cbd5e1'; ctx.lineWidth = 1.2;
  ctx.fillRect(lx, lyy, lw, lh); ctx.strokeRect(lx, lyy, lw, lh);
  const items = (st.phase === 'q3')
    ? [['line', '#94a3b8', '完整轨迹（虚线）'],
       ['line', '#dc2626', '已走轨迹'],
       ['dot',  '#dc2626', '粒子 +q'],
       ['dot',  '#0f172a', '参考点 (x, y)']]
    : [
    ['x', '#7c3aed', '区域Ⅰ  B₁（⊗）'],
    ['x', '#0ea5e9', '区域Ⅱ  B₂（⊗）'],
    ['line', '#dc2626', '粒子轨迹'],
    ['up', '#2563eb', '电场 E（竖直向上）']
  ];
  const cols = 2, rowsN = 2;
  const iw = lw / cols, ih = lh / rowsN;
  for (let i = 0; i < items.length; i++){
    const row = Math.floor(i / cols), col = i % cols;
    const cx0 = lx + iw * col + 12 * k, cy0 = lyy + ih * row + ih / 2;
    ctx.strokeStyle = items[i][1]; ctx.fillStyle = items[i][1]; ctx.lineWidth = 1.5;
    const d = 3.4 * k;
    if (items[i][0] === 'x'){
      ctx.beginPath();
      ctx.moveTo(cx0 - d, cy0 - d); ctx.lineTo(cx0 + d, cy0 + d);
      ctx.moveTo(cx0 + d, cy0 - d); ctx.lineTo(cx0 - d, cy0 + d);
      ctx.stroke();
    } else if (items[i][0] === 'line'){
      ctx.beginPath(); ctx.moveTo(cx0 - d, cy0); ctx.lineTo(cx0 + d, cy0); ctx.stroke();
    } else if (items[i][0] === 'dot'){
      ctx.beginPath(); ctx.arc(cx0, cy0, d * 0.72, 0, 7); ctx.fill();
    } else {
      ctx.beginPath(); ctx.moveTo(cx0, cy0 + d); ctx.lineTo(cx0, cy0 - d); ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(cx0, cy0 - d - 1);
      ctx.lineTo(cx0 - d * 0.7, cy0 + d * 0.3);
      ctx.lineTo(cx0 + d * 0.7, cy0 + d * 0.3);
      ctx.closePath(); ctx.fill();
    }
    ctx.fillStyle = '#334155'; ctx.font = (10.6 * k).toFixed(1) + 'px sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText(items[i][2], cx0 + 9 * k, cy0 + 3.8 * k);
  }
  ctx.restore();
}
function hudLines(st){
  if (st.phase === 'q3') return ['第(3)问  电场改为沿 +y 方向',
    'F_B = qvB₁ẑ = mgẑ 抵消重力',
    '净力 qEŷ ⇒ a = gŷ（平抛）',
    'y = gx²/(2v²)，z = 0'];
  if (st.phase === 'q1'){
    if (st.tau < TAU[1] * 0.45) return ['第(1)问  受力分析',
      '匀速圆周 ⇒ qE = mg',
      'E = mg/q ，R₁ = v²/g'];
    return ['第(1)问  区域Ⅰ 内的圆弧',
      '圆心 (0, R₁)，半径 R₁ = v²/g',
      'z = z₀ = 0.4R₁ ⇒ x = 4v²/(5g)'];
  }
  if (st.atP) return ['到达 P 点！',
    'k = 3 ，r₂ = 1/3 ，B₂ = 3mg/(qv)',
    't = (2π + 4arccos 3/5)·v/g ≈ 9.99 v/g'];
  if (t < TT.a) return ['第(2)问  区域Ⅱ 内转过 253.74°',
    'r₂ = R₂/R₁ ，横移 −1.6r₂',
    '出射速度 (0.6, −0.8)'];
  if (t < TT.b) return ['第(2)问  圆弧与 x 轴相切',
    '圆心纵坐标 z₀ + 0.6R₁ = R₁',
    '最低点恰好 z = 0（相切）'];
  return ['第(2)问  相切点递推',
    'x_k = 1.6k(1 − r₂) = 3.2',
    'r₂ = (k−2)/k ，k ≥ 3'];
}
"""

DRAWFRAME_JS = r"""
/* ===== 逐帧绘制 ===== */
const st = stateAt(t);
/* ⚠ 不用模板的 clearBg()：它按 ctx.canvas.width/height（设备像素）清屏，
   而 resize 已执行 setTransform(ratio,…)，绘制坐标按 CSS 像素解释
   ⇒ 顶部约 H/ratio 的条带永远清不掉，上一帧的横幅/文字会残留成一条污迹。
   这里改用 getBoundingClientRect 取 CSS 像素尺寸清屏。 */
clearBgCss();
function clearBgCss(){
  /* 双保险：① 复位 transform 后按设备像素全清（必定覆盖整块画布）；
     ② 再按 CSS 像素铺白（此时绘制坐标解释正确）。 */
  ctx.save();
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
  ctx.restore();
  const _r = ctx.canvas.getBoundingClientRect();
  const w = (_r && _r.width) ? _r.width : ctx.canvas.width;
  const h = (_r && _r.height) ? _r.height : ctx.canvas.height;
  ctx.clearRect(0, 0, w, h);
  ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, w, h);
}

/* ---------- 第(3)问：整屏改为 xOy 俯视抛物线画面 ----------
   本题 W2S 依赖全局 VIEW，故此处临时改写 VIEW，画完立即还原，
   避免污染左栏题图（t=0 走 q1 分支，不受影响）。 */
if (st.phase === 'q3'){
  const sv = { xmin: VIEW.xmin, xmax: VIEW.xmax, ymin: VIEW.ymin, ymax: VIEW.ymax };
  VIEW.xmin = -0.16; VIEW.xmax = 2.26; VIEW.ymin = -0.20; VIEW.ymax = 2.62;
  FIG.processBanner('第(3)问  电场改为沿 +y 方向 ⇒ 轨迹为抛物线', {size: 15});
  drawParabolaScene(st);
  VIEW.xmin = sv.xmin; VIEW.xmax = sv.xmax; VIEW.ymin = sv.ymin; VIEW.ymax = sv.ymax;
  if (ctx.canvas.id === 'cv') drawHud(st);
  return;
}

/* ---------- 顶部过程横幅（仅右侧动画画布） ----------
   到达 P（TT.atp ~ TT.c）是第(2)问的收尾，必须单独一段，
   否则横幅还停在「相切点递推」，与画面里的结论粒子不一致。 */
if (ctx.canvas.id === 'cv'){
  let txt = null;
  if (t >= TT.atp){
    txt = '到达 P 点！k = 3，r₂ = 1/3，B₂ = 3mg/(qv)，t = 9.99 v/g';
  } else {
    for (let i = 0; i < BANNERS.length; i++){
      if (t < BANNERS[i][1]){ txt = BANNERS[i][2]; break; }
    }
  }
  if (txt){
    let fs = 15;
    ctx.font = 'bold ' + fs + 'px sans-serif';
    const need = ctx.measureText(txt).width + 26;
    const _r = ctx.canvas.getBoundingClientRect();
    const cw = (_r && _r.width) ? _r.width : ctx.canvas.width;
    const cap = cw * 0.94;
    if (need > cap) fs = Math.max(9, Math.floor(fs * cap / need));
    FIG.processBanner(txt, {size: fs});
  }
}

/* ---------- 区域底色 ---------- */
drawZones();

/* ---------- 坐标系 ---------- */
FIG.coord(VIEW.xmin + 0.03, VIEW.xmax - 0.05, VIEW.ymin + 0.02, 1.02,
          {labels: ['x', 'z']});

/* ---------- 磁场符号（两区都 ⊗ 向里） ---------- */
drawFields();

/* ---------- 界面 z = z₀ ---------- */
ctx.save();
ctx.strokeStyle = '#334155'; ctx.lineWidth = 1.8; ctx.setLineDash([7, 4]);
const d1 = W2S(VIEW.xmin + 0.03, PAR.z0), d2 = W2S(VIEW.xmax - 0.05, PAR.z0);
ctx.beginPath(); ctx.moveTo(d1[0], d1[1]); ctx.lineTo(d2[0], d2[1]); ctx.stroke();
ctx.setLineDash([]);
ctx.restore();
/* 标注放在界面上方右侧空白处（左侧被 E 箭头与受力标注占用）；
   与「区域Ⅱ（B₂）」上下错开一行，避免两个标注横向叠字 */
haloText(3.55, PAR.z0 + 0.085, 'z = z₀ = 2v²/(5g)', '#334155',
         {size: 12, align: 'right'});

/* ---------- 电场方向箭头（左边界空白处竖直向上） ---------- */
wArrow(-0.31, -0.40, -0.31, 0.56, '#2563eb', 2.6, 10);
FIG.text(-0.31, 0.65, 'E', {size: 15, color: '#2563eb', align: 'center'});
FIG.text(-0.31, -0.50, '电场方向', {size: 11, color: '#2563eb', align: 'center', italic: false});

/* ---------- 完整轨迹（浅色底轨） ---------- */
FIG.trajectory(FULL_PATH, {color: 'rgba(148,163,184,0.75)', lw: 1.6, dash: [4, 3]});

/* ---------- 已走过的轨迹（红色实线） ---------- */
const walked = FULL_PATH.filter(function(p, i){ return i <= pathIndexOf(st.tau); });
if (walked.length > 1) FIG.trajectory(walked, {color: '#dc2626', lw: 2.4});

/* ---------- 当前段的圆心 ---------- */
if (st.phase !== 'q3'){
  centerMark(st.cx, st.cz);
  /* 右侧那颗区域Ⅱ 圆心若仍把名字写在正上方，会与右上角 z = z₀ 标注相撞 ⇒ 改放左侧 */
  if (st.reg === 'II' && st.cx > 2.0) centerName(st.cx, st.cz, 'O₂', -0.075, 0.02);
  else centerName(st.cx, st.cz, st.reg === 'I' ? 'O₁' : 'O₂');
}

/* ---- 关键点与标注 ----
   ⚠ 粒子每次穿越界面 z=z₀ 都会经过 (0.8,0.4) 与 (1.6,0.4) 附近，
     而「x = 4v²/(5g) 引线标注」锚在 (0.8,0.4)、「区域Ⅱ（B₂）」在 (x∈[1.9,2.6], z≈0.60)
     —— 两者都会被运动粒子扫过造成叠字。判据：粒子贴近界面（|z - z₀| < 0.16）时隐藏，
     该时段结论由 HUD 与数据面板承载，信息不丢。 */
const nearIface = (st.phase !== 'q3') && (Math.abs(st.z - PAR.z0) < 0.16);
drawKeyLabels(st, nearIface);

/* ---------- 第(1)问：粒子受力箭头 ----------
   ⚠ t 很小的时候 F_E 与 F_B 同向（粒子刚离开 O，两力都竖直向上），
     两个箭头与四个标签会叠在一起。故受力图从 t=1.3 起才出现，
     此时粒子已沿弧线右移，F_B 指向左上、与竖直的 F_E 明显分开。 */
if (st.phase === 'q1' && t >= 1.3 && t < 3.4){
  drawForceArrows(st);
}

/* ---------- 粒子 ---------- */
drawParticle(st.x, st.z, st.vx, st.vz, '#dc2626',
              (t >= 1.3 && t < 3.4) ? null : '+q', 0);

/* ---------- 到达 P 点高亮 ---------- */
if (st.phase === 'q2' && st.atP){
  const p = W2S(PAR.XP, 0);
  ctx.save();
  ctx.strokeStyle = '#f59e0b'; ctx.lineWidth = 2.6;
  ctx.beginPath(); ctx.arc(p[0], p[1], 0.060 * scale, 0, 7); ctx.stroke();
  ctx.beginPath(); ctx.arc(p[0], p[1], 0.092 * scale, 0, 7);
  ctx.strokeStyle = 'rgba(245,158,11,0.5)'; ctx.lineWidth = 1.6; ctx.stroke();
  ctx.restore();
}

/* ---------- HUD ---------- */
if (ctx.canvas.id === 'cv') drawHud(st);

/* =========================================================================
   绘图子函数
   ========================================================================= */

/* 区域底色 */
function drawZones(){
  const a = W2S(VIEW.xmin + 0.03, VIEW.ymax - 0.02);
  const b = W2S(VIEW.xmax - 0.05, PAR.z0);
  ctx.save();
  ctx.fillStyle = 'rgba(14,165,233,0.055)';
  ctx.fillRect(a[0], a[1], b[0] - a[0], b[1] - a[1]);
  const c = W2S(VIEW.xmin + 0.03, PAR.z0);
  const d = W2S(VIEW.xmax - 0.05, VIEW.ymin + 0.02);
  ctx.fillStyle = 'rgba(124,58,237,0.05)';
  ctx.fillRect(c[0], c[1], d[0] - c[0], d[1] - c[1]);
  ctx.restore();
}

/* 磁场 ⊗ 符号：跳过靠近轨迹、坐标轴、标注的位置 */
function drawFields(){
  const step = 0.335;
  ctx.save();
  ctx.lineWidth = 1.25;
  for (let x = VIEW.xmin + 0.14; x <= VIEW.xmax - 0.10; x += step){
    for (let z = VIEW.ymin + 0.10; z <= 1.12; z += step){
      if (z > PAR.z0 - 0.075 && z < PAR.z0 + 0.075) continue;   /* 让开界面虚线 */
      if (Math.abs(z) < 0.085) continue;                        /* 让开 x 轴 */
      if (Math.abs(x) < 0.115) continue;                        /* 让开 z 轴 */
      let hit = false;
      for (let i = 0; i < FIELD_AVOID.length; i++){
        const a = FIELD_AVOID[i];
        if (x > a[0] && x < a[1] && z > a[2] && z < a[3]){ hit = true; break; }
      }
      if (hit) continue;
      if (tooCloseToPath(x, z, 0.135)) continue;
      const col = (z > PAR.z0) ? '#0ea5e9' : '#7c3aed';
      ctx.strokeStyle = col;
      const p = W2S(x, z), r = 0.050 * scale;
      ctx.beginPath();
      ctx.moveTo(p[0] - r, p[1] - r); ctx.lineTo(p[0] + r, p[1] + r);
      ctx.moveTo(p[0] + r, p[1] - r); ctx.lineTo(p[0] - r, p[1] + r);
      ctx.stroke();
    }
  }
  ctx.restore();
}
function tooCloseToPath(x, z, tol){
  for (let i = 0; i < FULL_PATH.length; i++){
    const dx = FULL_PATH[i][0] - x, dz = FULL_PATH[i][1] - z;
    if (dx * dx + dz * dz < tol * tol) return true;
  }
  return false;
}

/* 关键点、区域名、尺寸线 */
function drawKeyLabels(st, nearIface){
  /* 原点 O */
  ctx.save();
  ctx.fillStyle = '#0f172a';
  const op = W2S(0, 0);
  ctx.beginPath(); ctx.arc(op[0], op[1], 3.0, 0, 7); ctx.fill();
  ctx.restore();
  FIG.text(0.03, -0.135, 'O', {size: 14, color: '#0f172a'});

  /* 区域名（磁感应强度放在图例与 HUD，避免画面内文字拥挤；
     用 haloText 加白底，可压在浅色虚线完整轨迹上仍清晰）。
     粒子贴近界面时隐藏：那两个位置正处在界面上，粒子必然扫过。 */
  if (st.phase !== 'q3' && !nearIface){
    haloText(2.62, 0.60, '区域Ⅱ（B₂）', '#0284c7', {size: 12.5, align: 'right'});
  }
  if (st.phase !== 'q3'){
    haloText(0.05, -0.44, '区域Ⅰ（B₁）', '#6d28d9', {size: 12.5});
  }

  /* 第一次过界点（0.8, 0.4）—— 第(1)问结论 */
  if (t >= 2.4){
    const q = W2S(0.8, PAR.z0);
    ctx.save();
    ctx.fillStyle = '#0f172a';
    ctx.beginPath(); ctx.arc(q[0], q[1], 3.2, 0, 7); ctx.fill();
    ctx.restore();
    if (!nearIface){
      leadLabel(0.8, PAR.z0, 1.46, 0.74, 'x = 4v²/(5g)', '#b91c1c', {size: 12.5});
    }
  }

  /* 第一个相切点 */
  if (t >= 7.4){
    const q = W2S(GEO.xTan1, 0);
    ctx.save();
    ctx.fillStyle = '#b45309';
    ctx.beginPath(); ctx.arc(q[0], q[1], 3.2, 0, 7); ctx.fill();
    ctx.restore();
    FIG.text(GEO.xTan1, -0.13, 'x₁', {size: 13, color: '#b45309', align: 'center'});
  }
  /* 第二个相切点 */
  if (t >= 12.2){
    const q = W2S(GEO.xTan2, 0);
    ctx.save();
    ctx.fillStyle = '#b45309';
    ctx.beginPath(); ctx.arc(q[0], q[1], 3.2, 0, 7); ctx.fill();
    ctx.restore();
    FIG.text(GEO.xTan2, -0.13, 'x₂', {size: 13, color: '#b45309', align: 'center'});
  }
  /* 相切点间距尺寸线：标注放在线的下方，与刻度标签、区域名错层 */
  if (t >= 12.6){
    dimLine(GEO.xTan1, GEO.xTan2, -0.36, 'x₂ − x₁ = 1.6(1 − r₂)R₁',
            '#b45309', -0.085);
  }
  /* P 点（坐标信息由下方 OP 尺寸线给出，此处不再重复引线标注） */
  ctx.save();
  ctx.fillStyle = '#b91c1c';
  const pp = W2S(PAR.XP, 0);
  ctx.beginPath(); ctx.arc(pp[0], pp[1], 3.6, 0, 7); ctx.fill();
  ctx.restore();
  /* 到达 P 时高亮圈半径 0.092R₁ 会盖住 z=-0.13 处的 P 标签 ⇒ 此时把标签下移到 -0.26 */
  FIG.text(PAR.XP, (t >= TT.atp - 1e-6) ? -0.26 : -0.13, 'P',
           {size: 14, color: '#b91c1c', align: 'center'});
  /* OP 总长 */
  if (t >= 13.4){
    dimLine(0, PAR.XP, -0.60, 'OP = 16v²/(5g) = 3.2R₁', '#334155', -0.095);
  }
}

/* 第(1)问：竖直方向受力（只画 F_E 与 mg，突出「二者平衡」这一结论；
   F_B 恒垂直于速度、不参与竖直平衡，画出来只会挤在一起，故只用文字说明）。
   标签一律用「箭头端点屏幕坐标 + 固定像素偏移」，不同画布宽度下也不会重叠。 */
function drawForceArrows(st){
  const L = 0.42;
  wArrow(st.x, st.z + 0.02, st.x, st.z + L, '#2563eb', 2.4, 9);   /* F_E 向上 */
  wArrow(st.x, st.z - 0.02, st.x, st.z - L, '#334155', 2.4, 9);   /* mg 向下 */
  const top = W2S(st.x, st.z + L), bot = W2S(st.x, st.z - L);
  ctx.save();
  ctx.font = 'italic bold 12.5px serif';
  ctx.lineWidth = 3.8; ctx.strokeStyle = 'rgba(255,255,255,0.95)';
  /* F_E / mg 标签：分居箭头左右两侧并垂直错开。
     关键坑：F_E 箭头只有 ~0.30 世界单位高，屏幕上约 20px，
     故其标签放在箭头**左侧**、mg 标签放在**右侧**，才能真正分开。 */
  ctx.textAlign = 'right';
  ctx.strokeText('F', top[0] - 8, top[1] - 3); ctx.fillStyle = '#2563eb';
  ctx.fillText('F', top[0] - 8, top[1] - 3);
  ctx.fillText('E', top[0] - 8, top[1] + 10);
  ctx.textAlign = 'left';
  ctx.strokeText('mg', bot[0] + 9, bot[1] + 5); ctx.fillStyle = '#334155';
  ctx.fillText('mg', bot[0] + 9, bot[1] + 5);
  /* 平衡结论与 F_B 说明：放在粒子**右下方的空白区**。
     ⚠ 不能只按粒子位置做固定像素偏移：t≈2.4s 时粒子 z≈0.30，
        pc[1]+20 恰好落在 x 轴上 ⇒ 「F = mg」压住轴线。
        故改用**世界坐标**定位到轴线下方（z = -0.20 / -0.42），
        该区域除「区域Ⅰ（B₁）」（x<0.55）外全是空白。 */
  const c1 = W2S(1.02, -0.16), c2 = W2S(1.02, -0.40);
  ctx.font = 'italic bold 13px serif';
  ctx.textAlign = 'left';
  ctx.strokeText('F = mg', c1[0], c1[1]); ctx.fillStyle = '#2563eb';
  ctx.fillText('F = mg', c1[0], c1[1]);
  ctx.font = 'italic bold 12px serif';
  ctx.fillStyle = '#7c3aed';
  ctx.fillText('F', c2[0], c2[1]);
  ctx.fillText('B', c2[0], c2[1] + 13);
  ctx.fillText('：水平方向', c2[0] + 12, c2[1] + 13);
  ctx.restore();
}

/* 粒子：实心圆 + 速度矢量 + 标签。tagPos: 0=上方, -1=左下, 1=右下 */
function drawParticle(x, z, vx, vz, color, name, tagPos){
  const p = W2S(x, z);
  ctx.save();
  ctx.fillStyle = color;
  ctx.beginPath(); ctx.arc(p[0], p[1], GEO.pr * scale, 0, 7); ctx.fill();
  ctx.strokeStyle = '#ffffff'; ctx.lineWidth = 1.6;
  ctx.beginPath(); ctx.arc(p[0], p[1], GEO.pr * scale, 0, 7); ctx.stroke();
  const n = Math.hypot(vx, vz) || 1;
  const e = W2S(x + vx / n * 0.24, z + vz / n * 0.24);
  ctx.strokeStyle = color; ctx.fillStyle = color; ctx.lineWidth = 2.4;
  ctx.beginPath(); ctx.moveTo(p[0], p[1]); ctx.lineTo(e[0], e[1]); ctx.stroke();
  const ang = Math.atan2(e[1] - p[1], e[0] - p[0]), hd = 8;
  ctx.beginPath();
  ctx.moveTo(e[0], e[1]);
  ctx.lineTo(e[0] - hd * Math.cos(ang - 0.42), e[1] - hd * Math.sin(ang - 0.42));
  ctx.lineTo(e[0] - hd * Math.cos(ang + 0.42), e[1] - hd * Math.sin(ang + 0.42));
  ctx.closePath(); ctx.fill();
  ctx.restore();
  const R = GEO.pr * scale;
  /* ⚠ 受力图期间要彻底隐藏 +q 标签：传 null 判空即可。
     若传空串 '' 会掉进 else 分支被画到粒子正上方，正好压住 F_E 箭头。 */
  if (name === null || name === undefined || name === '') return;
  if (tagPos === -1) haloTag(x, z, name, color, R + 15, -R - 6);
  else if (tagPos === 1) haloTag(x, z, name, color, R + 15, R + 6);
  else haloTag(x, z, name, color, -R - 13);
}

/* 第(3)问：xOy 俯视抛物线（整屏）。
   调用前主流程已把 VIEW 临时改为 x∈[-0.16,2.26]、y∈[-0.20,2.26]，
   故此处直接用 W2S 即可；画完由主流程还原 VIEW。
   ⚠ 顶部 HUD 占 y≈42~116px ⇒ 世界 y 上限约 1.10；底部图例占 y≈Hp-36~Hp
     ⇒ 抛物线只画到 x=1.72（y=1.48 在允许范围内需上移），故取 x_max=1.62。 */
function drawParabolaScene(st){
  const XMAX = 1.62;
  const _rr = ctx.canvas.getBoundingClientRect();
  const k2 = (_rr && _rr.width) ? Math.max(0.62, Math.min(1, _rr.width / 520)) : 1;

  /* 底色：区域Ⅰ（z ≤ z₀）说明条 */
  ctx.save();
  ctx.fillStyle = 'rgba(124,58,237,0.05)';
  ctx.fillRect(PAD, PAD, W - 2 * PAD, H - 2 * PAD);
  ctx.restore();

  /* 坐标轴：自 +z 俯视，x̂ × ŷ = ẑ */
  FIG.coord(VIEW.xmin + 0.02, 1.86, VIEW.ymin + 0.02, 2.06,
            {labels: ['x', 'y']});

  /* 抛物线 y = x²/(2R₁)（R₁=1 ⇒ y = x²/2），完整曲线用浅色，走过部分加粗 */
  const pts = [];
  for (let x = 0; x <= XMAX + 1e-9; x += 0.03) pts.push([x, x * x / 2]);
  FIG.trajectory(pts, {color: 'rgba(148,163,184,0.8)', lw: 1.8, dash: [4, 3]});
  const nw = Math.max(2, Math.round(st.x / 0.03) + 1);
  if (nw > 2) FIG.trajectory(pts.slice(0, Math.min(nw, pts.length)), {color: '#dc2626', lw: 2.6});

  /* 出发点 O 与 z 轴说明 */
  FIG.text(0.04, -0.135, 'O', {size: 14, color: '#0f172a'});

  /* 参考点：x 与 y 的对应关系，直接体现 y ∝ x²。
     ⚠ 刻度单位标注「x / R₁」若仍放在 x=0.85（正是 0.8 刻度位置）会与数字叠字，
       故单位标注移到 x 轴**右端箭头之外**，靠 VIEW.xmax 留白。 */
  for (const xr of [0.4, 0.8, 1.2, 1.6]){
    const yr = xr * xr / 2;
    ctx.save();
    ctx.fillStyle = '#0f172a';
    const p = W2S(xr, yr);
    ctx.beginPath(); ctx.arc(p[0], p[1], 2.6, 0, 7); ctx.fill();
    ctx.restore();
    FIG.text(xr, -0.145, xr.toFixed(1), {size: 11, color: '#475569', align: 'center', italic: false});
    FIG.text(-0.06, yr, yr.toFixed(2), {size: 11, color: '#475569', align: 'right', italic: false});
  }
  FIG.text(2.16, -0.145, 'x / R₁', {size: 12, color: '#334155', align: 'right', italic: false});
  /* ⚠「y / R₁」不能放在 y≈2.0（第(3)问 HUD 占住顶部约 86px），
     也不能放在 y≈1.62（会压住 0.72 刻度标签）⇒ 放到 y 轴顶端箭头上方右侧，
     该处既无刻度也无 HUD（HUD 左边界在 bx≈100px > y 轴位置）。 */
  FIG.text(-0.02, 2.14, 'y / R₁', {size: 12, color: '#334155', align: 'right', italic: false});

  /* 粒子 + 速度方向 (v, gt) ∝ (1, gt/v) = (1, x) */
  const px = st.x, py = st.x * st.x / 2;
  const nn = Math.hypot(1, px) || 1;
  const q = W2S(px, py), e = W2S(px + 0.34 / nn, py + px * 0.34 / nn);
  ctx.save();
  ctx.strokeStyle = '#dc2626'; ctx.fillStyle = '#dc2626'; ctx.lineWidth = 2.4;
  ctx.beginPath(); ctx.moveTo(q[0], q[1]); ctx.lineTo(e[0], e[1]); ctx.stroke();
  const a2 = Math.atan2(e[1] - q[1], e[0] - q[0]);
  ctx.beginPath(); ctx.moveTo(e[0], e[1]);
  ctx.lineTo(e[0] - 9 * Math.cos(a2 - 0.42), e[1] - 9 * Math.sin(a2 - 0.42));
  ctx.lineTo(e[0] - 9 * Math.cos(a2 + 0.42), e[1] - 9 * Math.sin(a2 + 0.42));
  ctx.closePath(); ctx.fill();
  ctx.beginPath(); ctx.arc(q[0], q[1], 5.4, 0, 7); ctx.fill();
  ctx.strokeStyle = '#fff'; ctx.lineWidth = 1.6;
  ctx.beginPath(); ctx.arc(q[0], q[1], 5.4, 0, 7); ctx.stroke();
  ctx.restore();
  /* +q 放粒子正上方 -30px：速度分量标注已移到左上方（-16/-2px），
     若 +q 仍用 -18px 会与 vx/vy 首行叠字。 */
  haloTag(px, py, '+q', '#dc2626', -30);
  /* 速度分量标注：仅在粒子离开原点后显示。
     ⚠ 水平放在粒子右侧会与右下角的「结论卡片」（x∈[1.05,1.98], y∈[0.22,0.62]）
       在中段帧相撞 ⇒ 改为放在粒子**左上方**（抛物线上方恒为空白）。 */
  if (st.x > 0.30){
    ctx.save();
    ctx.font = 'italic bold 12.5px serif';
    ctx.textAlign = 'right';
    ctx.lineWidth = 3.6; ctx.strokeStyle = 'rgba(255,255,255,0.94)';
    const s1 = 'vx = v', s2 = 'vy = gt';
    const bx = q[0] - 12, by1 = q[1] - 16, by2 = q[1] - 2;
    ctx.strokeText(s1, bx, by1); ctx.fillStyle = '#b91c1c'; ctx.fillText(s1, bx, by1);
    ctx.strokeText(s2, bx, by2); ctx.fillText(s2, bx, by2);
    ctx.textAlign = 'left';
    ctx.restore();
  }

  /* 说明：z ≡ 0 ⇒ 始终在区域Ⅰ 内，不会跨界面。
     ⚠ ① ctx.fillText 的坐标是**屏幕像素**，直接写世界坐标会把文字丢到画布左上角
          （表现为画布顶端一条被裁掉的残字）⇒ 必须先过 W2S。
       ② 这两行必须避开「粒子 + 速度分量标注」：粒子沿抛物线右移，
          y≈0.3~0.6 的中段在 x≈0.9 附近被粒子与 vx/vy 文字占据。
          抛物线在低 x 处紧贴 x 轴 ⇒ 画面左上 (x∈[0.05,1.0], y≈0.8~1.0) 必然空白。
       ③ ⚠ 用 textAlign='center'/'right' 且锚点 x 太靠左 ⇒ 文字整行跑出画布左缘被裁。
          「轨迹：y = gx²/(2v²)，z = 0」14px 粗体宽约 230px，
          画布 CSS 宽 515 ⇒ 锚点屏幕 x 必须 > 240px（世界 x ≳ 0.70）才放得下。
       ④ 纵向也不能乱放：抛物线在 x=1.2 处 y=0.72、x=1.6 处 y=1.28，
          参考点就落在这两点上。故结论放在**曲线下方** y≈0.30 一带：
          该处 x∈[1.0,1.9] 全是空白（抛物线 y 值更高、参考点在曲线上）。 */
  ctx.save();
  ctx.textAlign = 'left';
  /* 粒子沿抛物线移动，结论文字是静态的：无论怎么挪位置，在某一帧都会与
     「+q / vx / vy」标注擦边。故给两行铺一块白底卡片 ——
     既保证任何时刻都不叠字，视觉上也把「结论」与「图」明确分开。
     卡片必须完全落在 y∈[0.24,0.62]、x∈[1.05,1.98] 这块**曲线下方**的空白里：
     抛物线在 x=1.2/1.6 处 y=0.72/1.28，参考点都在曲线上；
     x 轴刻度标签在 y=-0.145、图例在画布底部，都不能碰。 */
  const cT = W2S(1.00, 0.62)[1] + 4 * k2;     /* 卡片顶 */
  const cB = W2S(1.00, 0.22)[1] - 4 * k2;     /* 卡片底 */
  const cL = W2S(1.05, 0.4)[0] - 7 * k2;
  const cR = W2S(1.98, 0.4)[0] + 4 * k2;
  ctx.fillStyle = 'rgba(255,255,255,0.93)';
  ctx.strokeStyle = '#e2e8f0'; ctx.lineWidth = 1;
  ctx.fillRect(cL, cT, cR - cL, cB - cT);
  ctx.strokeRect(cL, cT, cR - cL, cB - cT);
  ctx.font = 'bold 13.5px serif';
  const c2 = W2S(1.07, 0.49);
  ctx.lineWidth = 3.4; ctx.strokeStyle = 'rgba(255,255,255,0.95)';
  ctx.strokeText('轨迹：y = gx² / (2v²)，z = 0', c2[0], c2[1]);
  ctx.fillStyle = '#b91c1c';
  ctx.fillText('轨迹：y = gx² / (2v²)，z = 0', c2[0], c2[1]);
  ctx.font = '11px sans-serif';
  ctx.lineWidth = 3.2;
  const c1 = W2S(1.07, 0.31);
  ctx.strokeText('z ≡ 0 ⇒ 始终留在区域Ⅰ，不穿越界面', c1[0], c1[1]);
  ctx.fillStyle = '#475569';
  ctx.fillText('z ≡ 0 ⇒ 始终留在区域Ⅰ，不穿越界面', c1[0], c1[1]);
  ctx.restore();
}
"""

READOUTS_JS = r"""
/* =========================================================================
   数据面板读数（与 stateAt 共用同一套几何，保证「动画 = 解析可视化」）
   ========================================================================= */
const st = stateAt(t);
const rows = [];
const DEG = 180 / Math.PI;

if (st.phase === 'q3'){
  rows.push(['当前过程', '第(3)问  电场沿 +y', '']);
  rows.push(['$x$ 方向', '匀速 $v$', '']);
  rows.push(['$y$ 方向', '匀加速 $g$', '']);
  rows.push(['$F_B$', '$qvB_1 = mg$', '（抵消重力）']);
  rows.push(['$a$', '$(0,\\ g,\\ 0)$', 'm/s²']);
  rows.push(['$t$（示意）', st.tHat.toFixed(2), '× 2 s']);
  rows.push(['$x = vt$', st.x.toFixed(3), 'R₁']);
  rows.push(['$y = gx^2/2v^2$', (st.x * st.x / 2).toFixed(3), 'R₁']);
  rows.push(['$z$', '0（恒在区域Ⅰ）', '']);
  return rows;
}

rows.push(['当前过程', st.phase === 'q1' ? '第(1)问  区域Ⅰ 圆弧' : '第(2)问  往返穿越界面', '']);
if (st.atP) rows.push(['状态', '已到达 P 点', '']);
rows.push(['$R_1 = v^2/g$', '1.000', '（长度单位）']);
rows.push(['$z_0 = 2v^2/5g$', PAR.z0.toFixed(3), 'R₁']);
rows.push(['$P$ 点', PAR.XP.toFixed(3), 'R₁']);
rows.push(['$E = mg/q$', '1.000', '（竖直向上）']);
rows.push(['$B_1 = mg/qv$', '1.000', '⊗ 向里']);

if (st.phase === 'q1'){
  rows.push(['所在区域', '区域Ⅰ（$z < z_0$）', '']);
  rows.push(['半径 $R$', st.R.toFixed(4), 'R₁']);
  rows.push(['已转角 $\\theta$', (st.tau * DEG).toFixed(2), 'deg']);
  rows.push(['当前位置 $x$', st.x.toFixed(4), 'R₁']);
  rows.push(['当前位置 $z$', st.z.toFixed(4), 'R₁']);
  rows.push(['速度方向', '(' + st.vx.toFixed(3) + ', ' + st.vz.toFixed(3) + ')', '']);
  if (st.tau > 1e-6) rows.push(['第一次过界面 $x$', '0.800 = 4v²/(5g)', 'R₁']);
} else {
  rows.push(['$r_2 = R_2/R_1$', PAR.r2.toFixed(4), '（$k=3$）']);
  rows.push(['$B_2 = k/(k-2)\\,B_1$', '3.000 B₁ = 3mg/(qv)', '']);
  rows.push(['所在区域', st.reg === 'I' ? '区域Ⅰ' : '区域Ⅱ', '']);
  rows.push(['本段半径 $R$', st.R.toFixed(4), 'R₁']);
  rows.push(['本段序号', '第 ' + (st.seg + 1) + ' 段 / 共 7 段', '']);
  rows.push(['本段已转角', (st.frac * SEGS[st.seg].sweep * DEG).toFixed(2), 'deg']);
  rows.push(['当前位置 $x$', st.x.toFixed(4), 'R₁']);
  rows.push(['当前位置 $z$', st.z.toFixed(4), 'R₁']);
  rows.push(['速度方向', '(' + st.vx.toFixed(3) + ', ' + st.vz.toFixed(3) + ')', '']);
  rows.push(['相切点 $x_1$', GEO.xTan1.toFixed(4), 'R₁']);
  rows.push(['相切点 $x_2$', GEO.xTan2.toFixed(4), 'R₁']);
  rows.push(['$\\tau$（$t\\cdot v/R_1$）', st.tau.toFixed(4), '']);
  rows.push(['$t_{min}$', '(2π + 4arccos 3/5)·v/g ≈ 9.9924 v/g', '']);
}
return rows;
"""

# ============================================================
# 六、写入模板
# ============================================================
tpl = open(TPL, encoding='utf-8').read()

# ⚠ 写进 JS 源码的字面量必须做 JS 转义：Python 的 %r 只在串含单引号时才转义反斜杠，
#   'a\Db' 的 repr 仍是 'a\Db'，而 JS 会把 \D 当转义序列吞掉反斜杠 ⇒ MathJax 收到 'aDb'。
#   统一走 json.dumps（与 JS 字面量完全兼容）。
import json as _json


def _js(s):
    return _json.dumps(s, ensure_ascii=False)


prob_js = (
    "const PROBLEM = {\n"
    "  title: %s,\n"
    "  given: %s,\n"
    "  images: [{ src: \"__CANVAS_STATIC__\", caption: \"\" }],\n"
    "  asks: [\n%s\n  ],\n"
    "  options: [],\n"
    "  knowledgePoints: [%s]\n"
    "};\n"
) % (
    _js(PROBLEM_TITLE),
    _js(PROBLEM_GIVEN),
    '\n'.join('    %s,' % _js(a) for a in PROBLEM_ASKS),
    ', '.join('{ id: "%s" }' % k for k in KNOWLEDGE_IDS),
)

steps_js = "const STEPS = [\n"
for _s in STEPS:
    steps_js += ("  { q: %d, title: %s, tex: %s, note: %s, basis: %s, t0: %s, t1: %s },\n"
                 % (_s['q'], _js(_s['title']), _js(_s['tex']),
                    _js(_s['note']), _js(_s['basis']),
                    _s['t0'], _s['t1']))
steps_js += "];\n"

view_js = ("const VIEW = { xmin: %s, xmax: %s, ymin: %s, ymax: %s };\n"
           "const SIM  = { duration: %s };\n"
           % (VIEW['xmin'], VIEW['xmax'], VIEW['ymin'], VIEW['ymax'], T_END))


def _repl(text, marker, payload):
    pat = _re.compile(r'/\*\s*' + marker + r'\s*\*/')
    return pat.sub(lambda m: payload, text, count=1)


BANNERS_JS = ("const BANNERS = %s;\n"
              % ('[' + ','.join('[%.2f,%.2f,"%s"]' % (a, b, c) for a, b, c in TIMELINE) + ']'))

out = tpl
# ⚠ 必须用 lambda 返回替换串：re.sub 会把替换字符串里的 \b \d \t \f 等
#   当成「反向引用 / 转义」处理，直接吞掉反斜杠 ⇒ JS 里 LaTeX 变成 'big'、'Delta'，
#   MathJax 收到残缺公式 ⇒ Math input error。（历史上 %r 版本也是栽在这里。）
out = _re.sub(r'const PROBLEM = \{[\s\S]*?\n\};', lambda m: prob_js.rstrip('\n'), out, count=1)
out = _re.sub(r'const STEPS = \[[\s\S]*?\n\];', lambda m: steps_js.rstrip('\n'), out, count=1)
out = _re.sub(r'const VIEW = \{[^\n]*\n\s*const SIM\s*=\s*\{[^\n]*\n', lambda m: view_js, out, count=1)

out = _repl(out, '__GLOBALS__', GLOBALS_JS.strip() + '\n\n' + HELPERS_JS.strip()
            + '\n\n' + BANNERS_JS)
out = _repl(out, '__SETUP__', SETUP_JS.strip())
out = _repl(out, '__DRAWFRAME__', DRAWFRAME_JS.strip())
out = _repl(out, '__READOUTS__', READOUTS_JS.strip())

CSS_TUNE = (
    '<style id="tune-width">\n'
    '.col-analysis{flex:1.95 1 400px}\n'
    '.step{padding:8px 9px 8px 11px}\n'
    '.step .tex{padding:2px 0 6px}\n'
    '.step .tex mjx-container[display="true"]{max-width:100%}\n'
    '.step .tex mjx-container[display="true"] svg{max-width:100%;height:auto}\n'
    '.step .note{line-height:1.62}\n'
    '</style>\n'
)
out = out.replace('</head>', CSS_TUNE + '</head>', 1) if '</head>' in out else CSS_TUNE + out

open(OUT, 'w', encoding='utf-8').write(out)

probes = [PROBLEM_TITLE, '__CANVAS_STATIC__', 'em-cyclotron', 'processBanner',
          'FIG.magInto', 'function stateAt', 'const BANNERS', 'function segPos',
          '4v^{2}}{5g', '3mg}{qv', 'dfrac{gx^{2}}{2v^{2}}',
          'x_k=1.6k', 'y = gx²/(2v²)', 'pathIndexOf', 'drawParabolaScene', 'FIELD_AVOID',
          # 回归探针：JS 转义（re.sub 吞反斜杠）、PATH_OFF 哨兵、粒子标签判空
          '_js(PROBLEM_TITLE)', 'PATH_OFF.push(FULL_PATH.length)',
          "name === null || name === undefined", 'nearIface',
          '__GLOBALS__', '__SETUP__', '__DRAWFRAME__', '__READOUTS__']
print('=== 探针自检 ===')
for _p in probes:
    print(('FOUND   ' if _p in out else 'MISSING ') + _p)
print('\noutput: %s  (%d bytes)' % (OUT, os.path.getsize(OUT)))

# ==== 反斜杠层数硬门禁 =====================================================
# 产物 HTML 里，JS 字符串字面量中的 LaTeX 必须写成两个反斜杠（\\Delta），
# 否则 JS 解析时 \D 被当转义序列吞掉 ⇒ MathJax 收到 'Delta' ⇒ Math input error。
# 这层检查比 Playwright 门禁更早发现，能直接指出是哪个公式被吞。
_out = _io.open(OUT, encoding='utf-8').read()
_bad = []
for _m in _re.finditer(r'tex: "((?:[^"\\]|\\.)*)"', _out):
    _t = _m.group(1)
    if _re.search(r'(?<!\\)\\[A-Za-z]', _t):      # 单反斜杠 + 字母 = 危险
        _bad.append(_t[:70])
print('=== 反斜杠层数自检 ===')
if _bad:
    for _b in _bad:
        print('BAD  单反斜杠: %s' % _b)
    raise SystemExit('反斜杠被吞：re.sub 替换串未用 lambda 包一层')
print('PASS  全部 tex 反斜杠已正确转义（%d 条）'
      % len(_re.findall(r'tex: "', _out)))
print('TAU = %s' % ['%.6f' % v for v in TAU])
print('T_total = %.7f  (期望 2*pi+4*acos(3/5) = %.7f)' % (T_TOTAL, 2 * math.pi + 4 * A))
print('r2 = %.6f  B2/B1 = %.4f' % (R2, 1.0 / R2))
print('x_tan1 = %.6f  x_tan2 = %.6f' % (X_TAN1, X_TAN2))