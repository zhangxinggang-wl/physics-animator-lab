# -*- coding: utf-8 -*-
"""
生成《自行车气门芯的位移》教学动画 HTML。
题源：自行车匀速直线运动（纯滚动），气门芯由最高点到最低点的位移大小。
答案 D：Δs = sqrt(π²R² + 4r²)
做法：复制 assets/template.html，填充 6 个区域（PROBLEM / STEPS / VIEW+SIM / setup / drawSceneBody / readouts）。
"""
import io, os, sys

BASE = r"C:\Users\19368\Desktop\physics-animator-lab"
TPL = os.path.join(BASE, "assets", "template.html")
OUT = os.path.join(BASE, "2026-09-13_自行车气门芯位移_教学动画.html")

# ---------------------------------------------------------------- ① PROBLEM
PROBLEM = r'''const PROBLEM = {
  title: "",   // 原题无标题（仅有题号 5.），故不另拟标题
  /* 题干：与原题逐字一致（含题号与已填答案标记） */
  given: "5.如图，自行车在水平地面上做匀速直线运动。车轮外边缘半径为 $R$，气门芯距轮心的距离为 $r$，自行车行驶过程中轮胎不打滑，初始时刻气门芯在最高点，不考虑车轮的形变。气门芯从初始时刻到第一次运动至最低点过程位移的大小为( D )",

  /* 题图：方式② Canvas 2D 像素级重绘 + 与右栏动画孪生锁定
     （左栏题图 = drawSceneBody(0)，即右栏动画第 0 帧，几何零偏差） */
  images: [
    { src: "__CANVAS_STATIC__", caption: "题图：自行车与气门芯（前轮）", pos: "bottom" }
  ],

  /* 选择题：A/B/C/D 四项完整录入（模板在题图下方渲染） */
  options: [
    "A. $\\sqrt{4R^{2}+\\pi^{2}R^{2}}$",
    "B. $\\sqrt{4R^{2}+\\pi^{2}r^{2}}$",
    "C. $\\sqrt{4r^{2}+\\pi^{2}r^{2}}$",
    "D. $\\sqrt{4r^{2}+\\pi^{2}R^{2}}$"
  ],

  asks: [],

  knowledgePoints: [
    { id: "princ-relative-motion" },
    { id: "princ-vector-basics" },
    { id: "mech-circular-horizontal" }
  ]
};

'''

