from extensions import db
from datetime import datetime

class Face(db.Model):
    """人臉資料模型"""
    __tablename__ = 'faces'
    
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id', ondelete='CASCADE'), nullable=False, index=True)
    photo_id = db.Column(db.Integer, db.ForeignKey('photos.id', ondelete='CASCADE'), nullable=False, index=True)
    face_encoding = db.Column(db.Text, comment='人臉編碼(128維特徵向量)')
    face_location = db.Column(db.String(255), comment='人臉位置座標(top,right,bottom,left)')
    confidence = db.Column(db.Float, comment='辨識信心度')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='建立時間')
    
    # 關聯
    review_records = db.relationship('ReviewRecord', backref='face', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self, include_person=True, include_photo=True):
        """轉換為字典格式"""
        result = {
            'id': self.id,
            'person_id': self.person_id,
            'photo_id': self.photo_id,
            'face_location': self.face_location,
            'confidence': self.confidence,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
        
        if include_person and self.person:
            result['person'] = {
                'id': self.person.id,
                'name': self.person.name,
                'name_jp': self.person.name_jp
            }
        
        if include_photo and self.photo:
            result['photo'] = {
                'id': self.photo.id,
                'filename': self.photo.filename,
                'filepath': self.photo.filepath
            }
        
        return result
    
    def __repr__(self):
        return f'<Face person_id={self.person_id} photo_id={self.photo_id}>'
