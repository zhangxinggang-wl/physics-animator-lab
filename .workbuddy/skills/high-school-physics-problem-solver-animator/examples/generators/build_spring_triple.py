# -*- coding: utf-8 -*-
"""生成《2026·江苏·16 双弹簧连接的 A、A₁、A₂ 与 B 的弹性正碰》教学动画。

物理内核（与官方答案逐条核对）
--------------------------------
小球：A 质量 m；A₁、A₂ 各 3m/5（分别套在两根平行的固定细杆上，只能沿杆方向运动）；
B 质量 M，以 v₀ 沿平行于细杆的方向与 A 发生弹性正碰。

(1) 弹性正碰（B 与 A，弹簧还来不及形变）：
    v₁ = 2M/(M+m)·v₀，u_B = (M−m)/(M+m)·v₀
(2) 碰后系统只有沿杆方向的速度：由对称性 A₁、A₂ 同步运动，形变量始终相同 d。
    动量守恒：m v₁ = (m + 2·3m/5)V ⇒ V = 5v₁/11（与 M 无关）
    共速瞬间形变量最大 ⇒ 弹性势能最大：
    ½mv₁² = ½·(11m/5)V² + 2Ep ⇒ Ep,max = 3mv₁²/22 = 6mM²v₀²/(11(M+m)²)
    以 d_max 为世界单位：ω² = 11k/(3m)，d̈ = −ω²d ⇒ d = d_max sin ωt，d_max = v₁/ω
    A 的位移 x_A = Vt + (6/11)d_max sin ωt，A₁ 的位移 x₁ = Vt − (5/11)d_max sin ωt
    速度：v_A = V + (6/11)v₁cos ωt，v₁' = V − (5/11)v₁cos ωt
(3) 弹簧再次恢复原长（t = T/2 = π/ω）时：d = 0，相对速度反向 ⇒
    v_A = −v₁/11，v_A₁ = v_A₂ = 10v₁/11
    此时 A 的位移 = V·T/2（平均速度恰为 V），B 的位移 = u_B·T/2。
    「B 又恰能与 A 碰撞」⇒ 同时刻同位置 ⇒ u_B = V ⇒
    (M−m)/(M+m) = (5/11)·2M/(M+m) ⇒ 11(M−m) = 10M ⇒ m/M = 1/11（演示取此值）

演示用无量纲化：v₀ = 1、m = 1、M = 11、ω = v₁（于是 d_max = 1 世界单位），
1 世界单位 = d_max，时间即真实秒。故 A 的位移上限 = 5π/11 ≈ 1.4286，B 的速率 5/6。
整段动画冻结在：初始 / 碰后瞬间 / 共速（Ep 最大）/ 恢复原长（再次相碰）。
"""
import os
import re
import json
import math

LAB = r'C:/Users/19368/Desktop/physics-animator-lab'
SKILL = os.path.join(LAB, '.workbuddy', 'skills', 'high-school-physics-problem-solver-animator')
TPL = os.path.join(SKILL, 'assets', 'template.html')
OUT = os.path.join(LAB, '2026江苏16_双弹簧三球_教学动画.html')

PI = math.pi
V0 = 1.0
MASS_A = 1.0                 # m
MASS_B = 11.0                # M = 11m  ⇒ m/M = 1/11
MASS_S = 0.6 * MASS_A        # 每根弹簧末端小球 3m/5
V1 = 2 * MASS_B / (MASS_B + MASS_A) * V0          # 11/6
UB = (MASS_B - MASS_A) / (MASS_B + MASS_A) * V0   # 5/6
OMEGA = V1                   # 使 d_max = v₁/ω = 1（世界单位）
THALF = PI / OMEGA           # 弹簧再次恢复原长的时刻（碰后计时）
VCOM = 5 * V1 / 11           # 共速速度 = 5v₁/11
DMAX = 1.0
KSPR = 3 * MASS_A * OMEGA ** 2 / 11               # 每根弹簧劲度（ω² = 11k/3m）
EPMAX = 0.5 * KSPR * DMAX ** 2                    # 每根弹簧最大弹性势能

# ============================================================
# 一、物理自检
# ============================================================
assert abs(V1 - 11 / 6) < 1e-12
assert abs(UB - 5 / 6) < 1e-12
assert abs(VCOM - UB) < 1e-12, '第(3)问的核心：B 的速度恰等于系统共速'
EP_SYMB = 6 * MASS_A * MASS_B ** 2 * V0 ** 2 / (11 * (MASS_B + MASS_A) ** 2)
assert abs(EPMAX - EP_SYMB) < 1e-12, (EPMAX, EP_SYMB)
assert abs(EPMAX - 3 * MASS_A * V1 ** 2 / 22) < 1e-12
assert abs(KSPR - 11 / 12) < 1e-12


def xA(t):
    return VCOM * t + (6 / 11) * DMAX * math.sin(OMEGA * t)


def xS(t):
    return VCOM * t - (5 / 11) * DMAX * math.sin(OMEGA * t)


def vA(t):
    return VCOM + (6 / 11) * V1 * math.cos(OMEGA * t)


def vS(t):
    return VCOM - (5 / 11) * V1 * math.cos(OMEGA * t)


assert abs(xA(THALF) - UB * THALF) < 1e-12          # 恢复原长时 A 与 B 同位置
assert abs(xA(THALF) - 5 * PI / 11) < 1e-12         # A 的总位移
assert abs(vA(THALF) + V1 / 11) < 1e-12             # A 反向：−v₁/11
assert abs(vS(THALF) - 10 * V1 / 11) < 1e-12
assert abs(0.5 * MASS_A * V1 ** 2
           - (0.5 * 11 * MASS_A / 5 * VCOM ** 2 + 2 * EPMAX)) < 1e-12
