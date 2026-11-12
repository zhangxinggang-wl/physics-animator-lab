# 大学物理与强基（强基础）拓展知识点参考手册

> 本手册配合 `assets/template.html` 的 `FIG.*` 图元库使用，面向**强基计划校测、竞赛预赛与更高难度物理题**。
> 每条知识点给出：核心公式（标准 LaTeX）、推荐 `FIG.*` 图元、典型题型与易错点。
> 高中基础板块见 `references/高中物理知识点全景索引.md` 与各分册；图形重绘规范见 `references/figures_redraw_spec.md`。
>
> **通用约定**：所有图形一律走 `FIG.*`（或经审批的自定义 `ctx` 1:1 绘制），与 `drawFrame` 同世界坐标、同比例尺；重绘遵守「完全相同＝7 维度」（见 figures_redraw_spec.md §6）。

---

## 1. 量子物理（Quantum）

### 1.1 黑体辐射与光电效应
- 公式：
  - 光电效应方程：$E_k = h\nu - W_0 = h\nu - h\nu_0$，截止频率 $\nu_0 = W_0/h$。
  - 光子能量 $E = h\nu = \hbar\omega$，动量 $p = h/\lambda$。
- FIG 图元：`FIG.energyLevels`（能级 + 吸收/发射跃迁箭头）。
- 易错点：逸出功 $W_0$ 与截止频率对应关系；光强只影响光电流大小，不影响最大初动能。

### 1.2 玻尔原子模型
- 公式：
  - 定态能量 $E_n = -\dfrac{13.6\ \text{eV}}{n^2}$（氢原子）。
  - 轨道半径 $r_n = n^2 a_0$，角动量量子化 $L = n\hbar$。
  - 跃迁频率 $\nu = \dfrac{E_i - E_f}{h}$。
- FIG 图元：`FIG.bohrOrbit(cx,cy,[a0,4a0,9a0],{electron,phase})`（同心圆轨道 + 电子）；`FIG.energyLevels`（能级跃迁）。
- 易错点：跃迁是**二能级之差**，不是相邻能级差；吸收对应低→高（向上箭头），发射对应高→低（向下箭头）。

### 1.3 一维势阱与束缚态
- 公式（无限深方势阱）：
  - 能级 $E_n = \dfrac{n^2\pi^2\hbar^2}{2mL^2}$（$n=1,2,3,\dots$）。
  - 波函数 $\psi_n(x) = \sqrt{\dfrac{2}{L}}\sin\dfrac{n\pi x}{L}$。
- FIG 图元：`FIG.quantumWell(x,y,w,V0,{levels:[E1,E2,E3]})`（势函数 + 束缚态能级虚线）。
- 易错点：基态 $n=1$ 无节点；能级随 $L$ 减小而升高（纳米尺度显著）。

### 1.4 物质波与不确定性
- 公式：德布罗意波长 $\lambda = h/p = h/(mv)$；不确定关系 $\Delta x\,\Delta p_x \ge \hbar/2$。
- FIG 图元：`FIG.wave`（概率波包示意）；`FIG.ripple`（波前）。

---

## 2. 原子与原子核（Nuclear）

### 2.1 原子核组成与衰变
- 公式：
  - $\alpha$ 衰变：${}^{A}_{Z}X \to {}^{A-4}_{Z-2}Y + {}^{4}_{2}\text{He}$。
  - $\beta^-$ 衰变：${}^{A}_{Z}X \to {}^{A}_{Z+1}Y + e^- + \bar\nu_e$。
  - 半衰期 $N = N_0 e^{-\lambda t}$，$T_{1/2}=\ln 2/\lambda$。
- FIG 图元：`FIG.nucleus(cx,cy,Z,N,{label})`（质子红/中子蓝团簇，标注 ${}^{A}_{Z}X$）。
- 易错点：质量数 $A$ 守恒、电荷数 $Z$ 守恒；$\beta$ 衰变质子数 +1。

### 2.2 质能方程与核反应
- 公式：$E = mc^2$，$\Delta E = \Delta m\,c^2$；比结合能越大越稳定。
- FIG 图元：`FIG.nucleus`（对比反应前后核子数）。
- 易错点：质量亏损 $\Delta m$ 是「反应前总质量 − 反应后总质量」，非单个核子质量。

---

## 3. 狭义相对论（Relativity）

### 3.1 洛伦兹变换与时空
- 公式：
  - 时间膨胀 $\Delta t = \gamma\,\Delta \tau$（$\gamma = 1/\sqrt{1-v^2/c^2}$）。
  - 长度收缩 $L = L_0/\gamma$。
  - 洛伦兹变换 $x' = \gamma(x-vt),\ t' = \gamma(t - vx/c^2)$。
