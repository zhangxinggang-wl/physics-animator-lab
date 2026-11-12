# -*- coding: utf-8 -*-
"""生成《2026·河北·18 速度选择器+三区域复合场》教学动画单文件 HTML。

【题图几何反编译】（原图右侧装置图，世界坐标 x 向右、y 向上）
  粒子发生器 / 速度选择器：第二象限内两个竖直长方块，位于 y=-x 边界线左上方
  区域Ⅰ：第二象限内 y ≥ -x 的三角形（含边界），磁场 ⊙ 向外，B1
  区域Ⅱ：x 轴下方，磁场 ⊗ 向里，5B
  区域Ⅲ：第一象限，磁场 ⊗ 向里，12B
  关键点：(-h,h)、O、2R2=2mv/5qB、P=(19mv/30qB,0)、相遇点 x1=34mv/15qB

【物理量纲约定】画布世界单位取 k = mv/(qB)，故 R2=1/5、R3=1/12、x1=34/15。

【答案】
  (1) B0 = E/v（磁场垂直纸面向里）；B1 = mv/(qh)
  (2) t  = 29πm/(60qB)
  (3) M = 17m/10，x1 = 34mv/(15qB)（a 第 9 次上穿 x 轴、b 第 5 次上穿 x 轴）
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = os.path.join(ROOT, 'assets', 'template.html')
OUT = os.path.join(ROOT, '2026-10-12_速度选择器三区域复合场_教学动画.html')

# ============================================================
# 一、物理参数（以 k = mv/(qB) 为长度单位，世界坐标即「以 k 为单位」）
# ============================================================
import math

H_SHOW = 0.40           # 题目参数 h 的示意取值（世界单位）；物理上 B1 = mv/(qh)
R2 = 1.0 / 5.0         # 区域Ⅱ半径 R2 = mv/(5qB)
R3 = 1.0 / 12.0        # 区域Ⅲ半径 R3 = mv/(12qB)
DX = 2 * R2 - 2 * R3   # 每个「区域Ⅱ半圆+区域Ⅲ半圆」周期的横移 = 7/30
X_P = 4 * R2 - 2 * R3  # = 19/30  ← 与题给 P 点坐标 mv*19/(30qB) 完全一致
N_MEET_A = 9           # a 第 9 次上穿 x 轴
N_MEET_B = 5           # b 第 5 次上穿 x 轴
M_RATIO = 17.0 / 10.0  # M/m
X_MEET = 34.0 / 15.0   # 相遇点 x1 = 34mv/(15qB)

assert abs(X_P - 19.0 / 30.0) < 1e-12
assert abs(M_RATIO * (7 * N_MEET_B + 5) / 30.0 - X_MEET) < 1e-12

# ============================================================
# 二、题面（逐字录入）
# ============================================================
PROBLEM_TITLE = '2026·河北·18（16分）'
PROBLEM_GIVEN = (
    '如图所示，在 \\(Oxy\\) 坐标系中，第二象限有一粒子发生器，其右侧放置速度选择器，'
    '速度选择器中电场的电场强度大小为 \\(E\\)，方向沿 \\(y\\) 轴负方向，'
    '匀强磁场方向垂直 \\(Oxy\\) 面向里；'
    '\\(y=-x\\,(x\\leqslant 0)\\) 与 \\(y\\) 轴正半轴所围区域Ⅰ（含边界）中充满'
    '垂直 \\(Oxy\\) 面 向外的匀强磁场；'
    '\\(x\\) 轴下方为区域Ⅱ、第一象限为区域Ⅲ，两区域均充满方向垂直 \\(Oxy\\) 面向里的匀强磁场，'
    '磁感应强度大小分别为 \\(5B\\) 和 \\(12B\\)。'
    '粒子发生器可发出质量不同、带电荷量均为 \\(+q\\) 的粒子。'
    '其中质量为 \\(m\\) 的粒子 \\(a\\) 经速度选择器后以速率 \\(v\\) '
    '从点 \\((-h,h)\\) 沿 \\(x\\) 轴正方向进入区域Ⅰ，一段时间后恰好从原点 \\(O\\) '
    '沿 \\(y\\) 轴负方向进入区域Ⅱ。不计粒子重力及粒子间相互作用。'
)
PROBLEM_ASKS = [
    '求速度选择器中磁感应强度大小 \\(B_0\\) 和区域Ⅰ中磁感应强度的大小 \\(B_1\\)；',
    '求粒子 \\(a\\) 从 \\(O\\) 点运动到 \\(P\\left(\\dfrac{19mv}{30qB},0\\right)\\) 的时间 \\(t\\)；',
    '当粒子 \\(a\\) 从点 \\(\\left(\\dfrac{2mv}{5qB},0\\right)\\) 离开区域Ⅱ进入区域Ⅲ时，'
    '带电荷量为 \\(+q\\) 的粒子 \\(b\\) 恰好从 \\(O\\) 点以速率 \\(v\\) 沿 \\(y\\) 轴负方向进入区域Ⅱ，'
    '若要使粒子 \\(a、b\\) 在 \\(x\\) 轴相遇，且相遇时速度恰好都沿 \\(y\\) 轴正方向，'
    '求粒子 \\(b\\) 的质量 \\(M\\)（用 \\(m\\) 表示）及两粒子第一次相遇时的 \\(x\\) 轴坐标 \\(x_1\\)。',
]
KNOWLEDGE_IDS = [
    'em-lorentz-force',
    'em-cyclotron',
    'em-electric-field',
    'em-ampere-force',
]

# ============================================================
# 三、STEPS（分步解析；t0/t1 与动画时间轴对齐）
# ============================================================
STEPS = [
    # ================= 第一问 =================
    dict(q=1, title='速度选择器：直线通过 ⇒ 电场力与磁场力平衡',
         tex=r'qE=qvB_0',
         note='粒子 \\(a\\) 带正电、自左向右沿 \\(x\\) 轴正方向穿过速度选择器。'
              '电场沿 \\(y\\) 轴负方向，故电场力 \\(F_E=qE\\) 竖直向下；'
              '要使粒子做匀速直线运动，磁场力必须竖直向上与之平衡。'
              '由左手定则，粒子速度沿 \\(+x\\)、磁场垂直纸面向里时，'
              '洛伦兹力 \\(F_B=qvB_0\\) 恰沿 \\(+y\\)（与题设「磁场向里」自洽）。'
              '平衡条件给出 \\(B_0=E/v\\)。',
         basis='匀速直线运动条件（合力为零）+ 洛伦兹力公式'),
    dict(q=1, title='区域Ⅰ：确定轨道圆心与半径',
         tex=r'R_1=h',
         note='粒子 \\(a\\) 从 \\((-h,h)\\) 沿 \\(x\\) 轴正方向进入区域Ⅰ（该点在边界 \\(y=-x\\) 上）。'
              '区域Ⅰ磁场垂直纸面**向外**，由左手定则洛伦兹力沿 \\(-y\\) 方向，'
              '故圆心必在出发点正下方，即 \\((-h,\\,h-R_1)\\)。'
              '又粒子恰好从原点 \\(O\\) 沿 \\(y\\) 轴负方向离开，'
              '说明 \\(O\\) 处速度沿 \\(y\\) 轴 ⟹ \\(O\\) 与圆心的连线沿 \\(x\\) 轴 ⟹ 圆心 \\(y\\) 坐标为 0。'
              '于是 \\(h-R_1=0\\)，得 \\(R_1=h\\)：轨迹是以 \\((-h,0)\\) 为圆心、'
              '从 \\((-h,h)\\) 到 \\(O\\) 的四分之一圆弧。',
         basis='洛伦兹力提供向心力 + 圆周运动几何'),
    dict(q=1, title='区域Ⅰ磁感应强度',
         tex=r'qvB_1=\tfrac{mv^{2}}{R_1}\ \Rightarrow\ B_1=\tfrac{mv}{qh}',
         note='由 \\(qvB_1=m\\dfrac{v^2}{R_1}\\) 与 \\(R_1=h\\) 得 '
              '\\(B_1=\\dfrac{mv}{qh}\\)。'
              '注意 \\(B_1\\) 与 \\(h\\) 成反比：轨道半径越大（圆心越靠下），'
              '在速率不变时所需的磁场越弱。',
         basis='洛伦兹力提供向心力'),
    # ================= 第二问 =================
    dict(q=2, title='区域Ⅱ（5B，⊗）：从 O 出发做半圆',
         tex=r'R_2=\tfrac{mv}{5qB},\qquad x=2R_2=\tfrac{2mv}{5qB}',
         note='粒子在 \\(O\\) 点以速率 \\(v\\) 沿 \\(y\\) 轴负方向进入区域Ⅱ。'
              '区域Ⅱ磁场垂直纸面向里，洛伦兹力沿 \\(+x\\) 方向，'
              '故圆心在 \\(O\\) 的正右方 \\((R_2,0)\\)，'
              '轨迹为以 \\((R_2,0)\\) 为圆心的**下半圆**，'
              '在 \\(x=2R_2=\\dfrac{2mv}{5qB}\\) 处回到 \\(x\\) 轴且速度沿 \\(+y\\)。'
              '半径 \\(R_2=\\dfrac{mv}{5qB}\\)。',
         basis='洛伦兹力提供向心力 + 圆周运动几何'),
    dict(q=2, title='区域Ⅲ（12B，⊗）：半圆向左，横移 2R₃',
         tex=r'R_3=\tfrac{mv}{12qB},\qquad 2R_2-2R_3=\tfrac{7mv}{30qB}',
         note='粒子在 \\(x=2R_2\\) 处以速度 \\(+y\\) 进入第一象限的区域Ⅲ。'
              '区域Ⅲ磁场垂直纸面向里，洛伦兹力沿 \\(-x\\) 方向，'
              '圆心在 \\((2R_2-R_3,\\,0)\\)，轨迹为上半圆，'
              '在 \\(x=2R_2-2R_3\\) 处回到 \\(x\\) 轴且速度沿 \\(-y\\)。'
              '半径 \\(R_3=\\dfrac{mv}{12qB}\\)。'
              '由此可见粒子每经历「区域Ⅱ半圆 + 区域Ⅲ半圆」一个周期，'
              '沿 \\(x\\) 轴正向平移 \\(2R_2-2R_3=\\dfrac{7mv}{30qB}\\)。',
         basis='洛伦兹力提供向心力 + 圆周运动几何'),
    dict(q=2, title='到达 P 点：路径与时间累计',
         tex=r't=\Big(\tfrac{1}{5}+\tfrac{1}{12}+\tfrac{1}{5}\Big)\tfrac{\pi m}{qB}'
             r'=\tfrac{29\pi m}{60qB}',
         note='从 \\(O\\) 到 \\(P\\) 的路径为：区域Ⅱ下半圆 → 区域Ⅲ上半圆 → 区域Ⅱ下半圆。'
              '对应的横坐标为 \\(2R_2 \\rightarrow 2R_2-2R_3 \\rightarrow 4R_2-2R_3\\)，'
              '而 \\(4R_2-2R_3=\\dfrac{19mv}{30qB}\\)，与题给 \\(P\\) 点坐标吻合，'
              '说明 \\(P\\) 正是粒子第二次上穿 \\(x\\) 轴（速度沿 \\(+y\\)）的位置。'
              '半圆周运动用时 \\(t=\\pi R/v\\)，逐段相加：'
              '\\(\\dfrac{\\pi m}{5qB}+\\dfrac{\\pi m}{12qB}+\\dfrac{\\pi m}{5qB}'
              '=\\dfrac{29\\pi m}{60qB}\\)。',
         basis='半圆运动周期 + 分段累加'),
    # ================= 第三问 =================
    dict(q=3, title='相遇的表述：位置条件与时间条件',
         tex=r'm(7n+5)=M(7j+5)',
         note='设粒子 \\(a\\) 第 \\(n\\) 次上穿 \\(x\\) 轴、粒子 \\(b\\) 第 \\(j\\) 次上穿 \\(x\\) 轴处相遇。'
              '**位置条件**：\\(a\\) 第 \\(n\\) 次上穿的位置为 '
              '\\(x_n=\\dfrac{(7n+5)mv}{30qB}\\)，'
              '而 \\(b\\) 的半径整体按 \\(M/m\\) 放大，'
              '故 \\(x_j=\\dfrac{(7j+5)Mv}{30qB}\\)，两者相等即下式。'
              '**时间条件**：\\(b\\) 是在 \\(a\\) 第一次上穿 \\(x\\) 轴（即 \\(u_a=12\\)）时才发射的，'
              '晚 \\(\\dfrac{\\pi m}{5qB}=\\dfrac{12\\pi m}{60qB}\\)。'
              '而 \\(a\\) 第 \\(n\\) 次上穿的时刻为 '
              '\\(\\dfrac{(17n-5)\\pi m}{60qB}\\)，故时间条件为 '
              '\\(m(17n-5)=12m+M(17j-5)\\)。'
              '两式联立即得相遇的全部约束。',
         basis='圆周运动几何 + 速度-时间关系'),
    dict(q=3, title='联立求解：最小正整数解与质量比',
         tex=r'10n=17j+5\ \Rightarrow\ (n,j)=(9,5),\qquad M=\tfrac{17}{10}m',
         note='两式相除消去 \\(m、M\\)：\\(\\dfrac{17n-5}{7n+5}=\\dfrac{17j-5}{7j+5}\\)，'
              '展开即得 \\(120n=120j\\) 无信息，故改用联立代入，'
              '最终化为 \\(10n=17j+5\\)。'
              '要 \\(n、j\\) 均为正整数且取**最小**（第一次相遇），'
              '需 \\(17j+5\\equiv 0\\ (\\mathrm{mod}\\ 10)\\)，'
              '即 \\(j\\equiv 5\\ (\\mathrm{mod}\\ 10)\\)，最小取 \\(j=5\\)，得 \\(n=9\\)。'
              '代回位置条件：\\(M=\\dfrac{(7\\cdot 9+5)m}{7\\cdot 5+5}'
              '=\\dfrac{68m}{40}=\\dfrac{17m}{10}\\)。',
         basis='联立方程 + 整数性（取最小正整数解）'),
    dict(q=3, title='第一次相遇点坐标与相遇次数',
         tex=r'x_1=\dfrac{(7\\cdot 9+5)mv}{30qB}=\dfrac{34mv}{15qB}',
         note='相遇点即 \\(a\\) 第 9 次上穿 \\(x\\) 轴处：'
              '\\(x_1=\\dfrac{68mv}{30qB}=\\dfrac{34mv}{15qB}\\)。'
              '相遇时刻 \\(T=\\dfrac{148\\pi m}{60qB}\\)：'
              '此时 \\(a\\) 已走完 9 段半圆，\\(b\\) 走完 5 段半圆，'
              '二者速度都沿 \\(+y\\) 方向，恰好满足题目要求。'
              '**易错提醒**：\\(b\\) 质量大于 \\(m\\)，轨道半径整体放大，'
              '所以 \\(b\\) 的圆弧「更扁更长」，追上 \\(a\\) 需要更多次穿越；'
              '若误认为「轻的追重的」而取 \\(j>n\\) 的解，会得到 \\(M=\\dfrac{17m}{10}\\) 以外的错误结果。',
         basis='圆周运动几何'),
]

# ============================================================
# 四、VIEW / 时间轴
# ============================================================
VIEW = dict(xmin=-0.82, xmax=2.40, ymin=-0.75, ymax=1.18)
SIM_DURATION = 14.0

T_SEL = (0.00, 2.20)    # 阶段1：速度选择器
T_REG1 = (2.20, 4.40)   # 阶段2：区域Ⅰ 四分之一圆
T_AB = (4.40, 8.00)     # 阶段3：区域Ⅱ→Ⅲ→Ⅱ，到 P（相位 u: 0 → 34）
T_MEET = (8.00, 14.00)  # 阶段4：第(3)问，相遇（u_a: 12 → 148）

TIMELINE = [
    (0.00, 2.20, '阶段①  速度选择器：直线通过，B₀ = E/v'),
    (2.20, 4.40, '阶段②  区域Ⅰ 内四分之一圆弧，R₁ = h'),
    (4.40, 8.00, '阶段③  区域Ⅱ→Ⅲ→Ⅱ，到 P 点'),
    (8.00, 14.00, '阶段④  粒子 b 发射，首次在 x₁ 处相遇'),
]

# 阶段3/4 的相位换算（u 为归一化相位，详见 GLOBALS 中的定义）
U_AT_P = 34.0                 # u=34 时 a 第二次上穿 x 轴（= P 点）
U_MEET_A = 17 * N_MEET_A - 5  # = 148
U_MEET_B = 17 * N_MEET_B - 5  # = 80（b 自身相位）；实际 u_b = 1.7*80 = 136
U_LAUNCH = 12.0               # a 第一次上穿 = b 发射时刻（u_a = 12）


# ============================================================
# 五、动画实现（JS）
# ============================================================
GLOBALS_JS = r"""
/* =========================================================================
   本题全局：物理参数、相位约定、轨迹几何
   ---------------------------------------------------------------------------
   【相位 u 的定义】以 k = mv/(qB) 为长度单位，半圆弧长 πR2 = π/5 记作 12 个相位单位，
   半圆弧长 πR3 = π/12 记作 5 个相位单位。于是：
     · 区域Ⅱ内半圆  占相位 12，区域Ⅲ内半圆 占相位 5，一个周期占 17；
     · 粒子 a 第 n 次上穿 x 轴（速度 +y）对应 u = 17n - 5；
     · 粒子 b 的半径整体乘 λ = M/m = 1.7，故其自身相位 u_b' = u_b / λ。
   粒子速率为 v，相位随时间线性增长（a、b 速率相同 ⇒ 相位增速相同）。
   ========================================================================= */
