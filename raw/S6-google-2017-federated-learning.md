# S6　Federated Learning: Collaborative Machine Learning without Centralized Training Data
- 作者：Brendan McMahan、Daniel Ramage（Google Research）
- 發布：2017-04-06
- URL：https://research.google/blog/federated-learning-collaborative-machine-learning-without-centralized-training-data/
- 讀取日期：2026-11-10
- 類型：官方研究部落格

## 摘錄重點（自己的話）
1. 傳統機器學習要把訓練資料集中到一台機器或資料中心；聯邦學習讓很多手機一起學一個共享模型，但訓練資料留在各自手機上。
2. 流程：手機下載目前模型 → 用手機上的資料改進 → 把改變整理成一個小的更新 → 加密上傳 → 伺服器把大家的更新平均起來改進共享模型 → 重複。
3. 個別更新不會存在雲端。
4. 實例：Google 在 Android 鍵盤 Gboard 測試，用手機上「建議有沒有被點」的紀錄改進下一版建議模型。
5. Federated Averaging 演算法：用手機較強的處理器算出品質更好的更新，比天真版本少 10～100 倍通訊量。
6. 只在手機閒置、充電中、連免費 Wi-Fi 時才訓練，不影響使用。
7. Secure Aggregation：伺服器只有在數百到數千台手機參與時才能解開「平均後」的更新，看不到單一手機的更新。
8. 限制：不是所有問題都適用，例如需要人工仔細標註的任務（辨識狗的品種）；很多資料本來就在雲端的任務（垃圾郵件過濾）也不需要。
