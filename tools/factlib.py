"""Workflow v2 共用：把『wiki 頁#第幾條』解析成 wiki 原句，並讀 glossary 術語。"""
import re
from pathlib import Path

SKIP_SECTIONS = {"來源", "和其他概念的關係"}


def load_wiki(root):
    return {p.stem: p.read_text(encoding="utf-8") for p in (Path(root) / "wiki").glob("*.md")}


def facts_of(page_text):
    """回傳 {編號: 句子}，編號依文件順序計算所有事實區段的條列句；表格整段算 'table'。"""
    out, n, section, table = {}, 0, "", []
    for line in page_text.splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
            continue
        if section in SKIP_SECTIONS:
            continue
        if line.startswith("- "):
            n += 1
            out[str(n)] = line[2:]
        elif line.startswith("|") and "［S" in section:
            table.append(line)
    if table:
        out["table"] = "\n".join(table)
    return out


def resolve(wiki, fid):
    page, _, num = fid.partition("#")
    if page not in wiki:
        return None
    return facts_of(wiki[page]).get(num)


def glossary_terms(wiki):
    terms = []
    for m in re.finditer(r"\*\*([^*]+)\*\*", wiki["glossary"]):
        name = m.group(1)
        zh = re.sub(r"（.*?）", "", name).strip()
        en = re.findall(r"（(.*?)）", name)
        terms.append((zh, [a for a in [zh] + en if a]))
    return terms