const PAR = {
  E: 1.00, v: 1.00, B: 1.00, q: 1.00, m: 1.00,
  B0: 1.00,        /* = E/v，演示值 */
  h: %(h).4f,      /* 题目参数 h 的示意长度（世界单位） */
  R2: %(r2).6f,    /* = 1/5 */
  R3: %(r3).6f,    /* = 1/12 */
  DX: %(dx).6f,    /* = 2R2-2R3 = 7/30 */
  XP: %(xp).6f,     /* = 19/30  */
  lam: %(lam).4f,  /* = M/m = 1.7 */
  Xmeet: %(xm).6f, /* = 34/15 */
  UmeetA: %(uma).1f,
  UmeetB: %(umb).1f,
  Ulaunch: %(ul).1f,
  segA: 12, segB: 5, segT: 17
};
const MU_B0 = PAR.E / PAR.v;          /* B0 = E/v */
const MU_B1 = PAR.m * PAR.v / (PAR.q * PAR.h);  /* B1 = mv/(qh) */

/* 画布几何（世界坐标；坐标轴与区域边界） */
const GEO = {
  hShow: %(h).4f,           /* 起点 (-h,h) */
  xSel0: -0.62, xSel1: -0.48,   /* 速度选择器竖直盒 x 范围 */
  xGen0: -0.78, xGen1: -0.66,   /* 粒子发生器竖直盒 x 范围 */
  ySel0: 0.22, ySel1: 0.58,      /* 两盒 y 范围（粒子在 y=h 处穿过） */
  pr: 0.042,               /* 粒子世界半径 */
  yTrail: -0.30,           /* 区域Ⅱ 磁场符号带下沿 */
  yCap3: 0.30,             /* 区域Ⅲ 磁场符号带上沿 */
  yLeg: -0.62              /* 图例行 y */
};

