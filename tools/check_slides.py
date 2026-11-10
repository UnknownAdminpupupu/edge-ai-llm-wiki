#!/usr/bin/env python3
"""N6 內容檢查：簡報每一頁都要能追溯到 wiki。

檢查項目
 (a) 對應：每頁 data-wiki 列出的 wiki 頁都存在
 (b) 數字：頁面上的每個數字都要出現在它對應的 wiki 頁裡（數字邊界比對）
 (c) 術語：glossary 中的術語第一次出現在簡報時，必須用 <dfn> 解釋
 (d) 密度：一頁正文不超過 MAX_CHARS 字、每個清單不超過 5 點

用法：python3 tools/check_slides.py <專案根目錄> <簡報 html> <報告輸出>
"""
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup

root, deck, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
MAX_CHARS = 260
NUM_RE = re.compile(r"\d+(?:\.\d+)?")
META_CLASSES = ["src", "notes", "eyebrow", "who", "help", "refs"]  # run1 修正：參考文獻清單不算教學密度

wiki = {p.stem: p.read_text(encoding="utf-8") for p in (root / "wiki").glob("*.md")}

# glossary 術語：**中文（English）** → 中文與英文都算同一個術語
terms = []
for m in re.finditer(r"\*\*([^*]+)\*\*", wiki["glossary"]):
    name = m.group(1)
    zh = re.sub(r"（.*?）", "", name).strip()
    en = re.findall(r"（(.*?)）", name)
    terms.append((zh, [zh] + en))

soup = BeautifulSoup(deck.read_text(encoding="utf-8"), "html.parser")
slides = soup.select("section.slide")
rows = []  # (頁, 檢查, 結果, 說明)
seen_terms = set()

for i, s in enumerate(slides, 1):
    refs = [r for r in s.get("data-wiki", "").split(",") if r]
    # (a)
    missing = [r for r in refs if r not in wiki]
    rows.append((i, "a 對應", "FAIL" if (missing or not refs) else "PASS",
                 f"找不到 {missing}" if missing else ("沒有 data-wiki" if not refs else ",".join(refs))))
    body = BeautifulSoup(str(s), "html.parser")
    for c in META_CLASSES:
        for el in body.select("." + c):
            el.decompose()
    text = body.get_text(" ", strip=True)
    # (b)
    ref_text = "\n".join(wiki[r] for r in refs if r in wiki)
    bad = []
    for num in sorted(set(NUM_RE.findall(text)), key=lambda x: float(x)):
        if len(num) == 1:  # 單一位數多半是編號（1. 2. L3），略過
            continue
        pat = re.compile(r"(?<![\d.])" + re.escape(num) + r"(?![\d.])")
        if not pat.search(ref_text):
            bad.append(num)
    rows.append((i, "b 數字", "FAIL" if bad else "PASS", f"wiki 查無：{bad}" if bad else "全部可追溯"))
    # (c)
    dfn_text = " ".join(d.get_text() for d in s.select("dfn"))
    undefined = []
    for zh, aliases in terms:
        if zh in seen_terms:
            continue
        hit = next((a for a in aliases if a and a in text), None)
        if hit:
            seen_terms.add(zh)
            if not any(a in dfn_text for a in aliases if a):
                undefined.append(hit)
    rows.append((i, "c 術語", "FAIL" if undefined else "PASS", f"首次出現未解釋：{undefined}" if undefined else "OK"))
    # (d)
    chars = len(re.sub(r"\s", "", text))
    longest = max((len(ul.find_all("li", recursive=False)) for ul in s.select("ul:not(.refs)")), default=0)
    ok = chars <= MAX_CHARS and longest <= 5
    rows.append((i, "d 密度", "PASS" if ok else "FAIL", f"{chars} 字、最長清單 {longest} 點"))

fails = [r for r in rows if r[2] == "FAIL"]
lines = ["# 簡報內容檢查報告（N6）", "", f"- 投影片數：{len(slides)}",
         f"- 檢查項次：{len(rows)}，FAIL：{len(fails)}", f"- 結果：{'PASS' if not fails else 'FAIL'}", "",
         "| 頁 | 檢查 | 結果 | 說明 |", "|---|---|---|---|"]
lines += [f"| {a} | {b} | {c} | {d} |" for a, b, c, d in rows if c == "FAIL"]
lines += ["", f"（PASS 的 {len(rows) - len(fails)} 項省略）"]
out.write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
sys.exit(1 if fails else 0)
