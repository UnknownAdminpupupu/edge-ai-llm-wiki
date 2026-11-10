# N4 教學大綱（只用 Query wiki 規劃）

Query 方式：讀 wiki/index.md → 依「新手要先懂什麼」排順序 → 每頁只挑 1 個主要概念 → 標出依據的 wiki 頁。

| # | 頁面標題 | 教學目的 | 依據 wiki 頁 |
|---|---|---|---|
| 1 | Edge AI 入門 | 封面 | edge-ai |
| 2 | 今天學完你會知道 | 學習目標 4 條 | edge-ai |
| 3 | 手錶怎麼知道你跌倒了？ | 生活化引入，帶出「為什麼不全丟雲端」 | use-cases、cloud-vs-edge |
| 4 | 邊緣 AI 是什麼 | 狹義與廣義定義 | edge-ai |
| 5 | 雲端 vs 邊緣 | 比較與互補 | cloud-vs-edge |
| 6 | 先分清楚：訓練 vs 推論 | 前置概念 | training-vs-inference |
| 7 | 一套邊緣 AI 系統有哪些元件 | 硬體鏈 | edge-hardware |
| 8 | 不是二選一：六個等級 | 分級思維與取捨 | edge-intelligence-levels |
| 9 | 最大的難題：裝置太小 | 資源限制 | edge-hardware、tinyml-mcunet |
| 10 | 解法 1：把模型壓小 | 剪枝＋量化＋霍夫曼 | model-compression、pruning |
| 11 | 量化在實務上怎麼做 | LiteRT 三種方法 | quantization |
| 12 | 解法 2：模型和引擎一起設計 | MCUNet | tinyml-mcunet |
| 13 | 連訓練都在手機上：聯邦學習 | 延伸 | federated-learning |
| 14 | 怎麼評估一個邊緣 AI 系統 | 六個指標 | inference-kpis |
| 15 | 常見誤解 | 澄清 | misconceptions |
| 16 | 小測驗 | 自我檢查 | misconceptions、edge-intelligence-levels、quantization |
| 17 | 回顧與參考來源 | 收束 | sources |

覆蓋率：15 個概念頁中 14 頁被用到（glossary 用在每頁的術語解釋，不單獨成頁）。
