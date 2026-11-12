# -*- coding: utf-8 -*-
"""Build the self-contained HTML for 2026 黑吉辽蒙卷 物理 第10题 (wire frame in reverse fields)."""
import base64, re

TPL = r"C:\Users\19368\Desktop\physics-animator-lab\assets\template.html"
IMG = r"C:\Users\Administrator\.workbuddy\clipboard-images\clipboard-2026-09-07T00-04-25-748Z-792b879f.png"
OUT = r"C:\Users\19368\Desktop\physics-animator-lab\2026黑吉辽蒙卷物理第10题_线框反向磁场.html"

with open(TPL, "r", encoding="utf-8") as f:
    html = f.read()

with open(IMG, "rb") as f:
    b64 = base64.b64encode(f.read()).decode("ascii")
IMGURI = "data:image/png;base64," + b64

# NOTE: in this file we write \\n so that JSON -> file contains \n (a JS newline escape),
# and \\frac so that JSON -> file contains \frac (a single backslash, correct LaTeX).

PROBLEM = (
'const PROBLEM = {\n'
'  title: "2026 黑吉辽蒙卷 物理 第10题",\n'
'  given: "如图，光滑绝缘水平面上，\\\\(x=0\\\\) 两侧区域Ⅰ、Ⅱ分别存在竖直方向的匀强磁场，宽度均为 \\\\(L\\\\)，磁感应强度方向相反、大小分别为 \\\\(B\\\\)、\\\\(2B\\\\)；\\\\(x=-3L\\\\) 与 \\\\(x=3L\\\\) 处有固定挡板。同种材料制成、粗细均匀的正方形导体线框 \\\\(MNPQ\\\\)，边长为 \\\\(L\\\\)、质量为 \\\\(m\\\\)、总电阻为 \\\\(R\\\\)，以初速度 \\\\(v_0=\\\\frac{2026B^2L^3}{mR}\\\\) 从左侧进入磁场，沿 \\\\(x\\\\) 轴运动。线框平面始终与磁场方向垂直，\\\\(MN\\\\) 边始终与磁场边界平行，线框与挡板的碰撞均为弹性碰撞。\\\\n\\\\n选项：\\\\nA. \\\\(MN\\\\) 首次进入磁场时线框的加速度 \\\\(a=\\\\frac{2026B^4L^5}{m^2R^2}\\\\)\\\\nB. \\\\(MN\\\\) 每次经过 \\\\(x=1.5L\\\\) 时，电势差 \\\\(|U_{NM}|:|U_{PQ}|=1:1\\\\)\\\\nC. \\\\(MN\\\\) 与右侧挡板首次碰撞后瞬间线框的速度大小 \\\\(v=\\\\frac{2012B^2L^3}{mR}\\\\)\\\\nD. 线框停止处，穿过线框的磁通量为 \\\\(0\\\\)",\n'
'  images: [\n'
'    { src: "' + IMGURI + '", caption: "题图：线框在反向双磁场中运动", pos: "bottom" }\n'
'  ],\n'
'  asks: [],\n'
'  knowledgePoints: [\n'
'    { id: "em-ampere-force" },\n'
'    { id: "em-faraday-lenz" },\n'
'    { id: "mech-momentum-impulse-theorem" },\n'
'    { id: "mech-momentum-collision-1d" }\n'
'  ]\n'
'};'
)