_gapmin = min((6 / 11) * DMAX * math.sin(OMEGA * THALF * i / 400) for i in range(1, 400))
assert _gapmin > 0, 'B 与 A 在恢复原长之前必须保持不碰'

# ============================================================
# 二、动画几何（世界单位 = d_max；x 向右，y 向上；俯视图）
# ============================================================
R_A = 0.15          # A 的半径
R_B = 0.14          # B 的半径
R_S = 0.115         # A₁、A₂ 的半径
CONTACT = -(R_A + R_B)          # 碰后 A、B 球心的相对位置（B 球心）
B_X0 = -3.10                    # B 的出发点
L_ROD = 1.28                    # 细杆到中轴的距离（= 弹簧原长）

VIEW = dict(xmin=-3.35, xmax=2.25, ymin=-1.62, ymax=1.74)
assert abs((VIEW['ymax'] - VIEW['ymin']) / (VIEW['xmax'] - VIEW['xmin']) - 0.6) < 1e-9

# ============================================================
# 三、屏幕时间轴（秒）= 物理时间；四处定格
# ============================================================
T_IMP = (CONTACT - B_X0) / V0    # B 球心走到碰点（球面相切）所需时间
T_HOLD0 = 0.70                   # 初始定格
T_HIT1 = T_HOLD0 + T_IMP         # 3.80 第一次碰撞
T_HIT2 = T_HIT1 + 0.30           # 碰撞闪光定格结束
T_MAX = T_HIT2 + THALF / 2       # 共速、形变量最大
T_MAXH = T_MAX + 0.65            # 共速定格
T_NAT = T_MAXH + THALF / 2       # 弹簧恢复原长、B 恰追上 A
T_END = T_NAT + 1.20

TIMELINE = [
    (0.0, T_HOLD0, '① 初始：三球静止，弹簧均为原长'),
    (T_HOLD0, T_HIT1, '② B 以 v₀ 匀速驶向 A'),
    (T_HIT1, T_HIT2, '③ 弹性正碰：A 获得 v₁'),
    (T_HIT2, T_MAX, '④ 弹簧被拉长：A 减速、A₁A₂ 加速'),
    (T_MAX, T_MAXH, '⑤ 共速瞬间：形变量最大'),
    (T_MAXH, T_NAT, '⑥ 弹簧收缩回原长'),
    (T_NAT, T_END, '⑦ B 恰追上 A：再次碰撞'),
]

# ============================================================
# 四、题面
# ============================================================
PROBLEM_TITLE = '16.（2026·江苏·16）'
PROBLEM_GIVEN = (
    r'如图 16 所示，光滑水平面上质量为 \(m\) 的小球 \(A\) 通过两根相同的轻质弹簧分别与质量均为 '
    r'\(\dfrac{3}{5}m\) 的小球 \(A_1\)、\(A_2\) 连接，\(A_1\)、\(A_2\) 分别套在两根平行的细杆上，'
    r'细杆固定、光滑且足够长。初始时 \(A\)、\(A_1\)、\(A_2\) 位于垂直于细杆的直线上且处于静止状态，'
    r'每根弹簧都处于原长。现有质量为 \(M\) 的小球 \(B\) 以速度 \(v_0\) 沿平行于细杆的方向与 \(A\) '
    r'发生弹性正碰。'
)
PROBLEM_ASKS = [
    r'（1）求 \(A\) 获得的速度大小 \(v_1\)；',
    r'（2）在弹簧再次恢复原长的过程中，若 \(B\) 与 \(A\) 不发生碰撞，求此过程中每根弹簧的最大弹性势能 '
    r'\(E_{p\max}\)；',
    r'（3）在弹簧再次恢复原长时，若 \(B\) 又恰能与 \(A\) 碰撞，求 \(A\)、\(B\) 两球的质量之比 '
    r'\(\dfrac{m}{M}\)。',
]
KNOWLEDGE_IDS = ['mech-momentum-collision-1d', 'mech-momentum-conservation',
                 'mech-energy-conservation', 'mech-energy-spring-potential',
                 'mech-force-spring']

