from extensions import db
from datetime import datetime

class ReviewRecord(db.Model):
    """複習記錄模型"""
    __tablename__ = 'review_records'
    
    id = db.Column(db.Integer, primary_key=True)
    face_id = db.Column(db.Integer, db.ForeignKey('faces.id', ondelete='CASCADE'), nullable=False, index=True)
    is_correct = db.Column(db.Boolean, nullable=False, comment='是否答對')
    user_answer = db.Column(db.String(255), comment='使用者的答案')
    review_date = db.Column(db.DateTime, default=datetime.utcnow, index=True, comment='複習時間')
    response_time = db.Column(db.Integer, comment='回答時間(秒)')
    
    def to_dict(self):
        """轉換為字典格式"""
        return {
            'id': self.id,
            'face_id': self.face_id,
            'is_correct': self.is_correct,
            'user_answer': self.user_answer,
            'review_date': self.review_date.isoformat() if self.review_date else None,
            'response_time': self.response_time
        }
    
    def __repr__(self):
        return f'<ReviewRecord face_id={self.face_id} correct={self.is_correct}>'
