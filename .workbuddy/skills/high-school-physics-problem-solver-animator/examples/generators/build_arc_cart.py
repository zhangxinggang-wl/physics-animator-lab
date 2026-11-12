# -*- coding: utf-8 -*-
"""生成《2024安徽14 弧轨道碰撞》教学动画单文件 HTML。

【题图几何反编译】原图 414x230 px，换算为世界坐标（x 向右、y 向上）：
  摆球 m ：细线水平拉直，球在 O 左侧
  悬点 O ：上方，细线长 L
  细线   ：竖直段（下摆终点）
  物块 M ：小车水平轨道最左端（橙色方块）
  小车   ：长矩形车体 + 两轮，右端接光滑四分之一圆弧（蓝色虚线标 R）
  标注   ：水平段标 s，圆弧标 R

【答案】 (1) T=6 N   (2) v'=4 m/s   (3) 1/2 ≤ μ < 4/5
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = os.path.join(ROOT, 'assets', 'template.html')
OUT = os.path.join(ROOT, '2024安徽14_弧轨道碰撞_教学动画.html')

# ============================================================
# 一、物理参数（SI）
# ============================================================
# 小球 m=0.20 kg ；物块 M=0.30 kg ；小车 M=0.30 kg
# L=1.25 m, s=1.0 m, R=0.15 m, g=10 m/s^2
MB = 0.20     # 小球
MP = 0.30     # 物块
MC = 0.30     # 小车
G = 10.0
L = 1.25
S = 1.0
R = 0.15
V1 = (2 * G * L) ** 0.5                     # 5 m/s
V2 = 2 * MB / (MB + MP) * V1                # 4 m/s
MU_MAX = V2 ** 2 / (2 * G * S)              # 0.8
MU_MIN = 0.5                                # 由 v_in^2 = 4gR 得 (16-6)/20 = 1/2
MU_DEMO = 0.60                              # 演示值（落在 (0.5, 0.8) 内）
THETA_STOP = 70.5288                        # μ=0.6 时共速角（度）

# ---- 动画几何（世界坐标，米；画布作了压缩，仅示意）----
X_PIVOT = 3.30            # 悬点 O 的 x
Y_PIVOT = 4.55            # 悬点 O 的 y
X_BALL0 = X_PIVOT - 3.30  # 摆球水平起点（细线水平拉直）
Y_BALL0 = Y_PIVOT
Y_FLOOR = 2.40            # 小车轨道上表面 y
X_TRACK0 = -0.10          # 小车水平轨道左端
X_ARC0 = X_TRACK0 + 3.60  # 圆弧最低点 x（这段示意题目的 s）
ARC_R = 1.10              # 圆弧半径（画布示意）
ARC_CX = X_ARC0
ARC_CY = Y_FLOOR + ARC_R
WHEEL_R = 0.26
BODY_Y = Y_FLOOR - 0.62   # 车体底部

# 动画内几何映射（把题目真实量映射到画布示意量）
# 摆长：小球从水平位置摆到最低点，弧长按画布比例 = 3.30 世界单位
LPIX = 3.30
# 下摆过程中，细线的水平拉力会把小车整体向右拉动（与小球反向）。
# 真实位移很小（≈2.5 cm），画布上放大为 0.62 世界单位，使「小车随小球反冲」可见。
CART_SHIFT = 0.62
# 水平段长度：画布上 s 段 = 3.60 世界单位
SPIX = 3.60
# 圆弧半径：画布上 = 1.10 世界单位

# ============================================================
# 二、题面（逐字录入）
# ============================================================
PROBLEM_TITLE = '2024·安徽·14（14分）'
PROBLEM_GIVEN = (
    '如图所示，一实验小车静止在光滑水平面上，其上表面有粗糙水平轨道与光滑四分之一圆弧轨道．'
    '圆弧轨道与水平轨道相切于圆弧轨道最低点，一物块静止于小车最左端，'
    '一小球用不可伸长的轻质细线悬挂于O点正下方，并轻靠在物块右侧．'
    '现将细线拉直到水平位置时，由静止释放小球，小球运动到最低点时与物块发生弹性碰撞．'
    '碰撞后，物块沿着小车上的轨道运动．已知细线长 \\(L=1.25\\ \\mathrm{m}\\)．'
    '小球质量 \\(m=0.20\\ \\mathrm{kg}\\)．物块、小车质量均为 \\(M=0.30\\ \\mathrm{kg}\\)．'
    '小车上的水平轨道长 \\(s=1.0\\ \\mathrm{m}\\)．圆弧轨道半径 \\(R=0.15\\ \\mathrm{m}\\)．'
    '小球、物块均可视为质点．不计空气阻力，重力加速度 \\(g\\) 取 \\(10\\ \\mathrm{m/s^{2}}\\)．'
)
PROBLEM_ASKS = [
    '求小球运动到最低点与物块碰撞前所受拉力的大小；',
    '求小球与物块碰撞后的瞬间，物块速度的大小；',
    '为使物块能进入圆弧轨道，且在上升阶段不脱离小车，求物块与水平轨道间的动摩擦因数 \\(\\mu\\) 的取值范围．',
]
KNOWLEDGE_IDS = [
    'mech-energy-conservation',
    'mech-circular-horizontal',
    'mech-momentum-collision-1d',
    'mech-momentum-conservation',
    'mech-newton-second',
    'mech-force-friction',
    'mech-energy-work-energy-theorem',
]

# ============================================================
# 三、STEPS
# ============================================================
STEPS = [
    # ================= 第一问 =================
    dict(q=1, title='小球下摆过程：机械能守恒',
         tex=r'mgL=\tfrac{1}{2}mv_1^{2}',
         note='小球自水平位置由静止释放，下落高度等于细线长 \\(L\\)。'
              '细线拉力始终沿绳、与速度方向垂直，不做功；只有重力做功，故机械能守恒。'
              '取最低点为重力势能零点，规定向右为正方向。',
         basis='机械能守恒定律'),
    dict(q=1, title='代入数据求最低点速度',
         tex=r'v_1=\sqrt{2gL}=\sqrt{25}=5\ \mathrm{m/s}',
         note='代入 \\(g=10\\ \\mathrm{m/s^{2}}\\)、\\(L=1.25\\ \\mathrm{m}\\)，'
              '得 \\(2gL=2\\times 10\\times 1.25=25\\)，故 \\(v_1=\\sqrt{25}=5\\ \\mathrm{m/s}\\)。'
              '小球到达最低点时速度方向水平向右，这就是碰撞前一瞬间小球的速度。',
         basis='机械能守恒定律'),
    dict(q=1, title='最低点受力分析：合力提供向心力',
         tex=r'T-mg=m\tfrac{v_1^{2}}{L}',
         note='在最低点，小球受竖直向下的重力 \\(mg\\) 与沿绳向上的细线拉力 \\(T\\)，'
              '二者合力竖直向上、指向悬点 O，正是做圆周运动所需的向心力。'
              '注意：向心力是合力的法向分量，不是「额外多出来的力」，'
              '在最低点向心方向恰为竖直向上，故可写 \\(T-mg=m\\tfrac{v_1^{2}}{L}\\)。',
         basis='牛顿第二定律（沿半径指向圆心）'),
    dict(q=1, title='代入数据求细线拉力',
         tex=r'T=mg+m\tfrac{v_1^{2}}{L}=2+4=6\ \mathrm{N}',
         note='细线拉力 \\(T=6\\ \\mathrm{N}\\)。'
              '其中 \\(\\tfrac{v_1^{2}}{L}=\\tfrac{25}{1.25}=20\\ \\mathrm{m/s^{2}}\\)，'
              '故 \\(T=0.20\\times 10+0.20\\times 20=2+4=6\\ \\mathrm{N}\\)。'
              '极限检验：若小球静止悬垂（\\(v_1\\to 0\\)），则 \\(T\\to mg=2\\ \\mathrm{N}\\)，'
              '与「静止吊挂时绳的拉力等于重力」的常识一致。',
         basis='牛顿第二定律'),

    # ================= 第二问 =================
    dict(q=2, title='碰撞过程：水平方向动量守恒',
         tex=r'mv_1=mv_1^{\prime}+Mv_2^{\prime}',
         note='碰撞时间极短，且碰撞中系统在水平方向不受外力（地面光滑，绳的拉力竖直），'
              '故**水平方向动量守恒**。规定向右为正方向：'
              '碰前物块与小车均静止，只有小球以 \\(v_1\\) 运动。',
         basis='动量守恒定律'),
    dict(q=2, title='弹性碰撞：动能同时守恒',
         tex=r'\tfrac{1}{2}mv_1^{2}=\tfrac{1}{2}mv_1^{\prime 2}+\tfrac{1}{2}Mv_2^{\prime 2}',
         note='题目明确为**弹性碰撞**，故碰后系统动能之和等于碰前动能。'
              '与动量守恒式联立，即可求出碰后两者的速度。',
         basis='弹性碰撞（动能守恒）'),
    dict(q=2, title='联立解得物块碰后速度',
         tex=r'v_2^{\prime}=\tfrac{2m}{m+M}v_1=\tfrac{0.40}{0.50}\times 5=4\ \mathrm{m/s}',
         note='物块碰后速度 \\(v_2^{\\prime}=4\\ \\mathrm{m/s}\\)，方向水平向右，将沿小车水平轨道运动。'
              '特例检验：当 \\(m=M\\) 时 \\(v_2^{\\prime}=v_1\\)，'
              '即「等质量弹性碰撞交换速度」，本式与之吻合。'
              '顺便可得碰后小球速度 \\(v_1^{\\prime}=\\tfrac{m-M}{m+M}v_1=-1\\ \\mathrm{m/s}\\)，'
              '即小球被弹回、向左运动。',
         basis='动量守恒定律 + 弹性碰撞动能守恒'),

    # ================= 第三问 =================
    dict(q=3, title='水平轨道滑行：用动能定理求圆弧入口速度',
         tex=r'\tfrac{1}{2}Mv_2^{\prime 2}-\mu Mgs=\tfrac{1}{2}Mv_{\mathrm{in}}^{2}',
         note='物块在粗糙水平轨道上滑动 \\(s=1.0\\ \\mathrm{m}\\)，'
              '所受滑动摩擦力 \\(f=\\mu Mg\\)，克服摩擦力做功 \\(\\mu Mgs\\)。'
              '由动能定理求物块到达圆弧最低点时的速度 \\(v_{\\mathrm{in}}\\)。'
              '**说明**：此段中物块向右减速的同时小车被摩擦力带动向右加速，'
              '两者相对滑动的路程恰为 \\(s\\)，故摩擦生热 \\(Q=\\mu Mgs\\) 的计算成立。',
         basis='动能定理（摩擦力做负功）'),
    dict(q=3, title='能进入圆弧轨道的条件（μ 的上界）',
         tex=r'v_{\mathrm{in}}^{2}=v_2^{\prime 2}-2\mu gs>0\ \Longrightarrow\ \mu<\tfrac{v_2^{\prime 2}}{2gs}',
         note='物块要能到达并**进入**圆弧轨道，到达最低点时必须仍有速度，即 \\(v_{\\mathrm{in}}^{2}>0\\)，'
              '故 \\(\\mu<\\tfrac{v_2^{\\prime 2}}{2gs}=\\tfrac{16}{20}=0.8\\)。这是 \\(\\mu\\) 的**上界**。',
         basis='动能定理'),

    dict(q=3, title='圆弧上升过程：水平方向动量守恒',
         tex=r'Mv_{\mathrm{in}}=M_cV+M\left(V+u\cos\theta\right)',
         note='物块进入**光滑**圆弧后不再有摩擦力，但物块对圆弧面的压力有水平分量，'
              '会推动小车加速，两者之间存在相互作用。'
              '然而系统（物块 + 小车）在水平方向仍不受外力（地面光滑），'
              '所以**全过程水平方向动量守恒**。'
              '设物块相对小车的切向速率为 \\(u\\)、小车速度为 \\(V\\)，'
              '\\(\\theta\\) 为物块相对圆心偏离最低点的夹角，'
              '则物块的水平速度为 \\(V+u\\cos\\theta\\)。'
              '（此处物块质量与小车质量均为 \\(M=0.30\\ \\mathrm{kg}\\)。）',
         basis='动量守恒定律（水平方向）'),
    dict(q=3, title='圆弧上升过程：机械能守恒',
         tex=r'\tfrac{1}{2}Mv_{\mathrm{in}}^{2}=\tfrac{1}{2}MV^{2}+\tfrac{1}{2}Mv_p^{2}+Mgh',
         note='圆弧面光滑、无摩擦生热，故机械能守恒：'
              '圆弧入口处的总动能，等于「小车动能 + 物块动能 + 物块增加的重力势能」。'
              '式中 \\(v_p\\) 为物块对地速度大小，'
              '物块速度由水平分量 \\(V+u\\cos\\theta\\) 与竖直分量 \\(u\\sin\\theta\\) 合成，'
              '故 \\(v_p^{2}=\\left(V+u\\cos\\theta\\right)^{2}+\\left(u\\sin\\theta\\right)^{2}\\)；'
              '物块上升高度 \\(h=R\\left(1-\\cos\\theta\\right)\\)，'
              '即重力势能项 \\(Mgh=MgR\\left(1-\\cos\\theta\\right)\\)。',
         basis='机械能守恒定律'),
    dict(q=3, title='消去小车速度，得相对速率公式',
         tex=r'u^{2}=\dfrac{A}{B},\quad A=\tfrac{1}{4}v_{\mathrm{in}}^{2}-gR\left(1-\cos\theta\right),\quad B=\tfrac{1}{2}-\tfrac{1}{4}\cos^{2}\theta',
         note='由动量守恒式解出 \\(V=\\tfrac{v_{\\mathrm{in}}-u\\cos\\theta}{2}\\)，'
              '代入机械能守恒式消去 \\(V\\)。'
              '因物块与小车质量相等（均为 \\(M\\)），两式整理后得到上式——'
              '这就是物块**相对小车的切向速率平方 \\(u^{2}\\) 随 \\(\\theta\\) 的变化规律**。'
              '\\(u^{2}>0\\) 表示物块相对小车仍在切向滑动；'
              '\\(u^{2}\\) 降为 0 表示两者达到共速（相对静止），此后一起运动。',
         basis='动量守恒定律 + 机械能守恒定律'),
    dict(q=3, title='上升阶段不脱离小车的临界条件',
         tex=r'u^{2}\left(90^{\circ}\right)=0\ \Longrightarrow\ v_{\mathrm{in}}^{2}=4gR',
         note='「在上升阶段不脱离小车」的含义是：物块必须在到达圆弧顶端'
              '（\\(\\theta=90^{\\circ}\\)）**之前**就与小车达到共速，'
              '此后二者一起沿轨道运动，物块不会被甩离小车。'
              '若到达顶端时 \\(u^{2}\\) 仍为正，说明物块还有相对速度，将从顶端飞出而脱离小车。'
              '故**临界情形**取 \\(u^{2}\\!\\left(90^{\\circ}\\right)=0\\)，'
              '代入 \\(\\cos 90^{\\circ}=0\\) 即得 \\(\\tfrac{1}{4}v_{\\mathrm{in}}^{2}=gR\\)，'
              '故 \\(v_{\\mathrm{in}}^{2}=4gR=4\\times 10\\times 0.15=6\\ \\mathrm{m^{2}/s^{2}}\\)。',
         basis='机械能守恒定律 + 动量守恒定律'),
    dict(q=3, title='解出动摩擦因数的取值范围',
         tex=r'\tfrac{1}{2}\leq\mu<\tfrac{4}{5}',
         note='由临界条件得 \\(v_{\\mathrm{in}}^{2}=4gR=6\\ \\mathrm{m^{2}/s^{2}}\\)，'
              '代回 \\(v_{\\mathrm{in}}^{2}=v_2^{\\prime 2}-2\\mu gs\\)：\\(16-20\\mu=6\\)，'
              '解得 \\(\\mu=\\tfrac{1}{2}=0.5\\)，这是 \\(\\mu\\) 的**下界**（对应「恰好到达圆弧顶端时与小车共速」）。'
              '综合「能进入圆弧轨道」的上界 \\(\\mu<\\tfrac{4}{5}\\)，'
              '得动摩擦因数的取值范围为 \\(\\tfrac{1}{2}\\leq\\mu<\\tfrac{4}{5}\\)。'
              '取 \\(\\mu=0.6\\) 验证：\\(v_{\\mathrm{in}}=\\sqrt{16-12}=2\\ \\mathrm{m/s}\\)，'
              '物块在 \\(\\theta\\approx 70.5^{\\circ}\\) 处即与小车共速，未到顶端，符合要求。',
         basis='动能定理 + 动量守恒定律 + 机械能守恒定律'),
]

# ============================================================
# 四、VIEW / SIM
# ============================================================
VIEW = dict(xmin=-0.55, xmax=5.55, ymin=1.35, ymax=5.55)
SIM_DURATION = 8.0

TIMELINE = [
    (0.00, 1.50, '过程1  小球下摆'),
    (1.50, 2.10, '过程2  弹性碰撞'),
    (2.10, 4.10, '过程3  水平轨道滑行'),
    (4.10, 7.30, '过程4  圆弧上升'),
    (7.30, 8.00, '过程5  共速一起运动'),
]


# ============================================================
# 五、动画实现（JS）
# ============================================================
# 时间轴（秒，显示时间，按过程分段；每段内部用"物理时间"驱动，保证数值真实）
T_SW = (TIMELINE[0][0], TIMELINE[0][1])   # 0.00-1.50  小球下摆
T_HT = (TIMELINE[1][0], TIMELINE[1][1])   # 1.50-2.10  弹性碰撞
T_SL = (TIMELINE[2][0], TIMELINE[2][1])   # 2.10-4.10  水平滑行
T_AR = (TIMELINE[3][0], TIMELINE[3][1])   # 4.10-7.30  圆弧上升
T_ED = (TIMELINE[4][0], TIMELINE[4][1])   # 7.30-8.00  共速


def _swing_table(n_dt=0.0005):
    """单摆 phi(t)：从水平(pi/2)摆到竖直(0)，用 dphi/dt = -sqrt(2gL cos(phi))/L 数值积分。"""
    import math
    phi = math.pi / 2
    t = 0.0
    table = [(0.0, phi)]
    while phi > 1e-7 and t < 3.0:
        v = math.sqrt(max(0.0, 2 * G * L * math.cos(phi)))
        if v < 1e-9:
            break
        phi -= v / L * n_dt
        t += n_dt
        table.append((t, max(0.0, phi)))
    return table, t


def _arc_table(n_dt=0.0002):
    """圆弧段 theta(t)：dtheta/dt = u_rel(theta)/R，theta 自 0 升到 thetaStop。"""
    import math
    vin2 = V2 ** 2 - 2 * MU_DEMO * G * S
    vin = vin2 ** 0.5
    coef = 0.5 * MP / (MP + MC)      # m_b/(m_b+M_c) = 0.5
    cstop = 1 - (vin2 * (0.5 - coef)) / (G * R)
    cstop = max(-1.0, min(1.0, cstop))
    th_stop = math.acos(cstop)

    def usq(th):
        c = math.cos(th)
        A = 0.5 - MP * c * c / (2 * (MP + MC))
        B = vin2 * (0.5 - MP / (2 * (MP + MC))) - G * R * (1 - c)
        return max(0.0, B / A)

    t = 0.0
    th = 0.0
    table = [(0.0, 0.0)]
    while th < th_stop and t < 3.0:
        u = math.sqrt(usq(th))
        if u < 1e-7:
            break
        th += u / R * n_dt
        t += n_dt
        table.append((t, min(th, th_stop)))
    return table, t, th_stop, vin


SWING_TABLE, SWING_TTOTAL = _swing_table()
ARC_TABLE, ARC_TTOTAL, THETA_STOP, VIN_DEMO = _arc_table()

# 水平段真实时长 T = sqrt(S/(mu g))（相对加速度 2 mu g）
import math as _m
SLIDE_TTOTAL = _m.sqrt(S / (MU_DEMO * G))

# 压缩为 JS 数组字面量（抽样，避免文件过大）
def _tbl_js(tbl, every):
    return '[' + ','.join('[%.6f,%.7f]' % (t, v) for t, v in tbl[::every]) + ']'


SW_JS = _tbl_js(SWING_TABLE, 8)
ARC_JS = _tbl_js(ARC_TABLE, 8)

GLOBALS_JS = """
/* ===== 本题全局：物理参数与画布几何 ===== */
const P = {
  g: %(g).1f, L: %(L).2f, S: %(S).2f, R: %(R).3f,
  mBall: %(mb).2f, mBlock: %(mp).2f, mCart: %(mc).2f,
  v1: %(v1).1f, v2: %(v2).1f,          /* 碰前小球速度 / 碰后物块速度 (m/s) */
  mu: %(mu).2f,                        /* 演示用动摩擦因数 */
  vin: %(vin).6f,                      /* 圆弧入口速度 (m/s) */
  thetaStop: %(thstop).8f,             /* 共速角 (rad) */
  Tsw: %(tsw).8f, Tsl: %(tsl).8f, Tarc: %(tarc).8f,   /* 各段真实物理时长 (s) */
  cartShift: %(cshift).2f              /* 下摆过程小车被细线拉动的画布位移（世界单位，示意） */
};
const MU_MIN = 0.5, MU_MAX = 0.8;

