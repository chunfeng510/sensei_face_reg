# Sensei Face Recognition System
日本老師人臉辨識記憶系統

## 📋 專案需求

### 背景
朋友即將帶我去日本認識他的老師們，希望能夠記住他們的臉和姓名，開發此系統來輔助記憶。

### 核心功能

1. **照片上傳**
   - 使用者可上傳包含人物的照片
   - 支援常見圖片格式（JPG, PNG）
   - 可一次上傳多張照片

2. **人臉自動辨識**
   - 系統自動偵測照片中的人臉
   - 在照片上框出所有辨識到的人臉
   - 支援一張照片中有多個人臉的情況

3. **姓名標註**
   - 人臉框選完成後顯示輸入框
   - 使用者可為每個人臉輸入對應的姓名
   - 支援日文、中文姓名輸入

4. **資料儲存**
   - 將照片儲存至伺服器
   - 將人臉座標、姓名儲存至 MySQL 資料庫
   - 記錄上傳時間等元資料

5. **複習模式**
   - 隨機顯示已儲存的人臉
   - 使用者猜測姓名
   - 顯示正確答案並統計正確率
   - 支援篩選特定人物複習

---

## 🏗️ 系統架構

### 技術棧選擇

#### 前端
- **框架**: React.js
- **UI 庫**: Material-UI (MUI)
- **狀態管理**: React Hooks (useState, useEffect)
- **HTTP 客戶端**: Axios
- **圖片處理**: Canvas API

#### 後端
- **框架**: Flask (Python)
- **人臉辨識**: OpenCV + face_recognition 函式庫
- **資料庫**: MySQL
- **ORM**: SQLAlchemy
- **API 設計**: RESTful API
- **檔案儲存**: 本地檔案系統

#### 資料庫結構
```sql
-- 人物表
CREATE TABLE persons (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    name_jp VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 照片表
CREATE TABLE photos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    filepath VARCHAR(500) NOT NULL,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 人臉資料表
CREATE TABLE faces (
    id INT AUTO_INCREMENT PRIMARY KEY,
    person_id INT,
    photo_id INT,
    face_encoding TEXT,
    face_location VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (person_id) REFERENCES persons(id) ON DELETE CASCADE,
    FOREIGN KEY (photo_id) REFERENCES photos(id) ON DELETE CASCADE
);

-- 複習記錄表
CREATE TABLE review_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    face_id INT,
    is_correct BOOLEAN,
    review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (face_id) REFERENCES faces(id) ON DELETE CASCADE
);
```

---

## 📁 專案結構

```
sensei_face_reg/
├── backend/                  # 後端 Flask 應用
│   ├── app.py               # 主應用程式
│   ├── config.py            # 配置檔案
│   ├── requirements.txt     # Python 依賴
│   ├── models/              # 資料庫模型
│   │   ├── __init__.py
│   │   ├── person.py
│   │   ├── photo.py
│   │   ├── face.py
│   │   └── review.py
│   ├── routes/              # API 路由
│   │   ├── __init__.py
│   │   ├── upload.py
│   │   ├── face.py
│   │   └── review.py
│   ├── services/            # 業務邏輯
│   │   ├── __init__.py
│   │   ├── face_detection.py
│   │   └── face_recognition.py
│   └── uploads/             # 上傳檔案儲存目錄
│
├── frontend/                 # 前端 React 應用
│   ├── public/
│   ├── src/
│   │   ├── components/      # React 元件
│   │   │   ├── Upload.jsx
│   │   │   ├── FaceAnnotation.jsx
│   │   │   ├── Review.jsx
│   │   │   └── Gallery.jsx
│   │   ├── services/        # API 服務
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   └── index.js
│   ├── package.json
│   └── package-lock.json
│
├── database/                 # 資料庫相關
│   └── schema.sql           # 資料庫結構定義
│
├── .gitignore
└── README.md                # 本文件
```

---

## 🚀 開發步驟

### Phase 1: 環境設置與資料庫準備
1. ✅ 建立專案目錄結構
2. ✅ 建立 MySQL 資料庫結構
3. ✅ 設定 Python 虛擬環境
4. ✅ 安裝必要的 Python 套件（Flask, OpenCV, face_recognition, SQLAlchemy, pymysql）
5. ✅ 設定 React 前端專案

### Phase 2: 後端核心功能開發
6. ✅ 建立 Flask 基礎架構
7. ✅ 實作資料庫連接與模型
8. ✅ 實作檔案上傳 API
9. ✅ 實作人臉辨識功能
10. ✅ 實作人臉標註與儲存 API
11. ✅ 實作查詢人物與照片 API

### Phase 3: 前端介面開發
12. ✅ 建立基礎 React 應用架構
13. ✅ 實作照片上傳介面
14. ✅ 實作人臉框選與標註介面
15. ✅ 實作人物列表展示
16. ✅ 整合前後端 API

### Phase 4: 複習功能開發
17. ✅ 實作複習模式後端 API
18. ✅ 實作複習模式前端介面
19. ✅ 實作複習記錄統計功能

### Phase 5: 測試與優化
20. ✅ 功能測試
21. ✅ UI/UX 優化
22. ✅ 效能優化
23. ✅ 撰寫使用文件

