# -*- coding: utf-8 -*-
"""把《2026江苏16 双弹簧三球》完整版抽取为单栏「动画演示」页。

与技能自带 scripts/extract_anim_only.py 的差异（本页特有，均已踩坑验证）：
 1. 本页有两个 <style> 块（主样式 + tune-width），所以 </style> 锚点必须用 rfind；
 2. 栏宽上限必须 706（画布 680 + 左右 padding 24 + 边框 2），用 704 会把画布压成 678；
 3. kpToggle 按钮与 kpDrawer 抽屉必须整块删除（否则门禁 kpToggle=0 不过、抽屉还会露出来）；
 4. 删除后补探针，确认无 kpSearch / kpClose / </aside> 残留。
"""
import io
import os
import re

LAB = r'C:/Users/19368/Desktop/physics-animator-lab'
SRC = os.path.join(LAB, '2026江苏16_双弹簧三球_教学动画.html')
OUT = os.path.join(LAB, '2026江苏16_双弹簧三球_动画演示.html')

CV_W = 680
COL_MAX = 706          # 680 + 12*2 padding + 1*2 border


def find_wrap(s):
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


s = io.open(SRC, encoding="utf-8").read()

# ---------- ① 只保留动画栏 ----------
ws, we = find_wrap(s)
seg = s[ws:we]
cs = seg.index('<section class="col col-animation">')
ce = seg.index("</section>", cs) + len("</section>")
anim = seg[cs:ce]
assert 'id="cv"' in anim, "动画栏内未找到 #cv"
# ⚠ .wrap 外壳必须保留（直接删 ⇒ 审计 .wrap > section.col 计 0）
s = (s[:ws] + '<div class="wrap">\n<!-- 单栏动画版：仅保留「动画演示」栏目 -->\n'
     + anim + '\n</div>' + s[we:])

# ---------- ② 画布固定宽 ----------
old_css = "  canvas{width:100%;height:auto;display:block;background:#fff;border:1px solid var(--line);\n" \
          "         border-radius:8px;touch-action:none}"
assert s.count(old_css) == 1, "canvas 基础样式锚点不唯一"
new_css = ("  /* 单栏动画版：画布固定 680px 宽（边框 1px ⇒ clientWidth = 678） */\n"
           "  canvas{width:%dpx;max-width:100%%;height:auto;display:block;background:#fff;\n"
           "         border:1px solid var(--line);border-radius:8px;touch-action:none;margin:0 auto}"
           % CV_W)
s = s.replace(old_css, new_css, 1)

# ---------- ③ 追加单栏布局样式（多 style 块 ⇒ 用 rfind） ----------
extra = """
  /* ====== 单栏动画版专用布局 ====== */
  .wrap{flex-direction:column;align-items:center;padding:18px 14px 28px}
  .col-animation{flex:0 0 auto;width:100%;max-width:__MAXW__px;min-width:0;
                 position:static;margin:0 auto}
  .col-animation .controls{justify-content:center}
  @media (max-width:760px){
    .col-animation{max-width:100%}
    canvas{width:100%}
  }
""".replace("__MAXW__", str(COL_MAX))
pos = s.rfind("</style>")
assert pos > 0
s = s[:pos] + extra + s[pos:]

# ---------- ④ 关闭左/中栏渲染 ----------
for fn in ("renderProblem", "renderSteps", "renderInlineKnowledgeCards",
           "renderDrawer", "bindDrawer"):
    pat = re.compile(r"^(%s\(\);)$" % fn, re.M)
    assert len(pat.findall(s)) == 1, "%s(); 调用锚点不唯一" % fn
    s = pat.sub(lambda m: "/* 单栏动画版：已移除左/中栏，无需 %s */" % m.group(1)[:-2], s, count=1)

# ---------- ⑤ 题图补画步骤不再需要 ----------
pat = re.compile(r"^drawFigures\(\);$", re.M)
assert len(pat.findall(s)) == 1, "drawFigures 补画锚点不唯一"
s = pat.sub(lambda m: "/* 单栏动画版：左栏题图已移除，无需再补画 drawFigures() */", s, count=1)

# ---------- ⑥ 整块删掉知识点浮钮与抽屉 ----------
n_btn = len(re.findall(r'<button id="kpToggle"[^>]*>.*?</button>\s*\n', s))
s = re.sub(r'<button id="kpToggle"[^>]*>.*?</button>\s*\n', '', s)
n_dw = len(re.findall(r'<aside id="kpDrawer"[\s\S]*?</aside>', s))
s = re.sub(r'<aside id="kpDrawer"[\s\S]*?</aside>\s*\n', '', s)
print('删除 kpToggle 按钮 %d 处，kpDrawer 抽屉 %d 处' % (n_btn, n_dw))

io.open(OUT, "w", encoding="utf-8", newline="\n").write(s)
print("OK -> %s (%d bytes)" % (OUT, len(s.encode("utf-8"))))

probes = [
    ('<section class="col col-animation">', "保留动画栏", True),
    ('id="cv"', "动画画布", True),
    ('id="slider"', "时间轴", True),
    ('id="play"', "播放按钮", True),
    ('id="panelData"', "数据面板", True),
    ('width:%dpx' % CV_W, "画布固定宽度", True),
    ('max-width:%dpx' % COL_MAX, "栏宽上限 706", True),
    ('<section class="col col-problem">', "左栏已移除", False),
    ('id="kpToggle"', "kpToggle 元素已删", False),
    ('id="kpDrawer"', "kpDrawer 元素已删", False),
    ('id="kpSearch"', "kpSearch 元素已删", False),
    ('id="kpClose"', "kpClose 元素已删", False),
    ('</aside>', "aside 无残留", False),
    ('<button id="kpToggle"', "浮钮 DOM 已删", False),
    ('^drawFigures();', "drawFigures 补画已删", False),
]
bad = 0
for p, desc, want in probes:
    got = p in s
    ok = (got == want)
    bad += 0 if ok else 1
    print("  %s %-26s %s" % ("PASS" if ok else "FAIL", desc,
                             "FOUND" if got else "MISSING"))
if bad:
    raise SystemExit("单栏抽取探针未通过：%d 项" % bad)
print("全部探针通过")