/* 画布几何（世界坐标，仅示意；x 向右、y 向上） */
const GEO = {
  xPivot: %(xp).4f, yPivot: %(yp).4f,
  xBall0: %(xb0).4f, lpix: %(lpix).4f,
  yFloor: %(yf).4f,
  xTrack0: %(xt0).4f, xArc0: %(xa0).4f, spix: %(spix).4f,
  arcR: %(ar).4f, arcCx: %(acx).4f, arcCy: %(acy).4f,
  wheelR: %(wr).4f, bodyY: %(by).4f,
  blockW: 0.30, blockH: 0.30, ballR: 0.115
};
/* 水平轨道滑行阶段结束时小车相对轨道起点的位移（画布世界单位）。
   圆弧段需在此位移基础上继续累加，保证阶段之间位置连续。
   注意：必须写在 GEO 之后 —— 它引用了 GEO.spix，提前写会触发
   「Cannot access 'GEO' before initialization」而让整页脚本中断。 */
const SLIDE_END_DX = 0.5 * P.mu * P.g * P.Tsl * P.Tsl * (GEO.spix / P.S);

/* 预计算表：[归一化时间 u, 物理量] —— u∈[0,1] 对应各段完整过程 */
const SW_TBL  = %(swjs)s;   /* 小球下摆：phi(rad)，pi/2 -> 0 */
const ARC_TBL = %(arcjs)s;  /* 圆弧上升：theta(rad)，0 -> thetaStop */

