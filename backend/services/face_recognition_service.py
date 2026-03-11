import numpy as np
from services.face_detection import FaceDetectionService
from models import Face, Person
from extensions import db

class FaceRecognitionService:
    """人臉辨識服務"""
    
    def __init__(self, tolerance=0.6):
        """
        初始化人臉辨識服務
        :param tolerance: 辨識容錯率
        """
        self.tolerance = tolerance
        self.face_detector = FaceDetectionService()
    
    def recognize_face(self, face_encoding):
        """
        辨識人臉，找出最匹配的人物
        :param face_encoding: 待辨識的人臉編碼
        :return: 辨識結果 {'person_id': int, 'person_name': str, 'distance': float}
        """
        # 取得所有已知的人臉編碼
        all_faces = Face.query.all()
        
        if not all_faces:
            return None
        
        best_match = None
        min_distance = 1.0
        
        for face in all_faces:
            if not face.face_encoding:
                continue
            
            # 將字串編碼轉換為 numpy array
            known_encoding = np.array(eval(face.face_encoding))
            
            # 計算距離
            distance = self.face_detector.face_distance(known_encoding, face_encoding)
            
            if distance < min_distance and distance <= self.tolerance:
                min_distance = distance
                best_match = {
                    'face_id': face.id,
                    'person_id': face.person_id,
                    'person_name': face.person.name if face.person else 'Unknown',
                    'person_name_jp': face.person.name_jp if face.person else None,
                    'distance': distance,
                    'confidence': 1 - distance
                }
        
        return best_match
    
    def recognize_faces_in_image(self, image_path):
        """
        辨識圖片中的所有人臉
        :param image_path: 圖片路徑
        :return: 辨識結果列表
        """
        # 偵測人臉
        detection_result = self.face_detector.detect_faces(image_path)
        
        if not detection_result['success']:
            return {
                'success': False,
                'error': detection_result.get('error'),
                'faces': []
            }
        
        results = []
        for i, (location, encoding) in enumerate(zip(
            detection_result['face_locations'],
            detection_result['face_encodings']
        )):
            # 辨識每個人臉
            match = self.recognize_face(encoding)
            
            results.append({
                'face_index': i,
                'face_location': location,
                'face_encoding': encoding,
                'recognition': match
            })
        
        return {
            'success': True,
            'face_count': len(results),
            'faces': results
        }
    
    def find_similar_faces(self, face_encoding, top_n=5):
        """
        找出最相似的N個人臉
        :param face_encoding: 待比對的人臉編碼
        :param top_n: 返回前N個結果
        :return: 相似人臉列表
        """
        all_faces = Face.query.all()
        
        similarities = []
        for face in all_faces:
            if not face.face_encoding:
                continue
            
            known_encoding = np.array(eval(face.face_encoding))
            distance = self.face_detector.face_distance(known_encoding, face_encoding)
            
            similarities.append({
                'face_id': face.id,
                'person_id': face.person_id,
                'person_name': face.person.name if face.person else 'Unknown',
                'distance': distance,
                'confidence': 1 - distance
            })
        
        # 排序並返回前N個
        similarities.sort(key=lambda x: x['distance'])
        return similarities[:top_n]
    
    def save_face_with_encoding(self, person_id, photo_id, face_location, face_encoding):
        """
        儲存人臉資料及編碼
        :param person_id: 人物ID
        :param photo_id: 照片ID
        :param face_location: 人臉位置
        :param face_encoding: 人臉編碼
        :return: 儲存的Face物件
        """
        # 將編碼轉換為字串儲存
        encoding_str = str(face_encoding)
        location_str = ','.join(map(str, face_location))
        
        face = Face(
            person_id=person_id,
            photo_id=photo_id,
            face_encoding=encoding_str,
            face_location=location_str,
            confidence=1.0
        )
        
        db.session.add(face)
        db.session.commit()
        
        return face
