"""N7 技術檢查：翻頁、內容溢出、手機橫向捲動、測驗按鈕、console 錯誤。"""
import sys, json
from playwright.sync_api import sync_playwright
path, shots = sys.argv[1], sys.argv[2]
res = {"console": [], "overflow": [], "hscroll": [], "nav": None, "quiz": None}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
    for name, vp in [("desktop", {"width": 1280, "height": 720}), ("mobile", {"width": 390, "height": 844})]:
        pg = b.new_page(viewport=vp)
        pg.on("console", lambda m: m.type == "error" and "ERR_TUNNEL" not in m.text and res["console"].append(m.text))
        pg.on("pageerror", lambda e: res["console"].append(str(e)))
        pg.goto("file://" + path); pg.wait_for_timeout(200)
        n = pg.evaluate("document.querySelectorAll('.slide').length")
        for i in range(n):
            pg.evaluate(f"location.hash='s{i+1}'"); pg.wait_for_timeout(60)
            o = pg.evaluate("(()=>{const s=document.querySelector('.slide:not([hidden])');return [s.scrollHeight,s.clientHeight]})()")
            if name == "desktop" and o[0] > o[1] + 2:
                res["overflow"].append(f"{name} s{i+1}: 內容 {o[0]}px > 可視 {o[1]}px")
            if pg.evaluate("document.documentElement.scrollWidth > innerWidth + 1 || document.querySelector('.slide:not([hidden])').scrollWidth > document.querySelector('.slide:not([hidden])').clientWidth + 1"):
                res["hscroll"].append(f"{name} s{i+1}")
            if i in (0, 4, 7, 9, 12, 15) :
                pg.screenshot(path=f"{shots}/slide-{name}-{i+1}.png")
        if name == "desktop":
            pg.evaluate("location.hash='s1'"); pg.wait_for_timeout(50)
            for _ in range(n + 2): pg.keyboard.press("ArrowRight")
            res["nav"] = pg.inner_text("#count")
            pg.evaluate(f"location.hash='s16'"); pg.wait_for_timeout(50)
            qs = pg.query_selector_all(".q")
            okc = 0
            for q in qs:
                q.query_selector("button").click()
                if q.query_selector(".fb").is_visible() and q.query_selector("button.right"): okc += 1
            res["quiz"] = f"{okc}/{len(qs)} 題點擊後有回饋"
    b.close()
print(json.dumps(res, ensure_ascii=False, indent=1))
