from extensions import db
from datetime import datetime

class Photo(db.Model):
    """照片模型"""
    __tablename__ = 'photos'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False, comment='檔案名稱')
    filepath = db.Column(db.String(500), nullable=False, comment='檔案路徑')
    original_filename = db.Column(db.String(255), comment='原始檔案名稱')
    file_size = db.Column(db.Integer, comment='檔案大小(bytes)')
    upload_date = db.Column(db.DateTime, default=datetime.utcnow, index=True, comment='上傳時間')
    
    # 關聯
    faces = db.relationship('Face', backref='photo', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """轉換為字典格式"""
        return {
            'id': self.id,
            'filename': self.filename,
            'filepath': self.filepath,
            'original_filename': self.original_filename,
            'file_size': self.file_size,
            'upload_date': self.upload_date.isoformat() if self.upload_date else None,
            'face_count': len(self.faces)
        }
    
    def __repr__(self):
        return f'<Photo {self.filename}>'