/* ---------------------------------------------------------------------------
   posA(u)：质量 m 的粒子（红色）走完相位 u 后的位置与速度方向
   返回 {x, y, vx, vy, region, j, inA}
     段 A_j：u ∈ [17j, 17j+12]  区域Ⅱ下半圆，起点 (j·DX, 0)，速度 -y
     段 B_j：u ∈ [17j+12, 17j+17] 区域Ⅲ上半圆，起点 (j·DX+2R2, 0)，速度 +y
   --------------------------------------------------------------------------- */
function posA(u){
  const segT = PAR.segT, segA = PAR.segA, segB = PAR.segB;
  const j = Math.floor(u / segT);
  const loc = u - j * segT;
  if (loc <= segA){
    /* 区域Ⅱ：下半圆，圆心 (j·DX + R2, 0)，角度 180° → 360°（逆时针） */
    const f = loc / segA, th = Math.PI * (1 + f);
    const cx = j * PAR.DX + PAR.R2;
    return {
      x: cx + PAR.R2 * Math.cos(th),
      y: PAR.R2 * Math.sin(th),
      vx: -Math.sin(th), vy: Math.cos(th),
      region: 'R2', j: j, frac: f, cx: cx, cy: 0, rad: PAR.R2
    };
  }
  /* 区域Ⅲ：上半圆，圆心 (j·DX + 2R2 - R3, 0)，角度 0° → 180°（逆时针） */
  const f = (loc - segA) / segB, th = Math.PI * f;
  const cx = j * PAR.DX + 2 * PAR.R2 - PAR.R3;
  return {
    x: cx + PAR.R3 * Math.cos(th),
    y: PAR.R3 * Math.sin(th),
    vx: -Math.sin(th), vy: Math.cos(th),
    region: 'R3', j: j, frac: f, cx: cx, cy: 0, rad: PAR.R3
  };
}
/* 粒子 b：半径按 λ 放大 ⇒ 自身相位 u' = u/λ，位置再乘 λ */
function posB(u){
  const p = posA(u / PAR.lam);
  p.x *= PAR.lam; p.y *= PAR.lam; p.cx *= PAR.lam; p.rad *= PAR.lam;
  return p;
}

