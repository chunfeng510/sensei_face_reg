from extensions import db
from datetime import datetime

class Person(db.Model):
    """人物模型"""
    __tablename__ = 'persons'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, index=True, comment='姓名（中文或羅馬拼音）')
    name_jp = db.Column(db.String(255), comment='日文姓名')
    notes = db.Column(db.Text, comment='備註資訊')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='建立時間')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新時間')
    
    # 關聯
    faces = db.relationship('Face', backref='person', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """轉換為字典格式"""
        return {
            'id': self.id,
            'name': self.name,
            'name_jp': self.name_jp,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'face_count': len(self.faces)
        }
    
    def __repr__(self):
        return f'<Person {self.name}>'
