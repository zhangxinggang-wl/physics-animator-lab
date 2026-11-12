# -*- coding: utf-8 -*-
"""生成：细棒-铰链-定滑轮 缓慢转动选择题（F 与 F_N 变化判断）解析动画 HTML。
题图 = 动画第 0 帧（Canvas 孪生锁定，θ0=53° 与原图位形一致）；选项 A/B/C/D 横向渲染；解析禁微积分。"""
import io, re, os

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = os.path.join(WS, "assets", "template.html")
OUT = os.path.join(WS, "2026-09-09_细棒铰链定滑轮缓慢转动.html")

src = io.open(TPL, encoding="utf-8").read()

# ---------------- ① PROBLEM ----------------
problem = r"""const PROBLEM = {
  title: "",
  given: "7．如图所示，质量分布均匀的细棒中心为 $O$ 点，$O_1$ 为光滑铰链，$O_2$ 为光滑定滑轮，且 $O_2$ 在 $O_1$ 正上方，细绳跨过 $O_2$ 与 $O$ 连接，水平外力 $F$ 作用于细绳的一端．用 $F_N$ 表示铰链对细棒的作用力，现在水平外力 $F$ 作用下，$\\theta$ 从 $\\frac{\\pi}{2}$ 缓慢减小到 $0$ 的过程中，下列说法正确的是（　　）",

  images: [
    { src: "__CANVAS_STATIC__", caption: "题图：细棒—光滑铰链—定滑轮装置（按原图几何孪生重绘，与动画同坐标）", pos: "bottom" }
  ],

  // 选择题选项（A/B/C/D 四项缺一不可，横向排列渲染）
  options: [
    "A. $F$ 逐渐变小，$F_N$ 大小不变",
    "B. $F$ 逐渐变小，$F_N$ 逐渐变大",
    "C. $F$ 先变小再变大，$F_N$ 逐渐变小",
    "D. $F$ 先变小再变大，$F_N$ 逐渐变大"
  ],

  asks: [],

  knowledgePoints: [
    { id: "mech-torque-equilibrium", ch: "力学", sub: "刚体平衡", name: "有固定转动轴物体的力矩平衡",
      formula: "$M = FL$（力矩 = 力 × 力臂）；平衡条件 $\\sum M = 0$",
      conditions: "物体绕固定转动轴转动；「缓慢」过程中每一时刻均可视为平衡态",
      pitfalls: ["力臂是转轴到力的作用线的垂直距离，不是转轴到作用点的距离",
                 "重力力臂随角度变化：杆与竖直方向成 $\\theta$ 时，中点 $O$ 对轴 $O_1$ 的力臂为 $L\\sin\\theta$",
                 "求绳拉力的力臂用「等面积法」：$\\triangle O_1OO_2$ 面积 $= \\frac{1}{2}Lh\\sin\\theta = \\frac{1}{2}d\\cdot d_{\\perp}$，得 $d_{\\perp} = \\frac{Lh\\sin\\theta}{d}$"],
      extensions: ["本题也可全程用相似三角形法：力三角形与几何三角形 $\\triangle O_1OO_2$ 相似",
                   "求出 $T = \\frac{mgd}{h}$ 后，两种方法结果一致，可互为验算"],
      difficulty: "高考" },
    { id: "mech-force-vector-decomp" },
    { id: "mech-equilibrium-three-force", ch: "力学", sub: "共点力平衡", name: "三力汇交与相似三角形法",
      formula: "物体受三个不平行动力而平衡时，三力作用线必汇交于一点；力三角形与几何三角形相似，对应边成比例",
      conditions: "研究对象受三个力（或不共线多力可先合成）且处于平衡态",
      pitfalls: ["本题重力 $mg$ 与绳拉力 $T$ 都过 $O$ 点，故铰链作用力 $F_N$ 的作用线也必过 $O$——即 $F_N$ 沿杆方向",
                 "相似三角形对应边要按「力 / 几何边」一一平行对应：$mg$ 对 $O_1O_2 = h$，$T$ 对 $OO_2 = d$，$F_N$ 对 $O_1O = L$"],
      extensions: ["由相似比一步得 $T = \\frac{mgd}{h}$、$F_N = \\frac{mgL}{h}$，避免复杂的正交分解运算"],
      difficulty: "高考" },
    { id: "mech-pulley-rope", ch: "力学", sub: "绳与滑轮", name: "定滑轮与绳的张力",
      formula: "光滑定滑轮只改变力的方向、不改变力的大小：同一根轻绳上张力处处相等，水平端读数 $F = T$",
      conditions: "轻绳、光滑定滑轮（不计滑轮质量与摩擦）",
      pitfalls: ["跨过定滑轮两侧绳的张力大小相等，但方向分别沿各自绳段",
                 "绳对杆的拉力方向沿绳指向滑轮 $O_2$，不要误认为沿杆或沿竖直方向"],
      extensions: ["动滑轮才省力：理想情况下 $F = T/2$"],
      difficulty: "基础" },
    { id: "mech-quasistatic", ch: "力学", sub: "准静态过程", name: "缓慢过程（准静态平衡）",
      formula: "「缓慢」$\\Rightarrow$ 每一时刻动能近似为零 $\\Rightarrow$ 每一时刻均满足平衡条件",
      conditions: "过程进行得足够慢，可忽略动能变化与惯性效应",
      pitfalls: ["「缓慢」不等于「匀速」：转动的快慢可以不均匀，但每个状态仍是平衡态",
                 "不能用牛顿第二定律列动力学方程，应逐位置用静力平衡分析"],
      extensions: ["求变力做功时「缓慢」常配合动能定理使用"],
      difficulty: "基础" }
  ]
};"""