/* 区域Ⅰ 内四分之一圆弧：frac ∈ [0,1]，从 (-h,h) 到 O，顺时针 */
function posReg1(frac){
  const th = Math.PI / 2 * (1 - frac);
  return {
    x: -PAR.h + PAR.h * Math.cos(th),
    y: PAR.h * Math.sin(th),
    vx: Math.sin(th), vy: -Math.cos(th)
  };
}

/* ---- 由显示时间 t 求两粒子的相位与状态 ---- */
const T = {
  sel0: %(sel0).2f, sel1: %(sel1).2f,
  reg1_0: %(r10).2f, reg1_1: %(r11).2f,
  ab0: %(ab0).2f, ab1: %(ab1).2f,
  meet0: %(mt0).2f, meet1: %(mt1).2f
};
const T_U_LAUNCH = %(ul).1f;

function stateAt(t){
  const st = {stage: 'sel', u: 0, ua: 0, ub: 0, sel: 1,
              ax: -GEO.xGen0 - 0.02, ay: PAR.h, avx: 1, avy: 0,
              bx: 0, by: 0, bvx: 0, bvy: -1, bOn: false,
              meet: 0, meetA: false};
  if (t < T.sel1){
    /* 阶段①：粒子自发生器射出，沿 +x 匀速直线穿过速度选择器，
       再前进到 (-h,h)。到 t=T.sel1 时恰好抵达 (-h,h)。 */
    st.stage = 'sel';
    const f = Math.max(0, Math.min(1, t / (T.sel1 - T.sel0)));
    /* 行程：发生器出口 x=-0.66 → 终点 -h=-0.40 */
    st.sel = f;
    st.ax = (GEO.xGen1 - 0.02) + f * ((-PAR.h) - (GEO.xGen1 - 0.02));
    st.ay = PAR.h; st.avx = 1; st.avy = 0;
    st.ua = -1e9;                       /* 尚未进入 O 点之后的轨迹 */
  } else if (t < T.reg1_1){
    /* 阶段②：区域Ⅰ 内四分之一圆弧 */
    st.stage = 'reg1';
    const f = Math.max(0, Math.min(1, (t - T.reg1_0) / (T.reg1_1 - T.reg1_0)));
    const p = posReg1(f);
    st.ax = p.x; st.ay = p.y; st.avx = p.vx; st.avy = p.vy;
    st.ua = -1e9;
  } else {
    /* 阶段③④：O 点之后的主轨迹，相位 u 随时间线性增长 */
    st.stage = (t < T.ab1) ? 'ab' : 'meet';
    const uP = %(up).1f;
    st.ua = (t < T.ab1)
      ? (t - T.ab0) / (T.ab1 - T.ab0) * uP                /* 0 → u(P)，连续 */
      : uP + (t - T.meet0) / (T.meet1 - T.meet0) * (PAR.UmeetA - uP);
    const pa = posA(st.ua);
    st.ax = pa.x; st.ay = pa.y; st.avx = pa.vx; st.avy = pa.vy;
    st.aregion = pa.region; st.aj = pa.j; st.afrac = pa.frac;
    st.acx = pa.cx; st.arad = pa.rad;

    if (st.ua >= T_U_LAUNCH){
      /* b 发射：晚一个「区域Ⅱ半圆」的相位 12 */
      st.bOn = true;
      st.ub = st.ua - T_U_LAUNCH;
      const pb = posB(st.ub);
      st.bx = pb.x; st.by = pb.y; st.bvx = pb.vx; st.bvy = pb.vy;
      st.bregion = pb.region; st.bfrac = pb.frac;
    }
    /* 相遇高亮：a 第 9 次、b 第 5 次上穿 x 轴处 */
    const d = Math.hypot(st.ax - PAR.Xmeet, st.ay) + Math.hypot(st.bx - PAR.Xmeet, st.by);
    st.meetA = (Math.abs(st.ua - PAR.UmeetA) < 0.55) && (Math.abs(st.ub - PAR.lam * PAR.UmeetB) < 0.95);
    st.meet = st.meetA ? 1 : 0;
    if (t >= T.meet1) st.meet = 1;
  }
  return st;
}

/* 相位 → 该段已完成的半圆序号（用于面板显示「第几次上穿 x 轴」） */
function upCount(u){
  if (u < 12) return 0;
  return Math.floor((u + 5) / 17);
}
""" % dict(
    h=H_SHOW, r2=R2, r3=R3, dx=DX, xp=X_P, lam=M_RATIO, xm=X_MEET,
    uma=U_MEET_A, umb=U_MEET_B, ul=U_LAUNCH, up=U_AT_P,
    sel0=T_SEL[0], sel1=T_SEL[1], r10=T_REG1[0], r11=T_REG1[1],
    ab0=T_AB[0], ab1=T_AB[1], mt0=T_MEET[0], mt1=T_MEET[1],
)

SETUP_JS = """
/* 本题无需额外 setup：全部几何与相位换算已在全局完成 */
"""

HELPERS_JS = r"""
/* =========================================================================
   绘图辅助（全部声明在 GLOBALS 区，即顶层作用域）
   ⚠ 拿画布尺寸必须用 CSS 像素（getBoundingClientRect），不能用 ctx.canvas.width：
      框架 resize() 已执行 ctx.setTransform(dpr,…)，之后坐标按 CSS 像素解释。
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
  ctx.lineWidth = 3.2; ctx.strokeStyle = 'rgba(255,255,255,0.92)';
  ctx.strokeText(txt, q[0], q[1]);
  ctx.fillStyle = c; ctx.fillText(txt, q[0], q[1]);
  ctx.textAlign = 'left';
  ctx.restore();
}

/* ---- 带白底衬托的小标签（用于运动中的粒子 a / b） ---- */
function haloTag(x, y, txt, color, dy){
  const p = W2S(x, y);
  ctx.save();
  ctx.font = 'italic bold 14px serif';
  ctx.textAlign = 'center';
  ctx.lineWidth = 3.4; ctx.strokeStyle = 'rgba(255,255,255,0.95)';
  ctx.strokeText(txt, p[0], p[1] + dy);
  ctx.fillStyle = color; ctx.fillText(txt, p[0], p[1] + dy);
  ctx.textAlign = 'left';
  ctx.restore();
}

