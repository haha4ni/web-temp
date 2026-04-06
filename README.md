# Web Scrobbler Script

整合Web Scrobbler在不同PC上的資料

## 使用版本

- Python 3.11.6

## 使用方法

### 基本用法

1. 將Web Scrobbler已編輯曲目存成`local-cache.json`匯出
2. `local-cache.json`放進根目錄下
3. 點擊`main.bat`執行
4. 整合後的檔名為`out.json`


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
