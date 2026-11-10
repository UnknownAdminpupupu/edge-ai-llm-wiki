#!/usr/bin/env python3
"""Workflow v2 的 N6：逐句對事實卡檢查（取代 v1『整頁數字比對』）。

每個「論點元素」（清單項、卡片段落、導言、表格列、圖、測驗題）都要有 data-fact：
  - 事實 id（空白分隔），必須屬於這頁的事實卡；或
  - "frame"：引導句／比喻，不得含數字
檢查
 (a) 標記：論點元素都有 data-fact，id 都在這頁事實卡裡
 (b) 數字：論點裡的數字必須出現在『它引用的那幾句』wiki 原句裡（不再是整頁）
 (c) 對應強度：論點與引用原句的字元雙字組重疊率 < 0.2 → WARN，列入人工複查
 (d) 術語：第一次出現要用 <dfn>；事實卡 avoid 的術語不得出現
 (e) 密度：正文 ≤ 260 字、清單 ≤ 5 點

用法：python3 tools/check_slides_v2.py <專案根目錄> <factcards.json> <簡報 html> <報告>
"""
import json
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).parent))
from factlib import glossary_terms, load_wiki, resolve  # noqa: E402

root, cards_path, deck, out = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4])
wiki = load_wiki(root)
terms = glossary_terms(wiki)
cards = {c["n"]: c for c in json.loads(cards_path.read_text(encoding="utf-8"))["slides"]}
NUM_RE = re.compile(r"\d+(?:\.\d+)?")
CLAIM_SEL = ".pts > li:not(.refs li), .myth > p, .card > p, .lead, .big, table.grid tbody tr, svg.diagram, .bars, .q"
META = ["src", "notes", "eyebrow", "who", "help", "refs"]


def clean(t):
    return re.sub(r"\s+", " ", t).strip()


def bigrams(t):
    t = re.sub(r"[\s\W_]", "", t)
    return {t[i:i + 2] for i in range(len(t) - 1)}


soup = BeautifulSoup(Path(deck).read_text(encoding="utf-8"), "html.parser")
rows, warns, seen = [], [], set()
for i, s in enumerate(soup.select("section.slide"), 1):
    card = cards.get(i, {"facts": [], "avoid": []})
    allowed = set(card["facts"])
    for el in s.select(CLAIM_SEL):
        if el.find_parent(class_="refs") or (el.name == "p" and el.find_parent("div", class_="q")):
            continue
        text = clean(el.get_text(" "))
        tag = el.get("data-fact")
        if not tag:
            rows.append((i, "a 標記", f"沒有 data-fact：{text[:30]}"))
            continue
        if tag == "frame":
            if NUM_RE.search(text):
                rows.append((i, "b 數字", f"frame 句含數字：{text[:30]}"))
            continue
        ids = tag.split()
        stray = [f for f in ids if f not in allowed]
        if stray:
            rows.append((i, "a 標記", f"{stray} 不在這頁事实卡：{text[:24]}".replace("事实", "事實")))
        src = "\n".join(filter(None, (resolve(wiki, f) for f in ids)))
        if not src:
            rows.append((i, "a 標記", f"{ids} 解析不到原句"))
            continue
        for num in set(NUM_RE.findall(re.sub(r"^\d+\.\s", "", text))):  # 題號不算
            if len(num) == 1 and el.name in ("tr",):
                continue
            if not re.search(r"(?<![\d.])" + re.escape(num) + r"(?![\d.])", src):
                rows.append((i, "b 數字", f"「{num}」不在引用句 {ids}：{text[:30]}"))
        bg = bigrams(text)
        if bg:
            ratio = len(bg & bigrams(src)) / len(bg)
            if ratio < 0.2:
                warns.append((i, f"{ratio:.2f}", ids, text[:40]))
    # (d) 術語
    body = BeautifulSoup(str(s), "html.parser")
    for c in META:
        for el in body.select("." + c):
            el.decompose()
    text = body.get_text(" ", strip=True)
    dfn_text = " ".join(d.get_text() for d in s.select("dfn"))
    for zh, aliases in terms:
        hit = next((a for a in aliases if a in text), None)
        if zh in card.get("avoid", []) and hit:
            rows.append((i, "d 術語", f"刻意避免的「{zh}」出現了"))
        if zh in seen or not hit:
            continue
        seen.add(zh)
        if not any(a in dfn_text for a in aliases):
            rows.append((i, "d 術語", f"「{hit}」首次出現未解釋"))
    chars = len(re.sub(r"\s", "", text))
    longest = max((len(ul.find_all("li", recursive=False)) for ul in s.select("ul:not(.refs)")), default=0)
    if chars > 260 or longest > 5:
        rows.append((i, "e 密度", f"{chars} 字、最長清單 {longest} 點"))

lines = ["# 簡報內容檢查報告 v2（逐句對事實卡）", "", f"- FAIL：{len(rows)}　WARN（需人工複查）：{len(warns)}",
         f"- 結果：{'PASS' if not rows else 'FAIL'}", "", "## FAIL", "| 頁 | 檢查 | 說明 |", "|---|---|---|"]
lines += [f"| {a} | {b} | {c} |" for a, b, c in rows] or ["| - | - | 無 |"]
lines += ["", "## WARN：論點和引用原句字面重疊低（< 0.2），請人工確認意思一致", "| 頁 | 重疊率 | 引用 | 論點 |", "|---|---|---|---|"]
lines += [f"| {a} | {b} | {' '.join(c)} | {d} |" for a, b, c, d in warns] or ["| - | - | - | 無 |"]
out.write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
sys.exit(1 if rows else 0)