/* ---- 圆心标记：空心小十字 + 圆名 ---- */
function centerMark(cx, cy, name, opts){
  const p = W2S(cx, cy);
  ctx.save();
  ctx.strokeStyle = '#64748b'; ctx.lineWidth = 1.2;
  ctx.beginPath();
  ctx.moveTo(p[0] - 5, p[1]); ctx.lineTo(p[0] + 5, p[1]);
  ctx.moveTo(p[0], p[1] - 5); ctx.lineTo(p[0], p[1] + 5);
  ctx.stroke();
  ctx.restore();
  if (name){
    /* 圆心标签压在轨迹与磁符号上，故加白底描边让位 */
    const q = W2S(cx, cy - 0.035);
    ctx.font = 'italic bold ' + ((opts && opts.size) || 12) + 'px serif';
    ctx.textAlign = 'center';
    ctx.lineWidth = 3.2; ctx.strokeStyle = 'rgba(255,255,255,0.92)';
    ctx.strokeText(name, q[0], q[1]);
    ctx.fillStyle = (opts && opts.color) || '#64748b';
    ctx.fillText(name, q[0], q[1]);
    ctx.textAlign = 'left';
  }
}

/* ---- 竖直装置盒（粒子发生器 / 速度选择器），盒内文字竖排（与原题一致） ---- */
function deviceBox(x0, x1, y0, y1, title){
  const a = W2S(x0, y1), b = W2S(x1, y0);
  ctx.save();
  ctx.fillStyle = 'rgba(226,232,240,0.55)';
  ctx.fillRect(a[0], a[1], b[0] - a[0], b[1] - a[1]);
  ctx.strokeStyle = '#334155'; ctx.lineWidth = 1.6;
  ctx.strokeRect(a[0], a[1], b[0] - a[0], b[1] - a[1]);
    /* 竖排文字：逐字自上而下，水平居中于盒内。
       盒内净高仅 ~50px，5 个字须用 10.5px/11.5px 步进，否则末字被盒底截断 */
    const cx = (a[0] + b[0]) / 2;
    ctx.font = '10.5px sans-serif';
    ctx.textAlign = 'center'; ctx.fillStyle = '#0f172a';
    const step = 11.5;
    const y0s = a[1] + 2;
    for (let i = 0; i < title.length; i++){
      if (y0s + i * step > b[1] - 6) break;
      ctx.fillText(title[i], cx, y0s + 9 + i * step);
    }
  ctx.textAlign = 'left';
  ctx.restore();
}

/* ---- 顶部信息盒（CSS 像素定位；随阶段显示关键结论） ---- */
function drawHud(st){
  const _r = ctx.canvas.getBoundingClientRect();
  const Wp = (_r && _r.width) ? _r.width : ctx.canvas.width;
  const Hp = (_r && _r.height) ? _r.height : ctx.canvas.height;
  if (Wp < 360) return;
  const k = Math.max(0.60, Math.min(1, Wp / 520));

  /* ---- 顶部：阶段名 + 关键结论 ----
     顶部横幅（FIG.processBanner）占 y = 8 ~ 8+(15+14)=37，故 HUD 从 42 起，避免重叠 */
  const lines = hudLines(st);
  const bw = Math.min(Wp - 16, 360 * k), bh = (14 + lines.length * 15) * k;
  const bx = (Wp - bw) / 2, by = 42 * k;
  ctx.save();
  ctx.fillStyle = 'rgba(255,255,255,0.95)';
  ctx.strokeStyle = '#cbd5e1'; ctx.lineWidth = 1.2;
  ctx.fillRect(bx, by, bw, bh); ctx.strokeRect(bx, by, bw, bh);
  ctx.fillStyle = '#1d4ed8'; ctx.font = 'bold ' + (12.5 * k).toFixed(1) + 'px sans-serif';
  ctx.fillText(lines[0], bx + 9 * k, by + 15 * k);
  ctx.fillStyle = '#0f172a'; ctx.font = (11.5 * k).toFixed(1) + 'px sans-serif';
  for (let i = 1; i < lines.length; i++){
    ctx.fillText(lines[i], bx + 9 * k, by + (15 + (i) * 15) * k);
  }
  ctx.restore();

  /* ---- 底部图例：4 项分两行排布（单行时 iw 不足，文字互相重叠） ---- */
  const lw = Math.min(Wp - 16, 350 * k), lh = 42 * k;
  const lx = (Wp - lw) / 2, lyy = Hp - lh - 6 * k;
  ctx.save();
  ctx.fillStyle = 'rgba(255,255,255,0.94)';
  ctx.strokeStyle = '#cbd5e1'; ctx.lineWidth = 1.2;
  ctx.fillRect(lx, lyy, lw, lh); ctx.strokeRect(lx, lyy, lw, lh);
  const items = [
    ['dot', '#7c3aed', '区域Ⅰ  B₁（⊙ 向外）'],
    ['x',   '#7c3aed', '区域Ⅱ  5B（⊗ 向里）'],
    ['x',   '#0ea5e9', '区域Ⅲ  12B（⊗ 向里）'],
    ['x',   '#64748b', '选择器  B₀（⊗）']
  ];
  const cols = 2, rowsN = 2;
  const iw = lw / cols, ih = lh / rowsN;
  for (let i = 0; i < items.length; i++){
    const row = Math.floor(i / cols), col = i % cols;
    const cx0 = lx + iw * col + iw / 2, cy0 = lyy + ih * row + ih / 2;
    ctx.strokeStyle = items[i][1]; ctx.lineWidth = 1.5;
    ctx.beginPath();
    if (items[i][0] === 'dot'){ ctx.arc(cx0 - 42 * k, cy0, 3.4 * k, 0, 7); ctx.stroke();
      ctx.beginPath(); ctx.arc(cx0 - 42 * k, cy0, 1.1 * k, 0, 7); ctx.fillStyle = items[i][1]; ctx.fill(); }
    else { const d = 3.6 * k;
      ctx.moveTo(cx0 - 42 * k - d, cy0 - d); ctx.lineTo(cx0 - 42 * k + d, cy0 + d);
      ctx.moveTo(cx0 - 42 * k + d, cy0 - d); ctx.lineTo(cx0 - 42 * k - d, cy0 + d); }
    ctx.stroke();
    ctx.fillStyle = '#334155'; ctx.font = (10.4 * k).toFixed(1) + 'px sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText(items[i][2], cx0 - 34 * k, cy0 + 3.6 * k);
  }
  ctx.restore();
}
function hudLines(st){
  if (st.stage === 'sel') return ['阶段① 速度选择器',
    'qE = qvB₀  ⇒  B₀ = E / v（磁场 ⊗ 向里）',
    '粒子沿 +x 匀速直线穿过选择器'];
  if (st.stage === 'reg1') return ['阶段② 区域Ⅰ（⊙ 向外，B₁）',
    '圆心 (−h, 0)，半径 R₁ = h',
    'B₁ = mv / (q h)'];
  if (st.meetA) return ['阶段④ 第一次相遇！',
    'a 第 9 次、b 第 5 次上穿 x 轴',
    'M = 17m/10 ，x₁ = 34mv/(15qB)'];
  if (st.stage === 'ab') return ['阶段③ 区域Ⅱ → Ⅲ → Ⅱ',
    'R₂ = mv/5qB ，R₃ = mv/12qB',
    '每周期横移 2R₂−2R₃ = 7mv/30qB',
    't = 29πm/(60qB)'];
  return ['阶段④ 粒子 b 发射（M = 17m/10）',
    '相遇需同时满足位置条件与时间条件',
    '10n = 17j + 5 ⇒ n = 9，j = 5'];
}
"""

DRAWFRAME_JS = r"""
/* ===== 逐帧绘制 ===== */
const st = stateAt(t);
clearBg();