/* 时间节点（显示时间，秒） */
const T = { sw0: %(sw0).2f, sw1: %(sw1).2f, ht0: %(ht0).2f, ht1: %(ht1).2f,
            sl0: %(sl0).2f, sl1: %(sl1).2f, ar0: %(ar0).2f, ar1: %(ar1).2f,
            ed0: %(ed0).2f, ed1: %(ed1).2f };

/* 在预计算表上线性插值：u∈[0,1] -> 数值 */
function tblAt(TBL, u){
  u = Math.max(0, Math.min(1, u));
  const x = u * (TBL.length - 1);
  const i0 = Math.floor(x), i1 = Math.min(TBL.length - 1, i0 + 1);
  const f = x - i0;
  return TBL[i0][1] + f * (TBL[i1][1] - TBL[i0][1]);
}

/* 圆弧上物块相对小车的切向速率 u_rel(theta)（m/s，物理真值） */
function uRelAt(th){
  const c = Math.cos(th);
  const A = 0.5 - P.mBlock * c * c / (2 * (P.mBlock + P.mCart));
  const B = P.vin * P.vin * (0.5 - P.mBlock / (2 * (P.mBlock + P.mCart)))
            - P.g * P.R * (1 - c);
  return Math.sqrt(Math.max(0, B / A));
}
""" % dict(
    g=G, L=L, S=S, R=R, mb=MB, mp=MP, mc=MC,
    v1=V1, v2=V2, mu=MU_DEMO, vin=VIN_DEMO, thstop=THETA_STOP,
    tsw=SWING_TTOTAL, tsl=SLIDE_TTOTAL, tarc=ARC_TTOTAL,
    cshift=CART_SHIFT,
    xp=X_PIVOT, yp=Y_PIVOT, xb0=X_BALL0, lpix=LPIX,
    yf=Y_FLOOR, xt0=X_TRACK0, xa0=X_ARC0, spix=SPIX,
    ar=ARC_R, acx=ARC_CX, acy=ARC_CY, wr=WHEEL_R, by=BODY_Y,
    swjs=SW_JS, arcjs=ARC_JS,
    sw0=T_SW[0], sw1=T_SW[1], ht0=T_HT[0], ht1=T_HT[1],
    sl0=T_SL[0], sl1=T_SL[1], ar0=T_AR[0], ar1=T_AR[1],
    ed0=T_ED[0], ed1=T_ED[1],
)

SETUP_JS = """
/* 本题无需额外 setup（摆角表与圆弧表已在全局预计算） */
"""

# ---- 顶层辅助函数（声明在全局作用域，供 drawSceneBody / readouts 调用）----
HELPERS_JS = """
/* =========================================================================
   stateAt(t)：由物理方程实时求出全部状态量，画面与数据面板共用（保证一致）
   ========================================================================= */