- FIG 图元：`FIG.spacetime(ox,oy,{worldline,labels})`（闵可夫斯基图：$t$ 轴向上、$x$ 轴向右、45° 红色光锥、蓝色世界线）。
- 易错点：同时性的相对性；因果由光锥内/外判定。

### 3.2 相对论能量动量
- 公式：$E^2 = (pc)^2 + (m_0c^2)^2$，$E_k = (\gamma-1)m_0c^2$。
- FIG 图元：配合 `FIG.spacetime` 或 `FIG.vec` 画能量-动量矢量。

---

## 4. 刚体力学（Rigid Body）

### 4.1 转动惯量与转动定律
- 公式：
  - 转动定律 $\tau = I\alpha$。
  - 转动惯量 $I = \sum m_i r_i^2$（常见：细杆 $I=\frac{1}{12}mL^2$，圆盘 $I=\frac{1}{2}mR^2$）。
  - 转动动能 $E_k = \frac{1}{2}I\omega^2$；平行轴定理 $I = I_c + md^2$。
- FIG 图元：`FIG.rigidDisk(cx,cy,R,{label:'ω'})`（圆盘 + 逆时针 $\omega$ 弧形箭头）；`FIG.vec`（切向力/速度）。
- 易错点：纯滚动条件 $v = \omega R$；转动惯量依赖转轴位置。

### 4.2 角动量与角动量守恒
- 公式：$\vec L = \vec r \times \vec p = I\vec\omega$；$\dfrac{d\vec L}{dt} = \vec\tau$；合外力矩为零时 $\vec L$ 守恒。
- FIG 图元：`FIG.axisVec(cx,cy,len,'L')`（沿转轴的角动量/力矩矢量 + 轴端圆，右手定则方向）；`FIG.rigidDisk`。
- 易错点：角动量是**矢量**，方向沿转轴（右手螺旋）；进动问题力矩垂直于 $\vec L$。

---

## 5. 电磁学进阶（Advanced EM）

### 5.1 螺线管与磁场
- 公式：长直螺线管内部 $B = \mu_0 n I$（$n$ 为单位长度匝数）。
- FIG 图元：`FIG.solenoid(x1,x2,y,{field:'into'})`（线圈半圆 + 内部 ×/⊙）；`FIG.magInto`/`FIG.magOut`。
- 易错点：内部近似匀强、外部近似为零；电流方向与内部磁场方向由右手螺旋判定。

### 5.2 环形电流与磁力矩
- 公式：圆电流中心 $B = \dfrac{\mu_0 I}{2R}$；线圈磁矩 $\vec\mu = I\vec S$；磁力矩 $\vec\tau = \vec\mu \times \vec B$。
- FIG 图元：`FIG.currentLoop(cx,cy,R,{axis:true})`（圆环 + 法向磁场箭头）；`FIG.axisVec`（磁矩/力矩矢量）。
- 易错点：磁力矩使磁矩转向外磁场方向；稳定平衡 $\vec\mu \parallel \vec B$。

### 5.3 变压器
- 公式：$\dfrac{U_1}{U_2} = \dfrac{n_1}{n_2}$，$\dfrac{I_1}{I_2} = \dfrac{n_2}{n_1}$（理想变压器）。
- FIG 图元：`FIG.transformer(x,y,{n1,n2})`（铁芯 + 原/副线圈）。
- 易错点：理想变压器功率守恒 $U_1I_1 = U_2I_2$；只改变交流。

### 5.4 二极管与交流电路
- 公式：整流（半波/全波）；交流 $u = U_m\sin\omega t$；感抗 $X_L=\omega L$、容抗 $X_C=1/(\omega C)$。
- FIG 图元：`FIG.diode(x,y,{flip,glow})`（三角+竖条，glow=LED）；`FIG.acSource`（圆内正弦）；`FIG.capacitor`/`FIG.inductor`/`FIG.resistor`。
- 易错点：二极管单向导电；整流后含直流分量。

### 5.5 电磁振荡与电磁波
- 公式：LC 振荡 $\omega = 1/\sqrt{LC}$，$q = Q_m\cos(\omega t+\phi)$。
- FIG 图元：`FIG.capacitor` + `FIG.inductor` + `FIG.wire` 组电路；`FIG.wave`（电场/磁场分量示意）。

---

## 6. 振动与波进阶（Advanced Oscillation & Waves）

