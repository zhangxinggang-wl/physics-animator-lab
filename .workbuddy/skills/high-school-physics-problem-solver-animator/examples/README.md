# examples —— 活案例，不是模板

这里放**已交付题目**的完整生成器脚本。它们是本技能最有价值的参考：
每一份都能跑通「读题 → 推导 → 动画 → 门禁」全流程，可直接复制改名后改写。

## 怎么用

**不要**从零写 `build_*.py`。做法：

1. 找一份**题型最接近**的（见下表），`cp` 到工作区 `_build/`；
2. 改顶部常量（题面、`PAR`、`VIEW`）与三区代码（`PROBLEM` / `STEPS` / `drawFrame` / `readouts`）；
3. 保留文件**尾部的 FOUND/MISSING 探针自检**与**反斜杠硬门禁**（见 `references/pitfalls.md` 第一节）；
4. 跑 `scripts/syntax_check.js` → `scripts/audit_page.js` → `scripts/shot_zoom.js`。

## 选题对照表

| 题型 | 参考脚本 | 关键可复用点 |
|---|---|---|
| **电场 + 重力 + 分区磁场复合场** | `build_zfield_gravity.py` | 7 段圆弧 `SEGS`/`TAU`/`tauOf` 分段映射、相切点递推、第(3)问整屏换场景、笔画哨兵、反斜杠门禁 |
| 速度选择器三区域复合场 | `build_em_selector.py` | 分区场边界、等势面/速度筛选动画 |
| 超声波测车速 | `build_ultrasound.py` | 脉冲往返测距（单程 = `v·t/2`）、波前弧硬裁剪、尺寸线联合约束 |
| 位移传感器测小车速度 | `build_sensor_cart.py` | 几何自洽画法（`X_P`/`X_Q` 严格满足 `Δx·K`）、两次接收时间间隔 |
| 弧轨道碰撞 | `build_arc_cart.py` | 相切/碰撞几何、碰撞前后分段 |
| **弹簧连接多体 + 弹性碰撞** | `build_spring_triple.py`（+ `extract_spring_triple_single.py`） | 斜置弹簧折线 `springSeg`（任意轴向、固定圈数）+ 尺寸线 `dimDx`（留缺口）+ 碰撞闪光 `flashRing`（二次方衰减）+ 7 段 `tauOf` 4 个定格点；单栏抽取脚本已含 wrap 保留 / 双 style 块 `rfind` / kpDrawer 整块删除 |
| 铁环滚动 N 圈半 | `build_ring_turns.py` | 纯滚动复合约束、圈数计数 |
| 配速法摆线 | `build_cycloid_velocity.py` | 摆线参数化、速度分解 |
| 斜面 + 滑轮 + 杆 | `build_rod_pulley.py` / `build_incline_pulley_swap.py` / `build_wedge_pulley.py` | 连接体约束、滑轮绕绳 |
| 自行车气门芯位移 | `build_bike_valve.py` | 传感器触发、速度曲线 |
| p–V 过程 | `build_pv_car.py` | 热学过程、状态点轨迹 |
| 线框 / 空间构图 | `build_wireframe.py` | 立体图元、投影 |

## 共同骨架（每份都含）

```python
# ① 题面/参数常量
PAR = {...}; VIEW = {...}
# ② 三区代码：PROBLEM（题面+选项+知识点）/ STEPS（分步解析）/ 绘图+readouts
# ③ 注入模板（⚠ re.sub 替换串必须用 lambda 包一层，见 pitfalls.md 1.1）
# ④ 产物级反斜杠硬门禁
# ⑤ FOUND/MISSING 探针自检
```

> ⚠ 这些脚本里**注释中保留了踩坑记录**（为什么这么写、写过什么错版本）。
> 改写前先读注释 —— 那里比代码本身更能说明哪些地方动不得。