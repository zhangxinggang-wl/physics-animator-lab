# -*- coding: utf-8 -*-
"""
physics-animator-lab 一键发布
------------------------------------------------
1. 扫描项目根目录下的 *.html 动画
2. 重新生成 index.html 索引首页（搜索 + 按年份筛选）
3. 自动 commit 并 push 到 GitHub（Pages 随即自动刷新）

用法：
    双击「一键发布.bat」           生成索引并推送
    python deploy.py               同上
    python deploy.py --dry-run     只生成索引，不提交不推送
"""

import os
import re
import sys
import html
import datetime
import subprocess

REPO = os.path.dirname(os.path.abspath(__file__))
SITE_URL = "https://zhangxinggang-wl.github.io/physics-animator-lab/"
KIND_ORDER = ["动画演示", "教学动画"]

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


# ---------------------------------------------------------------- 索引生成
def collect():
    items = []
    for name in os.listdir(REPO):
        if not name.lower().endswith(".html") or name.lower() == "index.html":
            continue
        stem = name[:-5]
        head, _, ver = stem.rpartition("_")
        if not head:
            head, ver = stem, ""
        if "教学" in ver:
            kind = "教学动画"
        elif "演示" in ver:
            kind = "动画演示"
        else:
            kind = ver or "动画"
        m = re.match(r"^(\d{4})", head)
        items.append({
            "file": name,
            "head": head,
            "kind": kind,
            "year": m.group(1) if m else "其他",
        })
    return items


def build_index():
    items = collect()
    groups, order = {}, []
    for it in items:
        if it["head"] not in groups:
            groups[it["head"]] = {"year": it["year"], "files": {}}
            order.append(it["head"])
        groups[it["head"]]["files"][it["kind"]] = it["file"]

    cards = []
    for head in order:
        g = groups[head]
        parts = head.split("_")
        no = parts[0]
        title = " ".join(parts[1:]) if len(parts) > 1 else head
        btns = []
        kinds = KIND_ORDER + [k for k in g["files"] if k not in KIND_ORDER]
        for k in kinds:
            if k in g["files"]:
                cls = "b1" if k == "动画演示" else "b2"
                btns.append('<a class="%s" href="%s">%s</a>'
                            % (cls, html.escape(g["files"][k]), html.escape(k)))
        cards.append(
            '<div class="card" data-k="{k}" data-y="{y}">'
            '<div class="no">{no}</div><div class="tt">{tt}</div>'
            '<div class="btns">{b}</div></div>'.format(
                k=html.escape((head + " " + title).lower()),
                y=html.escape(g["year"]), no=html.escape(no),
                tt=html.escape(title), b="".join(btns)))

    years = sorted({g["year"] for g in groups.values()})
    year_btns = "".join('<button class="yb" data-y="%s">%s</button>' % (y, y)
                        for y in years if y != "其他")
    today = datetime.date.today().strftime("%Y-%m-%d")

    page = TEMPLATE
    page = page.replace("__CARDS__", "\n".join(cards))
    page = page.replace("__YEARBTNS__", year_btns)
    page = page.replace("__NQ__", str(len(groups)))
    page = page.replace("__NA__", str(len(items)))
    page = page.replace("__TODAY__", today)
    return page, len(groups), len(items)


# ---------------------------------------------------------------- git 操作
def git(args, timeout=None):
    return subprocess.run(
        ["git"] + args, cwd=REPO,
        env=dict(os.environ, GIT_TERMINAL_PROMPT="0"),
        capture_output=True, text=True, encoding="utf-8",
        errors="replace", timeout=timeout)