### 6.1 驻波
- 公式：驻波方程 $y = 2A\cos(kx)\sin(\omega t)$；波节位置 $x = (2n+1)\lambda/4$，波腹 $x = n\lambda/2$。
- FIG 图元：`FIG.standingWave(x1,x2,y,amp,n,{nodes:true,axis:true})`（波节红点 + 平衡虚线）。
- 易错点：两端固定的弦长 $L = n\lambda/2$（$n=1,2,\dots$）。

### 6.2 参考圆 / 相量法
- 公式：SHM 与匀速圆周运动投影等价，$x = A\cos(\omega t+\phi)$。
- FIG 图元：`FIG.phasor(cx,cy,R,th,{project:true})`（旋转矢量 + 竖直投影）。
- 易错点：相位差决定叠加结果；拍频 $\Delta\omega$。

### 6.3 偏振与干涉 / 衍射
- 公式：马吕斯定律 $I = I_0\cos^2\theta$；双缝干涉 $\Delta x = \lambda L/d$；光栅 $d\sin\theta = k\lambda$。
- FIG 图元：`FIG.polarizer(x,yt,yb)`（偏振片透光轴双箭头）；`FIG.barrier(x,y,h,slits)`（双缝/光栅）；`FIG.ripple`（干涉圆环）；`FIG.lens`/`FIG.screen`（成像/光屏条纹）。
- 易错点：自然光通过偏振片强度减半；干涉条纹间距与波长成正比。

---

## 7. 流体力学（Fluid Mechanics）

### 7.1 伯努利方程与连续性
- 公式：$p + \dfrac{1}{2}\rho v^2 + \rho g h = \text{const}$；连续性 $A_1v_1 = A_2v_2$。
- FIG 图元：`FIG.streamline(pts,{head})`（流线 + 流向箭头）；`FIG.pipe`（变截面管，配合 `FIG.vec` 标流速）。
- 易错点：高速处低压（机翼升力、空吸）；黏性不可忽略时用泊肃叶/斯托克斯。

### 7.2 浮力与阿基米德
- 公式：$F_{\text{浮}} = \rho_{\text{液}} g V_{\text{排}}$。
- FIG 图元：`FIG.vec`（浮力向上 + 重力向下，对比）；`FIG.particle`/`FIG.block`（浸没物体）。

---

## 8. 热学进阶（Advanced Thermodynamics）

### 8.1 热力学循环（卡诺等）
- 公式：热机效率 $\eta = 1 - Q_c/Q_h$；卡诺效率 $\eta_c = 1 - T_c/T_h$。
- FIG 图元：`FIG.pvAxes` + `FIG.pvCurve`（p–V 图循环，等温/绝热/等压/等容分段折线）。
- 易错点：循环方向判定吸热/放热；卡诺循环由两条等温线 + 两条绝热线构成。

### 8.2 熵与统计
- 公式：玻尔兹曼熵 $S = k\ln\Omega$；克劳修斯不等式 $\oint \delta Q/T \le 0$。
- FIG 图元：`FIG.heatBath`（热源/冷源）；`FIG.pvCurve`（可逆过程）。
- 易错点：熵增原理只适用于孤立系统。

---

## 9. 综合制图要点（面向 HTML 动画）

> **录入试题即重绘（强制）**：凡题面含图形，生成 HTML 时一律按原图 **1:1 重新绘制**（方式 ② 矢量重绘），**禁止把原图位图直接塞进 `<img>` 当作「已重绘」**。重绘结果须与原图在「几何结构 / 线型线宽 / 比例尺寸 / 角度与相对位置 / 字母标注 / 填充阴影 / 坐标系」7 个维度逐一吻合（完全相同）；嵌入原图位图（方式 ①）不计入「重绘」，仅当图形确实无法用 `FIG.*` 表达或用户明确要求像素级原样时兜底。

1. **开普勒/天体**：`FIG.ellipseOrbit(cx,cy,a,b,{bodyFrac})` 画椭圆轨道（焦点恒星 + 行星），配合 `FIG.vec` 标速度/引力。
2. **多过程 + 知识点抽屉**：仍用 `FIG.processBanner` 显示过程名；强基题往往含 3–5 个物理过程，过程数必须 = 题设。
3. **公式一律标准 LaTeX**：如 $\vec L = \vec r\times \vec p$、$E_n = -13.6/n^2\ \text{eV}$、$p+\frac12\rho v^2+\rho gh = C$，禁止 `sqrt()`、`/` 行内分数等代码风格。
4. **动画与解析逐步骤对应**：`stateAt(t)` 同时驱动 `drawFrame` 与数据面板读数；例如螺线管电流变化→内部磁场×/⊙密度变化→导体棒受力加速度变化，三者用同一套参数。
5. **解析优先高中方法 · 默认禁用微积分（强制）**：本技能面向高中物理试题，解析**优先且默认使用高中物理方法**，`tex` 字段**不得出现 `\int`**。变电流 / 变力问题优先用：电荷量 `q=It` 或平均电流 `\bar{I}=(I_1+I_2)/2`；焦耳热 `Q=I^2Rt` 或 `I^2` 的时间平均 `(I_1^2+I_1I_2+I_2^2)/3`；动量定理 `m\Delta v=BLq`、动能定理、能量守恒、图像斜率与面积。仅当题目明确属大学物理 / 强基、高中方法确实不可行时，才可用微积分，并在 `note` 中说明原因。校验：Playwright 检查页面文本不含 `∫` 或 `\int`（属上述例外者除外）。