# ============================================================
# 五、STEPS
# ============================================================
STEPS = [
    dict(q=1, t0=0.0, t1=T_HIT1,
         title='碰前：B 匀速接近，A 与 A₁、A₂ 仍静止',
         tex=r'Mv_0=Mu+Mv_1,\qquad '
             r'\tfrac{1}{2}Mv_0^{2}=\tfrac{1}{2}Mu^{2}+\tfrac{1}{2}Mv_1^{2}',
         note='碰撞时间极短，弹簧还来不及形变，因此<b>只有 A 参与碰撞</b>，'
              r'A₁、A₂ 在碰后瞬间速度仍为零。取碰后 A 的速度方向（即 \(v_0\) 方向）为正，'
              '动量守恒给出动量式；题目说「弹性正碰」，补充动能守恒式。',
         basis='动量守恒定律 + 弹性碰撞（动能守恒）'),
    dict(q=1, t0=T_HIT1, t1=T_HIT2,
         title='解得 A 获得的速率',
         tex=r'v_1=\frac{2M}{M+m}v_0,\qquad u=\frac{M-m}{M+m}v_0',
         note=r'联立两式得 \(v_1=\dfrac{2M}{M+m}v_0\)（即本题第 (1) 问答案）。'
              r'同时得 B 碰后的速度 \(u=\dfrac{M-m}{M+m}v_0\)：因 \(M>m\)，B 碰后<b>仍沿原方向前进</b>，'
              r'只是变慢了——这正是第 (3) 问中 B 还能追上 A 的前提。'
              r'检验：若 \(M=m\)，则 \(v_1=v_0\)、\(u=0\)（等质量弹性正碰交换速度），与常识一致。',
         basis='弹性正碰的结论式'),
    dict(q=2, t0=T_HIT2, t1=T_MAX,
         title='碰后：三球共速时形变量最大',
         tex=r'mv_1=\left(m+2\cdot\tfrac{3}{5}m\right)V\ \Rightarrow\ V=\frac{5}{11}v_1',
         note=r'碰后 A 向右运动、A₁ 和 A₂ 被弹簧拉动，两弹簧的形变量始终相同（对称）。'
              '整个系统在沿杆方向不受外力，<b>动量守恒</b>；当三球速度相同时，'
              'A 与 A₁、A₂ 的相对速度为零、弹簧形变量达到最大，此后就要开始收缩。'
              r'注意 \(V=\dfrac{5}{11}v_1\) <b>与 \(M\) 无关</b>。',
         basis='动量守恒定律 + 弹簧形变最值条件'),
    dict(q=2, t0=T_MAX, t1=T_MAXH,
         title='能量守恒求每根弹簧的最大弹性势能',
         tex=r'\begin{aligned}\tfrac{1}{2}mv_1^{2}&=\tfrac{1}{2}\cdot\tfrac{11}{5}mV^{2}'
             r'+2E_{p\max}\\ E_{p\max}&=\tfrac{3}{22}mv_1^{2}'
             r'=\frac{6mM^{2}v_0^{2}}{11(M+m)^{2}}\end{aligned}',
         note='形变最大时三球共速，弹性势能最大、动能最小。系统的机械能守恒：'
              r'碰后 A 的动能 \(=\ \)共速时三球的动能 \(+\) 两根弹簧的弹性势能（每根 \(E_{p\max}\)，故乘 2）。'
              r'把 \(v_1=\dfrac{2M}{M+m}v_0\) 代入即得第 (2) 问答案。',
         basis='机械能守恒定律（或能量守恒定律）'),
    dict(q=3, t0=T_MAXH, t1=T_NAT,
         title='弹簧再次恢复原长时：各球速度',
         tex=r'd=0\ \Rightarrow\ v_A=-\frac{v_1}{11},\quad '
             r'v_{A_1}=v_{A_2}=\frac{10}{11}v_1',
         note=r'弹簧再次恢复原长时形变量回到零，A 与 A₁ 的<b>相对速度大小又回到 \(v_1\)，方向相反</b>；'
              r'再由沿杆方向动量守恒 \(v_A+\dfrac{6}{5}v_{A_1}=v_1\)。两式联立即得：'
              r'A 已被弹簧拉回（\(v_A\lt 0\)，大小只有 \(v_1/11\)），而 A₁、A₂ 速度快到 \(10v_1/11\)。',
         basis='动量守恒 + 简谐运动的半周期对称性'),
    dict(q=3, t0=T_NAT, t1=T_END,
         title='位移条件 ⇒ m/M = 1/11',
         tex=r'\frac{M-m}{M+m}v_0=\frac{5}{11}\cdot\frac{2M}{M+m}v_0'
             r'\ \Rightarrow\ \frac{m}{M}=\frac{1}{11}',
         note=r'A 相对原点的位移 \(x_A=Vt+\dfrac{6}{11}d_{\max}\sin\omega t\)，其<b>平均值恰为 \(V\)</b>，'
              r'故一个半周期内 A 的位移为 \(V\cdot\dfrac{T}{2}\)；B 碰后匀速，位移为 \(u\cdot\dfrac{T}{2}\)。'
              r'「恰能再次碰撞」= 此时刻两者<b>同时同地</b> ⇒ \(u=V\)。代入 \(u\)、\(V\) 即可解出 '
              r'\(\dfrac{m}{M}=\dfrac{1}{11}\)。'
              r'（在此之前 B 始终落后于 A：间距 \(=\dfrac{6}{11}d_{\max}\sin\omega t>0\)，'
              r'所以确实「不发生碰撞」。）',
         basis='运动学（平均速度）+ 追及相遇的临界条件'),
]

