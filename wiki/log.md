# 執行紀錄（append-only）

格式：`## [日期 時間] 節點 | 做了什麼`，下面記結果 PASS/FAIL、問題、處理、重試次數。

## [2026-11-10 19:13] N0 範圍討論 | 定主題 Edge AI、讀者、要講與不講
- 結果：PASS
- 紀錄：discussion/N0-N1-範圍與來源討論.md
- 自我反駁 1 次：否決用「市場規模」當引入（會過時）

## [2026-11-10 19:14] N1 蒐集來源 | 搜尋 6 組關鍵字，候選 10 篇
- 結果：PASS（6 收、4 不收）
- 品質關卡：二手整理文（Simplilearn、Built In、TechTarget、KDnuggets）不收，改找一手來源
- 重試：0

## [2026-11-10 19:15] N2 ingest | S1 IBM〈What is edge AI?〉
- 新增：edge-ai、cloud-vs-edge、edge-hardware、use-cases、glossary、sources
- 衝突：無（第一篇）
- 排除：市場預測數字

## [2026-11-10 19:15] N2 ingest | S2 Zhou et al. 2019
- 新增：training-vs-inference、edge-intelligence-levels、inference-kpis；修改 edge-ai、cloud-vs-edge
- 衝突：⚠️ 定義衝突（S1 狹義 vs S2 廣義）→ 兩者都記，採 S2
- 標記 ⏳ 舊資料 2 筆（Cisco 2021 預測、Gartner 2018 預測），不進 wiki 正文
- 備註：PDF 只讀了第 I–V 節（約 70%），第 VI 節未來方向未讀

## [2026-11-10 19:16] N2 ingest | S3 Deep Compression
- 新增：model-compression、pruning；建立 quantization
- 衝突：剪枝與省電的關係（S2 提醒 vs S3 能效數據）→ 加註，誤解頁收錄

## [2026-11-10 19:16] N2 ingest | S4 LiteRT 訓練後量化
- 修改：quantization（加三種方法表）、model-compression
- 重複處理：S3 的「訓練量化」與 S4 的「訓練後量化」分開寫

## [2026-11-10 19:17] N2 ingest | S5 MCUNet
- 新增：tinyml-mcunet；修改 edge-hardware
- 衝突：⚠️ 同篇數字不一致（記憶體少 4.8 倍 vs 3.4 倍）→ 兩者都記，簡報不用

## [2026-11-10 19:17] N2 ingest | S6 Google 聯邦學習
- 新增：federated-learning；修改 misconceptions、use-cases
- 衝突：S1「訓練在雲端」vs S6「訓練在手機」→ 用 S2 分級解釋，不矛盾
- Ingest 小計：6 篇來源、16 個 wiki 頁（含 index、glossary、sources）

## [2026-11-10 19:22] N3 Wiki Lint | 第 1 次（checks/lint_run1_pass1.md）
- 結果：FAIL，21 個問題
- 孤兒頁 2：glossary、sources 只有 index 連到 → edge-ai 加連 glossary，glossary 加連 sources
- 術語未定義 18：激活值、反向傳播、量化感知訓練、DRAM、top-1 等 → glossary 補 18 條定義
- 衝突未處理 1：其實是 lint 工具誤判（log.md 不該被檢查）→ 修工具，跳過 log
- 重試：1

## [2026-11-10 19:24] N3 Wiki Lint | 第 2 次（checks/lint_run1_pass2.md）
- 結果：FAIL，2 個問題
- 「卷積層／全連接層」合寫成一條，工具找不到「全連接層」→ 拆成兩條
- 「top-1」的 1 被當成數字 → 工具誤判，改成粗體術語名不算數字
- 重試：2

## [2026-11-10 19:25] N3 Wiki Lint | 第 3 次 + 反向測試
- 第 3 次 PASS，但我故意塞一句「剪枝減少 20 倍［S3］」測試工具，**沒有抓到**
- 原因：數字回查用子字串比對，「20」誤配到 raw 裡的「2016」→ 工具其實形同虛設
- 修正：改成數字邊界比對；反向測試成功抓到假數字
- 第 4 次（checks/lint_run1_pass4.md）：PASS，0 個問題
- 心得：檢查工具本身也要被檢查，PASS 不代表真的沒問題

## [2026-11-10 19:31] N3 產出 HTML Wiki | tools/build_wiki_html.py → site/edge-ai-wiki.html
- 技術檢查（tools/check_wiki_html.py，桌機 1280px＋手機 390px）
- 第 1 次：FAIL，手機版 sources、raw-s4 兩頁出現橫向捲動（長網址撐開版面）→ 加 overflow-wrap
- 第 2 次：PASS（26 個區塊都能切換、0 個壞連結、0 個橫向捲動）
- 看截圖再修：桌機目錄連結擠成一行、關係圖標籤被切掉 → 改成直排目錄、圖上用短標題
- 備註：沙盒連不到 Google Fonts 的 2 個錯誤訊息屬環境限制，線上正常
- 已發佈 HTML Wiki（artifact）

## [2026-11-10 19:40] N4 教學大綱 | Query wiki/index.md → slides/outline.md
- 結果：PASS（17 頁；15 個概念頁用到 14 頁）
- 每頁只列一個主要的依據 wiki 頁

## [2026-11-10 19:44] N5 生成 | Run 1 第一版 slides/edge-ai-slides.html（17 頁）
- 每頁用 data-wiki 標記依據頁

