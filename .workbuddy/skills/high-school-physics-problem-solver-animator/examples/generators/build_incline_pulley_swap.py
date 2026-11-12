# -*- coding: utf-8 -*-
"""生成：光滑斜面-定滑轮-两物块互换位置多选题解析动画 HTML。
题图 = 动画第 0 帧（Canvas 孪生锁定）；选项 A/B/C/D 完整录入；解析禁微积分。"""
import io, re, os

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = os.path.join(WS, "assets", "template.html")
OUT = os.path.join(WS, "2026-09-09_光滑斜面滑轮互换位置多选题.html")

src = io.open(TPL, encoding="utf-8").read()

# ---------------- ① PROBLEM ----------------
problem = r'''const PROBLEM = {
  title: "",
  given: "【练习 7】（多选）如图 19 所示，有一倾角为 $\alpha$ 且固定在地面上的光滑斜面。将质量分别为 $M$ 和 $m$ 的物块（$m<M$），通过轻绳跨过光滑定滑轮连接。当两物块按图甲方式连接，绳子平行于斜面，释放 $m$ 时，$M$ 能一起沿斜面加速上滑。若互换两物块位置，按图乙放置，然后释放 $M$，则下列说法正确的是（　　）",

  images: [
    { src: "__CANVAS_STATIC__", caption: "题图：图甲（$M$ 在斜面、$m$ 悬挂）与图乙（互换位置）装置示意图（按原图几何孪生重绘，与动画同坐标）", pos: "bottom" }
  ],

  asks: [],

  // 选择题选项（A/B/C/D 四项缺一不可）
  options: [
    "A. $m$ 一定沿斜面加速上滑",
    "B. $m$ 一定沿斜面加速下滑",
    "C. 若 $m$ 沿斜面加速上滑，此时绳子拉力一定大于图甲中的绳子拉力",
    "D. 若 $m$ 沿斜面加速下滑，此时绳子拉力一定等于图甲中的绳子拉力"
  ],

  knowledgePoints: [
    { id: "mech-newton-second", ch: "力学", sub: "牛顿定律", name: "牛顿第二定律",
      formula: "$\\sum \\vec{F} = m \\vec{a}$",
      conditions: "惯性系；质量恒定；低速宏观物体。",
      pitfalls: ["加速度方向与合力方向相同，不一定与速度方向相同",
                 "沿绳连接的物体加速度大小相等（绳不可伸长）"],
      extensions: ["连接体问题：整体法求加速度，隔离法求内力"],
      difficulty: "基础" },
    { id: "mech-newton-connected", ch: "力学", sub: "牛顿定律", name: "连接体问题",
      formula: "$a = \\dfrac{\\sum F_{\\text{外}}}{m_{\\text{总}}}$；隔离求绳张力 $T$",
      conditions: "绳/杆轻质不可伸长，连接体加速度大小相同。",
      pitfalls: ["绳只能提供拉力，方向沿绳指向绳收缩方向",
                 "斜面上要正确分解重力：沿斜面 $mg\\sin\\alpha$，垂直斜面 $mg\\cos\\alpha$"],
      extensions: ["滑轮两侧质量互换时，注意张力表达式的对称性"],
      difficulty: "高考" },
    { id: "mech-force-vector-decomp", ch: "力学", sub: "相互作用", name: "力的正交分解",
      formula: "$F_x = F\\cos\\theta,\\; F_y = F\\sin\\theta$",
      conditions: "平面共点力；选定相互垂直的坐标轴。",
      pitfalls: ["斜面问题通常选沿斜面与垂直斜面方向建轴",
                 "分力的正负号由坐标方向决定"],
      extensions: ["三力平衡可用三角形法则"],
      difficulty: "基础" },
    { id: "mech-incline-motion", ch: "力学", sub: "牛顿定律", name: "斜面上物体的加速度",
      formula: "沿斜面 $a = g\\sin\\alpha$（光滑下滑）；含绳张力时由牛顿第二定律列方程",
      conditions: "斜面光滑或已知动摩擦因数；物体沿斜面运动。",
      pitfalls: ["不要漏掉绳张力沿斜面的分量",
                 "悬挂物块的加速度方向与沿斜面物块的加速度方向由同一根绳约束"],
      extensions: ["斜面-滑轮系统是连接体问题的典型模型"],
      difficulty: "高考" }
  ]
};'''

src = re.sub(r"const PROBLEM = \{[\s\S]*?\n\};", lambda m: problem, src, count=1)