src = re.sub(r"const PROBLEM = \{[\s\S]*?\n\};", lambda m: problem, src, count=1)

# ---------------- ② STEPS ----------------
steps = r"""const STEPS = [
  { q: 1, title: "缓慢转动：每一时刻均为准静态平衡",
    tex: "\\sum \\vec F = 0,\\qquad \\sum M = 0",
    note: "「缓慢」意味着细棒转动的动能可忽略，任一时刻都可看作平衡态：细棒既满足合力为零，也满足对转轴 $O_1$ 的合力矩为零。因此可对每一个 $\\theta$ 位置直接用静力平衡求 $F$ 与 $F_N$ 随 $\\theta$ 的变化。",
    basis: "准静态过程的平衡条件", t0: 0, t1: 1.6 },

  { q: 1, title: "对 O₁ 列力矩平衡，求绳的拉力",
    tex: "mgL\\sin\\theta = T\\cdot\\frac{Lh\\sin\\theta}{d}\\;\\Rightarrow\\; T = \\frac{mgd}{h}",
    note: "设杆长 $2L$（$O_1$ 到中点 $O$ 为 $L$）、$O_1O_2 = h$、$O$ 到 $O_2$ 的距离为 $d$。重力作用在中点 $O$，对 $O_1$ 的力臂为 $L\\sin\\theta$；拉力 $T$ 沿 $O \\to O_2$ 方向，用等面积法求其力臂：$\\triangle O_1OO_2$ 的面积 $= \\frac{1}{2}Lh\\sin\\theta = \\frac{1}{2}d\\cdot d_{\\perp}$，故 $d_{\\perp} = \\frac{Lh\\sin\\theta}{d}$。代入力矩平衡即得 $T = \\frac{mgd}{h}$。",
    basis: "有固定转动轴物体的力矩平衡条件（等面积法求力臂）", t0: 1.6, t1: 3.2 },

  { q: 1, title: "余弦定理判断 F 的变化：单调减小",
    tex: "d^2 = L^2 + h^2 - 2Lh\\cos\\theta\\;\\Rightarrow\\; \\theta\\downarrow \\Rightarrow \\cos\\theta\\uparrow \\Rightarrow d\\downarrow \\Rightarrow F = \\frac{mgd}{h}\\downarrow",
    note: "在 $\\triangle O_1OO_2$ 中，$O_1O = L$、$O_1O_2 = h$、夹角 $\\theta$，由余弦定理 $d^2 = L^2 + h^2 - 2Lh\\cos\\theta$。$\\theta$ 从 $\\frac{\\pi}{2}$ 减小到 $0$ 的过程中，$\\cos\\theta$ 从 $0$ 单调增大到 $1$，故 $d$ 单调减小；再由定滑轮不改变力的大小（$F = T$），得水平拉力 $F = \\frac{mgd}{h}$ 逐渐变小。",
    basis: "余弦定理 + 定滑轮特点", t0: 3.2, t1: 4.8 },

  { q: 1, title: "三力汇交 + 相似三角形求 F_N",
    tex: "F_N = \\frac{L}{h}\\,mg = \\frac{mgL}{h}",
    note: "细棒受三个力：重力 $mg$（作用在 $O$，竖直向下）、绳的拉力 $T$（沿 $O \\to O_2$ 方向）、铰链作用力 $F_N$。前两个力都通过 $O$ 点，由三力汇交定理，$F_N$ 的作用线也必通过 $O$——即 $F_N$ 沿杆方向。于是力三角形与几何三角形 $\\triangle O_1OO_2$ 相似：$mg$ 对应 $O_1O_2 = h$、$T$ 对应 $OO_2 = d$、$F_N$ 对应 $O_1O = L$，由相似比 $\\frac{mg}{h} = \\frac{T}{d} = \\frac{F_N}{L}$ 得 $T = \\frac{mgd}{h}$（与力矩法一致，互为验证）、$F_N = \\frac{mgL}{h}$。",
    basis: "三力汇交定理 + 相似三角形法", t0: 4.8, t1: 6.4 },

  { q: 1, title: "F_N 大小恒定，选 A",
    tex: "F\\ \\text{逐渐变小}，\\qquad F_N = \\frac{mgL}{h}\\ \\text{大小不变}",
    note: "$F_N = \\frac{mgL}{h}$ 与 $\\theta$ 无关——大小不变（方向始终沿杆、随杆缓慢转动）。综上：$F$ 逐渐变小、$F_N$ 大小不变，选 A。B 错在 $F_N$ 并非变大；C、D 错在 $d$ 单调减小，$F$ 没有先减后增的转折。动画从题图位置 $\\theta = 53^{\\circ}$ 开始演示到 $0$；在题设全过程 $\\frac{\\pi}{2} \\to 0$ 中 $F$ 同样单调减小。",
    basis: "矢量合成 + 结论闭环", t0: 6.4, t1: 8.0 }
];"""