# ---------------------------------------------------------------- ② STEPS
STEPS = r'''const STEPS = [
  {
    title: "运动的分解：平动 + 绕轮心转动",
    tex: "\\Delta \\vec{s} = \\Delta \\vec{s}_{1} + \\Delta \\vec{s}_{2}",
    note: "气门芯的运动可分解为两部分：随轮心以速度 $v$ 做匀速平动，同时绕轮心做匀速转动（角速度 $\\omega = \\frac{v}{R}$，由轮胎不打滑这一纯滚动条件决定）。由运动的合成，气门芯对地的位移等于这两个分位移的矢量和，即 $\\Delta \\vec{s} = \\Delta \\vec{s}_{1} + \\Delta \\vec{s}_{2}$。",
    basis: "运动的合成与分解；纯滚动（不打滑）条件",
    t0: 0, t1: 0.49
  },
  {
    title: "轮心平动引起的分位移",
    tex: "s_{1} = R\\theta = \\pi R",
    note: "纯滚动时，轮心前进的距离等于轮缘接触点滚过的弧长：$s_{1} = R\\theta$。气门芯由最高点转到最低点，车轮恰好转过半个圆周，$\\theta = \\pi$，故 $s_{1} = \\pi R \\approx 0.94$ m（取 $R = 0.30$ m）。该分位移只由车轮外半径 $R$ 决定，与气门芯的径向位置 $r$ 无关。",
    basis: "纯滚动：轮心位移 = 轮缘滚过的弧长",
    t0: 0.49, t1: 0.98
  },
  {
    title: "气门芯相对轮心的分位移",
    tex: "s_{2} = 2r",
    note: "在随轮心一起平动的参考系中，气门芯绕轮心做半径 $r$ 的匀速圆周运动。由最高点到最低点转过的圆心角为 $\\pi$，气门芯相对轮心的位置由竖直向上 $r$ 变为竖直向下 $r$，故相对位移方向竖直向下、大小 $s_{2} = 2r \\approx 0.36$ m（取 $r = 0.18$ m）。",
    basis: "匀速圆周运动；转过 $\\pi$ 时弦长等于直径",
    t0: 0.98, t1: 1.47
  },
  {
    title: "两个互相垂直的分位移合成",
    tex: "\\Delta s = \\sqrt{s_{1}^{2} + s_{2}^{2}} = \\sqrt{(\\pi R)^{2} + (2r)^{2}}",
    note: "平动分位移 $s_{1}$ 沿水平方向，气门芯相对轮心的分位移 $s_{2}$ 沿竖直方向，二者互相垂直，用勾股定理合成即得合位移的大小 $\\Delta s = \\sqrt{s_{1}^{2} + s_{2}^{2}}$。所以位移的大小与过程中的弧长无关，只与始末位置有关。",
    basis: "矢量的正交分解与合成（勾股定理）",
    t0: 1.47, t1: 1.96
  },
  {
    title: "气门芯从最高点到最低点的位移大小",
    tex: "\\Delta s = \\sqrt{\\pi^{2}R^{2} + 4r^{2}}",
    note: "把 $s_{1} = \\pi R$、$s_{2} = 2r$ 代入得 $\\Delta s = \\sqrt{\\pi^{2}R^{2} + 4r^{2}}$，对应选项 D。取 $R = 0.30$ m、$r = 0.18$ m 检验：$\\Delta s = \\sqrt{(\\pi \\times 0.30)^{2} + 0.36^{2}} \\approx 1.01$ m，与右栏数据面板一致。A 项把相对轮心的位移误写成 $2R$；B 项两个半径都用错；C 项把平动位移误写成 $\\pi r$——平动位移由车轮半径 $R$ 决定，与气门芯位置 $r$ 无关。",
    basis: "位移的合成；纯滚动条件",
    t0: 1.96, t1: 2.44
  }
];

'''

# ---------------------------------------------------------------- ③ VIEW / SIM
VIEWSIM = r'''const VIEW = { xmin: -0.22, xmax: 2.62, ymin: -0.44, ymax: 1.247 };
const SIM  = { duration: 2.44 };
/* 说明：世界纵横比取 2.84 : 1.687，扣除四周 36px 内边距后与画布像素纵横比一致，
   使 x、y 方向比例尺相等（车轮画出来是真正的圆，且恰好落在地面上）。 */

'''

