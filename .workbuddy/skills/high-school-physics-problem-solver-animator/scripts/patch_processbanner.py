# -*- coding: utf-8 -*-
"""
把「老版模板遗留的 FIG.processBanner 设备像素 bug」补丁应用到指定 HTML。

背景
----
`FIG.processBanner` 早期实现是：
    const W = ctx.canvas.width, H = ctx.canvas.height;
框架 resize() 里执行了 `ctx.setTransform(ratio,0,0,ratio,0,0)`（ratio = devicePixelRatio），
之后**所有绘制坐标都按 CSS 像素解释**；而 `ctx.canvas.width` 是**设备像素**（dpr=2 时翻倍）。
于是 `bx = (W - bw)/2` 用的是 2 倍宽度，横幅被画到约 2× 的位置 —— 在 678px 宽的画布上
右半截（甚至整块）落到画布外，表现是「过程横幅不见了 / 只剩一小截」。

修复：改用 `ctx.canvas.getBoundingClientRect()` 取真实 CSS 尺寸。
（`assets/template.html` 已修；本脚本用于给修好之前生成的历史页面补丁。）

用法：
  python _build/patch_processbanner.py <html> [<html> ...]
"""
import io
import os
import sys

OLD = """    const W = ctx.canvas.width, H = ctx.canvas.height;
    const fs = (opts.size || 18);"""

NEW = """    /* 关键：拿到「CSS 像素」尺寸，而不是 ctx.canvas.width。
       框架 resize() 里执行了 ctx.setTransform(ratio,0,0,ratio,0,0)（ratio=devicePixelRatio），
       之后所有绘制坐标都按 CSS 像素解释；而 ctx.canvas.width 是设备像素（2× 屏即翻倍）。
       若直接用它居中，横幅会按 2 倍偏移画到画布外（表现为横幅缺失或只剩左半截）。
       注意：本函数可能被左栏题图画布复用（drawStaticGraph 里临时改 ctx 指向题图画布），
       故用 getBoundingClientRect() 取真实 CSS 尺寸，而非全局 W/H。 */
    const rect = ctx.canvas.getBoundingClientRect();
    const W = (rect && rect.width)  ? rect.width  : ctx.canvas.width;
    const H = (rect && rect.height) ? rect.height : ctx.canvas.height;
    const fs = (opts.size || 18);"""


def patch(path):
    s = io.open(path, encoding="utf-8").read()
    n = s.count(OLD)
    if n == 0:
        if "const rect = ctx.canvas.getBoundingClientRect();" in s:
            print("SKIP  %s（已打过补丁）" % os.path.basename(path))
        else:
            print("FAIL  %s（未找到旧实现，需人工确认）" % os.path.basename(path))
        return False
    assert n == 1, "锚点不唯一：%s（出现 %d 次）" % (path, n)
    s = s.replace(OLD, NEW, 1)
    io.open(path, "w", encoding="utf-8", newline="\n").write(s)
    print("OK    %s（%.2f MB）" % (os.path.basename(path), len(s.encode("utf-8")) / 1048576.0))
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    changed = 0
    for p in sys.argv[1:]:
        if patch(p):
            changed += 1
    print("已修改 %d 个文件" % changed)