## [2026-11-10 19:46] N6 內容檢查 | Run 1 第 1 次（checks/slides_run1_pass1.md）
- 結果：FAIL，68 項中 8 項失敗
- b 數字查無 3 頁（5 個數字）：
  - 第 4 頁「2019」、第 10 頁「32」「2016」：內容其實來自 sources、quantization 頁，但 data-wiki 沒列 → **生成時用了大綱沒指定的 wiki 頁**
  - 第 9 頁「100～1000 倍」：我自己把「2～3 個數量級」換算成倍數，wiki 沒有 → **生成時自行推導數字**
- c 術語未解釋 4 頁：「雲端 AI」（p2）、「訓練／推論」（p4，第 6 頁才教）、「聯邦學習」（p8，第 13 頁才教）、「ImageNet」（p10，第 12 頁才解釋）→ **術語在被教之前就先用了**
- d 密度 1 頁：第 17 頁參考文獻 6 條 → 規則修正：參考文獻清單不算教學密度
- 處理：補 data-wiki、刪掉自行換算的倍數、在首次出現處加 <dfn>
- 重試：1

## [2026-11-10 19:48] N6 內容檢查 | Run 1 第 2 次（checks/slides_run1_pass2.md）
- 結果：PASS（68/68）
- 人工複查又發現 1 個漏網之魚：第 9 頁我改寫成「一個數量級就是差 10 倍」，「10」剛好在 tinyml-mcunet 頁（每秒 10 次推論）出現，所以工具誤判成有來源 → 改成不含數字的說法
- 心得：數字比對只看「數字有沒有出現」，不看「意思一不一樣」，會漏掉巧合

## [2026-11-10 19:52] N7 技術檢查 | tools/check_slides_tech.py（1280×720 與 390×844）
- 結果：PASS：17 頁可鍵盤翻到底（17 / 17）、0 頁內容溢出、0 頁橫向捲動、測驗 3/3 題有回饋、0 個 console 錯誤
- 看截圖再修：卡片被拉高留大片空白、字太小、聯邦學習循環圖沒有箭頭 → 調整版面與字級、補箭頭後重跑仍 PASS

## [2026-11-10 20:02] F 回顧 Run 1 | 統計各節點錯誤
- N3 Wiki Lint：21 個內容問題（術語未定義 18、孤兒頁 2、術語合寫 1）＋ 3 個 lint 工具本身的 bug
- N3 HTML 檢查：1 次 FAIL（手機橫向捲動 2 頁）
- N6 簡報內容：8 個（術語先用後教 4、數字不在指定 wiki 頁 3、太擠 1）＋人工抓到 1 個（巧合數字）
- N7 技術：0
- 錯誤來源：N2 寫 wiki（21 個，其中 19 個是術語沒定義或合寫）、N5 生成簡報（9 個，種類最多）
- 根本原因：檢查都排在「生成之後」；大綱（N4）只寫「這頁用哪個 wiki 頁」，沒有規定「能用哪幾句」「哪頁教哪個術語」，生成時就自由發揮
- 決定：改成 Workflow v2（見 discussion/F-workflow-v1-v2.md）

## [2026-11-10 20:05] Run 2 / N4 v2 | 產生事實卡 slides/factcards.json（17 頁、75 張）
## [2026-11-10 20:06] Run 2 / N4.5 大綱檢查（v2 新增，生成前）| checks/outline_run2_pass1.md
- 結果：FAIL，7 個問題 → **在生成前就抓到**
- 「延遲」第 3 頁就會用到，卻排在第 5 頁才教 → 改成第 3 頁教
- 「卸載」「權重共享」「k-means」出現在事實裡但沒有頁面負責教 → 判斷對新手太深，列入 avoid（不准出現在簡報）
- glossary 把「TinyNAS／TinyEngine」合寫成一條 → 拆開（和 Run 1 的「卷積層／全連接層」是同一種錯）
- 第 2 次：PASS

## [2026-11-10 20:10] Run 2 / N5 v2 | 每個論點加上 data-fact（共 101 個元素）
## [2026-11-10 20:12] Run 2 / N6 v2 逐句檢查 | checks/slides_run2_pass1.md
- 結果：FAIL 4（年份 2019、2016 沒有引用 sources 頁；測驗題的 L1、L6 沒引用等級表）＋ WARN 17
- 17 條 WARN 人工複查，5 條確定是錯（checks/warn_review_run2.md）：多寫「位置」、「IBM 等企業文章多半」過度概括、「基地台」不在 wiki、「手機相機是 L3」來自沒有來源的［整理］句、回顧頁引用錯頁
- 這 5 個錯在 Run 1 的 v1 檢查全部 PASS（v1 只比數字，抓不到沒有數字的錯）
- 處理：回 N4 補事實卡、回 N5 改寫句子；重試 1
## [2026-11-10 20:15] Run 2 / N6 v2 第 2 次 | checks/slides_run2_pass2.md
- 結果：PASS（FAIL 0；WARN 9 條人工確認都是合理改寫）
- v1 檢查回歸測試：68/68 PASS
## [2026-11-10 20:16] Run 2 / N7 技術檢查
- 結果：PASS（17/17 頁、0 溢出、0 橫向捲動、測驗 3/3、0 錯誤）

## [2026-11-10 20:20] N8 發佈 | 簡報與 Wiki 都發佈為網頁
- 教學 HTML 簡報（17 頁）發佈；Wiki 更新第 2 版：加上 loop/graph 設計頁、10 份檢查報告、簡報連結
- 下一步：繳交前在無痕視窗確認兩個連結都已開放分享

## [2026-11-10 20:24] 驗證 | 繳交文字的數字逐一對回 checks/ 報告
- 發現 log 自己寫錯：Run 1 N6 數字問題寫成「4 頁」，報告實際是 3 頁（5 個數字）；N2 錯誤數寫成 19，實際 21 → 已更正