# ---------------------------------------------------------------- ④ GLOBALS
GLOBALS = r'''/* ===== 本题物理常量与几何参数 =====
   世界坐标：x 向右、y 向上，地面取 y = 0，长度单位 m。
   取 R = 0.30 m、r = 0.18 m、v = 0.40 m/s（纯滚动 ⇒ ω = v/R = 4/3 rad/s）。 */
const R_WHEEL = 0.30;   // 车轮外边缘半径 R
const R_VALVE = 0.18;   // 气门芯距轮心的距离 r
const V_BIKE  = 0.40;   // 自行车匀速前进的速度 v
const WHEELBASE = 1.05; // 前后车轮轴距（仅作图尺度）
const HUB0_X  = 1.30;   // t=0 时前轮（装气门芯）轮心的水平位置
const OMEGA   = V_BIKE / R_WHEEL;      // 车轮角速度 ω = v/R（纯滚动条件）
const T_HALF  = Math.PI / OMEGA;       // 气门芯由最高点转到最低点的时间（转半圈）
const S1_END  = Math.PI * R_WHEEL;     // 轮心平动位移 s₁ = Rθ = πR
const S2_END  = 2 * R_VALVE;           // 气门芯相对轮心的位移 s₂ = 2r
const DS_END  = Math.sqrt(S1_END * S1_END + S2_END * S2_END);   // 合位移 Δs
/* 「起点」引线标注的文字锚点（世界坐标）。放在画面最左侧的**永久空白带**：
   自行车车架最左可达 x = 0（后轮心最小值 − 车架半宽 0.30），气门芯轨迹左端也 > 0.6，
   故 x = 0.05 一线全程无任何几何体经过。取值经 _build/probe_start_label.py 暴力搜索验证：
   离车架最小 76 px、离轮圈最小 19 px、离绿环 268 px（引线正是为跨越这段距离而设）。 */
const START_TAG_X = 0.02;
const START_TAG_Y = 0.62;

/* 气门芯的运动状态：画面（drawSceneBody）与数据面板（readouts）共用同一函数，
   从机制上保证「画面一套数、面板另一套数」不可能发生。
   t ≥ T_HALF 时定格于最低点（末段为定格展示）。 */
function stateAt(t){
  const tt = Math.min(t, T_HALF);
  const th = OMEGA * tt;                        // 车轮转角 θ(t) = ωt
  const hx = HUB0_X + V_BIKE * tt;              // 轮心：匀速平动
  const x0 = HUB0_X, y0 = R_WHEEL + R_VALVE;    // 初始位置（最高点）
  const vx = hx + R_VALVE * Math.sin(th);       // 气门芯：摆线（短幅旋轮线）
  const vy = R_WHEEL + R_VALVE * Math.cos(th);
  const relx = R_VALVE * Math.sin(th);          // 相对轮心的位移分量
  const rely = R_VALVE * Math.cos(th) - R_VALVE;
  return {
    tt: tt, th: th, hx: hx, x0: x0, y0: y0, vx: vx, vy: vy,
    relx: relx, rely: rely,
    s1: V_BIKE * tt,                            // 平动分位移 = Rθ
    s2: Math.hypot(relx, rely),                 // 相对分位移大小 = 2r·sin(θ/2)
    ds: Math.hypot(vx - x0, vy - y0),           // 合位移大小
    frozen: t >= T_HALF
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
function tag(x, y, str, color, size, align){
  const p = W2S(x, y);
  ctx.save();
  ctx.fillStyle = color;
  ctx.font = 'bold ' + (size || 12) + 'px "Microsoft YaHei","PingFang SC",sans-serif';
  ctx.textAlign = align || 'left';
  ctx.fillText(str, p[0], p[1]);
  ctx.restore();
}
function dotW(x, y, r, fill, stroke, lw){
  const p = W2S(x, y);
  ctx.save();
  ctx.beginPath(); ctx.arc(p[0], p[1], r * scale, 0, 7);
  if (fill){ ctx.fillStyle = fill; ctx.fill(); }
  if (stroke){ ctx.strokeStyle = stroke; ctx.lineWidth = lw || 2; ctx.stroke(); }
  ctx.restore();
}
/* 车轮：轮圈 + 随车轮转动的轮辐 + 轮毂（+ 气门芯） */
function drawWheel(cx, cy, rot, withValve, st){
  const R = R_WHEEL, c = W2S(cx, cy), rp = R * scale;
  ctx.save();
  ctx.strokeStyle = '#1f2937'; ctx.lineWidth = 2.4;
  ctx.beginPath(); ctx.arc(c[0], c[1], rp, 0, 7); ctx.stroke();
  /* 轮辐（随车轮一起转动，前进时顺时针） */
  ctx.strokeStyle = '#9aa7b4'; ctx.lineWidth = 1.1;
  for (let k = 0; k < 6; k++){
    const a = rot + k * Math.PI / 3;
    const a1 = W2S(cx + 0.045 * Math.cos(a), cy + 0.045 * Math.sin(a));
    const a2 = W2S(cx + (R - 0.02) * Math.cos(a), cy + (R - 0.02) * Math.sin(a));
    ctx.beginPath(); ctx.moveTo(a1[0], a1[1]); ctx.lineTo(a2[0], a2[1]); ctx.stroke();
  }
  dotW(cx, cy, 0.028, '#1f2937', null);
  if (withValve){
    const th = st.th;
    strokePolyValveHold(cx, cy, th);
    dotW(cx + R_VALVE * Math.sin(th), cy + R_VALVE * Math.cos(th), 0.032, '#dc2626', '#7f1d1d', 1.4);
  }
  ctx.restore();
}
/* 轮心 → 气门芯的半径连线（单独抽出，避免与外层 ctx.save/restore 冲突） */
function strokePolyValveHold(cx, cy, th){
  poly2([[cx, cy], [cx + R_VALVE * Math.sin(th), cy + R_VALVE * Math.cos(th)]], '#b91c1c', 1.6);
}
/* 自行车（简化城市车：两轮 + 车架 + 鞍座 + 车把 + 前进方向速度矢量） */
function drawBike(st){
  const hx = st.hx, rx = st.hx - WHEELBASE, R = R_WHEEL;
  drawWheel(rx, R, -st.th, false, st);
  drawWheel(hx, R, -st.th, true, st);
  const BB = [hx - 0.60, R - 0.03];   // 中轴
  const ST = [hx - 0.80, 0.72];       // 座管顶
  const HT = [hx - 0.04, 0.80];       // 头管顶（车把）
  const frame = [
    [[rx, R], [BB[0], BB[1]]],
    [[rx, R], [ST[0], ST[1]]],
    [[BB[0], BB[1]], [ST[0], ST[1]]],
    [[BB[0], BB[1]], [HT[0], HT[1]]],
    [[ST[0], ST[1]], [HT[0], HT[1]]],
    [[HT[0], HT[1]], [hx, R]]
  ];
  frame.forEach(function(sg){ poly2(sg, '#1f2937', 2.2); });
  poly2([[ST[0] - 0.11, ST[1] + 0.02], [ST[0] + 0.07, ST[1] + 0.02]], '#0f172a', 4.5);  // 鞍座
  poly2([[HT[0] - 0.03, HT[1]], [HT[0] + 0.16, HT[1] + 0.03]], '#0f172a', 3.5);          // 车把
  poly2([[HT[0] + 0.16, HT[1] + 0.03], [HT[0] + 0.19, HT[1] - 0.05]], '#0f172a', 3.5);
  dotW(BB[0], BB[1], 0.055, '#fff', '#1f2937', 2);                                      // 中轴齿盘
  /* 气门芯标注（引线 + 文字），与原题图一致；
     气门芯转到下半圈后隐去文字标注，避免与位移矢量标注重叠（红点仍标出气门芯） */
  const vxr = hx + R_VALVE * Math.sin(st.th), vyr = R + R_VALVE * Math.cos(st.th);
  if (Math.cos(st.th) > 0.05){
    poly2([[vxr, vyr], [vxr + 0.16, vyr + 0.13]], '#dc2626', 1.2);
    tag(vxr + 0.17, vyr + 0.16, '气门芯', '#dc2626', 12);
  }
  /* 前进方向速度矢量（匀速率，长度恒定；置于后轮上方空白处，不遮挡车架与解题标注） */
  FIG.vec(rx - 0.35, 0.70, 0.40, 0, 'v', { color: '#0f766e', lw: 3, head: 10 });
}
/* 位移可视化：轨迹 + 起点/终点 + 分位移 s₁、s₂ + 合位移 Δs */
function drawDisplacement(st){
  /* 气门芯轨迹（摆线，灰色虚线） */
  const N = 90, traj = [];
  for (let i = 0; i <= N; i++){
    const s = st.tt * i / N;
    traj.push([HUB0_X + V_BIKE * s + R_VALVE * Math.sin(OMEGA * s),
               R_WHEEL + R_VALVE * Math.cos(OMEGA * s)]);
  }
  if (traj.length > 1) poly2(traj, '#8d99a6', 1.8, [5, 4]);

  /* 终点（最低点）标记：蓝环 + 地面下方文字标注 */
  const fx = HUB0_X + S1_END, fy = R_WHEEL - R_VALVE;
  dotW(fx, fy, 0.032, '#fff', '#2563eb', 2);
  tag(fx, -0.26, '终点（最低点）', '#2563eb', 12, 'center');

  /* 起点（最高点）标记：绿环 + **引线标注**（本题最棘手的一处标注，见下）
     ⚠ 核心矛盾：绿环固定在世界的初始位置 (x0, y0) ≈ (1.30, 0.48)，而**自行车整体
       向右平移**（后轮心 x 从 0.30 扫到 1.24，车架最左可达 x = 0）——所以任何靠近
       绿环的固定世界坐标，迟早都会被「驶过该处的车架/轮圈」扫到：
         · 放绿环右上方       → 与座管/上管斜线叠字（t 小时）；
         · 放绿环正左方 x0−0.30 → θ≈130° 时后轮的座管/后叉斜线扫过来叠字；
         · 放绿环正上方 y0+0.20 → 座管顶 ST = (hx−0.80, 0.72) 扫过世界 y≈0.72 的水平带，
                                  在 θ = 0°/30°/120°/150° 实测最小间距仅 1~2 px。
     用 _build/probe_start_label.py 对整个画布做过暴力搜索，结论是：
         ★ **绿环 75 px 邻域内不存在「全程离车架/轮圈 ≥14 px」的位置**，需要 ≥268 px 才干净。
     故改用**引线标注**：文字锚点放到全程绝对空白的左侧区域（世界 x ≤ 0.05，
       自行车任何时刻都到不了——车架最左 x = 0，且该点在气门芯轨迹左侧），
       再画一条细虚引线连回绿环，读者视线自然跟随。
     ⚠ 锚点 (0.05, 0.60) 经暴力搜索验证：离车架最小 76 px、离轮圈最小 19 px、离绿环 268 px。
       引线用点线（[2,3]）而非实线，避免看起来像「尺寸线」；颜色取浅绿降低存在感。 */
  dotW(st.x0, st.y0, 0.032, '#fff', '#059669', 2);
  poly2([[START_TAG_X + 0.055, START_TAG_Y + 0.02], [st.x0 - 0.02, st.y0 + 0.055]],
        '#6ee7b7', 1.1, [2, 3]);
  tag(START_TAG_X, START_TAG_Y, '起点（最高点）', '#059669', 12);

  /* 车轮转角的参考线与角度弧（从竖直向上量起，顺时针为正） */
  const degNow = st.th * 180 / Math.PI;
  if (degNow > 1.5){
    poly2([[st.hx, R_WHEEL], [st.hx, R_WHEEL + R_VALVE + 0.06]], '#dc2626', 1.1, [4, 3]);
    FIG.angleArc(st.hx, R_WHEEL, 0.20, 90, 90 - degNow, 'θ(t)', { color: '#dc2626' });
  }

  /* 分位移矢量：s₁（水平，轮心平动）、s₂（气门芯相对轮心）；长度正比于分量大小 */
  if (st.s1 * scale > 10)
    FIG.vec(st.x0, st.y0, st.s1, 0, '', { color: '#2563eb', lw: 2.4, head: 9 });
  if (st.s2 * scale > 10)
    FIG.vec(st.x0 + st.s1, st.y0, st.relx, st.rely, '', { color: '#059669', lw: 2.4, head: 9 });
  /* 合位移矢量 Δs（红）——
     ⚠ 不交给 FIG.vec 自动放标签：它在矢量末端 1.12 倍处放置，而本题 Δs 是
       「起点(左上) → 终点(右下)」的右上斜向长矢量，1.12 倍处**恰好落在红色 θ(t)
       角度弧上**（弧画在轮心右侧，半径 0.20），实测末态完全叠字。
       故这里只画箭头（label 传空串），标签改由本函数末尾手动放置。 */
  if (st.ds * scale > 12)
    FIG.vec(st.x0, st.y0, st.vx - st.x0, st.vy - st.y0, '', { color: '#dc2626', lw: 3.2, head: 11 });

  /* 分位移标签（数值见右下方数据面板，此处只标符号，避免画面拥挤） */
  if (st.s1 * scale > 26)
    tag(st.x0 + st.s1 * 0.5, st.y0 + 0.10, 's₁', '#2563eb', 13, 'center');
  /* ⚠ s₂ 标签（本题最难的标注，实测重做 9 次；结论写在下面，请勿再改回旧方案）
     为什么难：绿矢量极短（|s₂| = 2r·sin(θ/2) ≤ 0.36 m，屏幕最长仅 80 px），
       而它整段泡在**车轮内部**——四周被轮圈、辐条、轮心、θ(t) 弧、蓝色 s₁ 线、
       红色 Δs 线、座管围死。用 _build/probe_s2_label.py / probe_s2_rule.py
       逐角度暴力搜索过，三条结论：
         ★ 矢长 < 29 px（θ < 44°）时画布上**不存在**「离障碍≥11px 且离矢量≤26px」
           的位置——即小角度下无处可标；
         ★ 「中点 + 屏幕向下偏移」方案在 θ = 102°~136° 时，所需偏移仅 0.02 世界单位，
           标签会直接压在绿矢量自身上（离自身 2~3 px）；增大偏移又把标签推进轮圈。
           任何常数偏移、任何 A+B·sinθ 规则均无法覆盖全部角度；
         ★ 唯一全程干净的区域是**地面线以下**（screen y ≈ 336），但离绿矢量 49~117 px，
           引线过长，看起来像一条无关的标注线。
     故最终方案（在「可读关联」与「不压线」之间取的折中）：
       **门限抬到 29 px（θ ≥ 44° 才显示）+ 标签贴在绿矢量尖端、沿矢向外推 0.06 世界单位。**
       - 门限：θ < 44° 时矢量只有十几像素、与箭头三角头基本重合，标了也读不出对应关系，
         不标反而更干净（数据面板始终给出 s₂ 数值，信息不丢失）。
       - 外推 0.06 ≈ 13 px：实测各角度与障碍间距 ≥13 px、与矢量端 13.3 px（= 字高一半，
         视觉上紧贴但不相交），是「贴得最近且不压线」的临界值。
     排查过的错误放法（逐条留档，避免后人重走弯路）：
       ✗ 绿矢量中点（不加偏移）    —— 直接压在箭头三角头上；
       ✗ 屏幕右法线外推 0.26       —— **θ=0°/15°/28°/135° 与障碍间距 0 px**（实测被轮圈、
                                      座管完全盖住，是本次抓到的真实缺陷）；
       ✗ 右法线外推、偏移递减       —— 低角度仍无解（矢长本身不足，非偏移量问题）；
       ✗ 中点 + 屏幕向下 0.09       —— θ=70°~140° 区间间距 <11 px（压轮圈）；
       ✗ 中点 + 屏幕向下随 θ 增大   —— θ=102°~136° 时压绿矢量自身（间距 2~3 px）；
       ✗ 起点侧楔形带              —— 带宽随 θ 变化（45° 仅 11px < 字高 13px）；
       ✗ 固定屏幕点 + 长引线        —— 引线 49~117 px，视觉上像无关标注。 */
  if (st.s2 * scale > 29){
    const L2 = Math.hypot(st.relx, st.rely) || 1;
    const ux = st.relx / L2, uy = st.rely / L2;
    tag(st.x0 + st.s1 + st.relx + ux * 0.06,
        st.y0 + st.rely + uy * 0.06, 's₂', '#059669', 13);
  }
  /* 合位移标签 Δs：手动画（理由见上方 FIG.vec 调用处注释）。
     定位规则（本题共试了 7 种方案，逐条记录以免后人重走弯路）：
       ✗ FIG.vec 自动标签（末端 1.12 倍） —— 恰好落在红色 θ(t) 角度弧上，实测完全叠字；
       ✗ 末端 + 屏幕上方（朝上）法线 0.22 —— 距 θ(t) 标签最近仅 2 px（θ≈120°）；
       ✗ 加上「最小离轮心半径 0.55」     —— 小角度时把标签顶到画布上沿、压住车架；
       ✗ 末端 + 上方法线 0.12             —— 小角度时与 θ(t) 标签仅 2~6 px；
       ✗ 矢量方向延长 1.08 倍             —— 小角度时 Δs 与 s₁ 近乎平行，压在蓝色 s₁ 线上；
       ✗ 方向延长 + 法线微调              —— θ(t) 间距仍只有 5~8 px；
       ✗ 把 θ(t) 标签固定化（改画在其他位置）—— 仍与 Δs 标签争同一块空间；
       ✓ **末端 + 屏幕「下方」法线 0.42，再加世界 y 下限 0.16**
         （偏移取 0.42 而非 0.22：因为 s₂ 标签改为贴在绿矢量尖端后，两者在
           θ = 100°~150° 会同时落在该区域——实测 0.22 时两标签仅相距 21~26 px
           （占位各约 26×13 px，肉眼已糊成一团），加大到 0.42 后间距 ≥35.6 px。实测各时刻最小间距：蓝线 ≥48、θ(t) ≥73、s₁ 标签 ≥70、
       「气门芯」文字 ≥89、地面 ≥34 px；与红色 Δs 线本身在末段贴近（2~4 px）属正常——
       那是标签所标注的矢量本身，文字绘制在矢量之后，可读性不受影响。
     ⚠ 法线要按**屏幕坐标系**判断（屏幕 y 向下、与世界 y 相反）：
       本方案取「屏幕朝下」的一侧 ⇒ 世界法线为 (+uy, +ux) 的对应方向（见代码）。
     ⚠ 世界 y 下限 0.16：地面线在世界 y=0，其下方还有「终点（最低点）」文字（y=−0.26），
       故标签最低只能到 y=0.16（约离地面线 34 px），避免压到地面线与该文字。 */
  if (st.ds * scale > 12){
    const dx = st.vx - st.x0, dy = st.vy - st.y0;
    const sdx = dx, sdy = -dy;                              // 转屏幕方向（y 取反）
    const LD = Math.hypot(sdx, sdy) || 1;
    const ux = sdx / LD, uy = sdy / LD;                     // 屏幕单位矢量
    let nx = -uy, ny = ux;                                  // 屏幕右法线
    if (ny < 0){ nx = -nx; ny = -ny; }                      // 取屏幕朝「下」的一侧
    const wnx = nx, wny = -ny;                              // 换回世界坐标
    let lx = st.x0 + dx + wnx * 0.42;
    let ly = st.y0 + dy + wny * 0.42;
    if (ly < 0.16) ly = 0.16;                               // 世界 y 下限（避地面线与终点文字）
    /* 右侧边界保护：末态 Δs 末端世界 x ≈ 2.24，加偏移后可能逼近 VIEW.xmax = 2.62，
       故按字宽（约 30px）换算留边，防止 "Δs" 被画布右边缘裁切。 */
    const xHi = VIEW.xmax - 30 / scale;
    if (lx > xHi) lx = xHi;
    tag(lx, ly, 'Δs', '#dc2626', 13);
  }
}
/* 画布右上角：θ(t) 实时角度显示器（度 + 弧度）与时间（位于过程横幅下方一行） */
function drawAngleHUD(st){
  const deg = (st.th * 180 / Math.PI).toFixed(1);
  const rad = st.th.toFixed(3);
  ctx.save();
  const l1 = 'θ(t) = ' + deg + '° = ' + rad + ' rad';
  const l2 = 't = ' + st.tt.toFixed(2) + ' s（R=' + R_WHEEL + ' m, r=' + R_VALVE + ' m）';
  ctx.font = 'bold 12px "Microsoft YaHei",sans-serif';
  const w1 = ctx.measureText(l1).width;
  ctx.font = '11px "Microsoft YaHei",sans-serif';
  const w2 = ctx.measureText(l2).width;
  const bw = Math.max(w1, w2) + 18, bh = 40;
  const bx = W - PAD - bw + 8, by = 40;
  ctx.fillStyle = 'rgba(15,23,42,0.88)';
  ctx.fillRect(bx, by, bw, bh);
  ctx.fillStyle = '#fff'; ctx.textAlign = 'left';
  ctx.font = 'bold 12px "Microsoft YaHei",sans-serif'; ctx.fillText(l1, bx + 9, by + 16);
  ctx.font = '11px "Microsoft YaHei",sans-serif';      ctx.fillText(l2, bx + 9, by + 32);
  ctx.restore();
}
/* 画布底部：颜色图例 */
function drawMiniLegend(){
  ctx.save();
  ctx.font = '11px "Microsoft YaHei",sans-serif';
  ctx.fillStyle = '#dc2626'; ctx.fillText('红：合位移 Δs', 10, H - 26);
  ctx.fillStyle = '#2563eb'; ctx.fillText('蓝：平动位移 s₁', 112, H - 26);
  ctx.fillStyle = '#059669'; ctx.fillText('绿：相对轮心位移 s₂', 220, H - 26);
  ctx.fillStyle = '#64748b'; ctx.fillText('灰虚线：气门芯轨迹（摆线）　绿环=起点　蓝环=终点', 10, H - 11);
  ctx.restore();
}

'''

