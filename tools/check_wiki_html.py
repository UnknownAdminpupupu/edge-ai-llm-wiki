"""N3 技術檢查：HTML Wiki 每個頁面都能開、連結不壞、手機不橫向捲動。"""
import sys, json
from playwright.sync_api import sync_playwright
path, shots = sys.argv[1], sys.argv[2]
res = {"errors": [], "pages": 0, "bad_links": [], "hscroll": []}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
    for name, vp in [("desktop", {"width": 1280, "height": 800}), ("mobile", {"width": 390, "height": 844})]:
        pg = b.new_page(viewport=vp)
        pg.on("console", lambda m: m.type == "error" and res["errors"].append(m.text))
        pg.on("pageerror", lambda e: res["errors"].append(str(e)))
        pg.goto("file://" + path)
        ids = pg.evaluate("Array.from(document.querySelectorAll('section[data-page]')).map(s=>s.dataset.page)")
        res["pages"] = len(ids)
        hrefs = pg.evaluate("Array.from(document.querySelectorAll('a[href^=\"#\"]')).map(a=>a.getAttribute('href').slice(1))")
        res["bad_links"] = sorted(set(h for h in hrefs if h not in ids))
        for i in ids:
            pg.evaluate(f"location.hash='{i}'"); pg.wait_for_timeout(30)
            vis = pg.evaluate("document.querySelector('section:not([hidden])').dataset.page")
            if vis != i: res["errors"].append(f"{name}: #{i} 顯示成 {vis}")
            if pg.evaluate("document.documentElement.scrollWidth > window.innerWidth + 1"):
                res["hscroll"].append(f"{name}:{i}")
        pg.evaluate("location.hash='home'"); pg.wait_for_timeout(300)
        pg.screenshot(path=f"{shots}/wiki-{name}.png", full_page=False)
        pg.evaluate("location.hash='quantization'"); pg.wait_for_timeout(100)
        pg.screenshot(path=f"{shots}/wiki-{name}-quant.png", full_page=False)
    b.close()
print(json.dumps(res, ensure_ascii=False, indent=1))