---

### 9.1 四大图形约定（GEOMETRY_REVERSE_ENGINEERING / CANVAS_PIXEL / TWIN_LOCK / CONSISTENCY_CHECKLIST）+ GREEK_SYMBOLS

> 本册 §9 所列大学·强基图形与右栏动画**共用同一套几何来源（同源 world 坐标 / `FIG.*` / `W2S`）**，二者几何必须 1:1。静态题图**默认走 Canvas 2D 孪生锁定（路径 B，`__CANVAS_STATIC__`）**：`<canvas>` 在 `t=0` 由 `drawStaticGraph()` 用 Canvas 2D 上下文按原图 1:1 硬编码绘制（模板已在 `renderProblem()` 之后补调 `drawFigures()`，加载即绘制、不依赖 resize 事件），独立双击打开必显示——**严禁用 SVG `viewBox` 通用缩放另绘**（坐标漂移、破坏孪生锁定）。**仅「不生成动画的纯静态几何重绘」允许 Mermaid / 内联 SVG（含 viewBox）**（见 `figures_redraw_spec.md` §10）。四大约定与 [GREEK_SYMBOLS] 配套，详见 `figures_redraw_spec.md` §3.2 与 SKILL.md「## 图形重绘工作流」。

- **[GEOMETRY_REVERSE_ENGINEERING] 几何反编译**：重绘前先反编译原题图几何——列出四类几何基元：① 顶点坐标（以画布左上角为原点的 X、Y 像素级相对位置）；② 线段/路径（起止点与曲率）；③ 角度标注弧位置；④ 文字锚点（m、F、v₀ 等精确落点）。**不得凭空「画」相似图形**。
- **[CANVAS_PIXEL] Canvas 2D 像素级 + 禁用 viewBox**：静态题图由 `drawStaticGraph(c)` 在左栏 `<canvas class="fig-canvas">` 上以 `t=0` 绘制，使用固定像素尺寸硬编码、像素级绘制；**严禁 SVG `viewBox` 通用缩放**（坐标会漂移）。
- **[TWIN_LOCK] 孪生锁定**：右栏动画直接复用 `drawStaticGraph()`；不动元素（轨道轮廓/固定墙壁/坐标轴框）只在背景层绘一次，移动元素（行星/电子/矢量箭头）严格按解析运动方程逐帧移动；**动画第 0 帧与左栏题图像素级重合**。
- **[CONSISTENCY_CHECKLIST] 一致性自检（生成 HTML 前于 CoT 隐式核对）**：[CHECK_1] 动图角度参数与左图**绝对相等**（同一变量控制）；[CHECK_2] 矢量箭头长度比例与左图一致（同一 `scale = 5px/N`）；[CHECK_3] 动图标签移动时始终锚定物体同一相对位置。
- **[GREEK_SYMBOLS] 希腊角度符号禁中文名**：解析与动画中 $\theta$、$\alpha$、$\beta$、$\phi$、$\delta$ 一律用符号、禁「西塔/阿尔法/贝塔/斐/德尔塔」等中文名；时变角写 $\theta(t)$/$\phi(t)$。

### 通用强制条款（公式符号 · 与 mechanics_reference.md §7 / SKILL.md 同源）

> 以下四类写法适用于 `given` / `note` / `basis` / `readouts` 名称 / `tex` / 每问结论式 **所有字段**，不限于 `tex`：

