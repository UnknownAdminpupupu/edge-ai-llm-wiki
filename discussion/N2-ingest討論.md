# N2：逐篇 Ingest 前的討論（先討論、後寫入）

每篇都先回答三件事，再動 wiki：①3～5 個重點 ②和既有 wiki 有沒有衝突或重複 ③要新增／修改哪些頁。

---

## Ingest 1｜S1 IBM〈What is edge AI?〉
① 重點：定義（AI 模型放在本地裝置）；訓練多在雲端、推論在邊緣；五種元件；九項好處；五個產業用例。
② 衝突／重複：wiki 還是空的，無衝突。
③ 要寫的頁：新增 edge-ai、cloud-vs-edge、edge-hardware、use-cases、glossary、sources。
決定：S1 的市場預測數字不收（理由見 N0 討論）。

## Ingest 2｜S2 Zhou et al. 2019
① 重點：資料在邊緣產生；雲端與純裝置各自的缺點；六級評等；推論六指標；推論加速技術清單。
② 衝突：**定義衝突**。S1 把邊緣 AI 定義成「在本地裝置上跑模型」；S2 明確反對這個窄定義，主張雲-邊-端協作都算。
　　處理：edge-ai 頁兩種定義都寫，簡報用 S2 的廣義定義、把 S1 的說法當作「最常見的形式」。
　　另一處：S1 說訓練「通常」在雲端；S2 的 L4～L6 允許訓練也在邊緣。不算矛盾，是「常見做法」與「可能範圍」的差別。
③ 要寫的頁：新增 training-vs-inference、edge-intelligence-levels、inference-kpis；修改 edge-ai（加廣義定義）、cloud-vs-edge（加雲端與裝置兩邊的缺點）。

## Ingest 3｜S3 Deep Compression
① 重點：三階段壓縮；剪枝 9～13 倍、量化 32→5 位元；AlexNet 240MB→6.9MB、VGG-16 552MB→11.3MB；放得進 SRAM 才省電。
② 衝突：S2 提醒「剪掉的權重數不等於省下的電」，S3 則報告能效提升 3～7 倍。兩者不矛盾（S3 有搭配量化與 SRAM 放置），但簡報不能寫成「剪枝就會省電」。
③ 要寫的頁：新增 model-compression、pruning；quantization 先建立（量化的權重共享部分）。

## Ingest 4｜S4 LiteRT 訓練後量化
① 重點：量化 = 降低數字精度；三種訓練後量化與效果；整數量化要代表性資料 100～500 筆；掉準確率改用量化感知訓練。
② 重複：S3 也有量化，但 S3 是「訓練量化＋權重共享」，S4 是「訓練後量化」，方法不同，要在 quantization 頁分開寫，避免混用數字。
③ 要寫的頁：修改 quantization（加實務做法表）；修改 model-compression（連到 LiteRT）。

## Ingest 5｜S5 MCUNet
① 重點：MCU 記憶體比手機小 2～3 個數量級；SRAM 管激活值、Flash 管模型；TinyNAS＋TinyEngine；ImageNet >70%。
② 衝突：**同一篇內數字不一致**：摘要頁 v2 寫記憶體少 4.8 倍，PDF 內文寫峰值記憶體少 3.4 倍（可能是版本不同）。
　　處理：wiki 兩個數字都記並標 ⚠️；簡報不放這個倍數，只講「推論快 1.7～3.3 倍」（兩處一致）。
③ 要寫的頁：新增 tinyml-mcunet；修改 edge-hardware（加 SRAM/Flash）。

## Ingest 6｜S6 Google 聯邦學習
① 重點：資料留在手機、只上傳更新；Gboard 實例；少 10～100 倍通訊；閒置＋充電＋Wi-Fi 才訓練；有不適用的情境。
② 衝突：S1「訓練多在雲端」vs S6「訓練在手機上」→ 用 S2 的 L4～L6 解釋，屬於不同等級，不矛盾。
③ 要寫的頁：新增 federated-learning；修改 edge-intelligence-levels（舉例）、misconceptions。
