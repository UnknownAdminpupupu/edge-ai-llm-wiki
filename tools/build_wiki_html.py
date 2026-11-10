#!/usr/bin/env python3
"""把 wiki/*.md、raw/*.md、log、schema 打包成一個可瀏覽的單頁 HTML Wiki。

用法：python3 tools/build_wiki_html.py <專案根目錄> <輸出 html>
"""
import html
import json
import math
import re
import sys
from pathlib import Path

import markdown

root = Path(sys.argv[1])
out = Path(sys.argv[2])
wiki = root / "wiki"

GROUPS = [
    ("概念", ["edge-ai", "cloud-vs-edge", "training-vs-inference", "edge-intelligence-levels"]),
    ("技術", ["model-compression", "pruning", "quantization", "tinyml-mcunet", "federated-learning"]),
    ("支撐", ["edge-hardware", "inference-kpis", "use-cases", "misconceptions", "glossary", "sources"]),
]
GROUP_OF = {p: g for g, ps in GROUPS for p in ps}
LINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


def title_of(text):
    m = re.search(r"^# (.+)$", text, re.M)
    return m.group(1).strip() if m else "?"


pages = {p.stem: p.read_text(encoding="utf-8") for p in wiki.glob("*.md")}
titles = {k: title_of(v) for k, v in pages.items()}


def render(md_text):
    def link(m):
        t = m.group(1)
        return f'<a class="wl" href="#{t}">{html.escape(titles.get(t, t))}</a>'

    md_text = LINK_RE.sub(link, md_text)
    h = markdown.markdown(md_text, extensions=["tables", "fenced_code"])
    h = re.sub(r"［(S\d)］", lambda m: f'<a class="tag" href="#raw-{m.group(1).lower()}">{m.group(1)}</a>', h)
    h = h.replace("［整理］", '<span class="tag syn" title="由多個來源整理，未含具體數字">整理</span>')
    h = re.sub(r"(https://[^\s<]+)", r'<a href="\1" target="_blank" rel="noopener">\1</a>', h)
    h = re.sub(r'<pre><code class="language-mermaid">(.*?)</code></pre>', r'<pre class="mermaid">\1</pre>', h, flags=re.S)
    return h


# 關係圖：節點 = wiki 頁，邊 = [[連結]]（略過 index/log）
nodes = [p for _, ps in GROUPS for p in ps]
edges = set()
for name in nodes:
    for t in LINK_RE.findall(pages[name]):
        if t in nodes and t != name:
            edges.add(tuple(sorted((name, t))))
W, H, R = 760, 460, 175
pos = {}
for i, n in enumerate(nodes):
    a = -math.pi / 2 + 2 * math.pi * i / len(nodes)
    pos[n] = (W / 2 + R * 1.25 * math.cos(a), H / 2 + R * math.sin(a))
svg = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="wiki 頁面關係圖">']
for a, b in sorted(edges):
    (x1, y1), (x2, y2) = pos[a], pos[b]
    svg.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" class="edge"/>')
for n in nodes:
    x, y = pos[n]
    deg = sum(1 for e in edges if n in e)
    r = 5 + deg * 0.9
    g = {"概念": "g1", "技術": "g2", "支撐": "g3"}[GROUP_OF[n]]
    anchor = "start" if x > W / 2 + 5 else ("end" if x < W / 2 - 5 else "middle")
    dx = 10 if anchor == "start" else (-10 if anchor == "end" else 0)
    dy = 4 if anchor != "middle" else (-12 if y < H / 2 else 20)
    svg.append(
        f'<a href="#{n}"><circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" class="node {g}"/>'
        f'<text x="{x + dx:.1f}" y="{y + dy:.1f}" text-anchor="{anchor}" class="nlabel">{html.escape(re.sub(r"（.*?）", "", titles[n]))}</text></a>'
    )
svg.append("</svg>")

# 統計
fact_lines = sum(len(re.findall(r"［S\d］", pages[n])) for n in nodes)
stats = {"pages": len(nodes), "sources": len(list((root / "raw").glob("S*.md"))), "edges": len(edges), "facts": fact_lines}

