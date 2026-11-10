# TinyML 與 MCUNet
> TinyML 是把機器學習放進便宜、省電、記憶體極小的微控制器；MCUNet 是讓微控制器也能做影像辨識的代表研究。

## 重點
- 微控制器的記憶體比手機小 2～3 個數量級，在上面跑深度學習很困難。［S5］
- 晶片上記憶體比雲端 GPU 小 5～6 個數量級。［S5］
- SRAM 限制激活值，Flash 限制模型大小，所以「模型小」還不夠，運算中途的資料也要小。［S5］
- MCUNet 同時設計 TinyNAS（在記憶體限制下自動找網路架構）和 TinyEngine（省記憶體的推論函式庫）。［S5］
- 成果：第一個在市售微控制器上達到 ImageNet top-1 準確率超過 70% 的方法。［S5］
- 語音喚醒詞任務達到 91% 準確率、每秒 10 次推論。［S5］
- TinyEngine 比 TF-Lite Micro 與 CMSIS-NN 推論快 1.7～3.3 倍。［S5］
- ⚠️ 衝突：記憶體節省倍數，摘要頁（v2）寫 4.8 倍，PDF 內文寫峰值記憶體 3.4 倍；可能是版本差異。簡報不使用此數字。［S5］

## 和其他概念的關係
- [[edge-hardware]]：SRAM 與 Flash。
- [[model-compression]]：MCUNet 是壓縮之外的另一條路。
- [[quantization]]：MCU 通常需要整數模型。

## 來源
- S5