# ---------------- ② STEPS ----------------
steps = r'''const STEPS = [
  { q: 1, title: "分析图甲：由 $M$ 沿斜面加速上滑确定倾角条件",
    tex: "\\begin{aligned} T - Mg\\sin\\alpha &= Ma_{\\text{甲}} \\\\ mg - T &= ma_{\\text{甲}} \\\\ a_{\\text{甲}} &= \\frac{mg - Mg\\sin\\alpha}{M + m} > 0 \\end{aligned}",
    note: "图甲中 $M$ 沿斜面向上加速，$m$ 竖直向下加速，二者加速度大小相同。由 $a_{\\text{甲}}>0$ 得 $mg > Mg\\sin\\alpha$，即 $\\sin\\alpha < \\dfrac{m}{M}$。",
    basis: "牛顿第二定律 + 连接体约束", t0: 0, t1: 2.0 },

  { q: 1, title: "分析图乙：判断 $m$ 的运动方向（选项 A、B）",
    tex: "\\begin{aligned} Mg - T &= Ma_{\\text{乙}} \\\\ T - mg\\sin\\alpha &= ma_{\\text{乙}} \\\\ a_{\\text{乙}} &= \\frac{Mg - mg\\sin\\alpha}{M + m} \\end{aligned}",
    note: "互换位置后，$M$ 竖直向下加速，$m$ 沿斜面向上加速。因 $M>m$ 且 $\\sin\\alpha<1$，总有 $Mg > mg\\sin\\alpha$，故 $a_{\\text{乙}}>0$ 恒成立。因此 $m$ 一定沿斜面加速上滑，选项 A 正确、B 错误。",
    basis: "牛顿第二定律 + 不等式判断", t0: 2.0, t1: 4.0 },

  { q: 1, title: "比较图甲与图乙的绳子拉力（选项 C、D）",
    tex: "\\begin{aligned} T_{\\text{甲}} &= \\frac{Mm\\,g\\,(1 + \\sin\\alpha)}{M + m} \\\\ T_{\\text{乙}} &= \\frac{Mm\\,g\\,(1 + \\sin\\alpha)}{M + m} \\\\ T_{\\text{甲}} &= T_{\\text{乙}} \\end{aligned}",
    note: "分别由图甲、图乙的方程消去加速度，可得两绳张力表达式完全相同。因此图乙中若 $m$ 上滑，拉力等于（不是大于）图甲中的拉力，选项 C 错误。选项 D 的前提是“$m$ 加速下滑”，这在图乙中不可能发生，因此不是对实际情景的正确描述。",
    basis: "方程消元与代数比较", t0: 4.0, t1: 5.5 },

  { q: 1, title: "结论：正确选项",
    tex: "\\boxed{\\text{A}}",
    note: "综上，$m$ 一定沿斜面加速上滑；两图中绳子拉力大小相等。正确选项为 A。",
    basis: "综合判断", t0: 5.5, t1: 6.5 }
];'''

src = re.sub(r"const STEPS = \[[\s\S]*?\n\];", lambda m: steps, src, count=1)

# ---------------- ③ VIEW / SIM ----------------
src = re.sub(r"const VIEW = \{[^\n]*\};\nconst SIM[^\n]*\};",
             lambda m: "const VIEW = { xmin: -0.5, xmax: 9.5, ymin: -0.5, ymax: 4.0 };\nconst SIM  = { duration: 6.5 };",
             src, count=1)