SETUP = r'''  /* 本题的运动学量全部可解析给出（stateAt 即为解析解），
     无需数值积分或轨迹预计算。模拟时长 = 转半圈时间 + 0.08 s 定格。
     T_HALF ≈ 2.356 s，SIM.duration = 2.44 s（末段 0.084 s 为最低点定格展示）。 */

  /* 窗口尺寸变化时，框架的 resize() 会重置动画画布尺寸（画布内容随之清空）并只补画题图，
     动画画布要等下一次 render() 才有内容。此处补挂一个监听（在框架监听之后执行），
     使改变窗口大小后动画画面立即重绘，不会出现空白画布。 */
  window.addEventListener("resize", function(){ render(); });
'''

DRAWFRAME = r'''  const st = stateAt(t);

  /* 地面（粗横线 + 斜线阴影） */
  FIG.ground(VIEW.xmin + 0.04, VIEW.xmax - 0.04, 0, { gap: 0.16, hatchLen: 0.7, color: '#334155' });

  /* 自行车（前轮上带气门芯） */
  drawBike(st);

  /* 位移标注、过程横幅、角度显示器、图例：t>0 才画，
     使第 0 帧（＝左栏题图）保持与原题图一致，不含解题辅助元素 */
  if (t > 0.002){
    drawDisplacement(st);
    /* 过程横幅（本题为单一过程：匀速直线运动，气门芯由最高点转到最低点） */
    FIG.processBanner(st.frozen
      ? '气门芯到达最低点 · 位移合成完成'
      : '匀速直线运动 · 由最高点到最低点', { size: 14 });
    /* 右上角 θ(t) 实时角度显示器 */
    drawAngleHUD(st);
    /* 底部图例 */
    drawMiniLegend();
  }
'''