# ============================================================
# 六、GLOBALS
# ============================================================
GLOBALS_JS = r"""
/* =========================================================================
   世界单位 = d_max（弹簧最大形变量）。俯视图：x 沿细杆向右，y 垂直细杆向上。
   v₀ = 1、m = 1、M = 11、ω = v₁ ⇒ d_max = 1；时间即真实秒。
   ========================================================================= */
const PAR = {
  V0: 1.0,
  V1: /*@V1@*/,          /* 11/6 */
  UB: /*@UB@*/,          /* 5/6  B 碰后速度 */
  VCOM: /*@VCOM@*/,      /* 5/6  三球共速 */
  OMG: /*@OMG@*/,        /* ω = v₁ */
  THALF: /*@THALF@*/,    /* π/ω */
  DMAX: 1.0,
  K: /*@K@*/,            /* 每根弹簧劲度 11/12 */
  EPMAX: /*@EPMAX@*/,    /* 每根最大弹性势能 3mv₁²/22 */
  L: /*@L@*/,            /* 细杆到中轴距离（= 原长） */
  XB0: /*@XB0@*/,
  CX: /*@CX@*/,          /* 碰点处 B 球心的 x */
  RA: 0.15, RB: 0.14, RS: 0.115,
  NTOT: /*@NTOT@*/       /* 时间轴节点个数（仅作图例排版用） */
};
const BANNERS = /*@BANNERS@*/;

/* 时间轴节点（秒） */
const T_HOLD0 = /*@HOLD0@*/, T_HIT1 = /*@HIT1@*/, T_HIT2 = /*@HIT2@*/,
      T_MAX = /*@TMAX@*/, T_MAXH = /*@TMAXH@*/, T_NAT = /*@TNAT@*/,
      T_ENDA = /*@TEND@*/;
const TZ = /*@TZVAL@*/;      /* 碰撞对应的物理时刻（B 球心到达碰点） */

/* 阶段：0 初始 1 接近 2 碰撞 3 拉长 4 共速 5 收缩 6 再碰撞 */
function phaseOf(t){
  if (t < T_HOLD0) return 0;
  if (t < T_HIT1) return 1;
  if (t < T_HIT2) return 2;
  if (t < T_MAX) return 3;
  if (t < T_MAXH) return 4;
  if (t < T_NAT) return 5;
  return 6;
}
const PHASE_NAMES = ['① 初始', '② B 接近', '③ 弹性正碰', '④ 弹簧拉长',
                     '⑤ 共速（Ep 最大）', '⑥ 弹簧收缩', '⑦ 再次碰撞'];

/* 物理时间：碰撞前 τ = t，碰撞后 τ = t - 碰后经过的时间；四处定格用常量段表示 */
function tauOf(t){
  const P = PAR;
  if (t < T_HOLD0) return 0;
  if (t < T_HIT1) return (t - T_HOLD0);                    /* 走向碰点 */
  if (t < T_HIT2) return TZ;                             /* 定格：碰后 τ=0 */
  if (t < T_MAX) return TZ + (t - T_HIT2);
  if (t < T_MAXH) return TZ + P.THALF / 2;               /* 定格：共速 */
  if (t < T_NAT) return TZ + P.THALF / 2 + (t - T_MAXH);
  return TZ + P.THALF;                                   /* 定格：恢复原长 */
}

/* 状态函数：画面与数据面板共用同一份公式 */
function stateAt(t){
  const P = PAR, ph = phaseOf(t), tau = tauOf(t);
  const to = tau - TZ;                    /* 碰后物理时间（<0 表示尚未碰撞） */
  let ax, a1x, bx, av, a1v;
  if (to < 0){
    ax = 0; a1x = 0; av = 0; a1v = 0;
    bx = P.XB0 + tau;                       /* B 匀速驶向 A */
  } else {
    const s = Math.sin(P.OMG * to), c = Math.cos(P.OMG * to);
    ax = P.VCOM * to + (6 / 11) * P.DMAX * s;
    a1x = P.VCOM * to - (5 / 11) * P.DMAX * s;
    av = P.VCOM + (6 / 11) * P.V1 * c;
    a1v = P.VCOM - (5 / 11) * P.V1 * c;
    bx = P.CX + P.UB * to;
  }
  const d = ax - a1x;
  return { ph: ph, tau: tau, to: to, ax: ax, a1x: a1x, bx: bx,
           av: av, a1v: a1v, d: d, ep: 0.5 * P.K * d * d,
           bv: (to < 0 ? P.V0 : P.UB), gap: ax - bx, pre: (to < 0) };
}
"""