# ---------------- ④ GLOBALS ----------------
globals_code = r'''/* 几何与物理参数（长度以米为单位，力以 N 为单位） */
const G     = 10.0;                     // 重力加速度，m/s²
const ALPHA = 30 * Math.PI / 180;       // 斜面倾角（示例取 30°，结论对任意满足条件的 α 成立）
const SIN_A = Math.sin(ALPHA);
const COS_A = Math.cos(ALPHA);
const M     = 4.0;                      // 大物块质量，kg
const m     = 3.0;                      // 小物块质量，kg（m < M）

/* 真实物理量（由解析推导） */
const aJia = (m - M * SIN_A) * G / (M + m);   // 图甲加速度
const aYi  = (M - m * SIN_A) * G / (M + m);   // 图乙加速度
const T    = M * m * G * (1 + SIN_A) / (M + m); // 绳张力（两图相等）

/* 动画示意位移系数：真实加速度导致位移过大，动画按同一比例缩小仅作可视化 */
const K_ANIM = 0.12;
const aJiaAnim = aJia * K_ANIM;
const aYiAnim  = aYi  * K_ANIM;

/* 图甲几何（左侧） */
const JA_X0 = 0.3,  JA_Y0 = 0.5;        // 斜面左下角
const JA_BASE = 2.4;                    // 斜面底边长
const JA_H    = JA_BASE * Math.tan(ALPHA);
const JA_X1   = JA_X0 + JA_BASE;        // 斜面右下角
const JA_Y1   = JA_Y0 + JA_H;           // 斜面顶端 y
const JA_OX   = JA_X1 + 0.3;            // 滑轮 x
const JA_OY   = JA_Y1 + 0.26;           // 滑轮 y
const JA_S0   = 0.5;                    // M 初始距底端距离
let   JA_Mx   = JA_X0 + JA_S0 * COS_A;  // M 初始 x
let   JA_My   = JA_Y0 + JA_S0 * SIN_A;  // M 初始 y
const JA_mY0  = JA_OY - 0.75;           // 悬挂 m 初始中心 y
const BLOCK_R = 0.18;                   // 物块半宽（世界单位）

/* 图乙几何（右侧） */
const YI_X0 = 5.3,  YI_Y0 = 0.5;
const YI_BASE = 2.4;
const YI_H    = YI_BASE * Math.tan(ALPHA);
const YI_X1   = YI_X0 + YI_BASE;
const YI_Y1   = YI_Y0 + YI_H;
const YI_OX   = YI_X1 + 0.3;
const YI_OY   = YI_Y1 + 0.26;
const YI_S0   = 0.5;
let   YI_mx   = YI_X0 + YI_S0 * COS_A;
let   YI_my   = YI_Y0 + YI_S0 * SIN_A;
const YI_MY0  = YI_OY - 0.75;           // 悬挂 M 初始中心 y

function clamp(v, lo, hi){ return Math.max(lo, Math.min(hi, v)); }

function stateAt(t){
  /* 阶段 1：图甲运动（0 ~ 2.5 s），图乙静止 */
  const t1 = 2.5;
  const t2 = 5.0;
  let sJia = 0, sYi = 0, phase = 0;
  if (t <= t1) {
    phase = 0;
    sJia = 0.5 * aJiaAnim * t * t;
  } else if (t <= t2) {
    phase = 1;
    sJia = 0.5 * aJiaAnim * t1 * t1;
    const tau = t - t1;
    sYi = 0.5 * aYiAnim * tau * tau;
  } else {
    phase = 2;
    sJia = 0.5 * aJiaAnim * t1 * t1;
    sYi = 0.5 * aYiAnim * (t2 - t1) * (t2 - t1);
  }
  return { phase: phase, sJia: sJia, sYi: sYi,
           aJia: aJia, aYi: aYi, T: T,
           /* 图甲实时位置 */
           Mx: JA_Mx + sJia * COS_A,
           My: JA_My + sJia * SIN_A,
           mhy: JA_mY0 - sJia,
           /* 图乙实时位置 */
           mx: YI_mx + sYi * COS_A,
           my: YI_my + sYi * SIN_A,
           Myh: YI_MY0 - sYi };
}'''
src = src.replace("/*__GLOBALS__*/", globals_code, 1)

# ---------------- ⑤ SETUP ----------------
src = src.replace("/*__SETUP__*/", "// 几何参数已在全局作用域定义，无需额外初始化", 1)

