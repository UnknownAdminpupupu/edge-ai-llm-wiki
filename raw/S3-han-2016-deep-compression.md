# S3　Deep Compression: Compressing Deep Neural Networks with Pruning, Trained Quantization and Huffman Coding
- 作者：Song Han, Huizi Mao, William J. Dally
- 發表：ICLR 2016（arXiv:1510.00149）
- URL：https://arxiv.org/abs/1510.00149
- 讀取日期：2026-11-10（讀 arXiv 摘要頁與 PDF 前段）
- 類型：經典論文

## 摘錄重點（自己的話）
1. 神經網路又吃運算又吃記憶體，很難放進硬體資源有限的嵌入式系統。
2. 三階段壓縮：剪枝（只留重要的連線）→ 訓練量化（權重共享）→ 霍夫曼編碼；前兩步之後再重新訓練微調。
3. 剪枝讓連線數減少 9～13 倍；量化讓每條連線從 32 位元降到 5 位元。
4. 在 ImageNet 上，AlexNet 從 240MB 壓到 6.9MB（35 倍），VGG-16 從 552MB 壓到 11.3MB（49 倍），準確率沒有下降。
5. 壓縮後模型可以放進晶片上的 SRAM，不必去讀晶片外、較耗能的 DRAM；行動裝置的能耗主要由記憶體存取決定。
6. 在 CPU、GPU、行動 GPU 上，壓縮後的網路逐層加速 3～4 倍、能源效率提升 3～7 倍。
7. 權重共享用 k-means 分群：同一群的權重共用一個值，只需存「代表值表」和索引。
8. 動機之一：App 商店對大檔案有下載限制，模型太大就很難放進手機 App。
