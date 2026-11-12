# -*- coding: utf-8 -*-
"""
从完整教学动画 HTML 中「单独抽出动画演示部分」，生成一个轻量单文件 HTML。

原理（不依赖任何第三方库）：
  1. 定位三栏骨架 <div class="wrap">…</div>，只保留 <section class="col col-animation">；
  2. 把右栏 <canvas id="cv"> 的 CSS 宽度从「占满栏宽」改为固定像素（默认 680×449，
     与原始 640×420 同比例 0.65625），避免单栏居中后画布被放大到失真；
  3. 注释掉左/中栏相关的 renderProblem / renderSteps / 知识点卡片 / 抽屉 渲染，
     保留 canvas、控件、数据面板的全部逻辑；
  4. 在 </style> 前追加单栏居中布局样式。

用法：
  python extract_anim_only.py            # 处理默认的「铁环滚动三圈半」
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

SRC = os.path.join(ROOT, "2026-09-13_铁环滚动三圈半_教学动画.html")
OUT = os.path.join(ROOT, "2026-09-13_铁环滚动三圈半_动画演示.html")

CV_W, CV_H = 680, 449          # 单栏动画画布固定尺寸（保持 0.65625 原始纵横比）
RATIO = 420 / 640.0


def find_wrap(s):
    """返回 <div class="wrap"> … </div>（配平标签）的 [start, end) 区间。"""
    start = s.index('<div class="wrap">')
    i = s.index(">", start) + 1
    depth = 1
    pat = re.compile(r"<(/?)div\b[^>]*>")
    while depth > 0:
        m = pat.search(s, i)
        if not m:
            raise RuntimeError("wrap 标签未配平")
        depth += -1 if m.group(1) else 1
        i = m.end()
    return start, i


def main():
    s = io.open(SRC, encoding="utf-8").read()

    # ---------- ① 骨架：只保留动画栏 ----------
    ws, we = find_wrap(s)
    seg = s[ws:we]
    cs = seg.index('<section class="col col-animation">')
    ce = seg.index("</section>", cs) + len("</section>")
    anim = seg[cs:ce]
    assert 'id="cv"' in anim, "动画栏内未找到 #cv"

    head = '<!-- 单栏动画版：仅保留「动画演示」栏目（题图/解析/知识点入口已移除） -->\n'
    new_seg = head + anim
    s = s[:ws] + new_seg + s[we:]

    # ---------- ② 画布 CSS 尺寸固定 ----------
    old_css = "  canvas{width:100%;height:auto;display:block;background:#fff;border:1px solid var(--line);\n" \
              "         border-radius:8px;touch-action:none}"
    assert s.count(old_css) == 1, "canvas 基础样式锚点不唯一"
    new_css = ("  /* 单栏动画版：画布固定为 %d×%d，居中显示（resize() 内部会按 clientWidth 与\n"
               "     0.66 重算像素尺寸，故此处的 CSS 宽度即为呈现宽度，比例与原版一致） */\n"
               "  canvas{width:%dpx;max-width:100%%;height:auto;display:block;background:#fff;\n"
               "         border:1px solid var(--line);border-radius:8px;touch-action:none;margin:0 auto}"
               % (CV_W, CV_H, CV_W))
    s = s.replace(old_css, new_css, 1)

    # ---------- ③ 追加单栏居中布局样式 ----------
    extra = """
  /* ====== 单栏动画版专用布局 ====== */
  /* 原版三栏为 .wrap{flex-wrap:wrap} 中 1 + 2 + 1.3 的比例；只剩一栏时 flex 会
     把它拉满整页宽度（画布随之被放大失真），故此处改为「定宽 + 水平居中」。 */
  .wrap{flex-direction:column;align-items:center;padding:18px 14px 28px}
  .col-animation{flex:0 0 auto;width:100%;max-width:__MAXW__px;min-width:0;
                 position:static;margin:0 auto}
  .col-animation .controls{justify-content:center}
  @media (max-width:760px){
    .col-animation{max-width:100%}
    canvas{width:100%}
  }
""".replace("__MAXW__", str(CV_W + 24))
    anchor = "</style>"
    assert s.count(anchor) == 1, "</style> 锚点不唯一"
    s = s.replace(anchor, extra + anchor, 1)

    # ---------- ④ 关闭左/中栏渲染（保留动画所需的一切） ----------
    for fn in ("renderProblem", "renderSteps", "renderInlineKnowledgeCards",
               "renderDrawer", "bindDrawer"):
        pat = re.compile(r"^(%s\(\);)$" % fn, re.M)
        assert len(pat.findall(s)) == 1, "%s(); 调用锚点不唯一" % fn
        s = pat.sub(lambda m: "/* 单栏动画版：已移除左/中栏，无需 %s */" % m.group(1)[:-2], s, count=1)

    # ---------- ⑤ 清理：清空题图后补画题图的那一步也不再需要 ----------
    old_draw = """/* 关键修复：renderProblem() 之后题图 <canvas class="fig-canvas"> 才被创建，
   必须在此补画一次，否则独立打开 HTML（无 resize 事件）时题图永远空白。 */
drawFigures();"""
    assert s.count(old_draw) == 1, "drawFigures 补画锚点不唯一"
    s = s.replace(old_draw,
                  "/* 单栏动画版：左栏题图已移除，无需再补画 drawFigures() */", 1)

    io.open(OUT, "w", encoding="utf-8", newline="\n").write(s)
    print("OK -> %s (%d bytes)" % (OUT, len(s.encode("utf-8"))))

    probes = [
        ('<section class="col col-animation">', "保留动画栏"),
        ('id="cv"', "交互动画画布"),
        ('id="slider"', "时间轴"),
        ('id="play"', "播放按钮"),
        ('id="panelData"', "实时数据面板"),
        ("width:%dpx" % CV_W, "画布固定宽度 CSS"),
        ("justify-content:center", "控件居中"),
        ('<section class="col col-problem">', "左栏应已移除（MISSING 才对）"),
    ]
    for p, desc in probes:
        print("  probe %-34s : %s" % (desc, "FOUND" if p in s else "MISSING"))


if __name__ == "__main__":
    main()