# ============================================================
# 七、HELPERS（世界原语；像素原语只用于左下角图例）
# ============================================================
HELPERS_JS = r"""
/* ---- 带白描边的文字（动态标签一律 halo，避免白底切断弹簧/细杆） ---- */
function lab(x, y, str, o){
  o = o || {};
  const p = W2S(x, y);
  const fs = o.size || 14;
  ctx.save();
  ctx.font = (o.italic === false ? '' : 'italic ') + 'bold ' + fs + 'px ' +
             ((o.sans === true || o.italic === false) ? 'sans-serif' : 'serif');
  ctx.textAlign = o.align || 'left';
  if (o.halo !== false){
    ctx.lineWidth = 3.4; ctx.strokeStyle = 'rgba(255,255,255,0.96)';
    ctx.strokeText(str, p[0], p[1]);
  }
  ctx.fillStyle = o.color || '#111827';
  ctx.fillText(str, p[0], p[1]);
  ctx.restore();
}

/* ---- 任意方向 z 字形弹簧（世界坐标），圈数固定 ⇒ 拉长时圈距变大，视觉上真的"被拉开" ---- */
function springSeg(ax, ay, bx, by, o){
  o = o || {};
  const coils = o.coils || 13, amp = (o.amp != null ? o.amp : 0.062);
  const dx = bx - ax, dy = by - ay, len = Math.hypot(dx, dy) || 1e-6;
  const ux = dx / len, uy = dy / len, nx = -uy, ny = ux;
  const lead = 0.10;
  const pts = [[ax, ay]];
  pts.push([ax + ux * len * lead * 0.6, ay + uy * len * lead * 0.6]);
  for (let i = 1; i <= coils; i++){
    const tt = lead * 0.6 + (1 - lead * 1.2) * (i - 0.5) / coils;
    const sg = (i % 2 ? 1 : -1) * amp;
    pts.push([ax + ux * len * tt + nx * sg, ay + uy * len * tt + ny * sg]);
  }
  pts.push([ax + ux * len * (1 - lead * 0.6), ay + uy * len * (1 - lead * 0.6)]);
  pts.push([bx, by]);
  FIG.wire(pts, {lw: (o.lw || 1.8), color: o.color || '#92400e'});
}

/* ---- 虚线段（世界坐标） ---- */
function dashLine(x1, y1, x2, y2, color, lw, dash){
  const a = W2S(x1, y1), b = W2S(x2, y2);
  ctx.save();
  ctx.setLineDash(dash || [4, 4]);
  ctx.strokeStyle = color || '#cbd5e1'; ctx.lineWidth = lw || 1;
  ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.lineTo(b[0], b[1]); ctx.stroke();
  ctx.restore();
}

/* ---- 小球（质心实心圆 + 深色描边） ---- */
function ball(x, y, r, fill, edge){
  const p = W2S(x, y);
  ctx.save();
  ctx.beginPath(); ctx.arc(p[0], p[1], r * scale, 0, 7);
  ctx.fillStyle = fill; ctx.fill();
  ctx.lineWidth = 1.7; ctx.strokeStyle = edge || '#7c2d12'; ctx.stroke();
  ctx.restore();
}

/* ---- 弹簧形变量 Δx 标注（形变太小就不标，避免贴字；够大时中间留缺口放标签） ---- */
function dimDx(x1, x2, d){
  if (d < 0.46) return;          /* 形变太小时只画两根短竖线毫无意义，整体不画 */
  const y0 = 0.34;
  FIG.wire([[x1, y0 - 0.05], [x1, y0 + 0.05]], {lw: 1.4, color: '#3b82f6'});
  FIG.wire([[x2, y0 - 0.05], [x2, y0 + 0.05]], {lw: 1.4, color: '#3b82f6'});
  const gapw = 0.34, mx = (x1 + x2) / 2;
  FIG.wire([[x1, y0], [mx - gapw / 2, y0]], {lw: 1.0, color: '#93c5fd'});
  FIG.wire([[mx + gapw / 2, y0], [x2, y0]], {lw: 1.0, color: '#93c5fd'});
  lab(mx - 0.08, y0 - 0.04, 'Δx', {size: 12, color: '#1d4ed8', align: 'center', italic: false});
}

/* ---- 碰撞闪光：扩散圆环（按进度平方淡出，结束后彻底消失） ---- */
function flashRing(x, y, u, color, rf){
  if (u < 0 || u > 1) return;
  const p = W2S(x, y), r = (0.22 + 0.58 * u) * (rf || 1) * scale;
  ctx.save();
  ctx.globalAlpha = (1 - u) * (1 - u);
  ctx.strokeStyle = color || '#dc2626'; ctx.lineWidth = 2.4 * (1 - u) + 0.8;
  ctx.beginPath(); ctx.arc(p[0], p[1], r, 0, 7); ctx.stroke();
  ctx.restore();
}

/* ---- 左下角图例（像素空间：只画在画布下沿的留白带里） ---- */
function drawLegendPx(){
  const rr = ctx.canvas.getBoundingClientRect();
  const Wp = (rr && rr.width) ? rr.width : W;
  const Hp = (rr && rr.height) ? rr.height : H;
  const k = Math.max(0.82, Math.min(1.12, Wp / 420));
  const fs = 10.6 * k;
  ctx.save();
  ctx.font = fs.toFixed(1) + 'px sans-serif';
  ctx.textAlign = 'left';
  let x = 8 * k, y = Hp - 23 * k;
  const chip = function(color, text){
    const tw = ctx.measureText(text).width;
    if (x + tw + 26 * k > Wp - 6) return;
    ctx.fillStyle = color;
    ctx.beginPath(); ctx.arc(x + 4.2 * k, y - 3.4 * k, 3.5 * k, 0, 7); ctx.fill();
    ctx.fillStyle = '#334155';
    ctx.fillText(text, x + 11 * k, y);
    x += 11 * k + tw + 14 * k;
  };
  chip('#f59e0b', 'A：m');
  chip('#fbbf24', 'A₁、A₂：3m/5');
  chip('#0891b2', 'B：M');
  y = Hp - 8 * k; x = 8 * k;
  ctx.fillStyle = '#64748b';
  ctx.fillText('俯视图：光滑水平面内，A₁、A₂ 只能沿固定细杆运动', x, y);
  ctx.restore();
}
"""