def main():
    dry = "--dry-run" in sys.argv

    if not os.path.isdir(os.path.join(REPO, ".git")):
        print("[错误] 当前目录不是 git 仓库：", REPO)
        return 1

    # 换机器时补上必要的 git 配置
    if not git(["config", "--get", "user.name"]).stdout.strip():
        git(["config", "user.name", "zhangxinggang-wl"])
    if not git(["config", "--get", "user.email"]).stdout.strip():
        git(["config", "user.email", "zhangxinggang-wl@users.noreply.github.com"])
    if not git(["config", "--get", "http.proxy"]).stdout.strip():
        git(["config", "http.proxy", "http://127.0.0.1:7897"])
        git(["config", "http.version", "HTTP/1.1"])
        git(["config", "http.schannelCheckRevoke", "false"])

    print("扫描目录:", REPO)
    page, n_q, n_a = build_index()

    idx = os.path.join(REPO, "index.html")
    old = ""
    if os.path.exists(idx):
        with open(idx, "r", encoding="utf-8") as f:
            old = f.read()
    changed_index = (old != page)
    if changed_index:
        with open(idx, "w", encoding="utf-8", newline="\n") as f:
            f.write(page)
        print("index.html 已更新：%d 道试题 / %d 个动画" % (n_q, n_a))
    else:
        print("index.html 无变化：%d 道试题 / %d 个动画" % (n_q, n_a))

    nj = os.path.join(REPO, ".nojekyll")
    if not os.path.exists(nj):
        open(nj, "w").close()
        print("已补上 .nojekyll")

    print("暂存改动 ...", flush=True)
    r = git(["add", "-A"])
    if r.returncode != 0:
        print("[错误] git add 失败：")
        print((r.stderr or "")[-800:])
        return 1

    staged = git(["diff", "--cached", "--name-only"])
    names = [x for x in staged.stdout.splitlines() if x.strip()]
    if not names:
        print("\n没有需要提交的改动，仓库已是最新。")
        print("线上地址:", SITE_URL)
        return 0

    print("本次改动 %d 个文件：" % len(names))
    for n in names[:15]:
        print("   ", n)
    if len(names) > 15:
        print("    ...另有 %d 个" % (len(names) - 15))

    if dry:
        print("\n[dry-run] 已生成索引但未提交、未推送。")
        return 0

    msg = "chore: 更新动画索引（%s，%d 题 / %d 动画）" % (
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), n_q, n_a)
    r = git(["commit", "-q", "-m", msg])
    if r.returncode != 0:
        print("[错误] 提交失败：")
        print((r.stderr or "")[-800:])
        return 1
    print("已提交:", msg)

    print("正在推送到 GitHub ...", flush=True)
    try:
        r = git(["push", "origin", "main"], timeout=1800)
    except subprocess.TimeoutExpired:
        print("[错误] 推送超时（30 分钟），请检查网络或代理。")
        return 1
    if r.returncode != 0:
        print("[错误] 推送失败：")
        print(((r.stderr or "") + (r.stdout or ""))[-1000:])
        print("\n提示：本机 git 需要经代理 127.0.0.1:7897 才能连 github.com，")
        print("      请确认 Clash 等代理软件已开启后重试。")
        return 1

    print("\n发布成功！")
    print("仓库地址:", "https://github.com/zhangxinggang-wl/physics-animator-lab")
    print("学生访问:", SITE_URL)
    print("Pages 通常 30-60 秒内自动刷新，如未更新请稍等或强制刷新（Ctrl+F5）。")
    return 0


TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>高中物理试题动画演示库</title>
<style>
:root{--bg:#f6f7f9;--fg:#1f2328;--mut:#6b7280;--line:#e4e7ec;--acc:#2f6feb}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);
font-family:"Microsoft YaHei","微软雅黑","PingFang SC","Hiragino Sans GB",system-ui,sans-serif;
line-height:1.6}
header{background:linear-gradient(135deg,#2f6feb,#1a4fb8);color:#fff;padding:34px 20px 28px}
.wrap{max-width:1180px;margin:0 auto}
h1{margin:0 0 8px;font-size:26px;font-weight:600;letter-spacing:.5px}
.sub{opacity:.9;font-size:14px}
.stat{margin-top:14px;font-size:14px;opacity:.95}
.stat b{font-size:19px;padding:0 3px}
.bar{position:sticky;top:0;z-index:9;background:rgba(246,247,249,.96);
backdrop-filter:blur(8px);border-bottom:1px solid var(--line);padding:12px 20px}
.bar .wrap{display:flex;gap:10px;flex-wrap:wrap;align-items:center}
#q{flex:1;min-width:200px;padding:9px 13px;border:1px solid var(--line);border-radius:8px;
font-size:14px;outline:none;background:#fff}
#q:focus{border-color:var(--acc);box-shadow:0 0 0 3px rgba(47,111,235,.12)}
.yb{padding:7px 13px;border:1px solid var(--line);background:#fff;border-radius:7px;
font-size:13px;cursor:pointer;color:var(--mut)}
.yb:hover{border-color:var(--acc);color:var(--acc)}
.yb.on{background:var(--acc);border-color:var(--acc);color:#fff}
main{padding:22px 20px 60px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:13px}
.card{background:#fff;border:1px solid var(--line);border-radius:11px;padding:14px 15px;
transition:.18s;display:flex;flex-direction:column;gap:9px}
.card:hover{box-shadow:0 5px 18px rgba(20,40,90,.09);transform:translateY(-1px);
border-color:#cfd8e6}
.no{font-size:12px;color:var(--mut);font-weight:600;letter-spacing:.4px}
.tt{font-size:15px;font-weight:600;flex:1}
.btns{display:flex;gap:8px;flex-wrap:wrap}
.btns a{flex:1;text-align:center;text-decoration:none;padding:7px 10px;border-radius:7px;
font-size:13px;font-weight:600;white-space:nowrap}
.b1{background:var(--acc);color:#fff}
.b1:hover{background:#1a4fb8}
.b2{background:#eaf1ff;color:#1a4fb8}
.b2:hover{background:#dbe7ff}
footer{border-top:1px solid var(--line);padding:20px;text-align:center;
font-size:12px;color:var(--mut)}
.empty{text-align:center;color:var(--mut);padding:40px 0;display:none}
@media(max-width:520px){h1{font-size:21px}.grid{grid-template-columns:1fr}}
</style>
</head>
<body>
<header><div class="wrap">
<h1>高中物理试题动画演示库</h1>
<div class="sub">单文件 HTML · 无广告无外链 · 点击即播，支持手机与电脑</div>
<div class="stat">共 <b>__NQ__</b> 道试题 · <b>__NA__</b> 个动画（动画演示 / 教学动画两种版本）</div>
</div></header>
<div class="bar"><div class="wrap">
<input id="q" type="search" placeholder="搜索题号、省份或考点，例如：2024 湖南、磁场、回旋加速器">
<button class="yb on" data-y="all">全部</button>
__YEARBTNS__
</div></div>
<main><div class="wrap">
<div class="grid" id="grid">
__CARDS__
</div>
<div class="empty" id="empty">没有匹配的试题</div>
</div></main>
<footer>物理动画教学资源 · __TODAY__ 更新</footer>
<script>
var q=document.getElementById('q'),cards=[].slice.call(document.querySelectorAll('.card')),
empty=document.getElementById('empty'),curY='all';
function apply(){
  var k=q.value.trim().toLowerCase(),n=0;
  cards.forEach(function(c){
    var okY=(curY==='all'||c.dataset.y===curY);
    var okK=!k||c.dataset.k.indexOf(k)>-1;
    var show=okY&&okK;
    c.style.display=show?'':'none';
    if(show)n++;
  });
  empty.style.display=n?'none':'block';
}
q.addEventListener('input',apply);
[].slice.call(document.querySelectorAll('.yb')).forEach(function(b){
  b.addEventListener('click',function(){
    document.querySelectorAll('.yb').forEach(function(x){x.classList.remove('on')});
    b.classList.add('on');curY=b.dataset.y;apply();
  });
});
</script>
</body></html>"""


if __name__ == "__main__":
    sys.exit(main())
