import React, { useState } from 'react';
import {
  Box, Button, Typography, Paper, Alert, CircularProgress,
  TextField, Dialog, DialogTitle, DialogContent, DialogActions
} from '@mui/material';
import { CloudUpload } from '@mui/icons-material';
import { apiService } from '../services/api';

function UploadPhoto() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);
  const [faces, setFaces] = useState([]);
  const [currentFaceIndex, setCurrentFaceIndex] = useState(0);
  const [showNameDialog, setShowNameDialog] = useState(false);
  const [name, setName] = useState('');
  const [nameJp, setNameJp] = useState('');
  const [photoId, setPhotoId] = useState(null);
  // 儲存圖片原始尺寸，用來計算框框百分比位置
  const [imgSize, setImgSize] = useState({ width: 1, height: 1 });

  const handleImgLoad = (e) => {
    setImgSize({
      width: e.target.naturalWidth,
      height: e.target.naturalHeight,
    });
  };



  const handleFileSelect = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setPreview(URL.createObjectURL(selectedFile));
      setMessage(null);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage({ type: 'error', text: '請選擇檔案' });
      return;
    }

    setLoading(true);
    try {
      // 1. 上傳照片
      const uploadResult = await apiService.uploadPhoto(file);
      if (!uploadResult.success) {
        throw new Error(uploadResult.error);
      }

      setPhotoId(uploadResult.photo.id);
      setMessage({ type: 'success', text: '照片上傳成功！偵測人臉中...' });

      // 2. 偵測人臉
      const detectResult = await apiService.detectFaces(uploadResult.photo.id);
      if (!detectResult.success) {
        throw new Error(detectResult.error);
      }

      if (detectResult.face_count === 0) {
        setMessage({ type: 'warning', text: '未偵測到人臉，請嘗試其他照片' });
      } else {
        setMessage({ type: 'success', text: `偵測到 ${detectResult.face_count} 個人臉！` });
        
        // 準備人臉資料
        const faceData = detectResult.face_locations.map((location, index) => ({
          location,
          encoding: detectResult.face_encodings[index]
        }));
        
        setFaces(faceData);
        setCurrentFaceIndex(0);
        setShowNameDialog(true);
      }
    } catch (error) {
      setMessage({ type: 'error', text: `錯誤：${error.message}` });
    } finally {
      setLoading(false);
    }
  };

  const handleSaveFace = async () => {
    if (!name.trim()) {
      alert('請輸入姓名');
      return;
    }

    setLoading(true);
    try {
      const currentFace = faces[currentFaceIndex];
      
      await apiService.saveFace({
        name: name.trim(),
        name_jp: nameJp.trim() || null,
        photo_id: photoId,
        face_location: currentFace.location,
        face_encoding: currentFace.encoding
      });

      // 如果還有更多人臉，繼續標註
      if (currentFaceIndex < faces.length - 1) {
        setCurrentFaceIndex(currentFaceIndex + 1);
        setName('');
        setNameJp('');
      } else {
        // 完成所有標註
        setShowNameDialog(false);
        setMessage({ type: 'success', text: '所有人臉標註完成！' });
        setFile(null);
        setPreview(null);
        setFaces([]);
      }
    } catch (error) {
      setMessage({ type: 'error', text: `儲存失敗：${error.message}` });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Typography 
        variant="h5" 
        gutterBottom
        sx={{ fontSize: { xs: '1.25rem', sm: '1.5rem' } }}
      >
        上傳照片並標註人臉
      </Typography>

      {message && (
        <Alert 
          severity={message.type} 
          sx={{ 
            mb: 2,
            fontSize: { xs: '0.875rem', sm: '1rem' }
          }}
        >
          {message.text}
        </Alert>
      )}

      <Paper sx={{ 
        p: { xs: 2, sm: 3 }, 
        textAlign: 'center',
        bgcolor: 'white'
      }}>
        <input
          accept="image/*"
          style={{ display: 'none' }}
          id="photo-upload"
          type="file"
          onChange={handleFileSelect}
        />
        <label htmlFor="photo-upload">
          <Button
            variant="contained"
            component="span"
            startIcon={<CloudUpload />}
            size="large"
          >
            選擇照片
          </Button>
        </label>

        {preview && (
          <Box sx={{ mt: { xs: 2, sm: 3 } }}>
            <img
              src={preview}
              alt="預覽"
              onLoad={handleImgLoad}
              style={{ 
                maxWidth: '100%', 
                maxHeight: '400px',
                borderRadius: '8px',
                boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
              }}
            />
            <Box sx={{ mt: 2 }}>
              <Button
                variant="contained"
                color="primary"
                onClick={handleUpload}
                disabled={loading}
                fullWidth
                size="large"
                sx={{ 
                  py: { xs: 1.5, sm: 1 },
                  fontSize: { xs: '1rem', sm: '0.875rem' }
                }}
              >
                {loading ? <CircularProgress size={24} /> : '上傳並偵測人臉'}
              </Button>
            </Box>
          </Box>
        )}
      </Paper>

      {/* 姓名輸入對話框 */}
      <Dialog 
        open={showNameDialog} 
        onClose={() => {}}
        fullWidth
        maxWidth="sm"
        PaperProps={{
          sx: {
            m: { xs: 1, sm: 3 },
            maxHeight: { xs: '95vh', sm: '90vh' }
          }
        }}
      >
        <DialogTitle sx={{ 
          fontSize: { xs: '1.1rem', sm: '1.25rem' },
          pb: 0
        }}>
          標註人臉 {currentFaceIndex + 1} / {faces.length}
        </DialogTitle>
        <DialogContent sx={{ pt: 1, pb: 1, overflow: 'auto' }}>
          {/* 人臉位置提示圖（CSS overlay） */}
          <Box sx={{ mb: 2, borderRadius: 2, overflow: 'hidden', bgcolor: '#111' }}>
            <Box sx={{ position: 'relative', display: 'block', lineHeight: 0 }}>
              <img
                src={preview}
                alt="人臉位置"
                onLoad={handleImgLoad}
                style={{ width: '100%', display: 'block' }}
              />
              {/* 為每張偵測到的臉疊加框框 */}
              {faces.map((face, index) => {
                const [top, right, bottom, left] = face.location;
                const { width: W, height: H } = imgSize;
                const isCurrent = index === currentFaceIndex;
                return (
                  <Box
                    key={index}
                    sx={{
                      position: 'absolute',
                      left: `${(left / W) * 100}%`,
                      top: `${(top / H) * 100}%`,
                      width: `${((right - left) / W) * 100}%`,
                      height: `${((bottom - top) / H) * 100}%`,
                      border: isCurrent ? '3px solid #FF6B00' : '2px solid rgba(200,200,200,0.7)',
                      bgcolor: isCurrent ? 'rgba(255,107,0,0.18)' : 'rgba(255,255,255,0.05)',
                      boxSizing: 'border-box',
                      boxShadow: isCurrent ? '0 0 0 2px rgba(255,107,0,0.4)' : 'none',
                    }}
                  >
                    {/* 角標 */}
                    <Box sx={{
                      position: 'absolute',
                      top: -1,
                      left: -1,
                      bgcolor: isCurrent ? '#FF6B00' : 'rgba(180,180,180,0.85)',
                      color: '#fff',
                      fontSize: '11px',
                      fontWeight: 'bold',
                      px: 0.6,
                      lineHeight: '18px',
                      borderRadius: '0 0 4px 0',
                    }}>
                      {isCurrent ? `▶ ${index + 1}` : index + 1}
                    </Box>
                  </Box>
                );
              })}
            </Box>
            <Typography variant="caption" sx={{
              display: 'block',
              textAlign: 'center',
              color: '#FF6B00',
              fontWeight: 'bold',
              py: 0.5,
              bgcolor: '#1a1a1a',
            }}>
              ▶ 橘色框 = 目前要標註的人臉
            </Typography>
          </Box>

          <TextField
            autoFocus
            margin="dense"
            label="姓名（中文或羅馬拼音）"
            fullWidth
            value={name}
            onChange={(e) => setName(e.target.value)}
            onKeyDown={(e) => { if (e.key === 'Enter' && name.trim()) handleSaveFace(); }}
            sx={{ mb: 2 }}
            inputProps={{ style: { fontSize: '16px' } }}
          />
          <TextField
            margin="dense"
            label="日文姓名（選填）"
            fullWidth
            value={nameJp}
            onChange={(e) => setNameJp(e.target.value)}
            inputProps={{ style: { fontSize: '16px' } }}
          />
        </DialogContent>
        <DialogActions sx={{ p: { xs: 2, sm: 2 } }}>
          <Button 
            onClick={handleSaveFace} 
            disabled={loading}
            variant="contained"
            fullWidth
            size="large"
            sx={{ py: 1.5 }}
          >
            {loading ? '儲存中...' : (currentFaceIndex < faces.length - 1 ? `儲存，標註下一張 (${currentFaceIndex + 2}/${faces.length})` : '完成')}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default UploadPhoto;
