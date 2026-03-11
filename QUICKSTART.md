# Sensei Face Recognition - 快速啟動指南

## 📋 快速檢查清單

### 1. 確認環境

- [ ] Python 3.7+ 已安裝
- [ ] Node.js 14+ 已安裝  
- [ ] MySQL 5.7+ 已安裝並運行
- [ ] Git 已安裝

### 2. 資料庫設定（僅首次）

```bash
# 建立資料庫
mysql -u root -p
CREATE DATABASE sensei_face_reg CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE sensei_face_reg;
SOURCE database/schema.sql;
EXIT;
```

### 3. 後端設定（僅首次）

```bash
cd backend

# Windows:
python -m venv venv
venv\Scripts\activate

# 安裝依賴
pip install -r requirements.txt

# 設定環境變數
copy .env.example .env
# ⚠️ 編輯 .env 填入你的 MySQL 密碼
```

### 4. 前端設定（僅首次）

```bash
cd frontend

# 安裝依賴
npm install

# 設定環境變數
copy .env.example .env
```

## 🚀 每次啟動步驟

### 啟動後端（終端機 1）

```bash
cd backend
venv\Scripts\activate    # Windows
# source venv/bin/activate  # Mac/Linux
python app.py
```

看到 "Sensei Face Recognition System API 啟動中..." 表示成功！
後端運行在：http://localhost:9453

### 啟動前端（終端機 2）

```bash
cd frontend
npm start
```

瀏覽器會自動開啟：http://localhost:3000

## ✅ 驗證安裝

1. 訪問 http://localhost:9453/health 應該看到：
   ```json
   {"status": "ok", "message": "Sensei Face Recognition API is running"}
   ```

2. 前端應該正常顯示三個標籤頁：上傳照片、人物列表、開始複習

## ⚠️ 常見問題快速解決

### 問題：dlib 安裝失敗

**Windows 解決方案：**
```bash
# 下載預編譯版本
pip install https://github.com/jloh02/dlib/releases/download/v19.24.1/dlib-19.24.1-cp39-cp39-win_amd64.whl
# 注意：根據你的 Python 版本選擇對應的 wheel 檔案
```

### 問題：MySQL 連線失敗

檢查 `backend/.env` 檔案：
```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=sensei_face_reg
DB_USER=root
DB_PASSWORD=你的MySQL密碼  # ⚠️ 這裡要填你的密碼
```

### 問題：前端無法連接後端

1. 確認後端已啟動（http://localhost:9453/health 可訪問）
2. 檢查瀏覽器 Console 是否有錯誤
3. 確認防火牆沒有阻擋 9453 port

### 問題：npm install 很慢

```bash
# 使用淘寶鏡像（中國用戶）
npm config set registry https://registry.npmmirror.com
npm install
```

## 📱 使用流程

1. **上傳照片** → 選擇包含人臉的照片 → 系統自動偵測
2. **標註姓名** → 為每個人臉輸入姓名（支援中文和日文）
3. **開始複習** → 隨機顯示人臉 → 輸入答案 → 查看結果

## 💾 資料備份建議

定期備份以下資料：
- `backend/uploads/` - 照片檔案
- MySQL 資料庫 `sensei_face_reg`

備份指令：
```bash
mysqldump -u root -p sensei_face_reg > backup_$(date +%Y%m%d).sql
```

## 🆘 需要幫助？

1. 查看詳細 README.md
2. 檢查 backend/app.py 的日誌輸出
3. 檢查瀏覽器的 Console 錯誤訊息

---

建立日期：2026-03-11