# ============================================================
# 八、逐帧绘制
# ============================================================
DRAWFRAME_JS = r"""
const st = stateAt(t);
clearBg();

/* ---------- 顶部过程横幅（只画在动画画布上） ---------- */
if (ctx.canvas.id === 'cv'){
  for (let i = 0; i < BANNERS.length; i++){
    if (t < BANNERS[i][1]){
      const txt = BANNERS[i][2];
      const rc = ctx.canvas.getBoundingClientRect();
      const cap = ((rc && rc.width) ? rc.width : W) * 0.94;
      let fs = 15;
      ctx.font = 'bold ' + fs + 'px sans-serif';
      const need = ctx.measureText(txt).width + 26;
      if (need > cap) fs = Math.max(9, Math.floor(fs * cap / need));
      FIG.processBanner(txt, {size: fs});
      break;
    }
  }
}

/* ---------- 两根平行的固定细杆 ---------- */
const RX0 = VIEW.xmin + 0.12, RX1 = VIEW.xmax - 0.12;
[PAR.L, -PAR.L].forEach(function(yy){
  FIG.wire([[RX0, yy], [RX1, yy]], {lw: 3.2, color: '#475569'});
  FIG.wire([[RX0, yy - 0.06], [RX0, yy + 0.06]], {lw: 2.4, color: '#475569'});
  FIG.wire([[RX1, yy - 0.06], [RX1, yy + 0.06]], {lw: 2.4, color: '#475569'});
});

/* ---------- A、A₁、A₂ 的初始位置参考线（碰后才显示） ---------- */
if (st.to > 0.03){
  dashLine(0, -PAR.L + 0.12, 0, PAR.L - 0.12, '#cbd5e1', 1.0, [5, 5]);
}

/* ---------- 两根弹簧：拉得越长越红（弹性势能的直观提示） ---------- */
const kk = Math.max(0, Math.min(1, st.d / PAR.DMAX));
const sc = 'rgb(' + Math.round(124 + 96 * kk) + ',' +
           Math.round(45 + (1 - kk) * 20) + ',' + Math.round(18 * (1 - kk)) + ')';
springSeg(st.ax, 0, st.a1x, PAR.L, {color: sc, lw: 1.9});
springSeg(st.ax, 0, st.a1x, -PAR.L, {color: sc, lw: 1.9});

/* ---------- 弹簧形变量 Δx ---------- */
dimDx(st.a1x, st.ax, st.d);

/* ---------- 三个橙球（A₁、A₂ 套在细杆上）与 B ---------- */
ball(st.a1x, PAR.L, PAR.RS, '#fbbf24', '#b45309');
ball(st.a1x, -PAR.L, PAR.RS, '#fbbf24', '#b45309');
ball(st.ax, 0, PAR.RA, '#f59e0b', '#b45309');
ball(st.bx, 0, PAR.RB, '#0891b2', '#155e75');

/* ---------- 碰撞闪光（画在球之上、箭头与文字之下，避免盖住字母） ---------- */
if (st.ph === 2){
  const u = (t - T_HIT1) / Math.max(1e-6, T_HIT2 - T_HIT1);
  flashRing(-PAR.RA, 0, Math.min(1, u * 1.05), '#dc2626', 1.0);
  flashRing(-PAR.RA, 0, Math.min(1, u * 1.05), '#f59e0b', 0.66);
}
if (st.ph === 6){
  const u = Math.min(1, (t - T_NAT) / 0.62);
  flashRing(st.ax - PAR.RA, 0, Math.min(1, u * 1.05), '#dc2626', 1.0);
  flashRing(st.ax - PAR.RA, 0, Math.min(1, u * 1.05), '#f59e0b', 0.66);
}

/* ---------- 速度矢量（从球面起画；长度 ∝ 速率，阈值防"零矢量箭头"） ---------- */
const VS = 0.28;
if (st.bx + PAR.RB + st.bv * VS < st.ax - PAR.RA - 0.04){   /* 箭头不能戳进 A 的球里 */
  FIG.vec(st.bx + PAR.RB, 0, st.bv * VS, 0, '', {color: '#0369a1', lw: 2.6, head: 9});
  lab(st.bx, st.pre ? 0.31 : -0.34, st.pre ? 'v₀' : 'u',
      {size: 14, color: '#0369a1', align: 'center'});
}
if (Math.abs(st.av) * VS > 0.09){
  const sg = st.av > 0 ? 1 : -1, x0 = st.ax + sg * PAR.RA;
  FIG.vec(x0, 0, st.av * VS, 0, '', {color: '#dc2626', lw: 3.0, head: 10});
  lab(x0 + st.av * VS + sg * 0.06, 0.26, 'v₁',
      {size: 14, color: '#dc2626', align: sg > 0 ? 'left' : 'right'});
}
if (Math.abs(st.a1v) * VS > 0.09){
  const sg1 = st.a1v > 0 ? 1 : -1, x1 = st.a1x + sg1 * PAR.RS;
  FIG.vec(x1, PAR.L, st.a1v * VS, 0, '', {color: '#7c3aed', lw: 2.6, head: 9});
  FIG.vec(x1, -PAR.L, st.a1v * VS, 0, '', {color: '#7c3aed', lw: 2.6, head: 9});
}

/* ---------- 字母标注 ---------- */
lab(st.a1x - 0.20, PAR.L + 0.06, 'A₁', {size: 14, align: 'right', color: '#92400e'});
lab(st.a1x - 0.20, -PAR.L + 0.06, 'A₂', {size: 14, align: 'right', color: '#92400e'});
lab(st.ax + 0.16, 0.28, 'A', {size: 15, color: '#92400e'});
lab(st.bx - 0.20, 0.06, 'B', {size: 15, align: 'right', color: '#0e7490'});

/* ---------- 共速定格：形变量最大 ⇒ 弹性势能最大 ---------- */
if (st.ph === 4){
  const txt = 'Eₚ 最大';
  ctx.font = 'bold 12.5px sans-serif';
  const tw = ctx.measureText(txt).width;
  lab(-0.30, 0.62, txt, {size: 12.5, color: '#b45309', italic: false});
  /* 细虚线引出，指向被拉长的弹簧中点，避免标签"悬空" */
  dashLine(-0.30 + tw / scale + 0.05, 0.58, 0.70, 0.58, '#d9a441', 1.0, [3, 3]);
}

/* ---------- 恢复原长定格：点明"速度反向"这一关键 ---------- */
if (st.ph === 6 && t > T_NAT + 0.30){
  lab(-1.10, 0.90, 'A 已被弹簧拉回，速度反向', {size: 11, color: '#334155', italic: false});
  lab(-1.10, 0.68, 'B 仍向前，恰好追上 A', {size: 11, color: '#0e7490', italic: false});
}

/* ---------- 左下角图例 ---------- */
drawLegendPx();
"""

READOUTS_JS = r"""
const st = stateAt(t);
const P = PAR;
const rows = [];
rows.push(['当前阶段', PHASE_NAMES[st.ph], '']);
rows.push(['$v_A$', (st.av / P.V0).toFixed(2), 'v₀']);
rows.push(['$v_{A_1}=v_{A_2}$', (st.a1v / P.V0).toFixed(2), 'v₀']);
rows.push(['$u$（B 的速率）', (st.bv / P.V0).toFixed(2), 'v₀']);
rows.push(['弹簧形变量 $\\Delta x/d_{\\max}$', (st.d / P.DMAX).toFixed(2), '']);
rows.push(['每根弹簧 $E_p$', st.ep.toFixed(3), 'mv₀²']);
rows.push(['$E_k+E_p$（守恒）', (0.5 * P.V1 * P.V1).toFixed(3), 'mv₀²']);
rows.push(['演示值 $m/M$', '1/11', '第(3)问答案']);
return rows;
"""

# ============================================================
# 九、注入
# ============================================================
tpl = open(TPL, encoding='utf-8').read()


def _js(s):
    return json.dumps(s, ensure_ascii=False)