sections = []
home = f"""
<p class="lede">這是一個用 LLM 維護的知識庫：6 篇原始來源經過「先討論、後寫入」的 ingest，整理成 {stats['pages']} 個互相連結的頁面。每一句事實後面都有來源標記，點下去可以看到原始筆記。</p>
<p class="hint">用這個 wiki 做出的教學簡報：<a href="https://claude.ai/artifact/1o8METKZk88rmiNDqZ7dYr" target="_blank" rel="noopener">Edge AI 入門（HTML 簡報）</a>　·　流程設計：<a class="wl" href="#talk-f">Loop／Graph 設計 v1 → v2</a>　·　<a class="wl" href="#log">執行紀錄</a></p>
<div class="stats">
  <div><b>{stats['sources']}</b><span>原始來源</span></div>
  <div><b>{stats['pages']}</b><span>wiki 頁面</span></div>
  <div><b>{stats['edges']}</b><span>頁面連結</span></div>
  <div><b>{stats['facts']}</b><span>來源標記</span></div>
</div>
<h2>頁面關係圖</h2>
<p class="hint">點圓點開啟頁面。圓點越大，代表跟越多頁相連。<span class="lg g1">概念</span><span class="lg g2">技術</span><span class="lg g3">支撐</span></p>
<div class="graph">{''.join(svg)}</div>
<h2>三層架構</h2>
<table><thead><tr><th>層</th><th>內容</th><th>規則</th></tr></thead><tbody>
<tr><td>raw/</td><td>6 篇來源的摘錄筆記</td><td>建立後不改，記 URL 與讀取日期</td></tr>
<tr><td>wiki/</td><td>{stats['pages']} 個概念頁＋索引＋紀錄</td><td>每句事實要有 S 編號，數字要能在 raw 找到</td></tr>
<tr><td>schema</td><td>CLAUDE.md</td><td>頁面格式、衝突與舊資料的處理方式</td></tr>
</tbody></table>
"""
sections.append(("home", "Edge AI 知識庫", home))
for _, ps in GROUPS:
    for p in ps:
        sections.append((p, titles[p], render(re.sub(r"^# .+\n", "", pages[p], count=1))))
for f in sorted((root / "raw").glob("S*.md")):
    sid = f.name.split("-")[0].lower()
    t = f.read_text(encoding="utf-8")
    sections.append((f"raw-{sid}", title_of(t), render(re.sub(r"^# .+\n", "", t, count=1))))
sections.append(("log", "執行紀錄 log.md", render(re.sub(r"^# .+\n", "", pages["log"], count=1))))
sections.append(("schema", "Schema（CLAUDE.md）", render(re.sub(r"^# .+\n", "", (root / "CLAUDE.md").read_text(encoding="utf-8"), count=1))))
for f in sorted((root / "discussion").glob("*.md")):
    sid = "talk-" + f.name.split("-")[0].lower()
    t = f.read_text(encoding="utf-8")
    sections.append((sid, title_of(t), render(re.sub(r"^# .+\n", "", t, count=1))))

CHECKS = [
    ("lint_run1_pass1", "Run1 Wiki Lint 第 1 次"), ("lint_run1_pass2", "Run1 Wiki Lint 第 2 次"), ("lint_run1_pass4", "Run1 Wiki Lint 最終"),
    ("slides_run1_pass1", "Run1 簡報檢查 第 1 次"), ("slides_run1_pass2", "Run1 簡報檢查 第 2 次"),
    ("outline_run2_pass1", "Run2 大綱檢查 第 1 次"), ("outline_run2_pass2", "Run2 大綱檢查 第 2 次"),
    ("slides_run2_pass1", "Run2 逐句檢查 第 1 次"), ("slides_run2_pass2", "Run2 逐句檢查 第 2 次"), ("warn_review_run2", "Run2 WARN 人工複查"),
]
for stem, label in CHECKS:
    f = root / "checks" / f"{stem}.md"
    if f.exists():
        t = f.read_text(encoding="utf-8")
        sections.append(("chk-" + stem.replace("_", "-"), label, render(re.sub(r"^# .+\n", "", t, count=1))))

nav = ['<a href="#home" class="navhome">首頁與關係圖</a>']
for g, ps in GROUPS:
    nav.append(f'<p class="navg">{g}</p>')
    nav += [f'<a href="#{p}">{html.escape(titles[p])}</a>' for p in ps]
nav.append('<p class="navg">原始來源 raw/</p>')
nav += [f'<a href="#{sid}">{html.escape(t[:26])}</a>' for sid, t, _ in sections if sid.startswith("raw-")]
nav.append('<p class="navg">過程紀錄</p>')
nav += [f'<a href="#{sid}">{html.escape(t[:24])}</a>' for sid, t, _ in sections if sid.startswith("talk-") or sid in ("log", "schema")]
nav.append('<p class="navg">檢查紀錄 checks/</p>')
nav += [f'<a href="#{sid}">{html.escape(t)}</a>' for sid, t, _ in sections if sid.startswith("chk-")]

body = "\n".join(
    f'<section id="p-{sid}" data-page="{sid}"{"" if sid == "home" else " hidden"}><p class="crumb">{"LLM Wiki 首頁" if sid == "home" else ("原始來源" if sid.startswith("raw-") else ("檢查紀錄" if sid.startswith("chk-") else ("過程紀錄" if sid.startswith("talk-") or sid in ("log", "schema") else "Edge AI Wiki")))}</p><h1>{html.escape(t)}</h1>{h}</section>'
    for sid, t, h in sections
)
ids = json.dumps([s[0] for s in sections])

template = (root / "tools" / "wiki_template.html").read_text(encoding="utf-8")
page = template.replace("{{NAV}}", "\n".join(nav)).replace("{{BODY}}", body).replace("{{IDS}}", ids)
out.write_text(page, encoding="utf-8")
print(f"wrote {out} ({len(page)//1024} KB), sections={len(sections)}, edges={len(edges)}")