---

## 🔧 技術細節

### 人臉辨識實作
- 使用 `face_recognition` 函式庫（基於 dlib）
- 人臉偵測：使用 HOG 或 CNN 方法
- 人臉編碼：生成 128 維度的特徵向量
- 儲存編碼以供未來比對使用

### API 端點設計

#### 上傳與辨識
- `POST /api/upload` - 上傳照片
- `POST /api/detect-faces` - 偵測照片中的人臉
- `POST /api/save-face` - 儲存人臉與姓名

#### 查詢
- `GET /api/persons` - 取得所有人物列表
- `GET /api/persons/:id` - 取得特定人物詳情
- `GET /api/photos` - 取得所有照片
- `GET /api/faces/:person_id` - 取得特定人物的所有人臉

#### 複習
- `GET /api/review/random` - 取得隨機人臉進行複習
- `POST /api/review/submit` - 提交複習結果
- `GET /api/review/statistics` - 取得複習統計

---

## 📝 配置需求

### MySQL 資料庫連接資訊
需要提供以下資訊（將在 `backend/config.py` 中設定）：
- 主機位址
- 資料庫名稱
- 使用者名稱
- 密碼
- 埠號（預設 3306）

### 環境變數
```
DB_HOST=localhost
DB_NAME=sensei_face_reg
DB_USER=your_username
DB_PASSWORD=your_password
DB_PORT=3306
UPLOAD_FOLDER=./uploads
```

---

## 🎯 未來擴充功能（Optional）

1. **多語言支援**
   - 介面支援中文、日文、英文切換

2. **進階複習模式**
   - 間隔重複記憶法（Spaced Repetition）
   - 根據記憶強度調整複習頻率

3. **社交功能**
   - 分享人物卡片
   - 協作標註

4. **行動端支援**
   - 響應式設計
   - PWA 支援

5. **進階人臉識別**
   - 自動識別已知人物
   - 相似人臉提示

---

## ⚠️ 注意事項

1. **隱私保護**
   - 確保照片和個人資訊安全
   - 不對外公開資料
   - 建議本地部署使用

2. **效能考量**
   - 大量照片時考慮分頁載入
   - 人臉辨識可能需要較長時間

3. **相容性**
   - 確保瀏覽器支援 Canvas API
   - Python 版本需 3.7+

---

## 📦 開始使用

### 前置需求

- Python 3.7+
- Node.js 14+
- MySQL 5.7+
- CMake（用於編譯 dlib）

### 安裝步驟

#### 1. 複製專案

```bash
git clone <repository-url>
cd sensei_face_reg
```

#### 2. 設定資料庫

```bash
# 登入 MySQL
mysql -u root -p

# 建立資料庫
CREATE DATABASE sensei_face_reg CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 匯入資料庫結構
USE sensei_face_reg;
SOURCE database/schema.sql;
```

#### 3. 設定後端

```bash
cd backend

# 建立虛擬環境
python -m venv venv

# 啟動虛擬環境
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 安裝依賴
pip install -r requirements.txt

# 設定環境變數
copy .env.example .env
# 編輯 .env 檔案，填入你的資料庫連線資訊

# 啟動後端伺服器
python app.py
```

後端會在 http://localhost:9453 啟動

#### 4. 設定前端

```bash
# 開啟新終端機
cd frontend

# 安裝依賴
npm install

# 設定環境變數
copy .env.example .env

# 啟動前端開發伺服器
npm start
```

前端會在 http://localhost:3000 啟動並自動開啟瀏覽器

### 使用說明

#### 上傳照片並標註

1. 點擊「上傳照片」分頁
2. 選擇包含人臉的照片
3. 點擊「上傳並偵測人臉」
4. 系統會自動偵測照片中的人臉
5. 為每個偵測到的人臉輸入姓名（可輸入中文和日文名稱）
6. 點擊「下一個」或「完成」儲存

#### 查看人物列表

1. 點擊「人物列表」分頁
2. 可以看到所有已建立的人物
3. 點擊人物可查看詳細資訊
4. 可以刪除不需要的人物

#### 開始複習

1. 點擊「開始複習」分頁
2. 點擊「開始複習」按鈕
3. 系統會隨機顯示一個人臉
4. 輸入你記得的姓名
5. 按 Enter 或點擊「提交答案」
6. 系統會顯示正確答案和你的答題結果
7. 點擊「下一題」繼續複習

### 常見問題

#### dlib 安裝失敗

Windows 使用者可能需要先安裝 Visual C++ 編譯工具：
- 下載並安裝 Visual Studio Build Tools
- 或使用預編譯的 wheel 檔案：`pip install dlib-xxx.whl`

#### 資料庫連線失敗

- 確認 MySQL 服務已啟動
- 檢查 `.env` 檔案中的資料庫連線資訊是否正確
- 確認資料庫用戶有足夠的權限

#### 前端無法連接後端

- 確認後端伺服器已啟動（http://localhost:5000）
- 檢查瀏覽器的 console 是否有 CORS 錯誤
- 確認防火牆沒有阻擋連線

---

## 🤝 開發者

TeddyCFHuang

---

## 📄 授權

本專案僅供個人使用
