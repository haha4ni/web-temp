# Web Scrobbler Script

整合Web Scrobbler在不同PC上的資料

## 功能特點

- 📊 分析兩個JSON快取檔案的差異
- 🔍 檢測重複ID並顯示詳細資訊
- 🤝 智慧處理衝突（相同ID的不同內容）
- 📈 提供詳細的統計報告
- 🎵 支援音樂中繼資料（藝術家、專輯、歌曲等）

## 使用版本

- Python 3.11.6

## 使用方法

### 基本用法

```bash
python analyze_cache.py file1.json file2.json output.json
```

### 參數說明

- `file1.json` - 第一個JSON快取檔案
- `file2.json` - 第二個JSON快取檔案  
- `output.json` - 合併後的輸出檔案

### 使用示例

```bash
# 分析並合併兩個快取檔案
python analyze_cache.py local-cache.json local-cache2.json merged-cache.json

# 使用默認輸出檔案名 (out.json)
python analyze_cache.py local-cache.json local-cache2.json

# 交互模式 - 程式會提示輸入檔案路徑
python analyze_cache.py
```

## 功能說明

### 自動處理
- **重複ID但內容相同**：自動合併，無需使用者介入
- **新ID條目**：自動新增到合併檔案中

### 交互處理
- **重複ID但內容不同**：提供選擇界面，讓使用者選擇保留哪個版本
- **批量處理**：支援自動解決剩餘衝突的選項

### 輸出報告
- 檔案統計資訊
- 重複檢測結果
- 藝術家分佈統計（Top 10）
- 使用者選擇統計

## 檔案格式

期望的JSON檔案格式：
```json
{
  "id1": {
    "artist": "藝術家名稱",
    "track": "歌曲名稱",
    "album": "專輯名稱",
    "albumArtist": "專輯藝術家"
  },
  "id2": {
    "artist": "另一個藝術家",
    "track": "另一首歌"
  }
}
```

## 示例輸出

```
=== 音樂快取檔案分析報告 ===
檔案１: local-cache.json
檔案２: local-cache2.json
--------------------------------------------------
檔案１ 條目數量: 150
檔案２ 條目數量: 200
重複ID數量: 25
  - 內容相同的重複: 20
  - 內容不同的衝突: 5
檔案２獨有條目數: 175

=== 最終統計報告 ===
最終合併條目數: 325
追加的新條目數: 175
```

## 注意事項

- 確保輸入檔案是有效的JSON格式
- 程式會在衝突時暫停等待使用者選擇
- 輸出檔案會覆蓋已存在的同名檔案
- 建議在執行前備份重要檔案