/* ---------- 顶部过程横幅（仅右侧动画画布） ---------- */
if (ctx.canvas.id === 'cv'){
  for (let i = 0; i < BANNERS.length; i++){
    if (t < BANNERS[i][1]){
      const txt = BANNERS[i][2];
      let fs = 15;
      ctx.font = 'bold ' + fs + 'px sans-serif';
      const need = ctx.measureText(txt).width + 26;
      const _r = ctx.canvas.getBoundingClientRect();
      const cw = (_r && _r.width) ? _r.width : ctx.canvas.width;
      const cap = cw * 0.94;
      if (need > cap) fs = Math.max(9, Math.floor(fs * cap / need));
      FIG.processBanner(txt, {size: fs});
      break;
    }
  }
}

/* ---------- 坐标系 ----------
   顶部被 HUD 占据，故不画 y 轴端点标签（会被压住），改为在轴中段单独标 'y' */
FIG.coord(VIEW.xmin + 0.05, VIEW.xmax - 0.05, VIEW.ymin + 0.05, VIEW.ymax - 0.05,
          {labels: ['x']});
FIG.text(0.030, 0.09, 'y', {size: 14, italic: false, color: '#334155', align: 'left'});

/* ---------- 区域Ⅱ（x 轴下方）磁场 ⊗ 5B ---------- */
FIG.magInto(VIEW.xmin + 0.16, VIEW.xmax - 0.08, GEO.yTrail, -0.03,
            {step: 0.235, size: 0.115, color: '#8b5cf6'});
/* ---------- 区域Ⅲ（第一象限）磁场 ⊗ 12B ---------- */
FIG.magInto(0.44, VIEW.xmax - 0.08, 0.035, GEO.yCap3,
            {step: 0.30, size: 0.125, color: '#0ea5e9'});
/* ---------- 区域Ⅰ（第二象限 y ≥ -x）磁场 ⊙ B₁ ---------- */
drawReg1Field();

/* ---------- 区域Ⅰ 边界：y = −x 斜虚线 + 顶边 ---------- */
ctx.save();
ctx.strokeStyle = '#334155'; ctx.lineWidth = 1.8; ctx.setLineDash([6, 4]);
const d1 = W2S(-PAR.h, PAR.h), d2 = W2S(0, 0);
ctx.beginPath(); ctx.moveTo(d1[0], d1[1]); ctx.lineTo(d2[0], d2[1]); ctx.stroke();
ctx.setLineDash([]);
ctx.strokeStyle = '#475569'; ctx.lineWidth = 1.3;
const e1 = W2S(-PAR.h, PAR.h), e2 = W2S(0, PAR.h);
ctx.beginPath(); ctx.moveTo(e1[0], e1[1]); ctx.lineTo(e2[0], e2[1]); ctx.stroke();
ctx.restore();
FIG.text(-PAR.h * 0.52, PAR.h * 0.52 + 0.035, 'y = −x', {size: 12, color: '#475569', align: 'center'});

/* ---------- 粒子发生器 / 速度选择器 ---------- */
deviceBox(GEO.xGen0, GEO.xGen1, GEO.ySel0, GEO.ySel1, '粒子发生器');
deviceBox(GEO.xSel0, GEO.xSel1, GEO.ySel0, GEO.ySel1, '速度选择器');
/* 选择器下半部：磁场 ⊗（盒内 y < 0.34 一带，避开竖排文字与粒子通道） */
FIG.magInto(GEO.xSel0 + 0.030, GEO.xSel1 - 0.030, 0.075, 0.185,
            {step: 0.115, size: 0.095, color: '#64748b'});
/* 电场向下箭头：画在盒右下方的空白区（该处不在区域Ⅰ 内，无 ⊙ 符号） */
const ea = W2S(GEO.xSel1 + 0.022, 0.225), eb = W2S(GEO.xSel1 + 0.022, 0.115);
ctx.save();
ctx.strokeStyle = '#2563eb'; ctx.fillStyle = '#2563eb'; ctx.lineWidth = 1.7;
ctx.beginPath(); ctx.moveTo(ea[0], ea[1]); ctx.lineTo(eb[0], eb[1]); ctx.stroke();
ctx.beginPath();
ctx.moveTo(eb[0], eb[1]);
ctx.lineTo(eb[0] - 4, eb[1] + 7); ctx.lineTo(eb[0] + 4, eb[1] + 7);
ctx.closePath(); ctx.fill();
ctx.restore();

/* ---------- 已走过的轨迹 ---------- */
drawTrails(st);

/* ---------- 圆心与半径标记 ---------- */
drawCenters(st);

/* ---------- 关键点标注 ---------- */
drawKeyLabels(st);

/* ---------- 粒子 a / b ---------- */
if (st.ua > -1e8){
  drawParticle(st.ax, st.ay, st.avx, st.avy, '#dc2626', 'a');
} else {
  drawParticle(st.ax, st.ay, st.avx, st.avy, '#dc2626', 'a');
}
if (st.bOn) drawParticle(st.bx, st.by, st.bvx, st.bvy, '#2563eb', 'b');

/* ---------- 相遇高亮 ---------- */
if (st.meet){
  const p = W2S(PAR.Xmeet, 0);
  ctx.save();
  ctx.strokeStyle = '#f59e0b'; ctx.lineWidth = 2.6;
  ctx.beginPath(); ctx.arc(p[0], p[1], 0.055 * scale, 0, 7); ctx.stroke();
  ctx.beginPath(); ctx.arc(p[0], p[1], 0.085 * scale, 0, 7);
  ctx.strokeStyle = 'rgba(245,158,11,0.55)'; ctx.lineWidth = 1.6; ctx.stroke();
  ctx.restore();
}

/* ---------- HUD ---------- */
if (ctx.canvas.id === 'cv') drawHud(st);

/* =========================================================================
   下面各绘图子函数
   ========================================================================= */

/* 区域Ⅰ 内的 ⊙ 磁场符号（限制在三角形 y ≥ −x 内） */
function drawReg1Field(){
  const step = 0.115, sz = 0.105;
  ctx.save();
  ctx.strokeStyle = '#8b5cf6'; ctx.fillStyle = '#8b5cf6'; ctx.lineWidth = 1.3;
  for (let x = -PAR.h + 0.055; x <= -0.055; x += step){
    for (let y = -x + 0.05; y <= PAR.h - 0.03; y += step){
      /* 顶点右侧贴 y 轴的一小列留空，避免与 O 附近轨迹/标注挤在一起 */
      if (y > 0.30 && x > -0.075) continue;
      const c = W2S(x, y), r = sz * scale * 0.5;
      ctx.beginPath(); ctx.arc(c[0], c[1], r, 0, 7); ctx.stroke();
      ctx.beginPath(); ctx.arc(c[0], c[1], r * 0.32, 0, 7); ctx.fill();
    }
  }
  ctx.restore();
}