READOUTS = r'''  const st = stateAt(t);
  const degNow = st.th * 180 / Math.PI;
  const dirNow = Math.atan2(Math.abs(st.vy - st.y0), Math.abs(st.vx - st.x0)) * 180 / Math.PI;
  return [
    ["时间 $t$", t.toFixed(2), "s"],
    ["车轮转角 $\\theta(t)$", degNow.toFixed(1), "°"],
    ["轮心平动位移 $s_{1}$", st.s1.toFixed(3), "m"],
    ["相对轮心位移 $s_{2}$", st.s2.toFixed(3), "m"],
    ["合位移 $\\Delta s$", st.ds.toFixed(3), "m"],
    ["位移方向（俯角）", dirNow.toFixed(1), "°"]
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

    # ① PROBLEM（替换 const PROBLEM = { ... }; 之前的内容）
    s = replace_span(s, "const PROBLEM = {", "/* 选项由 PROBLEM.options 提供", PROBLEM)
    # ② STEPS
    s = replace_span(s, "const STEPS = [", "\n\n/* ===", STEPS)
    # ③ VIEW / SIM
    old_vs = "const VIEW = { xmin: -1, xmax: 11, ymin: -1, ymax: 7 };\nconst SIM  = { duration: 4 };"
    if old_vs not in s:
        raise SystemExit("VIEW/SIM 锚点未找到")
    s = s.replace(old_vs, VIEWSIM.rstrip("\n"), 1)
    # ④ 全局常量与绘图辅助 + ⑤ 逐帧绘制 + ⑥ 实时数据
    s = s.replace("/*__GLOBALS__*/", GLOBALS.rstrip("\n"), 1)
    s = s.replace("/*__SETUP__*/", SETUP.rstrip("\n"), 1)
    s = s.replace("/*__DRAWFRAME__*/", DRAWFRAME.rstrip("\n"), 1)
    s = s.replace("/*__READOUTS__*/", READOUTS.rstrip("\n"), 1)
    # 标题
    s = s.replace("<title>高中物理试题 · 分步解析与动画演示</title>",
                  "<title>自行车气门芯的位移 · 分步解析与动画演示</title>", 1)

    for mk in ("__GLOBALS__", "__SETUP__", "__DRAWFRAME__", "__READOUTS__"):
        if mk in s:
            raise SystemExit("标记未替换: " + mk)

    with io.open(OUT, "w", encoding="utf-8") as f:
        f.write(s)
    print("OK -> " + OUT)
    print("size = %.2f MB" % (os.path.getsize(OUT) / 1048576.0))


if __name__ == "__main__":
    main()
