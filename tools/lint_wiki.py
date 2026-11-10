#!/usr/bin/env python3
"""N3 Wiki Lint：依 CLAUDE.md 規則檢查 wiki/，輸出 Markdown 報告。

用法：python3 tools/lint_wiki.py <專案根目錄> <報告輸出路徑>
"""
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
out = Path(sys.argv[2])
wiki = root / "wiki"
raw = root / "raw"

SKIP_PAGES = {"index", "log"}
SKIP_SECTIONS = {"來源", "和其他概念的關係"}
TAG_RE = re.compile(r"［(S\d|整理)］")
LINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
NUM_RE = re.compile(r"\d+(?:\.\d+)?")

# 新手可能看不懂、應該在 glossary 定義的術語（出現在 wiki 正文就要有定義）
KEY_TERMS = [
    "激活值", "反向傳播", "前向傳遞", "損失函數", "霍夫曼編碼", "權重共享",
    "k-means", "代表性資料集", "量化感知訓練", "Edge TPU", "GPU", "DRAM",
    "ImageNet", "top-1", "卸載", "全連接層", "卷積層", "浮點數",
]

raw_text = {}
for f in raw.glob("S*.md"):
    raw_text[f.name.split("-")[0]] = f.read_text(encoding="utf-8")

pages = {p.stem: p.read_text(encoding="utf-8") for p in wiki.glob("*.md")}
issues = []  # (類別, 頁面, 說明)

# 1. 壞連結 + 被連結次數
inbound = {name: 0 for name in pages}
for name, text in pages.items():
    for target in LINK_RE.findall(text):
        if target not in pages:
            issues.append(("壞連結", name, f"[[{target}]] 不存在"))
        elif name != "index" and target != name:
            inbound[target] += 1

# 2. 孤兒頁（除了 index 以外沒有任何頁連到它）
for name, n in inbound.items():
    if name not in SKIP_PAGES and n == 0:
        issues.append(("孤兒頁", name, "除了 index 沒有其他頁連到這頁"))

# 3～5. 逐行檢查事實句
for name, text in pages.items():
    if name in SKIP_PAGES:
        continue
    section = ""
    for line in text.splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
            continue
        if not line.startswith("- ") or section in SKIP_SECTIONS:
            continue
        tags = TAG_RE.findall(line)
        if not tags and "［" not in section:
            issues.append(("缺來源標記", name, line[:60]))
            continue
        if "整理" in tags and NUM_RE.search(re.sub(r"\*\*[^*]+\*\*", "", line)):  # run1 修正：粗體術語名稱（如 top-1）不算數字
            issues.append(("［整理］句含數字", name, line[:60]))
        # 數字回查：句中的每個數字都要出現在它引用的 raw 來源裡
        cited = [t for t in tags if t.startswith("S")]
        if not cited:
            continue
        body = TAG_RE.sub("", line)
        body = re.sub(r"https?://\S+", "", body)
        for num in set(NUM_RE.findall(body)):
            if len(num) == 1 and num in "0123456":  # 等級編號等太短的數字略過
                continue
            # run1 修正：原本用子字串比對，「20」會誤配到「2016」；改成數字邊界比對
            pat = re.compile(r"(?<![\d.])" + re.escape(num) + r"(?![\d.])")
            if not any(pat.search(raw_text.get(s, "")) for s in cited):
                issues.append(("數字查無來源", name, f"「{num}」不在 {','.join(cited)}：{line[:50]}"))

# 6. 來源標記必須對應到真的 raw 檔
all_tags = set()
for text in pages.values():
    all_tags.update(t for t in TAG_RE.findall(text) if t.startswith("S"))
for t in sorted(all_tags):
    if t not in raw_text:
        issues.append(("來源不存在", "-", f"{t} 沒有對應的 raw 檔"))

# 7. 衝突標記必須寫出處理方式
for name, text in pages.items():
    if name in SKIP_PAGES:  # run1 修正：log 是紀錄不是正文，不檢查
        continue
    for line in text.splitlines():
        if "⚠️" in line and not re.search(r"採用|不使用|簡報", line):
            issues.append(("衝突未處理", name, line[:60]))

# 8. 術語表覆蓋
glossary = pages.get("glossary", "")
body_all = "\n".join(t for n, t in pages.items() if n not in {"glossary", "log", "sources"})
for term in KEY_TERMS:
    if term in body_all and f"**{term}" not in glossary and f"（{term}" not in glossary:
        where = [n for n, t in pages.items() if term in t and n not in {"glossary", "log"}]
        issues.append(("術語未定義", ",".join(where[:3]), f"「{term}」在正文出現但 glossary 沒有定義"))

# 報告
by_cat = {}
for cat, page, msg in issues:
    by_cat.setdefault(cat, []).append((page, msg))
lines = ["# Wiki Lint 報告", "", f"- 檢查頁數：{len(pages)}", f"- 問題總數：{len(issues)}",
         f"- 結果：{'PASS' if not issues else 'FAIL'}", ""]
for cat, items in by_cat.items():
    lines.append(f"## {cat}（{len(items)}）")
    lines += [f"- `{p}`：{m}" for p, m in items]
    lines.append("")
out.write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
sys.exit(1 if issues else 0)