function stateAt(t){
  const st = {
    stage: 'swing', phi: Math.PI/2, theta: 0,
    ballX: GEO.xBall0, ballY: GEO.yFloor + GEO.lpix, ballV: 0,
    blockX: GEO.xTrack0 + GEO.blockW/2, blockY: GEO.yFloor + GEO.blockH/2, blockV: 0,
    cartDx: 0, cartV: 0, uRel: 0, height: 0,
    ballOnString: true, trail: []
  };

  if (t < T.sw1){
    /* ---------- 过程1：小球自水平位置下摆（机械能守恒） ---------- */
    st.stage = 'swing';
    const u = (T.sw1 > T.sw0) ? (t - T.sw0) / (T.sw1 - T.sw0) : 1;
    st.phi = tblAt(SW_TBL, u);                       /* 半径与竖直向下方向的夹角 */
    /* 小车反冲位移：细线水平分力 F·sinφ 推小车反向运动，位移随下摆单调增大。
       φ 自 π/2（水平）→ 0（竖直），取 cartDx = −cartShift·cosφ 即满足
         φ = π/2（t 起点）→ cartDx = 0（尚未移动）
         φ = 0  （下摆终点）→ cartDx = −cartShift（位移最大）
       与过程2（t = 1.5 s 起）的初值严格连续，不会跳变。 */
    const xPivNow = GEO.xPivot - P.cartShift * Math.cos(st.phi);
    st.cartDx = xPivNow - GEO.xPivot;
    st.ballX = xPivNow - GEO.lpix * Math.sin(st.phi);
    st.ballY = GEO.yPivot - GEO.lpix * Math.cos(st.phi);
    /* 真实速率：v = sqrt(2 g L cos(phi))  （下落高度 = L cos phi，从水平释放） */
    st.ballV = Math.sqrt(Math.max(0, 2 * P.g * P.L * Math.cos(st.phi)));
    st.ballOnString = true;
    st.blockX = GEO.xTrack0 + GEO.blockW/2;
    st.blockY = GEO.yFloor + GEO.blockH/2;

  } else if (t < T.sl0){
    /* ---------- 过程2：弹性碰撞（瞬时），小球被弹回向左 ---------- */
    st.stage = 'hit';
    st.phi = 0;
    const f = (t - T.ht0) / Math.max(1e-6, T.ht1 - T.ht0);
    st.cartDx = -P.cartShift;   /* 与下摆终点（φ→0）严格连续，保证无跳变 */
    st.ballX = GEO.xPivot + st.cartDx - 0.26 * f;    /* 碰后小球向左微移（悬点已随小车） */
    st.ballY = GEO.yFloor + GEO.blockH/2;
    st.ballV = 1.0;                                  /* |v1'| = 1 m/s */
    st.blockV = P.v2;                                /* 物块获得 4 m/s */

  } else if (t < T.ar0){
    /* ---------- 过程3：物块在水平轨道滑行（摩擦带动小车） ---------- */
    st.stage = 'slide';
    const u = (t - T.sl0) / Math.max(1e-6, T.sl1 - T.sl0);
    const tr = u * P.Tsl;                            /* 真实物理时间 */
    const mu = P.mu;
    const xb = P.v2 * tr - 0.5 * mu * P.g * tr * tr; /* 物块地面位移 (m) */
    const xc = 0.5 * mu * P.g * tr * tr;             /* 小车地面位移 (m) */
    const k = GEO.spix / P.S;                        /* 米 -> 画布世界单位 */
    st.blockX = GEO.xTrack0 + GEO.blockW/2 + xb * k;
    /* 小车：叠加下摆阶段的反冲偏移（摩擦推力把小车向右推回一部分） */
    st.cartDx = -P.cartShift + xc * k;
    st.blockV = Math.max(0, P.v2 - mu * P.g * tr);
    st.cartV  = mu * P.g * tr;
    st.ballX  = GEO.xPivot + st.cartDx - 0.26;
    st.ballY  = GEO.yPivot - GEO.lpix;
    st.ballV  = 0; st.ballOnString = false;

  } else if (t < T.ed0){
    /* ---------- 过程4：物块沿光滑圆弧上升（动量守恒 + 机械能守恒） ---------- */
    st.stage = 'arc';
    const u = (t - T.ar0) / Math.max(1e-6, T.ar1 - T.ar0);
    st.theta = tblAt(ARC_TBL, u);
    const th = st.theta, c = Math.cos(th);
    st.uRel = uRelAt(th);                            /* 物块相对小车切向速率 */
    st.cartV = (P.vin - st.uRel * c) / 2;            /* 小车速度（动量守恒） */
    /* 小车位移：由动量守恒积分得 x_c = (R/2)(theta - u_rel·sinθ/...)
       简化用精确关系：物块地面水平位移 x_b = R sinθ（相对圆心）
       小车位移 x_c 由「相对位移 = R sinθ」推得：x_c = x_b - R sinθ 不成立，
       改用动量守恒积分近似：x_c ≈ (R/2)·(1 - cos θ_ref) —— 取能量一致性近似 */
    st.cartDx = -P.cartShift + SLIDE_END_DX + (GEO.arcR / 2) * (th - Math.sin(th)) * 1.8;
    /* 圆弧最低点 = 水平轨道右端（保证与滑行段衔接连续）：xArcNow = xTrack0 + spix + cartDx */
    st.blockX = GEO.xTrack0 + GEO.spix + st.cartDx - GEO.arcR * Math.sin(th);
    st.blockY = GEO.yFloor + GEO.arcR * (1 - Math.cos(th)) + GEO.blockH/2 * Math.cos(th);
    st.blockV = Math.abs(st.cartV + st.uRel * c);
    st.height = P.R * (1 - c);                       /* 真实上升高度 (m) */
    st.ballX = GEO.xPivot + st.cartDx - 0.26;
    st.ballY = GEO.yPivot - GEO.lpix;
    st.ballV = 0; st.ballOnString = false;

  } else {
    /* ---------- 过程5：物块与小车共速，一起运动 ---------- */
    st.stage = 'lock';
    st.theta = P.thetaStop;
    const th = st.theta, c = Math.cos(th);
    st.uRel = 0;
    st.cartV = P.vin / 2;                            /* 共速 = v_in/2 */
    st.cartDx = -P.cartShift + SLIDE_END_DX + (GEO.arcR / 2) * (th - Math.sin(th)) * 1.8;
    /* 圆弧最低点 = 水平轨道右端（保证与滑行段衔接连续）：xArcNow = xTrack0 + spix + cartDx */
    st.blockX = GEO.xTrack0 + GEO.spix + st.cartDx - GEO.arcR * Math.sin(th);
    st.blockY = GEO.yFloor + GEO.arcR * (1 - Math.cos(th)) + GEO.blockH/2 * Math.cos(th);
    st.blockV = st.cartV;
    st.height = P.R * (1 - c);
    st.ballX = GEO.xPivot + st.cartDx - 0.26;
    st.ballY = GEO.yPivot - GEO.lpix;
    st.ballV = 0; st.ballOnString = false;
  }
  return st;
}
/* ---- 小车：车体矩形 + 两轮 ---- */
function drawCart(st){
  const x0 = GEO.xTrack0 + st.cartDx;
  const x1 = GEO.xArc0 + st.cartDx + GEO.arcR * 0.10;
  const yb = GEO.bodyY, yt = GEO.yFloor;
  /* 车体（先画车体，再画上表面轨道线） */
  ctx.save();
  ctx.fillStyle = '#eef2f7';
  const a = W2S(x0, yt), b = W2S(x1, yb);
  ctx.fillRect(a[0], a[1], b[0] - a[0], b[1] - a[1]);
  ctx.restore();
  /* 车体轮廓 */
  FIG.wire([[x0, yb], [x1, yb], [x1, yt], [x0, yt], [x0, yb]], {lw: 2.2});
  /* 上表面：水平轨道段（粗糙，画虚线示意）+ 圆弧段 */
  FIG.wire([[x0, yt], [GEO.xArc0 + st.cartDx, yt]], {lw: 2.4});
  /* 轮子 */
  drawWheel(x0 + 0.62, yb - GEO.wheelR);
  drawWheel(x1 - 0.42, yb - GEO.wheelR);
}