/* 已走过的轨迹（a 实线红、b 虚线蓝） */
function drawTrails(st){
  /* a：从 O 到当前相位 */
  if (st.ua > -1e8){
    const pts = [];
    const uEnd = Math.max(0, st.ua);
    for (let u = 0; u <= uEnd + 1e-6; u += 0.55){
      const p = posA(u); pts.push([p.x, p.y]);
    }
    const pe = posA(uEnd); pts.push([pe.x, pe.y]);
    if (pts.length > 1) FIG.trajectory(pts, {color: '#dc2626', lw: 1.9});
  }
  /* 区域Ⅰ 内已走过的一段 */
  if (t >= T.reg1_0 && t < T.reg1_1){
    const pts = [];
    const fEnd = Math.min(1, (t - T.reg1_0) / (T.reg1_1 - T.reg1_0));
    for (let f = 0; f <= fEnd + 1e-6; f += 0.04){
      const p = posReg1(f); pts.push([p.x, p.y]);
    }
    const pe = posReg1(fEnd); pts.push([pe.x, pe.y]);
    if (pts.length > 1) FIG.trajectory(pts, {color: '#dc2626', lw: 1.9});
  }
  /* b：从 O 到当前相位 */
  if (st.bOn && st.ub > 0){
    const pts = [];
    const uEnd = Math.max(0, st.ub);
    for (let u = 0; u <= uEnd + 1e-6; u += 0.55){
      const p = posB(u); pts.push([p.x, p.y]);
    }
    const pe = posB(uEnd); pts.push([pe.x, pe.y]);
    if (pts.length > 1) FIG.trajectory(pts, {color: '#2563eb', lw: 1.7, dash: [5, 4]});
  }
}

/* 圆心标记：只在当前所在的那一段弧上标 */
function drawCenters(st){
  if (st.ua <= -1e8) return;
  const p = posA(st.ua);
  centerMark(p.cx, p.cy, p.region === 'R2' ? 'O₂' : 'O₃');
}

/* 关键点与长度标注 */
function drawKeyLabels(st){
  /* 原点 O */
  FIG.text(0.018, -0.125, 'O', {size: 14, align: 'left'});

  /* 起点 (−h,h)：红点 + 引线标注（横坐标 −h 标在轴下，起点标在上方空白处） */
  ctx.save();
  ctx.fillStyle = '#dc2626';
  const sp = W2S(-PAR.h, PAR.h);
  ctx.beginPath(); ctx.arc(sp[0], sp[1], 3.4, 0, 7); ctx.fill();
  ctx.restore();
  FIG.text(-PAR.h - 0.015, -0.085, '−h', {size: 13, align: 'right'});
  /* 起点标注：引线拉到三角内侧空白处（leadLabel 带白底描边，可压 ⊙ 符号仍清晰）。
     不能放到 y > 0.50 —— 那里已进顶部 HUD 覆盖区（sy ≈ 108px 以下） */
  leadLabel(-PAR.h, PAR.h, -0.20, 0.315, '(−h, h)', '#b91c1c', {size: 12.5});

  /* 区域Ⅰ 圆心 (−h,0) */
  centerMark(-PAR.h, 0, null);

  /* 区域名（只留简短标识，磁场强度放在图例与 HUD 中，避免画面内文字拥挤）。
     区域Ⅰ/Ⅲ 取 y ≈ 0.455：既在 ⊙/⊗ 符号带上沿之外，又在顶部 HUD 下沿之内 */
  FIG.text(-0.135, 0.50, '区域Ⅰ', {size: 12.5, color: '#7c3aed', align: 'center'});
  FIG.text(1.98, -0.60, '区域Ⅱ', {size: 12.5, color: '#7c3aed', align: 'center'});
  FIG.text(1.98, 0.50, '区域Ⅲ', {size: 12.5, color: '#0ea5e9', align: 'center'});

  /* 第一次上穿点 2R₂ = 2mv/5qB —— 标注放在带外，下方偏右 */
  leadLabel(2 * PAR.R2, 0, 2 * PAR.R2 + 0.14, -0.52,
            '2R₂ = 2mv/5qB', '#334155', {size: 12.5});
  /* 第一次横移 2R₃ —— 放在下方偏左，避开圆心 O₂ 标签 */
  leadLabel(PAR.DX, 0, -0.10, -0.34, '2R₃ = mv/6qB', '#334155', {size: 12});
  /* P 点 —— 放在上方 */
  leadLabel(PAR.XP, 0, PAR.XP + 0.02, 0.30,
            'P (19mv/30qB, 0)', '#b91c1c', {size: 12.5});
  /* 相遇点 x₁ —— 上方更右 */
  if (t >= T.meet0 - 0.6){
    leadLabel(PAR.Xmeet, 0, PAR.Xmeet - 0.06, 0.30,
              'x₁ = 34mv/15qB', '#b45309', {size: 12.5});
  }
}

/* 粒子：实心圆 + 速度矢量 + 名称（名称上下错开，避免相遇前后叠字） */
function drawParticle(x, y, vx, vy, color, name){
  const p = W2S(x, y);
  ctx.save();
  ctx.fillStyle = color;
  ctx.beginPath(); ctx.arc(p[0], p[1], GEO.pr * scale, 0, 7); ctx.fill();
  ctx.strokeStyle = '#ffffff'; ctx.lineWidth = 1.6;
  ctx.beginPath(); ctx.arc(p[0], p[1], GEO.pr * scale, 0, 7); ctx.stroke();
  /* 速度矢量 */
  const e = W2S(x + vx * 0.20, y + vy * 0.20);
  ctx.strokeStyle = color; ctx.fillStyle = color; ctx.lineWidth = 2.4;
  ctx.beginPath(); ctx.moveTo(p[0], p[1]); ctx.lineTo(e[0], e[1]); ctx.stroke();
  const ang = Math.atan2(e[1] - p[1], e[0] - p[0]), hd = 8;
  ctx.beginPath();
  ctx.moveTo(e[0], e[1]);
  ctx.lineTo(e[0] - hd * Math.cos(ang - 0.42), e[1] - hd * Math.sin(ang - 0.42));
  ctx.lineTo(e[0] - hd * Math.cos(ang + 0.42), e[1] - hd * Math.sin(ang + 0.42));
  ctx.closePath(); ctx.fill();
  ctx.restore();
  haloTag(x, y, name, color, (name === 'a' ? -1 : 1) * (GEO.pr * scale + 13));
}
"""

READOUTS_JS = r"""
/* =========================================================================
   数据面板读数（与 stateAt 共用同一套几何与相位，保证「动画 = 解析可视化」）
   ========================================================================= */