src = re.sub(r"const STEPS = \[[\s\S]*?\n\];", lambda m: steps, src, count=1)

# ---------------- ③ VIEW / SIM ----------------
src = re.sub(r"const VIEW = \{[^\n]*\};\nconst SIM[^\n]*\};",
             lambda m: "const VIEW = { xmin: -2.7, xmax: 2.7, ymin: -0.6, ymax: 2.96 };\nconst SIM  = { duration: 8 };",
             src, count=1)

# ---------------- ④ GLOBALS ----------------
globals_code = r"""/* 几何与物理参数（长度以 L 为单位，力以 mg 为单位）；
   θ0 = 53° 为题图初始位形（与原题图一致，特殊角吸附），动画从题图位置缓慢减小到 0 */
const RODL = 1.0;  // O₁ 到 O（杆半长）
const RODH = 1.7;  // O₁O₂ 高度（题图比例）
const TH0 = 53 * Math.PI / 180;
const KF = 0.42;   // 力矢量比例尺（世界长度 / mg）
function stateAt(t){
  const p  = Math.min(Math.max(t / SIM.duration, 0), 1);
  const th = TH0 * (1 - p);                                   // θ(t)：θ0 → 0 缓慢减小
  const d  = Math.sqrt(RODL*RODL + RODH*RODH - 2*RODL*RODH*Math.cos(th));  // OO₂（余弦定理）
  const Fo = d / RODH;                                        // F/mg = d/h
  const FN = RODL / RODH;                                     // F_N/mg = L/h（恒定）
  return { p: p, th: th, d: d, Fo: Fo, FN: FN };
}"""
src = src.replace("/*__GLOBALS__*/", globals_code, 1)

# ---------------- ⑤ SETUP ----------------
src = src.replace("/*__SETUP__*/",
                  "// 状态全部由全局 stateAt(t) 实时给出，无需预计算", 1)