function drawWheel(x, y){
  const p = W2S(x, y);
  ctx.save();
  ctx.fillStyle = '#cbd5e1'; ctx.strokeStyle = '#475569'; ctx.lineWidth = 1.8;
  ctx.beginPath(); ctx.arc(p[0], p[1], GEO.wheelR * scale, 0, 7); ctx.fill(); ctx.stroke();
  ctx.beginPath(); ctx.arc(p[0], p[1], GEO.wheelR * scale * 0.30, 0, 7); ctx.fillStyle = '#475569'; ctx.fill();
  ctx.restore();
}

/* ---- 圆弧半径 R 的蓝色虚线标注 ---- */
function drawArcRmark(st){
  const a = 225 * Math.PI / 180;
  const dx = st ? st.cartDx : 0;
  const cx = GEO.xTrack0 + GEO.spix + dx;      /* 圆弧最低点 x = 轨道右端（随小车平移） */
  const x1 = cx + GEO.arcR * Math.cos(a);
  const y1 = GEO.arcCy + GEO.arcR * Math.sin(a);
  const p0 = W2S(cx, GEO.arcCy), p1 = W2S(x1, y1);
  ctx.save();
  ctx.setLineDash([5, 4]); ctx.strokeStyle = '#0ea5e9'; ctx.lineWidth = 1.8;
  ctx.beginPath(); ctx.moveTo(p0[0], p0[1]); ctx.lineTo(p1[0], p1[1]); ctx.stroke();
  ctx.restore();
  /* R 标签贴在虚线朝外一侧（左下），避免物块升到圆弧中部时与 M 标签重叠 */
  /* R 标签：贴虚线外侧再外推，避开物块升到圆弧中段时的 M / u 标注 */
  FIG.text((cx + x1) / 2 - 0.46, (GEO.arcCy + y1) / 2 + 0.34,
           'R', {color: '#0ea5e9', italic: true});
}

