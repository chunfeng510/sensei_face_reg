import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

class Config:
    """應用程式配置類別"""
    
    # 基本配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    
    # 資料庫配置
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '3306')
    DB_NAME = os.getenv('DB_NAME', 'sensei_face_reg')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    
    # SQLAlchemy 配置
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = DEBUG
    
    # 檔案上傳配置
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # 人臉辨識配置
    FACE_DETECTION_MODEL = 'hog'  # 'hog' 或 'cnn'
    FACE_RECOGNITION_TOLERANCE = 0.6  # 辨識容錯率（越小越嚴格）
    
    @staticmethod
    def init_app(app):
        """初始化應用程式"""
        # 確保上傳目錄存在
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