prob_js = (
    "const PROBLEM = {\n"
    "  title: %s,\n"
    "  given: %s,\n"
    "  images: [{ src: \"__CANVAS_STATIC__\", caption: \"\" }],\n"
    "  asks: [\n%s\n  ],\n"
    "  options: [],\n"
    "  knowledgePoints: [%s]\n"
    "};\n"
) % (_js(PROBLEM_TITLE), _js(PROBLEM_GIVEN),
     '\n'.join('    %s,' % _js(a) for a in PROBLEM_ASKS),
     ', '.join('{ id: "%s" }' % k for k in KNOWLEDGE_IDS))

steps_js = "const STEPS = [\n"
for _s in STEPS:
    steps_js += ("  { q: %d, title: %s, tex: %s, note: %s, basis: %s, t0: %.3f, t1: %.3f },\n"
                 % (_s['q'], _js(_s['title']), _js(_s['tex']), _js(_s['note']),
                    _js(_s['basis']), _s['t0'], _s['t1']))
steps_js += "];\n"

view_js = ("const VIEW = { xmin: %s, xmax: %s, ymin: %s, ymax: %s };\n"
           "const SIM  = { duration: %s };\n"
           % (VIEW['xmin'], VIEW['xmax'], VIEW['ymin'], VIEW['ymax'], round(T_END, 3)))

banners_js = '[' + ','.join('[%.3f,%.3f,%s]' % (a, b, _js(c)) for a, b, c in TIMELINE) + ']'

g = GLOBALS_JS
for _k, _v in [('V1', V1), ('UB', UB), ('VCOM', VCOM), ('OMG', OMEGA), ('THALF', THALF),
               ('K', KSPR), ('EPMAX', EPMAX), ('L', L_ROD), ('XB0', B_X0), ('CX', CONTACT),
               ('NTOT', float(len(TIMELINE))), ('HOLD0', T_HOLD0), ('HIT1', T_HIT1),
               ('HIT2', T_HIT2), ('TMAX', T_MAX), ('TMAXH', T_MAXH), ('TNAT', T_NAT),
               ('TEND', T_END), ('TZVAL', T_IMP), ('BANNERS', banners_js)]:
    g = g.replace('/*@%s@*/' % _k, repr(_v) if not isinstance(_v, str) else _v)

out = tpl
out = re.sub(r'const PROBLEM = \{[\s\S]*?\n\};', lambda m: prob_js.rstrip('\n'), out, count=1)
out = re.sub(r'const STEPS = \[[\s\S]*?\n\];', lambda m: steps_js.rstrip('\n'), out, count=1)
out = re.sub(r'const VIEW = \{[^\n]*\n\s*const SIM\s*=\s*\{[^\n]*\n',
             lambda m: view_js, out, count=1)


def _repl(text, marker, payload):
    pat = re.compile(r'/\*\s*' + marker + r'\s*\*/')
    assert len(pat.findall(text)) == 1, "注入点不唯一: " + marker
    return pat.sub(lambda m: payload, text, count=1)


out = _repl(out, '__GLOBALS__', g.strip() + '\n\n' + HELPERS_JS.strip())
out = _repl(out, '__SETUP__', '/* 本题无需额外 setup：几何与时间轴全部由 stateAt(t) 推出 */')
out = _repl(out, '__DRAWFRAME__', DRAWFRAME_JS.strip())
out = _repl(out, '__READOUTS__', READOUTS_JS.strip())

CSS_TUNE = (
    '<style id="tune-width">\n'
    '.col-problem{flex:0.92 1 250px}\n'
    '.col-analysis{flex:2.0 1 390px}\n'
    '.col-animation{flex:1.45 1 450px}\n'
    '.step{padding:8px 9px 8px 11px}\n'
    '.step .tex{padding:2px 0 6px}\n'
    '.step .tex mjx-container[display="true"]{max-width:100%}\n'
    '.step .tex mjx-container[display="true"] svg{max-width:100%;height:auto}\n'
    '.step .note{line-height:1.62}\n'
    '.fig-canvas{max-width:100%;max-height:none}\n'
    '</style>\n'
)
assert out.count('</head>') == 1
out = out.replace('</head>', CSS_TUNE + '</head>', 1)

open(OUT, 'w', encoding='utf-8', newline='\n').write(out)

# ============================================================
# 十、探针自检
# ============================================================
probes = [PROBLEM_TITLE, '__CANVAS_STATIC__', 'mech-momentum-collision-1d',
          'processBanner', 'function stateAt', 'function springSeg', 'function dimDx',
          'function drawLegendPx', 'const BANNERS', 'PHASE_NAMES',
          r'\\frac{2M}{M+m}v_0', r'\\frac{m}{M}=\\frac{1}{11}',
          '__GLOBALS__', '__SETUP__', '__DRAWFRAME__', '__READOUTS__', '/*@']
print('=== 探针自检 ===')
for _p in probes:
    if _p.startswith('__') and _p != '__CANVAS_STATIC__':
        print(('PASS   已注入 ' if _p not in out else 'FAIL   标记未被替换 ') + _p)
    elif _p == '/*@':
        print(('FAIL   残留占位符 ' if '/*@' in out else 'PASS   无残留 /*@ 占位符'))
    else:
        print(('FOUND   ' if _p in out else 'MISSING ') + _p)

# 反斜杠层数硬门禁
_bad = []
for _m in re.finditer(r'tex: "((?:[^"\\]|\\.)*)"', out):
    _t = _m.group(1)
    _i = 0
    while _i < len(_t):
        if _t[_i] == '\\':
            if _i + 1 < len(_t) and _t[_i + 1] == '\\':
                _i += 2
                continue
            if _i + 1 < len(_t) and _t[_i + 1].isalpha():
                _bad.append(_t[max(0, _i - 12):_i + 18])
                break
            _i += 1
            continue
        _i += 1
print('=== 反斜杠层数自检 ===')
if _bad:
    for _b in _bad:
        print('BAD  单反斜杠: %s' % _b)
    raise SystemExit('反斜杠被吞：re.sub 替换串未用 lambda 包一层')