# ---------------- ⑥ DRAWFRAME ----------------
draw_code = r'''  const st = stateAt(t);

  clearBg();

  /* ---------- 公共样式 ---------- */
  const colorGround = '#1f2937';
  const colorSlope  = '#e2e8f0';
  const colorRope   = '#475569';
  const colorM      = '#2563eb';
  const colorm      = '#dc2626';

  function drawSubScene(left, x0, y0, base, h, ox, oy, s0, blockOnSlope, hangingMass, sMove,
                         labelSlope, labelHanging, showForces){
    const x1 = x0 + base;
    const y1 = y0 + h;

    /* 地面 */
    FIG.ground(x0 - 0.2, x1 + 1.0, y0, { color: colorGround });

    /* 斜面楔形 */
    FIG.incline(x0, x1, y1, y1, y0, { fill: colorSlope, hatch: true, color: colorGround });

    /* 角度标注 α */
    FIG.angleArc(x0, y0, 0.55, 0, 30, "α", { color: '#7c3aed' });

    /* 滑轮 */
    FIG.pulley(ox, oy, 0.12, {});
    FIG.text(ox + 0.05, oy + 0.18, "O", { size: 14 });

    /* 斜面上物块当前位置 */
    const bx = x0 + (s0 + sMove) * COS_A;
    const by = y0 + (s0 + sMove) * SIN_A;
    FIG.block(bx, by, 0.34, 0.22, labelSlope, { fill: '#f8fafc', border: colorGround, lw: 1.8 });

    /* 悬挂物块当前位置 */
    const hy = oy - 0.75 - sMove;
    FIG.block(ox, hy, 0.26, 0.26, labelHanging, { fill: '#f8fafc', border: colorGround, lw: 1.8 });

    /* 绳：斜面物块 → 滑轮 → 悬挂物块 */
    drawLine(bx, by, ox, oy, colorRope, 1.8);
    drawLine(ox, oy, ox, hy + BLOCK_R, colorRope, 1.8);

    /* 受力矢量（仅在非 0 阶段显示，避免初始帧太乱） */
    if (showForces){
      const kf = 0.018; // 力矢量比例尺（世界长度 / N）
      // 斜面上物块：沿斜面向上 T，沿斜面向下 mg sinα 或 Mg sinα
      const Tlen = T * kf;
      const Gslope = (labelSlope === 'M' ? M : m) * G * SIN_A * kf;
      FIG.vec(bx, by, Tlen * COS_A, Tlen * SIN_A, "T", { color: '#2563eb', lw: 2.4, head: 8 });
      FIG.vec(bx, by, -Gslope * COS_A, -Gslope * SIN_A, (labelSlope==='M'?'Mg\\sinα':'mg\\sinα'), { color: '#059669', lw: 2.2, head: 8 });
      // 悬挂物块：向上 T，向下 Mg 或 mg
      const Ghang = (labelHanging === 'M' ? M : m) * G * kf;
      FIG.vec(ox, hy, 0, Tlen, "T", { color: '#2563eb', lw: 2.4, head: 8 });
      FIG.vec(ox, hy, 0, -Ghang, (labelHanging==='M'?'Mg':'mg'), { color: '#059669', lw: 2.2, head: 8 });
    }

    /* 运动方向箭头 */
    if (sMove > 0.02){
      const ka = 0.25; // 速度/加速度方向箭头长度
      // 斜面上物块沿斜面向上
      FIG.vec(bx + 0.25, by + 0.35, ka * COS_A, ka * SIN_A, "a", { color: '#d97706', lw: 2.2, head: 7 });
      // 悬挂物块向下
      FIG.vec(ox + 0.25, hy, 0, -ka, "a", { color: '#d97706', lw: 2.2, head: 7 });
    }
  }

  /* ---------- 图甲（左侧） ---------- */
  const showJia = (st.phase >= 0);
  drawSubScene(true, JA_X0, JA_Y0, JA_BASE, JA_H, JA_OX, JA_OY, JA_S0,
               'M', 'm', st.sJia, showJia && st.sJia > 0.05);

  /* 图甲标签 */
  FIG.text(JA_X0 + 1.2, -0.25, "甲", { size: 16, align: 'center' });

  /* ---------- 图乙（右侧） ---------- */
  const showYi = (st.phase >= 1);
  drawSubScene(false, YI_X0, YI_Y0, YI_BASE, YI_H, YI_OX, YI_OY, YI_S0,
               'm', 'M', st.sYi, showYi && st.sYi > 0.05);

  /* 图乙标签 */
  FIG.text(YI_X0 + 1.2, -0.25, "乙", { size: 16, align: 'center' });

  /* ---------- 阶段横幅 ---------- */
  let banner = "";
  if (st.phase === 0) banner = "图甲：M 上滑，m 下落";
  else if (st.phase === 1) banner = "图乙：m 上滑，M 下落";
  else banner = "T甲 = T乙";
  if (banner) FIG.processBanner(banner, { size: 14 });'''
src = src.replace("/*__DRAWFRAME__*/", draw_code, 1)

# ---------------- ⑦ READOUTS ----------------
readouts_code = r'''  const st = stateAt(t);
  return [
    ["图甲加速度 $a_{\\text{甲}}$", st.aJia.toFixed(2), "m/s²"],
    ["图乙加速度 $a_{\\text{乙}}$", st.aYi.toFixed(2), "m/s²"],
    ["绳张力 $T$", st.T.toFixed(2), "N"],
    ["当前阶段", st.phase === 0 ? "图甲运动" : (st.phase === 1 ? "图乙运动" : "张力对比"), ""]
  ];'''
src = src.replace("/*__READOUTS__*/", readouts_code, 1)

# ---------------- 输出 ----------------
io.open(OUT, "w", encoding="utf-8").write(src)
print("Generated:", OUT)
print("Size:", len(src), "bytes")
