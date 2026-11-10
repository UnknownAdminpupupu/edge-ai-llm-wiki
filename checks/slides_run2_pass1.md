# 簡報內容檢查報告 v2（逐句對事實卡）

- FAIL：4　WARN（需人工複查）：17
- 結果：FAIL

## FAIL
| 頁 | 檢查 | 說明 |
|---|---|---|
| 4 | b 數字 | 「2019」不在引用句 ['edge-ai#4']：Zhou 等人（2019）認為只看「裝置上跑模型」太窄。本簡 |
| 10 | b 數字 | 「2016」不在引用句 ['model-compression#4']：資料：Deep Compression（Han 等，ICLR |
| 16 | b 數字 | 「1」不在引用句 ['edge-intelligence-levels#8']：2. 邊緣智慧等級從 L1 升到 L6，下列何者「不一定」變 |
| 16 | b 數字 | 「6」不在引用句 ['edge-intelligence-levels#8']：2. 邊緣智慧等級從 L1 升到 L6，下列何者「不一定」變 |

## WARN：論點和引用原句字面重疊低（< 0.2），請人工確認意思一致
| 頁 | 重疊率 | 引用 | 論點 |
|---|---|---|---|
| 3 | 0.13 | cloud-vs-edge#4 | 感測資料要先上傳，等雲端算完再回傳 |
| 3 | 0.08 | edge-ai#5 | 網路不穩或沒訊號時，就判斷不了 |
| 3 | 0.13 | cloud-vs-edge#4 use-cases#1 | 心率、位置這些私人資料都要離開手錶 |
| 3 | 0.14 | edge-ai#5 | 不用等網路，反應快 |
| 3 | 0.00 | use-cases#1 | 資料留在身上 |
| 4 | 0.07 | edge-ai#4 | IBM 等企業文章多半用這個定義。 |
| 4 | 0.13 | edge-ai#4 | Zhou 等人（2019）認為只看「裝置上跑模型」太窄。本簡報採用這個說法。 |
| 4 | 0.07 | edge-ai#1 | 關鍵字只有一個： 靠近資料產生的地方 。 |
| 5 | 0.11 | cloud-vs-edge#1 cloud-vs-edge#4 | 裝置 手錶、攝影機 邊緣節點 閘道、基地台旁 雲端 遠端資料中心 快、資料不出門 |
| 5 | 0.18 | cloud-vs-edge#5 | 全部放裝置：運算和電力不夠 |
| 8 | 0.08 | edge-intelligence-levels#4 | 例：手機相機辨識場景多半是 L3； 聯邦學習 把訓練也搬到手機上。 |
| 10 | 0.07 | model-compression#4 | 資料：Deep Compression（Han 等，ICLR 2016），在 I |
| 12 | 0.08 | tinyml-mcunet#4 | 兩者一起設計，才塞得進微控制器 |
| 16 | 0.17 | training-vs-inference#3 | 1. 邊緣裝置最常負責哪一件事？ 訓練大模型 推論 儲存所有資料 推論只做前向傳 |
| 17 | 0.08 | edge-ai#3 | 邊緣 AI 把 AI 放到靠近資料的地方，換來速度、隱私和斷網也能用 |
| 17 | 0.10 | cloud-vs-edge#6 edge-intelligence-levels#9 | 它和雲端是分工，不是取代；用六個等級思考分工方式 |
| 17 | 0.05 | model-compression#4 tinyml-mcunet#4 | 小裝置跑得動，靠的是壓縮模型，以及軟硬體一起設計 |