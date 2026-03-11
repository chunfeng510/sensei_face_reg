from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from extensions import db
from models import Photo
from services import FaceDetectionService
from config import Config
import os
import uuid
from datetime import datetime

upload_bp = Blueprint('upload', __name__)
face_detector = FaceDetectionService(model=Config.FACE_DETECTION_MODEL)

def allowed_file(filename):
    """檢查檔案類型是否允許"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@upload_bp.route('/upload', methods=['POST'])
def upload_photo():
    """上傳照片"""
    if 'photo' not in request.files:
        return jsonify({'success': False, 'error': '沒有上傳檔案'}), 400
    
    file = request.files['photo']
    
    if file.filename == '':
        return jsonify({'success': False, 'error': '沒有選擇檔案'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'success': False, 'error': '不支援的檔案類型'}), 400
    
    try:
        # 生成唯一檔名
        original_filename = secure_filename(file.filename)
        ext = original_filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        
        # 儲存檔案
        file.save(filepath)
        file_size = os.path.getsize(filepath)
        
        # 儲存到資料庫
        photo = Photo(
            filename=filename,
            filepath=filepath,
            original_filename=original_filename,
            file_size=file_size
        )
        db.session.add(photo)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '照片上傳成功',
            'photo': photo.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@upload_bp.route('/detect-faces', methods=['POST'])
def detect_faces():
    """偵測照片中的人臉"""
    data = request.get_json()
    
    if not data or 'photo_id' not in data:
        return jsonify({'success': False, 'error': '缺少photo_id參數'}), 400
    
    photo_id = data['photo_id']
    photo = Photo.query.get(photo_id)
    
    if not photo:
        return jsonify({'success': False, 'error': '找不到照片'}), 404
    
    try:
        # 偵測人臉
        result = face_detector.detect_faces(photo.filepath)
        
        if not result['success']:
            return jsonify(result), 500
        
        return jsonify({
            'success': True,
            'photo_id': photo_id,
            'face_count': result['face_count'],
            'face_locations': result['face_locations'],
            'face_encodings': result['face_encodings'],
            'image_shape': result['image_shape']
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@upload_bp.route('/photos', methods=['GET'])
def get_photos():
    """取得所有照片列表"""
    try:
        photos = Photo.query.order_by(Photo.upload_date.desc()).all()
        return jsonify({
            'success': True,
            'photos': [photo.to_dict() for photo in photos]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@upload_bp.route('/photos/<int:photo_id>', methods=['GET'])
def get_photo(photo_id):
    """取得特定照片資訊"""
    photo = Photo.query.get(photo_id)
    
    if not photo:
        return jsonify({'success': False, 'error': '找不到照片'}), 404
    
    return jsonify({
        'success': True,
        'photo': photo.to_dict()
    }), 200

@upload_bp.route('/photos/<int:photo_id>', methods=['DELETE'])
def delete_photo(photo_id):
    """刪除照片"""
    photo = Photo.query.get(photo_id)
    
    if not photo:
        return jsonify({'success': False, 'error': '找不到照片'}), 404
    
    try:
        # 刪除實體檔案
        if os.path.exists(photo.filepath):
            os.remove(photo.filepath)
        
        # 刪除資料庫記錄（會自動刪除關聯的人臉資料）
        db.session.delete(photo)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '照片已刪除'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@upload_bp.route('/uploads/<filename>', methods=['GET'])
def serve_photo(filename):
    """提供照片檔案"""
    return send_from_directory(Config.UPLOAD_FOLDER, filename)
