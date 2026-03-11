from flask import Flask
from flask_cors import CORS
from extensions import db
from config import Config

def create_app(config_class=Config):
    """應用程式工廠函式"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 初始化擴充套件
    db.init_app(app)
    CORS(app)  # 允許跨域請求
    
    # 初始化配置
    config_class.init_app(app)
    
    # 註冊藍圖（路由）
    from routes import upload_bp, face_bp, review_bp
    app.register_blueprint(upload_bp, url_prefix='/api')
    app.register_blueprint(face_bp, url_prefix='/api')
    app.register_blueprint(review_bp, url_prefix='/api')
    
    # 健康檢查端點
    @app.route('/health')
    def health_check():
        return {'status': 'ok', 'message': 'Sensei Face Recognition API is running'}
    
    # 首頁端點
    @app.route('/')
    def index():
        return {
            'message': 'Sensei Face Recognition System API',
            'version': '1.0.0',
            'endpoints': {
                'health': '/health',
                'upload': '/api/upload',
                'detect_faces': '/api/detect-faces',
                'save_face': '/api/save-face',
                'persons': '/api/persons',
                'photos': '/api/photos',
                'review': '/api/review'
            }
        }
    
    return app

# 建立應用程式實例（模組層級）
app = create_app()

if __name__ == '__main__':
    # 建立資料表（如果不存在）
    with app.app_context():
        db.create_all()
        print("資料庫表格已建立")
    
    # 啟動應用程式
    print("=" * 50)
    print("Sensei Face Recognition System API 啟動中...")
    print("=" * 50)
    app.run(host='0.0.0.0', port=9453, debug=True)
