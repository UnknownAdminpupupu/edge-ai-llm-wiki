# S5　MCUNet: Tiny Deep Learning on IoT Devices
- 作者：Ji Lin, Wei-Ming Chen, Yujun Lin, John Cohn, Chuang Gan, Song Han
- 發表：NeurIPS 2020（arXiv:2007.10319）
- URL：https://arxiv.org/abs/2007.10319
- 讀取日期：2026-11-10（讀 arXiv 摘要頁 v2、NeurIPS 摘要頁、PDF 引言）
- 類型：論文

## 摘錄重點（自己的話）
1. 在微控制器（MCU）上做機器學習很吸引人但很難：MCU 的記憶體比手機小 2～3 個數量級。
2. 引言補充：晶片上記憶體比雲端 GPU 小 5～6 個數量級。
3. SRAM 限制「激活值」（運算中途要讀寫的資料）大小；Flash 限制「模型」大小（唯讀）。
4. MCUNet 同時設計兩件事：TinyNAS（在記憶體限制下自動搜尋網路架構）＋ TinyEngine（省記憶體的推論函式庫）。這叫「系統與演算法共同設計」。
5. 成果：第一個在市售微控制器上達到 ImageNet top-1 準確率超過 70% 的方法；在語音喚醒詞任務（Speech Commands）達到 91% top-1 準確率、每秒 10 次推論。
6. TinyEngine 與 TF-Lite Micro、CMSIS-NN 相比，推論快 1.7～3.3 倍。
7. 記憶體節省倍數：arXiv 摘要頁（v2）寫「記憶體用量少 4.8 倍」；PDF 內文寫「峰值記憶體少 3.4 倍」。⚠️ 兩處數字不同。
8. 作者認為「隨時待命的微型機器學習（TinyML）」時代已經來臨。