STEPS = (
'const STEPS = [\n'
'  { q: 1, title: "1. 题设模型与初态", tex: "v_0=\\\\frac{2026B^2L^3}{mR}", note: "区域Ⅰ(宽L,磁感应强度B)与区域Ⅱ(宽L,2B)方向相反，位于 x=0 两侧；x=±3L 为弹性挡板。正方形线框边长 L，以 v0 从左侧进入。", basis: "电磁感应·动量定理", t0: 0, t1: 2.5 },\n'
'  { q: 1, title: "2. 选项 A：首次进入磁场的加速度", tex: "a=\\\\frac{F}{m}=\\\\frac{BIL}{m}=\\\\frac{B^2L^2v_0}{mR}=\\\\frac{2026B^4L^5}{m^2R^2}", note: "MN 刚进入磁场Ⅰ时仅 MN 边切割磁感线：E=BLv0，I=E/R=BLv0/R，安培力 F=BIL=B²L²v0/R。代入 v0 得 a。", basis: "安培力·牛顿第二定律", t0: 2.5, t1: 5.5 },\n'
'  { q: 1, title: "3. 选项 B：x=1.5L 处的电势差", tex: "|U_{NM}|:|U_{PQ}|=1:3\\\\neq 1:1", note: "x=1.5L 时线框一半在Ⅱ区(2B)、一半无磁场，仅 PQ 边切割：E_PQ=2BLv。PQ 为电源(内阻 r)，路端电压 U_PQ=3r·I=3/4·E_PQ=3/2·BLv；MN 为外电路一段导线 U_NM=r·I=1/2·BLv。故比值为 1:3，B 错。", basis: "部分导体作电源·路端电压", t0: 5.5, t1: 8.5 },\n'
'  { q: 1, title: "4. 选项 C：右侧挡板碰撞后的速度", tex: "v_{\\\\text{挡板}}=v_0-\\\\frac{14B^2L^3}{mR}=\\\\frac{2012B^2L^3}{mR}", note: "对向右全过程用动量定理分段：进入Ⅰ(仅MN在B, B_sum=1)冲量∝1²；穿越(两边,B_sum=1+2=3)冲量∝3²=9；离开Ⅱ(仅PQ在2B,B_sum=2)冲量∝2²=4。总 Δv=-14B²L³/(mR)，故 v_挡板=2026-14=2012 (单位 B²L³/mR)。弹性碰撞速度大小不变，C 正确。", basis: "动量定理·电磁感应", t0: 8.5, t1: 12.5 },\n'
'  { q: 1, title: "5. 选项 D 与结论", tex: "\\\\Phi=2B\\\\cdot L^2=2BL^2\\\\neq 0,\\\\quad \\\\text{选 A、C}", note: "线框经多次往复、磁场阻尼使其速度逐次减小 14B²L³/(mR)，最终静止于磁场Ⅱ区域内，此时穿过线框的磁通量 Φ=2BL²≠0，D 错。综上答案为 A、C。", basis: "楞次定律·能量衰减", t0: 12.5, t1: 16 }\n'
'];'
)

VIEW_SIM = (
'const VIEW = { xmin: -4, xmax: 4, ymin: -1.7, ymax: 2.7 };\n'
'const SIM  = { duration: 16 };\n'
'/* ===== 本题全局状态与物理辅助函数（线框反向双磁场） ===== */\n'
'let TRAJ = [];\n'
'let TAU_TOTAL = 1;\n'
'const L0 = 1;\n'
'function fieldMag(px){\n'
'  if (px >= -L0 && px <= 0) return 1;\n'
'  if (px >= 0   && px <= L0) return 2;\n'
'  return 0;\n'
'}\n'
'function fieldSigned(px){\n'
'  if (px >= -L0 && px <= 0) return 1;\n'
'  if (px >= 0   && px <= L0) return -2;\n'
'  return 0;\n'
'}\n'
'function Bsum(x){ return fieldMag(x) + fieldMag(x - L0); }\n'
'function fluxOf(x){\n'
'  function ov(a, b, c, d){ return Math.max(0, Math.min(b, d) - Math.max(a, c)); }\n'
'  const aI  = ov(x - L0, x, -L0, 0);\n'
'  const aII = ov(x - L0, x, 0, L0);\n'
'  return 1 * aI - 2 * aII;\n'
'}\n'
'function phaseName(x, v){\n'
'  if (v > 0){\n'
'    if (x < -L0) return "无场区匀速 → 接近磁场Ⅰ";\n'
'    if (x <= 0)  return "进入磁场Ⅰ（仅 MN 边切割 B）";\n'
'    if (x <= L0) return "穿越磁场Ⅰ→Ⅱ（MN 在 2B、PQ 在 B）";\n'
'    if (x <= 2*L0) return "离开磁场Ⅱ（仅 PQ 边切割 2B）";\n'
'    return "无场区匀速 → 右侧挡板";\n'
'  } else {\n'
'    if (x >= 2*L0) return "返回·无场区 → 左侧挡板";\n'
'    if (x >= L0)   return "返回·PQ 边切割 2B（离开磁场Ⅱ）";\n'
'    if (x >= 0)    return "返回·穿越（MN 在 2B、PQ 在 B）";\n'
'    if (x >= -L0)  return "返回·进入磁场Ⅰ（MN 边切割 B）";\n'
'    return "返回·无场区 → 左侧挡板";\n'
'  }\n'
'}\n'
)

