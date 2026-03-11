from flask import Blueprint, request, jsonify
from extensions import db
from models import Face, ReviewRecord, Person
from sqlalchemy import func
import random

review_bp = Blueprint('review', __name__)

@review_bp.route('/review/random', methods=['GET'])
def get_random_face():
    """取得隨機人臉進行複習（含選擇題選項）"""
    try:
        person_id = request.args.get('person_id', type=int)

        query = Face.query
        if person_id:
            query = query.filter_by(person_id=person_id)

        faces = query.all()

        if not faces:
            return jsonify({
                'success': False,
                'message': '沒有可複習的人臉'
            }), 404

        face = random.choice(faces)
        correct_person = face.person

        # 取得其他人物作為干擾選項（最多 3 個）
        other_persons = Person.query.filter(Person.id != correct_person.id).all()
        num_distractors = min(3, len(other_persons))
        distractors = random.sample(other_persons, num_distractors) if other_persons else []

        # 組合並洗牌
        choices = [{'id': correct_person.id, 'name': correct_person.name, 'name_jp': correct_person.name_jp}]
        for p in distractors:
            choices.append({'id': p.id, 'name': p.name, 'name_jp': p.name_jp})
        random.shuffle(choices)

        return jsonify({
            'success': True,
            'face': face.to_dict(include_person=False),
            'choices': choices,
            'correct_person_id': correct_person.id
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@review_bp.route('/review/submit', methods=['POST'])
def submit_review():
    """提交複習結果"""
    data = request.get_json()
    
    required_fields = ['face_id', 'user_answer', 'is_correct']
    if not all(field in data for field in required_fields):
        return jsonify({'success': False, 'error': '缺少必要欄位'}), 400
    
    try:
        face = Face.query.get(data['face_id'])
        if not face:
            return jsonify({'success': False, 'error': '找不到人臉'}), 404
        
        # 建立複習記錄
        record = ReviewRecord(
            face_id=data['face_id'],
            is_correct=data['is_correct'],
            user_answer=data['user_answer'],
            response_time=data.get('response_time')
        )
        
        db.session.add(record)
        db.session.commit()
        
        # 返回正確答案
        return jsonify({
            'success': True,
            'message': '複習記錄已儲存',
            'correct_answer': {
                'name': face.person.name,
                'name_jp': face.person.name_jp
            },
            'record': record.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@review_bp.route('/review/statistics', methods=['GET'])
def get_statistics():
    """取得複習統計"""
    try:
        # 總複習次數
        total_reviews = ReviewRecord.query.count()
        
        # 答對次數
        correct_reviews = ReviewRecord.query.filter_by(is_correct=True).count()
        
        # 正確率
        accuracy = (correct_reviews / total_reviews * 100) if total_reviews > 0 else 0
        
        # 每個人的統計
        person_stats = db.session.query(
            Person.id,
            Person.name,
            Person.name_jp,
            func.count(ReviewRecord.id).label('review_count'),
            func.sum(ReviewRecord.is_correct).label('correct_count')
        ).join(Face).join(ReviewRecord).group_by(Person.id).all()
        
        person_statistics = []
        for stat in person_stats:
            person_statistics.append({
                'person_id': stat.id,
                'name': stat.name,
                'name_jp': stat.name_jp,
                'review_count': stat.review_count,
                'correct_count': stat.correct_count or 0,
                'accuracy': (stat.correct_count / stat.review_count * 100) if stat.review_count > 0 else 0
            })
        
        # 最近的複習記錄
        recent_reviews = ReviewRecord.query.order_by(
            ReviewRecord.review_date.desc()
        ).limit(10).all()
        
        return jsonify({
            'success': True,
            'overall': {
                'total_reviews': total_reviews,
                'correct_reviews': correct_reviews,
                'accuracy': round(accuracy, 2)
            },
            'by_person': person_statistics,
            'recent_reviews': [record.to_dict() for record in recent_reviews]
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@review_bp.route('/review/statistics/<int:person_id>', methods=['GET'])
def get_person_statistics(person_id):
    """取得特定人物的複習統計"""
    person = Person.query.get(person_id)
    
    if not person:
        return jsonify({'success': False, 'error': '找不到人物'}), 404
    
    try:
        # 該人物的所有人臉ID
        face_ids = [face.id for face in person.faces]
        
        # 該人物的複習記錄
        reviews = ReviewRecord.query.filter(ReviewRecord.face_id.in_(face_ids)).all()
        
        total_reviews = len(reviews)
        correct_reviews = sum(1 for r in reviews if r.is_correct)
        accuracy = (correct_reviews / total_reviews * 100) if total_reviews > 0 else 0
        
        return jsonify({
            'success': True,
            'person': person.to_dict(),
            'statistics': {
                'total_reviews': total_reviews,
                'correct_reviews': correct_reviews,
                'accuracy': round(accuracy, 2)
            },
            'recent_reviews': [r.to_dict() for r in reviews[-10:]]
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@review_bp.route('/review/reset', methods=['POST'])
def reset_reviews():
    """重置所有複習記錄（慎用！）"""
    try:
        ReviewRecord.query.delete()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '所有複習記錄已重置'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
