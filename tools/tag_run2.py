"""Run 2 的 N5（v2）：把每個論點標上它依據的事實卡 id（data-fact）。標記時逐句對照 wiki 原句。"""
import re, sys
from pathlib import Path
p = Path(sys.argv[1]); s = p.read_text()
def tag(sub, ids):
    global s
    i = s.find(sub); assert i >= 0, sub
    e = i + 4
    j = max(s.rfind(x, 0, i + len(x)) for x in ('<li', '<p ', '<p>', '<tr', '<svg', '<div class="bars"', '<div class="q"'))
    k = s.find('>', j); head = s[j:k]
    assert 'data-fact' not in head, (sub, head)
    name = re.match(r'<(\w+)', head).group(1)
    s = s[:j] + '<' + name + f' data-fact="{ids}"' + s[j + 1 + len(name):]
T = [l.split(' => ') for l in Path(sys.argv[2]).read_text().splitlines() if ' => ' in l]
for sub, ids in T: tag(sub, ids)
p.write_text(s); print('tagged', len(T))