- **单位（强制正体 upright）**：物理量单位必须正体、**禁止斜体**。两种合规写法：① **首选——单位作为纯文本写在公式环境外**（天然正体、源码干净），如 `$m_A=0.4$ kg`、`$v_0=2$ m/s`；② **单位必须嵌在数学式内时**（分式、复合量等无法外提），用 `\mathrm{}` 强制正体，如 `1.2\,\mathrm{m/s}`、`0.20\,\mathrm{m}`、`a=9.8\,\mathrm{m/s²}`。禁止把单位裸写在公式环境内却不包裹（如 `m/s`、`kg` 直接放进 `$...$` 会渲染成斜体，正是「单位用了斜体」的根因）；禁止嵌套 `\mathrm{\mathrm{kg}}`。（参考资料公式示例为通用 LaTeX，仅作知识点对照。）
- **角度/度**：`\^{\circ}`，如 `60\^{\circ}`、`\theta=60\^{\circ}`。**禁止** Unicode `°`、禁止 `^o`/`^0`、禁止 `度` 字（如 `60度`）。
- **变化量（Δ）**：大写 `\Delta`，如 `\Delta E`、`\Delta s`、`\Delta t`。**禁止** Unicode `△`。
- **根号**：`\sqrt{被开方数}`，如 `\sqrt{v_x^{2}+v_y^{2}}`。**禁止** Unicode `√`、禁止 `sqrt()`。

> **渲染与查看（防误判）**：公式由内置 MathJax 3 运行时渲染，**必须用支持 JavaScript 的浏览器打开**（双击 `.html` 或 WorkBuddy 预览面板）。本技能已强制「单位正体」：生成稿单位一律正体——公式外纯文本（天然正体）或公式内 `\mathrm{}`（强制正体），任何查看环境都不会出现斜体单位；若仍看到斜体单位，是旧文件请重新生成。数学符号（`\Delta`、`\sqrt{}`、`^{\circ}`、`\theta`）须保留 LaTeX 命令，在 JS 浏览器正常渲染，在非 JS 查看器以源码出现属正常查看方式问题，并非生成缺陷。

### 角度符号与矢量标注强制规范（ANGLE_SNAP / GREEK_VARIABLE / VECTOR_ARROW）

> 与 SKILL.md「## 角度符号与矢量标注强制规范」同源、同等强制，本手册仅作大学·强基领域化提示。

1. **希腊角度符号强制（禁止中文名）**：物理常用角度一律用符号——$\theta$（西塔）、$\alpha$（阿尔法）、$\beta$（贝塔）、$\phi$（斐）、$\delta$（德尔塔），**禁止写成「西塔/阿尔法/贝塔/斐/德尔塔」等中文名**，也禁止 Unicode 近似；LaTeX 命令 `\theta \alpha \beta \phi \delta`（磁通量/相位用 `\Phi`/`\varphi`）。**时变角度须写 $\theta(t)$/$\phi(t)$**（如刚体转角 $\theta(t)$、转动相位 $\phi(t)$）。
2. **[ANGLE_SNAP]**：重绘/动画中接近 30°/37°/45°/53°/60° 的角度必须精确吸附为对应特殊角（如 $36.8^\circ\to37^\circ$），避免出现不利于手算的非整数角；生成器由 `snap_special(deg)` 自动完成。
3. **[GREEK_VARIABLE]**：刚体转动角 $\theta(t)$、进动方位角 $\phi(t)$、相量相位等时变角度，须在动画区右上方加**实时角度显示器**（° 与 rad 同显），画布角度弧标签用 Unicode 字形 `θ`/`φ`（不是 `\theta`/`\varphi` 源码）。
4. **[VECTOR_ARROW]**：角动量 $\vec L$、力矩 $\vec\tau$、洛伦兹力等带角度矢量，箭头旁须显式标注角度值或符号，箭头长度正比于标量大小（如 `rigidDisk` 的 $\omega$ 箭头、`axisVec` 的角动量矢量）。

## 10. 典型强基/竞赛题型索引（示例）

| 题型 | 关键知识点 | 主用图元 |
|------|-----------|----------|
| 氢原子跃迁与谱线 | 玻尔模型、能级 | `bohrOrbit` + `energyLevels` |
| 光电/康普顿效应 | 光子、动量守恒 | `energyLevels` + `vec` |
| 相对论同时性/光锥 | 洛伦兹变换 | `spacetime` |
| 刚体纯滚动/转动定律 | $I,\tau=I\alpha$ | `rigidDisk` + `vec` |
| 角动量守恒（含进动） | $\vec L$ 守恒 | `axisVec` |
| 螺线管/电磁炮 | $B=\mu_0 nI$、安培力 | `solenoid` + `magInto` + `vec` |
| 变压器/整流 | 匝数比、单向导电 | `transformer` + `diode` + `acSource` |
| 驻波/拍/偏振 | 叠加、马吕斯 | `standingWave` + `phasor` + `polarizer` |
| 伯努利/升力 | 流线、低压 | `streamline` + `pipe` |
| 卡诺循环效率 | p–V 循环 | `pvAxes` + `pvCurve` |
| 核衰变/质能 | 守恒、半衰期 | `nucleus` |
