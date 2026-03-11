import React, { useState } from 'react';
import {
  Box, Typography, Button, Paper, TextField, Alert,
  CircularProgress, Card, CardMedia, CardContent, CardActions
} from '@mui/material';
import { Quiz, CheckCircle, Cancel } from '@mui/icons-material';
import { apiService } from '../services/api';

function Review() {
  const [currentFace, setCurrentFace] = useState(null);
  const [userAnswer, setUserAnswer] = useState('');
  const [showResult, setShowResult] = useState(false);
  const [isCorrect, setIsCorrect] = useState(false);
  const [correctAnswer, setCorrectAnswer] = useState(null);
  const [loading, setLoading] = useState(false);
  const [startTime, setStartTime] = useState(null);
  const [statistics, setStatistics] = useState(null);

  const startReview = async () => {
    setLoading(true);
    try {
      const result = await apiService.getRandomFace();
      if (result.success) {
        setCurrentFace(result.face);
        setUserAnswer('');
        setShowResult(false);
        setStartTime(Date.now());
      } else {
        alert('沒有可複習的人臉');
      }
    } catch (err) {
      alert(`載入失敗：${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async () => {
    if (!userAnswer.trim()) {
      alert('請輸入答案');
      return;
    }

    setLoading(true);
    try {
      const responseTime = Math.floor((Date.now() - startTime) / 1000);
      
      // 這裡簡化處理，實際應該由後端判斷是否正確
      // 目前由前端判斷（僅供演示）
      const result = await apiService.submitReview({
        face_id: currentFace.id,
        user_answer: userAnswer.trim(),
        is_correct: false, // 暫時預設，實際需要後端判斷
        response_time: responseTime
      });

      if (result.success) {
        setCorrectAnswer(result.correct_answer);
        setIsCorrect(result.correct_answer.name.toLowerCase() === userAnswer.trim().toLowerCase());
        setShowResult(true);
      }
    } catch (err) {
      alert(`提交失敗：${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const loadStatistics = async () => {
    try {
      const result = await apiService.getStatistics();
      if (result.success) {
        setStatistics(result.overall);
      }
    } catch (err) {
      console.error('載入統計失敗', err);
    }
  };

  React.useEffect(() => {
    loadStatistics();
  }, []);

  return (
    <Box>
      <Typography 
        variant="h5" 
        gutterBottom
        sx={{ fontSize: { xs: '1.25rem', sm: '1.5rem' } }}
      >
        複習模式
      </Typography>

      {statistics && (
        <Alert 
          severity="info" 
          sx={{ 
            mb: 2,
            fontSize: { xs: '0.875rem', sm: '1rem' },
            '& .MuiAlert-message': {
              width: '100%'
            }
          }}
        >
          <Box sx={{ display: 'flex', flexDirection: { xs: 'column', sm: 'row' }, gap: { xs: 0.5, sm: 1 } }}>
            <span>總複習：{statistics.total_reviews}</span>
            <span sx={{ display: { xs: 'none', sm: 'inline' } }}> | </span>
            <span>答對：{statistics.correct_reviews}</span>
            <span sx={{ display: { xs: 'none', sm: 'inline' } }}> | </span>
            <span>正確率：{statistics.accuracy}%</span>
          </Box>
        </Alert>
      )}

      {!currentFace ? (
        <Paper sx={{ 
          p: { xs: 2, sm: 3 }, 
          textAlign: 'center',
          bgcolor: 'white'
        }}>
          <Typography 
            variant="body1" 
            gutterBottom
            sx={{ fontSize: { xs: '0.95rem', sm: '1rem' } }}
          >
            點擊下方按鈕開始隨機複習
          </Typography>
          <Button
            variant="contained"
            size="large"
            startIcon={<Quiz />}
            onClick={startReview}
            disabled={loading}
            fullWidth
            sx={{ 
              mt: 2,
              py: { xs: 1.5, sm: 1 },
              fontSize: { xs: '1rem', sm: '0.875rem' }
            }}
          >
            {loading ? <CircularProgress size={24} /> : '開始複習'}
          </Button>
        </Paper>
      ) : (
        <Card sx={{ 
          maxWidth: 600, 
          mx: 'auto',
          boxShadow: { xs: 2, sm: 3 }
        }}>
          {currentFace.photo && (
            <CardMedia
              component="img"
              height="400"
              image={`http://localhost:5000/api/uploads/${currentFace.photo.filename}`}
              alt="人臉照片"
            />
          )}
          <CardContent sx={{ p: { xs: 2, sm: 3 } }}>
            {!showResult ? (
              <>
                <Typography 
                  variant="h6" 
                  gutterBottom
                  sx={{ fontSize: { xs: '1.1rem', sm: '1.25rem' } }}
                >
                  這是誰？
                </Typography>
                <TextField
                  fullWidth
                  label="請輸入姓名"
                  value={userAnswer}
                  onChange={(e) => setUserAnswer(e.target.value)}
                  onKeyPress={(e) => {
                    if (e.key === 'Enter') {
                      handleSubmit();
                    }
                  }}
                  autoFocus
                  sx={{ 
                    mt: 2,
                    '& .MuiInputBase-input': {
                      fontSize: { xs: '1rem', sm: '1rem' }
                    }
                  }}
                  inputProps={{ 
                    style: { fontSize: '16px' },
                    autoComplete: 'off'
                  }}
                  size="large"
                />
              </>
            ) : (
              <Box sx={{ textAlign: 'center', py: { xs: 2, sm: 3 } }}>
                {isCorrect ? (
                  <>
                    <CheckCircle sx={{ 
                      fontSize: { xs: 50, sm: 60 }, 
                      color: 'success.main' 
                    }} />
                    <Typography 
                      variant="h6" 
                      color="success.main" 
                      sx={{ 
                        mt: 2,
                        fontSize: { xs: '1.1rem', sm: '1.25rem' }
                      }}
                    >
                      答對了！
                    </Typography>
                  </>
                ) : (
                  <>
                    <Cancel sx={{ 
                      fontSize: { xs: 50, sm: 60 }, 
                      color: 'error.main' 
                    }} />
                    <Typography 
                      variant="h6" 
                      color="error.main" 
                      sx={{ 
                        mt: 2,
                        fontSize: { xs: '1.1rem', sm: '1.25rem' }
                      }}
                    >
                      答錯了
                    </Typography>
                    <Typography 
                      variant="body1" 
                      sx={{ 
                        mt: 1,
                        fontSize: { xs: '0.95rem', sm: '1rem' },
                        fontWeight: 500
                      }}
                    >
                      正確答案：{correctAnswer.name}
                      {correctAnswer.name_jp && ` (${correctAnswer.name_jp})`}
                    </Typography>
                  </>
                )}
              </Box>
            )}
          </CardContent>
          <CardActions sx={{ 
            justifyContent: 'center', 
            p: { xs: 2, sm: 2 },
            pt: 0
          }}>
            {!showResult ? (
              <Button
                variant="contained"
                onClick={handleSubmit}
                disabled={loading}
                fullWidth
                size="large"
                sx={{ py: 1.5 }}
              >
                {loading ? '提交中...' : '提交答案'}
              </Button>
            ) : (
              <Button
                variant="contained"
                onClick={startReview}
                fullWidth
                size="large"
                sx={{ py: 1.5 }}
              >
                下一題
              </Button>
            )}
          </CardActions>
        </Card>
      )}
    </Box>
  );
}

export default Review;