print('PASS  全部 tex 反斜杠已正确转义（%d 条）' % len(re.findall(r'tex: "', out)))

# 未声明标识符门禁
INJECTED = g + '\n' + HELPERS_JS + '\n' + DRAWFRAME_JS + '\n' + READOUTS_JS


def _strip_js(src):
    src = re.sub(r'/\*[\s\S]*?\*/', ' ', src)
    src = re.sub(r'//[^\n]*', ' ', src)
    src = re.sub(r'"(?:[^"\\]|\\.)*"', '""', src)
    src = re.sub(r"'(?:[^'\\]|\\.)*'", "''", src)
    src = re.sub(r'`(?:[^`\\]|\\.)*`', '``', src)
    return src


_clean = _strip_js(INJECTED)


def _split_top_commas(stmt):
    parts, depth, cur = [], 0, ''
    for ch in stmt:
        if ch in '([{':
            depth += 1
        elif ch in ')]}':
            depth -= 1
        if ch == ',' and depth == 0:
            parts.append(cur)
            cur = ''
        else:
            cur += ch
    if cur.strip():
        parts.append(cur)
    return parts


_declared = set()
for _m in re.finditer(r'\b(?:const|let|var)\s+', _clean):
    _i, _stmt, _depth = _m.end(), '', 0
    while _i < len(_clean):
        _ch = _clean[_i]
        if _ch in '([{':
            _depth += 1
        elif _ch in ')]}':
            _depth -= 1
        if _ch == ';' and _depth <= 0:
            break
        _stmt += _ch
        _i += 1
    for _seg in _split_top_commas(_stmt):
        _name = _seg.split('=')[0] if '=' in _seg else _seg
        for _n in re.findall(r'[A-Za-z_$][A-Za-z0-9_$]*', _name):
            _declared.add(_n)
    for _o in re.finditer(r'\{([^{}]*)\}', _stmt):
        for _k2 in re.findall(r'([A-Za-z_$][A-Za-z0-9_$]*)\s*:', _o.group(1)):
            _declared.add(_k2)
for _m in re.finditer(r'\bfunction\s+([A-Za-z_$][A-Za-z0-9_$]*)', _clean):
    _declared.add(_m.group(1))
_declared |= {'W', 'H', 'PAD', 'scale', 'ctx', 't', 'VIEW', 'SIM', 'PROBLEM', 'STEPS',
              'FIG', 'W2S', 'Math', 'JSON', 'Object', 'Array', 'String', 'Number',
              'Boolean', 'Date', 'console', 'window', 'document', 'parseFloat',
              'parseInt', 'isNaN', 'Infinity', 'NaN', 'undefined', 'null', 'true', 'false'}
_used = set(re.findall(r'(?<![.\w$])[A-Z][A-Z0-9_]{1,}\b', _clean))
_miss = sorted(_used - _declared)
print('=== 未声明标识符门禁 ===')
if _miss:
    print('MISSING 未声明的大写常量: %s' % ', '.join(_miss))
    raise SystemExit('存在未声明标识符（会造成整页 JS 中断 ⇒ 动画卡死 + 题图空白）')
print('PASS  全部大写常量均已声明（%d 个）' % len(_used))

# 知识点 id 门禁
_kp_seg = tpl[tpl.find('const KNOWLEDGE_INDEX'):]
_kp_all = set(re.findall(r"id:'([^']+)'", _kp_seg))
_bad_kp = [k for k in KNOWLEDGE_IDS if k not in _kp_all]
print('=== 知识点 id 门禁 ===')
if _bad_kp:
    print('FAIL  模板索引中不存在: %s' % _bad_kp)
    raise SystemExit('知识点 id 不存在，左栏卡片会显示原始 id')
print('PASS  全部 %d 个知识点 id 均存在于模板索引' % len(KNOWLEDGE_IDS))

# 物理量自检
print('=== 物理量自检 ===')
_checks = [
    ('v₁ = 2M/(M+m)v₀ = 11/6', V1, 11 / 6),
    ('u_B = (M−m)/(M+m)v₀ = 5/6', UB, 5 / 6),
    ('V = 5v₁/11 恰等于 u_B', VCOM, UB),
    ('Ep,max = 6mM²v₀²/(11(M+m)²)', EPMAX, 6 * 1 * 121 / (11 * 144)),
    ('k = 3mω²/11 = 11/12', KSPR, 11 / 12),
    ('ω = v₁ ⇒ d_max = 1', V1 / OMEGA, 1.0),
    ('A 总位移 = 5π/11', xA(THALF), 5 * PI / 11),
    ('恢复原长时 A 与 B 同位置', xA(THALF), UB * THALF),
    ('v_A(T/2) = −v₁/11', vA(THALF), -V1 / 11),
    ('v_A₁(T/2) = 10v₁/11', vS(THALF), 10 * V1 / 11),
    ('能量守恒（碰后 = 共速 + 2Ep）', 0.5 * MASS_A * V1 ** 2,
     0.5 * 11 * MASS_A / 5 * VCOM ** 2 + 2 * EPMAX),
]
_ok = True
for _n, _a, _b in _checks:
    _good = abs(_a - _b) <= 1e-9 * max(1.0, abs(_b))
    _ok = _ok and _good
    print('%s %-32s 计算=%.8g 期望=%.8g' % ('PASS ' if _good else 'FAIL ', _n, _a, _b))
if not _ok:
    raise SystemExit('物理量自检未通过')
print('时间轴：碰点 %.2f s，碰后 %.2f s 共速，%.2f s 恢复原长，总时长 %.2f s'
      % (T_HIT1, T_MAX, T_NAT, T_END))
print('output: %s  (%d bytes)' % (OUT, os.path.getsize(OUT)))