const st = stateAt(t);
const rows = [];
const NAME = {sel: '①速度选择器', reg1: '②区域Ⅰ圆弧', ab: '③区域Ⅱ→Ⅲ→Ⅱ', meet: '④粒子b发射'};
rows.push(['当前过程', st.meetA ? '④ 第一次相遇' : (NAME[st.stage] || NAME.meet), '']);

if (st.stage === 'sel'){
  rows.push(['粒子速率 $v$', PAR.v.toFixed(2), 'm/s']);
  rows.push(['电场强度 $E$', PAR.E.toFixed(2), 'V/m']);
  rows.push(['$B_0=E/v$', (PAR.E / PAR.v).toFixed(3), 'T']);
  rows.push(['穿出位置', '(-h, h)', '']);
} else if (st.stage === 'reg1'){
  const f = Math.max(0, Math.min(1, (t - T.reg1_0) / (T.reg1_1 - T.reg1_0)));
  rows.push(['$R_1=h$', PAR.h.toFixed(3), 'k']);
  rows.push(['$B_1=mv/(qh)$', MU_B1.toFixed(4), 'B']);
  rows.push(['转过角度', (f * 90).toFixed(1), 'deg']);
  rows.push(['圆心', '(-h, 0)', '']);
} else {
  const ua = Math.max(0, st.ua);
  rows.push(['$R_2$（区域Ⅱ）', PAR.R2.toFixed(4), 'k']);
  rows.push(['$R_3$（区域Ⅲ）', PAR.R3.toFixed(4), 'k']);
  rows.push(['周期横移 $2R_2-2R_3$', PAR.DX.toFixed(4), 'k']);
  rows.push(['$a$ 的相位 $u$', ua.toFixed(1), '']);
  rows.push(['$a$ 第几次上穿 $x$ 轴', String(upCount(ua)), '次']);
  rows.push(['$a$ 坐标 $x$', st.ax.toFixed(4), 'k']);
  rows.push(['$a$ 所在场', st.aregion === 'R2' ? '区域Ⅱ 5B' : '区域Ⅲ 12B', '']);
  rows.push(['$b$ 已发射', st.bOn ? '是 ($M=1.7m$)' : '否', '']);
  if (st.bOn){
    rows.push(['$b$ 第几次上穿 $x$ 轴', String(upCount(st.ub / PAR.lam)), '次']);
    rows.push(['$b$ 坐标 $x$', st.bx.toFixed(4), 'k']);
  }
  /* O→P 的累计时间（单位：πm/(60qB)，即相位每 1 单位对应 π/(60) 的时间常数） */
  rows.push(['$t$（O→P）', (Math.min(ua, 34) * Math.PI / 60).toFixed(4), '·m/qB']);
  rows.push(['$t_{总}=29πm/(60qB)$', (29 * Math.PI / 60).toFixed(4), '·m/qB']);
  rows.push(['$x_1$', (34 / 15).toFixed(4), 'k']);
}
return rows;
"""

# ============================================================
# 六、写入模板
# ============================================================
import io  # noqa: F401
import re as _re

tpl = open(TPL, encoding='utf-8').read()

prob_js = (
    "const PROBLEM = {\n"
    "  title: %r,\n"
    "  given: %r,\n"
    "  images: [{ src: \"__CANVAS_STATIC__\", caption: \"\" }],\n"
    "  asks: [\n%s\n  ],\n"
    "  options: [],\n"
    "  knowledgePoints: [%s]\n"
    "};\n"
) % (
    PROBLEM_TITLE,
    PROBLEM_GIVEN,
    '\n'.join('    %r,' % a for a in PROBLEM_ASKS),
    ', '.join('{ id: "%s" }' % k for k in KNOWLEDGE_IDS),
)

steps_js = "const STEPS = [\n"
for _s in STEPS:
    steps_js += ("  { q: %d, title: %r, tex: %r, note: %r, basis: %r },\n"
                 % (_s['q'], _s['title'], _s['tex'], _s['note'], _s['basis']))
steps_js += "];\n"

view_js = ("const VIEW = { xmin: %s, xmax: %s, ymin: %s, ymax: %s };\n"
           "const SIM  = { duration: %s };\n"
           % (VIEW['xmin'], VIEW['xmax'], VIEW['ymin'], VIEW['ymax'], SIM_DURATION))


def _repl(text, marker, payload):
    pat = _re.compile(r'/\*\s*' + marker + r'\s*\*/')
    return pat.sub(lambda m: payload, text, count=1)


BANNERS_JS = ("const BANNERS = %s;\n"
              % ('[' + ','.join('[%.2f,%.2f,"%s"]' % (a, b, c) for a, b, c in TIMELINE) + ']'))

out = tpl
out = _re.sub(r'const PROBLEM = \{[\s\S]*?\n\};', prob_js.rstrip('\n'), out, count=1)
out = _re.sub(r'const STEPS = \[[\s\S]*?\n\];', steps_js.rstrip('\n'), out, count=1)
out = _re.sub(r'const VIEW = \{[^\n]*\n\s*const SIM\s*=\s*\{[^\n]*\n', view_js, out, count=1)

out = _repl(out, '__GLOBALS__', GLOBALS_JS.strip() + '\n\n' + HELPERS_JS.strip()
            + '\n\n' + BANNERS_JS)
out = _repl(out, '__SETUP__', SETUP_JS.strip())
out = _repl(out, '__DRAWFRAME__', DRAWFRAME_JS.strip())
out = _repl(out, '__READOUTS__', READOUTS_JS.strip())

CSS_TUNE = (
    '<style id="tune-width">\n'
    '.col-analysis{flex:2.05 1 380px}\n'
    '.step{padding:8px 9px 8px 11px}\n'
    '.step .tex{padding:2px 0 6px}\n'
    '.step .tex mjx-container[display="true"]{max-width:100%}\n'
    '.step .tex mjx-container[display="true"] svg{max-width:100%;height:auto}\n'
    '</style>\n'
)
out = out.replace('</head>', CSS_TUNE + '</head>', 1) if '</head>' in out else CSS_TUNE + out

open(OUT, 'w', encoding='utf-8').write(out)

probes = ['2026·河北·18', '__CANVAS_STATIC__', 'em-cyclotron', 'processBanner',
          'FIG.magInto', 'posA', 'posB', 'function stateAt', 'const BANNERS',
          '29\\pi m}{60qB', '34mv}{15qB', '17m}{10',
          '__GLOBALS__', '__SETUP__', '__DRAWFRAME__', '__READOUTS__']
print('=== 探针自检 ===')
for _p in probes:
    print(('FOUND   ' if _p in out else 'MISSING ') + _p)
print('\noutput: %s  (%d bytes)' % (OUT, os.path.getsize(OUT)))
print('R2=%.4f R3=%.4f DX=%.6f XP=%.6f Xmeet=%.6f lam=%.2f'
      % (R2, R3, DX, X_P, X_MEET, M_RATIO))
print('u(P)=%.1f  u_a(meet)=%.1f  u_b(meet)=%.1f' % (U_AT_P, U_MEET_A, M_RATIO * U_MEET_B))