# ---------------- ⑥ DRAWFRAME ----------------
draw_code = r"""  const st = stateAt(t);
  const th = st.th, deg = th * 180 / Math.PI;
  const ox = -RODL * Math.sin(th), oy = RODL * Math.cos(th);        // O（杆中点，绳的连接点）
  const ex = -2*RODL * Math.sin(th), ey = 2*RODL * Math.cos(th);    // 杆上端

  /* 地面（O₁ 两侧，斜线阴影） */
  FIG.ground(-2.4, 1.7, 0, {});

  /* O₁—O₂ 竖直虚线 */
  ctx.save(); ctx.setLineDash([6, 5]);
  drawLine(0, 0, 0, RODH, "#94a3b8", 1.4);
  ctx.restore();

  /* 天花板（定滑轮支架，斜线向上） */
  drawLine(-0.55, RODH + 0.32, 0.55, RODH + 0.32, "#1f2937", 2.2);
  for (let x = -0.48; x <= 0.5; x += 0.12){ drawLine(x, RODH + 0.32, x - 0.08, RODH + 0.44, "#94a3b8", 1); }

  /* 定滑轮 O₂ + 绳段 O→O₂ + 水平绳段与拉力 F（长度 ∝ F） */
  FIG.pulley(0, RODH, 0.11, {});
  drawLine(ox, oy, 0, RODH, "#475569", 1.6);
  drawLine(0.11, RODH, 0.26, RODH, "#475569", 1.6);
  FIG.vec(0.26, RODH, st.Fo * KF, 0, "F", { color: "#dc2626", lw: 2.6, head: 9 });

  /* 细杆（粗实线）+ 中点 O + 铰链 O₁ */
  FIG.rod(0, 0, ex, ey, { color: "#1f2937", lw: 4, joints: false });
  drawPoint(ox, oy, "#1f2937", 3.5);
  FIG.pivot(0, 0, {});

  /* θ 角弧（杆与竖直方向之间，随动画变化） */
  FIG.angleArc(0, 0, 0.5, 90, 90 + deg, "\u03b8", { color: "#0f172a" });

  /* 标签（Unicode 下标，锚定与原题图一致） */
  FIG.text(0.15, -0.26, "O\u2081", { size: 15 });
  FIG.text(0.2, RODH - 0.05, "O\u2082", { size: 15 });
  FIG.text(ox - 0.16 * Math.cos(th) - 0.04, oy - 0.16 * Math.sin(th), "O", { size: 15, align: "right" });

  if (t > 0.001){
    /* 实时角度显示器（° 与 rad 同显） */
    ctx.fillStyle = "#0f172a"; ctx.font = "12.5px sans-serif"; ctx.textAlign = "right";
    ctx.fillText("\u03b8(t) = " + deg.toFixed(1) + "\u00b0 = " + th.toFixed(3) + " rad", W - 10, 18);
    ctx.textAlign = "left";
    /* 受力分析可视化：重力 mg（过 O）、铰链作用力 FN（沿杆，大小恒定） */
    FIG.vec(ox, oy, 0, -KF, "mg", { color: "#2563eb", lw: 2.4, head: 9 });
    FIG.vec(-0.12 * Math.cos(th), -0.12 * Math.sin(th),
            -st.FN * KF * Math.sin(th), st.FN * KF * Math.cos(th),
            "FN", { color: "#059669", lw: 2.6, head: 9 });
  }"""
src = src.replace("/*__DRAWFRAME__*/", draw_code, 1)

# ---------------- ⑦ READOUTS ----------------
readouts_code = r"""  const st = stateAt(t);
  const deg = st.th * 180 / Math.PI;
  return [
    ["$\\theta(t)$", deg.toFixed(1), "\u00b0"],
    ["$\\theta(t)$", st.th.toFixed(3), "rad"],
    ["$d = OO_2$", st.d.toFixed(3), "$L$"],
    ["$F/mg$", st.Fo.toFixed(3), ""],
    ["$F_N/mg$", st.FN.toFixed(3), ""],
    ["$F$ 变化", st.p > 0.02 ? "逐渐变小" : "\u2014", ""],
    ["$F_N$ 变化", "大小不变", ""]
  ];"""
src = src.replace("/*__READOUTS__*/", readouts_code, 1)

# ---------------- ⑧ 选项横向 2×2 覆写（左栏窄，flex nowrap 会竖排，强制网格横排） ----------------
opt_override = (
    "<style id=\"opt-horizontal-override\">\n"
    "  /* 选择题四选项：受左栏宽度限制，改为 2×2 横排网格（A B / C D），文本可换行 */\n"
    "  .options{display:grid;grid-template-columns:1fr 1fr;column-gap:20px;row-gap:3px;margin:8px 0 6px}\n"
    "  .opt{font-size:13px;line-height:1.7;white-space:normal;min-width:0}\n"
    "</style>\n"
)
src = src.replace("</head>", opt_override + "</head>", 1)

io.open(OUT, "w", encoding="utf-8").write(src)
print("written:", OUT, os.path.getsize(OUT), "bytes")