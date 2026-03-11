from flask import Blueprint, request, jsonify, send_file
from extensions import db
from models import Person, Face, Photo
from services import FaceRecognitionService
from PIL import Image
import json
import io
import os

face_bp = Blueprint('face', __name__)
face_recognizer = FaceRecognitionService()

@face_bp.route('/save-face', methods=['POST'])
def save_face():
    """儲存人臉與姓名"""
    data = request.get_json()
    
    required_fields = ['name', 'photo_id', 'face_location', 'face_encoding']
    if not all(field in data for field in required_fields):
        return jsonify({'success': False, 'error': '缺少必要欄位'}), 400
    
    try:
        # 檢查照片是否存在
        photo = Photo.query.get(data['photo_id'])
        if not photo:
            return jsonify({'success': False, 'error': '找不到照片'}), 404
        
        # 查找或建立人物
        person = Person.query.filter_by(name=data['name']).first()
        if not person:
            person = Person(
                name=data['name'],
                name_jp=data.get('name_jp'),
                notes=data.get('notes')
            )
            db.session.add(person)
            db.session.flush()  # 取得person.id
        
        # 儲存人臉資料
        face = face_recognizer.save_face_with_encoding(
            person_id=person.id,
            photo_id=data['photo_id'],
            face_location=data['face_location'],
            face_encoding=data['face_encoding']
        )
        
        return jsonify({
            'success': True,
            'message': '人臉資料已儲存',
            'person': person.to_dict(),
            'face': face.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@face_bp.route('/recognize-face', methods=['POST'])
def recognize_face():
    """辨識人臉"""
    data = request.get_json()
    
    if not data or 'face_encoding' not in data:
        return jsonify({'success': False, 'error': '缺少face_encoding參數'}), 400
    
    try:
        result = face_recognizer.recognize_face(data['face_encoding'])
        
        if result:
            return jsonify({
                'success': True,
                'recognized': True,
                'result': result
            }), 200
        else:
            return jsonify({
                'success': True,
                'recognized': False,
                'message': '未辨識出已知人物'
            }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@face_bp.route('/persons', methods=['GET'])
def get_persons():
    """取得所有人物列表"""
    try:
        persons = Person.query.order_by(Person.created_at.desc()).all()
        return jsonify({
            'success': True,
            'persons': [person.to_dict() for person in persons]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@face_bp.route('/persons/<int:person_id>', methods=['GET'])
def get_person(person_id):
    """取得特定人物詳情"""
    person = Person.query.get(person_id)
    
    if not person:
        return jsonify({'success': False, 'error': '找不到人物'}), 404
    
    # 取得該人物的所有人臉
    faces = Face.query.filter_by(person_id=person_id).all()
    
    return jsonify({
        'success': True,
        'person': person.to_dict(),
        'faces': [face.to_dict() for face in faces]
    }), 200

@face_bp.route('/persons/<int:person_id>', methods=['PUT'])
def update_person(person_id):
    """更新人物資訊"""
    person = Person.query.get(person_id)
    
    if not person:
        return jsonify({'success': False, 'error': '找不到人物'}), 404
    
    data = request.get_json()
    
    try:
        if 'name' in data:
            person.name = data['name']
        if 'name_jp' in data:
            person.name_jp = data['name_jp']
        if 'notes' in data:
            person.notes = data['notes']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '人物資訊已更新',
            'person': person.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@face_bp.route('/persons/<int:person_id>', methods=['DELETE'])
def delete_person(person_id):
    """刪除人物（及其所有人臉資料）"""
    person = Person.query.get(person_id)
    
    if not person:
        return jsonify({'success': False, 'error': '找不到人物'}), 404
    
    try:
        db.session.delete(person)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '人物已刪除'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@face_bp.route('/faces/<int:face_id>/image', methods=['GET'])
def get_face_image(face_id):
    """取得裁切後的人臉圖片"""
    face = Face.query.get(face_id)
    if not face:
        return jsonify({'success': False, 'error': '找不到人臉資料'}), 404

    photo = face.photo
    if not photo or not os.path.exists(photo.filepath):
        return jsonify({'success': False, 'error': '找不到照片檔案'}), 404

    try:
        # face_location 格式：'top,right,bottom,left'
        top, right, bottom, left = [int(x) for x in face.face_location.split(',')]

        img = Image.open(photo.filepath).convert('RGB')
        img_w, img_h = img.size

        # 加邊距讓臉部不會太緊
        padding = max(30, int((bottom - top) * 0.4))
        crop_top    = max(0, top - padding)
        crop_left   = max(0, left - padding)
        crop_bottom = min(img_h, bottom + padding)
        crop_right  = min(img_w, right + padding)

        cropped = img.crop((crop_left, crop_top, crop_right, crop_bottom))
        cropped.thumbnail((300, 300))

        img_io = io.BytesIO()
        cropped.save(img_io, 'JPEG', quality=85)
        img_io.seek(0)

        return send_file(img_io, mimetype='image/jpeg')

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@face_bp.route('/faces', methods=['GET'])
def get_faces():
    """取得所有人臉列表"""
    try:
        # 支援分頁
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        pagination = Face.query.order_by(Face.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'success': True,
            'faces': [face.to_dict() for face in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@face_bp.route('/faces/<int:face_id>', methods=['DELETE'])
def delete_face(face_id):
    """刪除特定人臉資料"""
    face = Face.query.get(face_id)
    
    if not face:
        return jsonify({'success': False, 'error': '找不到人臉資料'}), 404
    
    try:
        db.session.delete(face)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '人臉資料已刪除'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