/* ---- 文字标注 ---- */
function drawLabels(t, st){
  /* 悬点随小车平移（真实过程：下摆时细线的水平拉力使小车向左反冲）。
     缓动系数：下摆前半段（φ 接近 π/2）细线几乎水平、水平分力小，小车移动很少；
     后半段细线趋于竖直，水平分力减小、小车也趋于停止——故用 (1-cosφ) 缓动。 */
  const xPv = GEO.xPivot + st.cartDx;
  FIG.text(xPv + 0.10, GEO.yPivot + 0.12, 'O', {italic: true});
  /* L：细线中部。偏移必须「垂直于细线」并固定朝左上方外推，
     否则细线摆到接近竖直时，标签会正好压到圆弧半径 R 的蓝色虚线上。 */
  if (st.stage === 'swing' && st.phi > 0.25){
    const mx = (xPv + st.ballX) / 2;
    const my = (GEO.yPivot + st.ballY) / 2;
    /* 细线方向的单位向量（由 O 指向球） */
    const dxu = (st.ballX - xPv), dyu = (st.ballY - GEO.yPivot);
    const len = Math.max(1e-6, Math.sqrt(dxu * dxu + dyu * dyu));
    /* 垂直方向（取指向左上方的一侧），再沿此方向外推 0.22 世界单位 */
    let px = -dyu / len, py = dxu / len;
    if (px > 0){ px = -px; py = -py; }
    FIG.text(mx + px * 0.24, my + py * 0.24, 'L', {italic: true});
  } else {
    FIG.text(xPv - 0.58, GEO.yPivot - GEO.lpix / 2, 'L', {italic: true});
  }
  /* 竖直细线（初始位置的细线，虚线示意） */
  const pa = W2S(xPv, GEO.yPivot), pb = W2S(xPv, GEO.yPivot - GEO.lpix);
  ctx.save(); ctx.setLineDash([4, 4]); ctx.strokeStyle = '#94a3b8'; ctx.lineWidth = 1.2;
  ctx.beginPath(); ctx.moveTo(pa[0], pa[1]); ctx.lineTo(pb[0], pb[1]); ctx.stroke(); ctx.restore();
  /* s：水平轨道中部。物块滑过之后把它留在轨道中点，避免与物块/圆弧标注挤在一起 */
  /* s：轨道中部偏左，压到车体上表面之上一点，避开物块滑行路径与速度矢量 */
  FIG.text(GEO.xTrack0 + GEO.spix * 0.30 + st.cartDx, GEO.yFloor + 0.30, 's', {italic: true});
  /* m 摆球标签、M 物块标签由 FIG 自动画 */

  /* u（物块相对小车的切向速率）标签：箭头本身很短（世界长度 ≈ u*0.070），
     若交给 FIG.vec 自动放在末端 1.12 倍处，会正好压在物块中心的「M」上。
     故改为在这里手动放置：沿「垂直于切线的圆弧外侧」方向外推，
     切线方向 = (−cosθ, sinθ) ⇒ 外法线（远离圆心）= (sinθ, cosθ) 取使其朝上的那一侧。 */
  if (st.stage === 'arc' && st.uRel > 0.10){
    const tx = -Math.cos(st.theta), ty = Math.sin(st.theta);
    let nx = ty, ny = -tx;                 /* 切线逆时针转 90° */
    if (ny < 0){ nx = -nx; ny = -ny; }     /* 取朝上的那一侧（远离车厢上表面） */
    FIG.text(st.blockX + nx * 0.26 + tx * 0.10,
             st.blockY + ny * 0.26 + ty * 0.10, 'u', {italic: true});
  }

  /* 细线本身：挂在小车上（和 O 同步平移），保证球收回时不与细线脱开 */
  if (st.ballOnString){
    FIG.pendulum(xPv, GEO.yPivot, GEO.lpix, -st.phi, GEO.ballR);
  } else {
    FIG.pendulum(xPv, GEO.yPivot, GEO.lpix, 0, GEO.ballR);
  }
}

/* ---- 放大视图 HUD：圆弧上升细节 ----
   ⚠ 必须取「CSS 像素」尺寸，不能取 ctx.canvas.width / height：
   框架 resize() 执行了 ctx.setTransform(devicePixelRatio,0,0,devicePixelRatio,0,0)，
   之后所有绘制坐标按 CSS 像素解释；而 ctx.canvas.width 是设备像素（2× 屏即翻倍）。
   用设备像素定位会把 HUD 画到 (2W − hudW − 10, 2H − hudH − 10)，整块落到画布外
   （表现为「HUD 不见了」）。用 getBoundingClientRect() 取真实 CSS 尺寸。 */