SETUP = (
'function setup(){\n'
'  TRAJ = [];\n'
'  const m = 1, R = 1;\n'
'  let x = -L0, v = 2026, tau = 0;\n'
'  const dt = 5e-6;\n'
'  let bounces = 0, guard = 0;\n'
'  TRAJ.push({ tau: 0, x: x, v: v, phase: phaseName(x, v), bounce: false });\n'
'  while (guard < 8000000){\n'
'    guard++;\n'
'    const bs = Bsum(x);\n'
'    const k = (L0 * L0 * bs * bs) / (m * R);\n'
'    let vNew = v - k * v * dt;\n'
'    let xNew = x + v * dt;\n'
'    if (xNew > 3 * L0){\n'
'      x = 3 * L0; v = -Math.abs(v); bounces++;\n'
'      TRAJ.push({ tau: tau, x: x, v: v, phase: "右侧挡板·弹性碰撞", bounce: true });\n'
'    } else if (xNew < -3 * L0){\n'
'      x = -3 * L0; v = Math.abs(v); bounces++;\n'
'      TRAJ.push({ tau: tau, x: x, v: v, phase: "左侧挡板·弹性碰撞", bounce: true });\n'
'    } else {\n'
'      x = xNew; v = vNew;\n'
'    }\n'
'    tau += dt;\n'
'    TRAJ.push({ tau: tau, x: x, v: v, phase: phaseName(x, v), bounce: false });\n'
'    if (bounces >= 2 && x >= -L0 && v > 0) break;\n'
'  }\n'
'  TAU_TOTAL = tau || 1;\n'
'}\n'
)

DRAW = (
'function drawFrame(t){\n'
'  const a = (TAU_TOTAL > 0) ? (t / SIM.duration) * TAU_TOTAL : 0;\n'
'  let st = TRAJ[0];\n'
'  for (let i = 0; i < TRAJ.length; i++){ if (TRAJ[i].tau <= a) st = TRAJ[i]; else break; }\n'
'  const x = st.x, v = st.v, ph = st.phase;\n'
'  const L = L0;\n'
'  ctx.clearRect(0, 0, W, H);\n'
'  ctx.fillStyle = "#fff"; ctx.fillRect(0, 0, W, H);\n'
'  FIG.magInto(-L, 0, -0.8, 0.8, { color: "#7c3aed" });\n'
'  FIG.magOut(0, L, -0.8, 0.8, { color: "#2563eb" });\n'
'  FIG.text(-L/2, 1.08, "区域Ⅰ  B（向里）", { color: "#7c3aed", align: "center", size: 13 });\n'
'  FIG.text(L/2, 1.08, "区域Ⅱ  2B（向外）", { color: "#2563eb", align: "center", size: 13 });\n'
'  drawLine(-3.6, 0, 3.6, 0, "#94a3b8", 1.5);\n'
'  FIG.text(3.55, -0.2, "x", { color: "#475569", size: 12 });\n'
'  FIG.wall(3 * L, -1.0, 1.0, { color: "#1f2937" });\n'
'  FIG.wall(-3 * L, -1.0, 1.0, { color: "#1f2937" });\n'
'  FIG.text(3 * L, 1.32, "挡板 x=3L", { color: "#1f2937", align: "center", size: 11 });\n'
'  FIG.text(-3 * L, 1.32, "挡板 x=-3L", { color: "#1f2937", align: "center", size: 11 });\n'
'  function fillBand(xa, xb, color){\n'
'    if (xb <= xa) return;\n'
'    const p1 = W2S(xa, 0.5), p2 = W2S(xb, -0.5);\n'
'    ctx.fillStyle = color;\n'
'    ctx.fillRect(p1[0], p1[1], p2[0] - p1[0], p2[1] - p1[1]);\n'
'  }\n'
'  fillBand(Math.max(x - L, -L), Math.min(x, 0), "rgba(124,58,237,0.12)");\n'
'  fillBand(Math.max(x - L, 0),  Math.min(x, L), "rgba(37,99,235,0.12)");\n'
'  const tr = W2S(x, 0.5), bl = W2S(x - L, -0.5);\n'
'  ctx.fillStyle = "#ffffff"; ctx.strokeStyle = "#0f172a"; ctx.lineWidth = 2.6;\n'
'  ctx.beginPath(); ctx.rect(bl[0], tr[1], tr[0] - bl[0], bl[1] - tr[1]); ctx.fill(); ctx.stroke();\n'
'  FIG.text(x, 0.64, "N", { color: "#0f172a", align: "center", size: 13 });\n'
'  FIG.text(x - L, 0.64, "P", { color: "#0f172a", align: "center", size: 13 });\n'
'  FIG.text(x, -0.64, "M", { color: "#0f172a", align: "center", size: 13 });\n'
'  FIG.text(x - L, -0.64, "Q", { color: "#0f172a", align: "center", size: 13 });\n'
'  const cx = x - L / 2, cy = 0;\n'
'  const vsign = v >= 0 ? 1 : -1;\n'
'  FIG.vec(cx, cy, vsign * 0.55, 0, "v", { color: "#16a34a", lw: 3, head: 10 });\n'
'  const bs = Bsum(x);\n'
'  if (bs > 0){\n'
'    FIG.vec(cx, cy, -vsign * 0.5, 0, "F_A", { color: "#dc2626", lw: 3, head: 10 });\n'
'    FIG.text(cx, 0.95, "i（感应电流·楞次定律）", { color: "#ea580c", align: "center", size: 11 });\n'
'  }\n'
'  if (st.bounce){\n'
'    const c = W2S(x, 0);\n'
'    ctx.strokeStyle = "rgba(220,38,38,0.9)"; ctx.lineWidth = 3;\n'
'    ctx.beginPath(); ctx.arc(c[0], c[1], 0.35 * scale, 0, 7); ctx.stroke();\n'
'  }\n'
'  const bg = v >= 0 ? "rgba(37,99,235,0.92)" : "rgba(124,58,237,0.92)";\n'
'  FIG.processBanner(ph, { bg: bg, color: "#fff", size: 16 });\n'
'}\n'
)

