import face_recognition
import cv2
import numpy as np
from PIL import Image
import os

class FaceDetectionService:
    """人臉偵測服務"""
    
    def __init__(self, model='hog'):
        """
        初始化人臉偵測服務
        :param model: 偵測模型 ('hog' 或 'cnn')
        """
        self.model = model
    
    def detect_faces(self, image_path):
        """
        偵測圖片中的所有人臉
        :param image_path: 圖片路徑
        :return: 偵測結果 {'face_locations': [], 'face_encodings': [], 'image_shape': (h, w)}
        """
        try:
            # 載入圖片
            image = face_recognition.load_image_file(image_path)
            
            # 偵測人臉位置
            face_locations = face_recognition.face_locations(image, model=self.model)
            
            # 生成人臉編碼
            face_encodings = face_recognition.face_encodings(image, face_locations)
            
            return {
                'success': True,
                'face_count': len(face_locations),
                'face_locations': face_locations,
                'face_encodings': [encoding.tolist() for encoding in face_encodings],
                'image_shape': image.shape[:2]  # (height, width)
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'face_count': 0,
                'face_locations': [],
                'face_encodings': []
            }
    
    def draw_faces(self, image_path, face_locations, output_path=None):
        """
        在圖片上繪製人臉框
        :param image_path: 原始圖片路徑
        :param face_locations: 人臉位置列表
        :param output_path: 輸出圖片路徑（如不提供則不儲存）
        :return: 繪製後的圖片（numpy array）
        """
        # 讀取圖片
        image = cv2.imread(image_path)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # 繪製人臉框
        for i, (top, right, bottom, left) in enumerate(face_locations):
            # 繪製矩形框
            cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
            
            # 繪製編號
            cv2.rectangle(image, (left, bottom - 25), (right, bottom), (0, 255, 0), cv2.FILLED)
            cv2.putText(image, f"Face {i+1}", (left + 6, bottom - 6),
                       cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
        
        # 儲存結果
        if output_path:
            cv2.imwrite(output_path, image)
        
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    def crop_face(self, image_path, face_location, output_path=None, padding=20):
        """
        裁切單個人臉
        :param image_path: 原始圖片路徑
        :param face_location: 人臉位置 (top, right, bottom, left)
        :param output_path: 輸出路徑
        :param padding: 邊距像素
        :return: 裁切後的圖片
        """
        image = Image.open(image_path)
        top, right, bottom, left = face_location
        
        # 加入邊距
        width, height = image.size
        left = max(0, left - padding)
        top = max(0, top - padding)
        right = min(width, right + padding)
        bottom = min(height, bottom + padding)
        
        # 裁切
        face_image = image.crop((left, top, right, bottom))
        
        if output_path:
            face_image.save(output_path)
        
        return face_image
    
    def compare_faces(self, known_encoding, unknown_encoding, tolerance=0.6):
        """
        比對兩個人臉編碼
        :param known_encoding: 已知的人臉編碼
        :param unknown_encoding: 待比對的人臉編碼
        :param tolerance: 容錯率（越小越嚴格）
        :return: 是否匹配
        """
        if isinstance(known_encoding, list):
            known_encoding = np.array(known_encoding)
        if isinstance(unknown_encoding, list):
            unknown_encoding = np.array(unknown_encoding)
        
        matches = face_recognition.compare_faces([known_encoding], unknown_encoding, tolerance=tolerance)
        return matches[0] if matches else False
    
    def face_distance(self, known_encoding, unknown_encoding):
        """
        計算人臉距離（相似度）
        :param known_encoding: 已知的人臉編碼
        :param unknown_encoding: 待比對的人臉編碼
        :return: 距離值（越小越相似）
        """
        if isinstance(known_encoding, list):
            known_encoding = np.array(known_encoding)
        if isinstance(unknown_encoding, list):
            unknown_encoding = np.array(unknown_encoding)
        
        distances = face_recognition.face_distance([known_encoding], unknown_encoding)
        return float(distances[0]) if distances else 1.0
