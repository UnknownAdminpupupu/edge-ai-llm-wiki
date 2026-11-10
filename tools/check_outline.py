#!/usr/bin/env python3
"""Workflow v2 新增節點 N4.5：在『生成簡報之前』檢查大綱的事實卡。

 (1) 每個事實 id 都能在 wiki 找到原句
 (2) 術語順序：某頁事實裡用到的 glossary 術語，必須在這頁或更早的頁被『教過』(introduces)
 (3) 每個 introduces 的術語都真的存在 glossary

用法：python3 tools/check_outline.py <專案根目錄> <factcards.json> <報告>
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from factlib import glossary_terms, load_wiki, resolve  # noqa: E402

root, cards_path, out = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
wiki = load_wiki(root)
terms = glossary_terms(wiki)
cards = json.loads(cards_path.read_text(encoding="utf-8"))["slides"]
taught_at = {}
for c in cards:
    for t in c["introduces"]:
        taught_at.setdefault(t, c["n"])
known = {zh for zh, _ in terms}

rows = []
for c in cards:
    texts = [c["title"]]
    for fid in c["facts"]:
        t = resolve(wiki, fid)
        if t is None:
            rows.append((c["n"], "事實不存在", fid))
        else:
            texts.append(t)
    blob = "\n".join(texts)
    avoid = set(c.get("avoid", []))
    for zh, aliases in terms:
        if zh in avoid:
            continue
        if any(a in blob for a in aliases):
            first = taught_at.get(zh)
            if first is None:
                rows.append((c["n"], "術語沒有安排教學", f"「{zh}」出現在事實中，但沒有任何一頁負責解釋"))
            elif first > c["n"]:
                rows.append((c["n"], "術語先用後教", f"「{zh}」第 {first} 頁才教"))
    for t in c["introduces"]:
        if t not in known:
            rows.append((c["n"], "術語不在 glossary", t))

lines = ["# 大綱事實卡檢查報告（N4.5，v2 新增）", "", f"- 投影片數：{len(cards)}",
         f"- 事實卡數：{sum(len(c['facts']) for c in cards)}", f"- 問題數：{len(rows)}",
         f"- 結果：{'PASS' if not rows else 'FAIL'}", "", "| 頁 | 問題 | 說明 |", "|---|---|---|"]
lines += [f"| {a} | {b} | {c} |" for a, b, c in rows]
out.write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
sys.exit(1 if rows else 0)
