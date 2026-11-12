# -*- coding: utf-8 -*-
"""为「起点」标签搜寻全程无车架/无轮圈遮挡的位置（一次性分析脚本，可删）。"""
import math

R_WHEEL, R_VALVE, V_BIKE, HUB0_X = 0.30, 0.18, 0.40, 1.30
OMEGA = V_BIKE / R_WHEEL
T_HALF = math.pi / OMEGA
PAD, WIN = 36, 678
scale = (WIN - 2 * PAD) / 2.84
WHEELBASE = 1.00


def W(x, y):
    return (PAD + (x + 0.22) * scale, 0.66 * WIN - PAD - (y + 0.44) * scale)


def seg_dist(p0, p1, q):
    x0, y0 = p0; x1, y1 = p1; x2, y2 = q
    dx, dy = x1 - x0, y1 - y0
    L2 = dx * dx + dy * dy
    if L2 == 0:
        return math.hypot(x2 - x0, y2 - y0)
    t = max(0, min(1, ((x2 - x0) * dx + (y2 - y0) * dy) / L2))
    return math.hypot(x2 - (x0 + t * dx), y2 - (y0 + t * dy))


def minframe(deg, lx, ly):
    """标签点到车架各段的最短距离（屏幕 px）。"""
    th = math.radians(deg); tt = th / OMEGA
    hx = HUB0_X + V_BIKE * tt
    R = R_WHEEL
    rx = hx - WHEELBASE
    BB = (hx - 0.60, R - 0.03); ST = (hx - 0.80, 0.72); HT = (hx - 0.04, 0.80)
    segs = [((hx, R), BB), ((hx, R), ST), (BB, ST), (BB, HT), (ST, HT), (HT, (hx, R)),
            ((rx, R), BB), ((rx, R), ST), ((rx, R), (hx, R))]
    return min(seg_dist(a, b, (lx, ly)) for a, b in segs) * scale


def minwheel(deg, lx, ly):
    """标签点到两个轮圈（圆）的最短距离。"""
    th = math.radians(deg); tt = th / OMEGA
    hx = HUB0_X + V_BIKE * tt
    q = W(lx, ly)
    out = 1e9
    for cx in (hx - WHEELBASE, hx):
        c = W(cx, R_WHEEL)
        d = math.hypot(q[0] - c[0], q[1] - c[1])
        out = min(out, abs(d - R_WHEEL * scale))     # 到圆周的距离，不在轮内也算
    return out


RX0, RX1 = HUB0_X - WHEELBASE, HUB0_X - WHEELBASE + V_BIKE * T_HALF
print("后轮轮心 x 扫过: %.2f → %.2f" % (RX0, RX1))
print("车架最左可达: x = 后轮心 - 0.30 = %.2f\n" % (RX0 - R_WHEEL))

print("起点绿环世界坐标 = (1.30, 0.48)  ← 固定不动")
print("搜寻「离绿环 ≤ 75 px」且「全程离车架/轮圈 ≥ 14 px」的位置：\n")
print("%-16s %-9s %-11s %-11s" % ("候选世界坐标", "离环px", "车架min", "轮圈min"))
best = None
for lx10 in range(70, 141, 4):
    for ly10 in range(10, 91, 4):
        lx, ly = lx10 / 100.0, ly10 / 100.0
        q = W(lx, ly); r = W(HUB0_X, R_WHEEL + R_VALVE)
        ringpx = math.hypot(q[0] - r[0], q[1] - r[1])
        if ringpx > 75 or ringpx < 26:
            continue
        f = min(minframe(d, lx, ly) for d in (0, 15, 30, 45, 60, 75, 90, 110, 130, 150, 170, 180))
        w = min(minwheel(d, lx, ly) for d in (0, 15, 30, 45, 60, 75, 90, 110, 130, 150, 170, 180))
        if f >= 14 and w >= 9:
            score = f + w
            if best is None or score > best[0]:
                best = (score, lx10, ly10, ringpx, f, w)
            print("%-16s %-9.0f %-11.0f %-11.0f" % ("(%.2f, %.2f)" % (lx, ly), ringpx, f, w))

print()
if best:
    _, a, b, rp, f, w = best
    print("★ 最佳：世界 (%.2f, %.2f)  离环 %.0fpx  车架 %.0fpx  轮圈 %.0fpx" % (a / 100, b / 100, rp, f, w))
else:
    print("★ 无满足条件的位置——需要放宽约束或改用引线标注")