function drawHud(t, st){
  const _r = ctx.canvas.getBoundingClientRect();
  const Wp = (_r && _r.width)  ? _r.width  : ctx.canvas.width;
  const Hp = (_r && _r.height) ? _r.height : ctx.canvas.height;
  if (Wp < 380) return;                       /* 画布过窄时不画，避免遮挡主体 */
  const k = Math.max(0.62, Math.min(1, Wp / 520));   /* 按画布宽度整体缩放 */
  const hudW = 160 * k, hudH = 132 * k;
  const hx = Wp - hudW - 10, hy = Hp - hudH - 10;
  ctx.save();
  ctx.fillStyle = 'rgba(255,255,255,0.94)';
  ctx.strokeStyle = '#cbd5e1'; ctx.lineWidth = 1.2;
  ctx.fillRect(hx, hy, hudW, hudH); ctx.strokeRect(hx, hy, hudW, hudH);
  ctx.fillStyle = '#475569'; ctx.font = 'bold ' + (11 * k).toFixed(1) + 'px sans-serif';
  ctx.fillText('轨迹追踪 (x–θ)', hx + 10 * k, hy + 16 * k);
  /* θ 跟踪条 */
  const th = st.theta || 0;
  const barX = hx + 10 * k, barY = hy + 28 * k, barW = hudW - 20 * k, barH = 11 * k;
  ctx.fillStyle = '#e2e8f0'; ctx.fillRect(barX, barY, barW, barH);
  const frac = Math.max(0, Math.min(1, th / (Math.PI / 2)));
  ctx.fillStyle = '#0ea5e9'; ctx.fillRect(barX, barY, barW * frac, barH);
  ctx.fillStyle = '#0f172a'; ctx.font = (11 * k).toFixed(1) + 'px monospace';
  ctx.fillText('θ = ' + (th * 180 / Math.PI).toFixed(1) + '°', barX, barY + barH + 15 * k);
  /* 上升高度条 */
  const h = st.height || 0;
  const hy2 = barY + barH + 24 * k;
  ctx.fillStyle = '#e2e8f0'; ctx.fillRect(barX, hy2, barW, barH);
  ctx.fillStyle = '#f59e0b';
  ctx.fillRect(barX, hy2, barW * Math.max(0, Math.min(1, h / P.R)), barH);
  ctx.fillStyle = '#0f172a';
  ctx.fillText('h = ' + h.toFixed(3) + ' m', barX, hy2 + barH + 15 * k);
  /* 当前过程 */
  ctx.fillStyle = '#475569'; ctx.font = 'bold ' + (11 * k).toFixed(1) + 'px sans-serif';
  const names = {'swing': '小球下摆', 'hit': '弹性碰撞', 'slide': '水平滑行', 'arc': '圆弧上升', 'lock': '共速一起运动'};
  ctx.fillText('当前：' + (names[st.stage] || ''), barX, hy2 + barH + 33 * k);
  ctx.restore();
}
const BANNERS = %(banners)s;
""" % dict(banners='[' + ','.join('[%.2f,%.2f,"%s"]' % (a, b, c) for a, b, c in TIMELINE) + ']')

# DRAWFRAME_JS：drawSceneBody 的函数体（模板已包 function drawSceneBody(t){ ... }）
DRAWFRAME_JS = """
/* ===== 逐帧绘制：全部走 FIG.* 图元，世界坐标 ===== */
const st = stateAt(t);
clearBg();

/* ---------- 顶部过程横幅（过程数 = 题设过程数）----------
   只在右侧动画画布（id="cv"）上绘制：左栏题图是与动画同源的 __CANVAS_STATIC__
   孪生重绘（drawSceneBody(0)），但题图画布窄得多（约 400px），过程中文横幅
   居中后必然溢出两侧被裁切。题图应保持与试卷原图一致的「静态示意图」外观。 */
if (ctx.canvas.id === 'cv'){
  for (let i = 0; i < BANNERS.length; i++){
    if (t < BANNERS[i][1]){
      /* 自动适配字号：窄窗口下横幅若超过画布宽 92%，按比例缩小，避免左右被裁切 */
      const txt = BANNERS[i][2];
      let fs = 15;
      ctx.font = 'bold ' + fs + 'px sans-serif';
      const need = ctx.measureText(txt).width + 26;
      const cap = ctx.canvas.width * 0.92;
      if (need > cap) fs = Math.max(9, Math.floor(fs * cap / need));
      FIG.processBanner(txt, {size: fs});
      break;
    }
  }
}

/* ---------- 光滑水平地面 ---------- */
FIG.ground(VIEW.xmin + 0.05, VIEW.xmax - 0.05,
           GEO.bodyY - GEO.wheelR - 0.05,
           {hatchLen: 0.50, gap: 0.38});

/* ---------- 小车（车体 + 两轮 + 上表面轨道）---------- */
drawCart(st);

/* ---------- 光滑四分之一圆弧（小车右端上表面）----------
   arcSurface 角度制：x = cx + R cos(a)，y = cy + R sin(a)，度、世界系、逆时针为正
   最低点 = (cx, cy-R) -> a = 270°；顶端 = (cx-R, cy) -> a = 180°
   故区间取 [180, 270] ---------------------------------------------------- */
FIG.arcSurface(GEO.xTrack0 + GEO.spix + st.cartDx, GEO.arcCy, GEO.arcR, 180, 270, {lw: 2.8});
drawArcRmark(st);

/* ---------- 小球 m（摆球）----------
   细线由 drawLabels() 统一绘制（含随小车平移的悬点），这里只画球与标签。 */
if (st.ballOnString){
  FIG.text(st.ballX + 0.13, st.ballY + GEO.ballR + 0.10, 'm', {italic: true});
} else {
  FIG.particle(st.ballX, st.ballY, GEO.ballR);
  FIG.text(st.ballX + 0.13, st.ballY + GEO.ballR + 0.10, 'm', {italic: true});
}

/* ---------- 物块 M（橙色方块）---------- */
FIG.block(st.blockX, st.blockY, GEO.blockW, GEO.blockH, 'M',
          {fill: '#f59e0b', border: '#b45309', labelDy: 0.055, lw: 1.6});

