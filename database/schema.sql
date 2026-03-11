-- Sensei Face Recognition System Database Schema
-- 日本老師人臉辨識記憶系統資料庫結構

-- 建立資料庫（如需要）
-- CREATE DATABASE IF NOT EXISTS sensei_face_reg CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
-- USE sensei_face_reg;

-- 人物表
CREATE TABLE IF NOT EXISTS persons (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL COMMENT '姓名（中文或羅馬拼音）',
    name_jp VARCHAR(255) COMMENT '日文姓名',
    notes TEXT COMMENT '備註資訊',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '建立時間',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新時間',
    INDEX idx_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='人物資訊表';

-- 照片表
CREATE TABLE IF NOT EXISTS photos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255) NOT NULL COMMENT '檔案名稱',
    filepath VARCHAR(500) NOT NULL COMMENT '檔案路徑',
    original_filename VARCHAR(255) COMMENT '原始檔案名稱',
    file_size INT COMMENT '檔案大小(bytes)',
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '上傳時間',
    INDEX idx_upload_date (upload_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='照片資訊表';

-- 人臉資料表
CREATE TABLE IF NOT EXISTS faces (
    id INT AUTO_INCREMENT PRIMARY KEY,
    person_id INT NOT NULL COMMENT '人物ID',
    photo_id INT NOT NULL COMMENT '照片ID',
    face_encoding TEXT COMMENT '人臉編碼(128維特徵向量)',
    face_location VARCHAR(255) COMMENT '人臉位置座標(top,right,bottom,left)',
    confidence FLOAT COMMENT '辨識信心度',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '建立時間',
    FOREIGN KEY (person_id) REFERENCES persons(id) ON DELETE CASCADE,
    FOREIGN KEY (photo_id) REFERENCES photos(id) ON DELETE CASCADE,
    INDEX idx_person_id (person_id),
    INDEX idx_photo_id (photo_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='人臉資料表';

-- 複習記錄表
CREATE TABLE IF NOT EXISTS review_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    face_id INT NOT NULL COMMENT '人臉ID',
    is_correct BOOLEAN NOT NULL COMMENT '是否答對',
    user_answer VARCHAR(255) COMMENT '使用者的答案',
    review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '複習時間',
    response_time INT COMMENT '回答時間(秒)',
    FOREIGN KEY (face_id) REFERENCES faces(id) ON DELETE CASCADE,
    INDEX idx_face_id (face_id),
    INDEX idx_review_date (review_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='複習記錄表';

-- 插入測試資料（可選）
-- INSERT INTO persons (name, name_jp, notes) VALUES 
-- ('山田太郎', '山田太郎', '測試老師1'),
-- ('佐藤花子', '佐藤花子', '測試老師2');