READ = (
'function readouts(t){\n'
'  const a = (TAU_TOTAL > 0) ? (t / SIM.duration) * TAU_TOTAL : 0;\n'
'  let st = TRAJ[0];\n'
'  for (let i = 0; i < TRAJ.length; i++){ if (TRAJ[i].tau <= a) st = TRAJ[i]; else break; }\n'
'  const x = st.x, v = st.v;\n'
'  const bs = Bsum(x);\n'
'  const F = bs > 0 ? (bs * bs) * Math.abs(v) / 2026 : 0;\n'
'  const phi = fluxOf(x);\n'
'  return [\n'
'    ["过程", st.phase, ""],\n'
'    ["x (MN)", x.toFixed(2), "L"],\n'
'    ["速度 v", v.toFixed(0), "·B²L³/(mR)"],\n'
'    ["安培力 F", F.toFixed(2), "（归一）"],\n'
'    ["磁通量 Φ", phi.toFixed(2), "·BL²"]\n'
'  ];\n'
'}\n'
)

html, n1 = re.subn(r"const PROBLEM = \{[\s\S]*?\n\};", PROBLEM, html, count=1)
html, n2 = re.subn(r"const STEPS = \[[\s\S]*?\n\];", STEPS, html, count=1)
html, n3 = re.subn(r"const VIEW = \{[^}]*\};\nconst SIM\s*=\s*\{[^}]*\};", VIEW_SIM, html, count=1)
html, n4 = re.subn(r"function setup\(\) \{[\s\S]*?\n\}", SETUP, html, count=1)
html, n5 = re.subn(r"function drawFrame\(t\) \{[\s\S]*?\n\}", DRAW, html, count=1)
html, n6 = re.subn(r"function readouts\(t\) \{[\s\S]*?\n\}", READ, html, count=1)

print("replacements:", n1, n2, n3, n4, n5, n6)
assert all([n1, n2, n3, n4, n5, n6]), "some block not replaced!"

with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)
print("written:", OUT, "size:", len(html))