/* ---------- 速度矢量（长度 ∝ 速率，近零淡出）---------- */
const vs = 0.30;
if (st.stage === 'swing' && st.ballV > 0.06){
  /* 切向速度：垂直于细线、指向运动方向（phi 为与竖直方向夹角） */
  FIG.vec(st.ballX, st.ballY,
          Math.cos(st.phi) * st.ballV * 0.050,
          Math.sin(st.phi) * st.ballV * 0.050, 'v', {color: '#dc2626'});
}
if (st.blockV > 0.06){
  FIG.vec(st.blockX, st.blockY, st.blockV * vs * 0.40, 0, "v'", {color: '#dc2626'});
}
if (st.stage === 'arc' && st.uRel > 0.10){
  /* 物块相对小车的切向速度：沿圆弧切线方向（向左上）。
     ⚠ 不用 FIG.vec 的自动标签：它在末端 1.12 倍处放置，而上式矢量的世界长度
     仅有 u*0.070（约 0.02 世界单位 ≈ 2px）——标签会正好压在物块中心的「M」上。
     故这里只画箭头，标签由 drawLabels() 按「垂直于切线、朝圆弧外侧」单独放置。 */
  FIG.vec(st.blockX, st.blockY,
          -Math.cos(st.theta) * st.uRel * 0.070,
          Math.sin(st.theta) * st.uRel * 0.070, '', {color: '#dc2626'});
}
if (st.cartV > 0.06){
  FIG.vec(GEO.xTrack0 + 0.34, GEO.bodyY - 0.26, st.cartV * vs * 0.32, 0, 'V', {color: '#2563eb'});
}

/* ---------- 文字标注（L / s / O / 竖直参考线）---------- */
drawLabels(t, st);

/* ---------- 关键状态高亮：碰撞点 ---------- */
if (st.stage === 'hit'){
  FIG.collisionPoint(GEO.xPivot + st.cartDx, GEO.yFloor + GEO.blockH/2, {label: ''});
}

/* ---------- 放大视图 HUD（圆弧上升细节，填充宽扁画布留白）---------- */
drawHud(t, st);
"""

READOUTS_JS = r"""
/* =========================================================================
   数据面板读数（与 stateAt 共用同一套物理量，保证「动画 = 解析可视化」）
   ========================================================================= */
const st = stateAt(t);
const f2 = function(x){ return x.toFixed(2); };
const f3 = function(x){ return x.toFixed(3); };
const NAMES = { swing: '①小球下摆', hit: '②弹性碰撞', slide: '③水平滑行',
                arc: '④圆弧上升', lock: '⑤共速一起运动' };
const rows = [];

rows.push(['当前过程', NAMES[st.stage] || '', '']);
rows.push(['小球速率 $v$', f2(st.ballV), 'm/s']);

if (st.stage === 'swing'){
  /* 下落高度 = L cos(phi)：自水平位置释放，phi 为细线与竖直方向夹角 */
  rows.push(['摆角 $\\theta$', (st.phi * 180 / Math.PI).toFixed(1), 'deg']);
  rows.push(['下落高度 $h$', f3(P.L * Math.cos(st.phi)), 'm']);
}
rows.push(["物块速率 $v_2'$", f2(st.blockV), 'm/s']);
rows.push(['小车速率 $V$', f2(st.cartV), 'm/s']);

if (st.stage === 'arc' || st.stage === 'lock'){
  rows.push(['相对小车速率 $u$', f2(st.uRel), 'm/s']);
  rows.push(['上升角 $\\theta$', (st.theta * 180 / Math.PI).toFixed(1), 'deg']);
  rows.push(['上升高度 $h$', f3(st.height), 'm']);
}
if (st.stage === 'slide'){
  const xb = (st.blockX - (GEO.xTrack0 + GEO.blockW/2)) / (GEO.spix / P.S);
  rows.push(['摩擦生热 $Q$', f2(P.mu * P.mBlock * P.g * xb), 'J']);
}
rows.push(['动摩擦因数 $\\mu$', f2(P.mu), '']);
rows.push(['$\\mu$ 取值范围', '0.50 ~ 0.80', '左闭右开']);
return rows;
"""

# ---- 写入模板 ----
tpl = io_open(TPL).read() if False else open(TPL, encoding='utf-8').read()

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


import re as _re

out = tpl
out = _re.sub(r'const PROBLEM = \{[\s\S]*?\n\};', prob_js.rstrip('\n'), out, count=1)
out = _re.sub(r'const STEPS = \[[\s\S]*?\n\];', steps_js.rstrip('\n'), out, count=1)
out = _re.sub(r'const VIEW = \{[^\n]*\n\s*const SIM\s*=\s*\{[^\n]*\n', view_js, out, count=1)

# 四个 JS 占位
# 注意：__GLOBALS__ 位于顶层作用域（函数声明之外），辅助函数必须放这里；
#       __SETUP__ 在 function setup(){...} 内部，只放语句，不能放函数声明。
out = _repl(out, '__GLOBALS__', GLOBALS_JS.strip() + '\n\n' + HELPERS_JS.strip())
out = _repl(out, '__SETUP__',   SETUP_JS.strip())
out = _repl(out, '__DRAWFRAME__', DRAWFRAME_JS.strip())
out = _repl(out, '__READOUTS__', READOUTS_JS.strip())

# ------------------------------------------------------------
# 版面微调（不改模板框架逻辑，仅追加一段样式覆盖）：
# 解析栏公式区在 1280~1600 宽屏下最容易横向溢出，这里把
# .step 的内边距收紧、公式容器左右留白收窄，并把 .katex/MathJax
# 容器的最大宽度放开，为长公式多争取约 30px 宽度。
# ------------------------------------------------------------
CSS_TUNE = (
    '<style id="tune-width">\n'
    '.col-analysis{flex:2.05 1 380px}\n'
    '.step{padding:8px 9px 8px 11px}\n'
    '.step .tex{padding:2px 0 6px}\n'
    '.step .tex mjx-container[display="true"]{max-width:100%}\n'
    '.step .tex mjx-container[display="true"] svg{max-width:100%;height:auto}\n'
    '</style>\n'
)
if '</head>' in out:
    out = out.replace('</head>', CSS_TUNE + '</head>', 1)
else:
    out = CSS_TUNE + out

open(OUT, 'w', encoding='utf-8').write(out)

probes = ['2024·安徽·14', '__CANVAS_STATIC__', 'mech-momentum-collision-1d',
          'processBanner', 'FIG.arcSurface', 'SW_TBL', 'ARC_TBL', 'uRelAt',
          'function stateAt', 'const BANNERS', '1}{2}', '4}{5}',
          '__GLOBALS__', '__SETUP__', '__DRAWFRAME__', '__READOUTS__']
print('=== 探针自检 ===')
for _p in probes:
    print(('FOUND   ' if _p in out else 'MISSING ') + _p)
import os as _os
print('\noutput: %s  (%d bytes)' % (OUT, _os.path.getsize(OUT)))
print('V1=%.4f V2=%.4f MU_MIN=%.4f MU_MAX=%.4f THETA_STOP=%.3fdeg VIN=%.4f'
      % (V1, V2, MU_MIN, MU_MAX, THETA_STOP * 180 / 3.141592653589793, VIN_DEMO))
print('Tswing=%.4f Tslide=%.4f Tarc=%.4f' % (SWING_TTOTAL, SLIDE_TTOTAL, ARC_TTOTAL))
