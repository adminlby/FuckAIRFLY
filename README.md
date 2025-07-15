# FuckXZ

一個高效能針對AIR FLY的帳號產生工具

## 特性

- 多線程並發註冊（1-20個線程）
- 可自訂註冊頻率（0.3-60秒/次）
- 智慧產生隨機帳號資訊：
  - 使用者名稱：20-25位元字母數字組合
  - 信箱：20-25位元字母數字組合
  - 密碼：32-40位元包含特殊字元的強密碼
- 即時顯示註冊進度和統計
- 支援優雅退出（Ctrl+C）
- 自動儲存成功註冊的帳號訊息
- 驗證碼自動辨識功能

## 環境要求

- Python 3.6+
- requests函式庫

## 安装

1. Clone仓库：
```bash
git clone [links]
cd 對應目錄
```

2. 安裝依賴：
```bash
pip install -r requirements.txt
```

## 使用方法

### 基本用法

```bash
python fuckairfly.py
```

### 命令列參數

- `--threads`: 並發執行緒數量（1-20，預設7）
- `--frequency`: 註冊頻率，單位秒（0.3-60，預設0.5）
- `--count`: 需要註冊的總帳號數量（預設1000）

### 示例

1. 使用預設配置（7個線程，0.5秒/次，註冊1000個帳號）：
```bash
python fuckairfly.py
```

2. 高速模式（10線程，0.3秒/次，註冊100個帳號）：
```bash
python fuckairfly.py --threads 10 --frequency 0.3 --count 100
```

3. 穩定模式（3線程，2秒/次，註冊50個帳號）：
```bash
python fuckairfly.py --threads 3 --frequency 2 --count 50
```

## 输出文件

成功註冊的帳號資訊會自動儲存在 `successful_accounts.txt` 檔案中，格式如下：
```
账号: Abc123xyz789def456ghi, 邮箱: Xyz123abc456def789ghi@domain.com, 密码: Kj#9$mP2*nX5@qL7^vR4&wY8!zC3%tB6
```

## 開發注意事項

1. 帳號產生規則
 - 使用者名稱：20-25位元字母數字組合，以字母開頭
 - 信箱前綴：20-25位元字母數字組合，以字母開頭
 - 密碼：32-40位，包含大小寫字母、數字和特殊字符

2. 效能優化
 - 每個執行緒使用獨立的session以提高效率
 - 使用線程鎖確保計數器和檔案寫入的線程安全
 - 實現了優雅退出機制，確保資料不會遺失

3. 注意事項
 - 建議從低線程數開始測試
 - 當線程數超過10時會顯示警告
 - 頻率設定過快可能導致註冊失敗或IP被封
 - 建議使用代理IP輪換以避免IP被封

4. 錯誤處理
 - 所有網路請求都有逾時處理
 - 失敗的請求會被記錄但不會中斷程序
 - 可以透過Ctrl+C隨時停止程序

## 自訂開發

### 修改帳號產生規則

可以修改以下函數來自訂生成規則：
- `generate_username()`: 自訂使用者名稱產生規則
- `generate_email_prefix()`: 自訂郵件信箱前綴產生規則
- `generate_password()`: 自訂密碼產生規則

### 新增功能

1. 新增代理支援：
```python
proxies = {
    'http': 'http://your-proxy:port',
    'https': 'https://your-proxy:port'
}
session.proxies = proxies
```

2. 新增驗證碼處理：
```python
# 在register_account函數中新增驗證碼處理邏輯
```

## 常見問題

1. 註冊失敗率高
 - 降低註冊頻率
 - 減少並發線程數
 - 檢查網路連接
 - 考慮使用代理IP

2. IP被封
 - 降低註冊頻率
 - 減少並發線程數
 - 使用代理IP
 - 增加註冊間隔時間

3. 程式意外關閉
 - 檢查網路連接
 - 查看錯誤日誌
 - 確保有寫入檔案權限

## 貢獻指南

1. Fork 項目
2. 建立新分支：`git checkout -b feature-name`
3. 提交更改：`git commit -am 'Add some feature'`
4. 推播分支：`git push origin feature-name`
5. 提交 Pull Request

## 免責聲明

本工具僅供學習研究使用，請勿用於非法用途。使用本工具所產生的任何後果由使用者自行承擔。

## 許可證

MIT License
