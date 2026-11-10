# S4　Post-training quantization（LiteRT 官方文件）
- 單位：Google AI Edge（LiteRT，前身 TensorFlow Lite）
- URL：https://developers.google.com/edge/litert/models/post_training_quantization
- 補充頁：https://ai.google.dev/edge/lite/models/model_optimization（Model optimization）
- 讀取日期：2026-11-10
- 類型：官方文件

## 摘錄重點（自己的話）
1. 量化是降低模型參數的數字精度；參數預設是 32 位元浮點數，量化後模型變小、計算變快。
2. 訓練後量化（post-training quantization）：拿已經訓練好的浮點模型，在轉換成 LiteRT 格式時直接量化，不必重新訓練。
3. 三種常見方法：
   - 動態範圍量化：約小 4 倍、加速 2～3 倍，適用 CPU。
   - 完整整數量化：約小 4 倍、加速 3 倍以上，適用 CPU、Edge TPU、微控制器。
   - float16 量化：約小 2 倍，可用 GPU 加速。
4. 完整整數量化需要「代表性資料集」來估計數值範圍，大約 100～500 筆訓練或驗證資料即可。
5. 微控制器與 Coral Edge TPU 常需要純整數模型。
6. 量化可能讓準確率下降（小網路尤其明顯），量化後要檢查準確率；掉太多時改用量化感知訓練（quantization-aware training）。
7. 模型變小的好處：下載更快、占用記憶體更少；延遲降低也連帶降低耗電。
