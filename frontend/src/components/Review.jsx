import React, { useState } from 'react';
import {
  Box, Typography, Button, Paper, Alert,
  CircularProgress, Card, CardMedia, CardContent, CardActions
} from '@mui/material';
import { Quiz, CheckCircle, Cancel } from '@mui/icons-material';
import { apiService } from '../services/api';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:9453/api';
// Docker 環境下 REACT_APP_API_URL=/api，透過 nginx 反向代理

function Review() {
  const [currentFace, setCurrentFace] = useState(null);
  const [choices, setChoices] = useState([]);
  const [correctPersonId, setCorrectPersonId] = useState(null);
  const [selectedChoice, setSelectedChoice] = useState(null);
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
        setChoices(result.choices || []);
        setCorrectPersonId(result.correct_person_id);
        setSelectedChoice(null);
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

  const handleChoiceClick = async (choice) => {
    if (showResult || loading) return;

    const correct = choice.id === correctPersonId;
    const correctChoice = choices.find(c => c.id === correctPersonId);
    const responseTime = Math.floor((Date.now() - startTime) / 1000);

    setSelectedChoice(choice);
    setIsCorrect(correct);
    setCorrectAnswer(correctChoice);
    setShowResult(true);

    try {
      await apiService.submitReview({
        face_id: currentFace.id,
        user_answer: choice.name,
        is_correct: correct,
        response_time: responseTime
      });
      loadStatistics();
    } catch (err) {
      console.error('提交記錄失敗', err);
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

  const getChoiceButtonSx = (choice) => {
    const base = {
      py: 1.5,
      fontSize: { xs: '0.9rem', sm: '0.95rem' },
      textTransform: 'none',
      justifyContent: 'flex-start',
      px: 2,
    };
    if (!showResult) return base;
    if (choice.id === correctPersonId) {
      return {
        ...base,
        bgcolor: 'success.main',
        color: 'white',
        borderColor: 'success.main',
        '&.Mui-disabled': { bgcolor: 'success.main', color: 'white', opacity: 1 },
      };
    }
    if (selectedChoice && choice.id === selectedChoice.id) {
      return {
        ...base,
        bgcolor: 'error.main',
        color: 'white',
        borderColor: 'error.main',
        '&.Mui-disabled': { bgcolor: 'error.main', color: 'white', opacity: 1 },
      };
    }
    return { ...base, opacity: 0.45 };
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom sx={{ fontSize: { xs: '1.25rem', sm: '1.5rem' } }}>
        複習模式
      </Typography>

      {statistics && (
        <Alert
          severity="info"
          sx={{ mb: 2, fontSize: { xs: '0.875rem', sm: '1rem' }, '& .MuiAlert-message': { width: '100%' } }}
        >
          <Box sx={{ display: 'flex', flexDirection: { xs: 'column', sm: 'row' }, gap: { xs: 0.5, sm: 1 } }}>
            <span>總複習：{statistics.total_reviews}</span>
            <span> | </span>
            <span>答對：{statistics.correct_reviews}</span>
            <span> | </span>
            <span>正確率：{statistics.accuracy}%</span>
          </Box>
        </Alert>
      )}

      {!currentFace ? (
        <Paper sx={{ p: { xs: 2, sm: 3 }, textAlign: 'center', bgcolor: 'white' }}>
          <Typography variant="body1" gutterBottom sx={{ fontSize: { xs: '0.95rem', sm: '1rem' } }}>
            點擊下方按鈕開始隨機複習
          </Typography>
          <Button
            variant="contained"
            size="large"
            startIcon={<Quiz />}
            onClick={startReview}
            disabled={loading}
            fullWidth
            sx={{ mt: 2, py: { xs: 1.5, sm: 1 }, fontSize: { xs: '1rem', sm: '0.875rem' } }}
          >
            {loading ? <CircularProgress size={24} /> : '開始複習'}
          </Button>
        </Paper>
      ) : (
        <Card sx={{ maxWidth: 600, mx: 'auto', boxShadow: { xs: 2, sm: 3 } }}>
          <CardMedia
            component="img"
            height="300"
            image={`${API_BASE_URL}/faces/${currentFace.id}/image`}
            alt="人臉照片"
            sx={{ objectFit: 'cover', bgcolor: '#f5f5f5' }}
          />
          <CardContent sx={{ p: { xs: 2, sm: 3 } }}>
            <Typography
              variant="h6"
              gutterBottom
              sx={{ fontSize: { xs: '1.1rem', sm: '1.25rem' }, textAlign: 'center', mb: 2 }}
            >
              這是誰？
            </Typography>

            {/* 結果提示 */}
            {showResult && (
              <Box sx={{ textAlign: 'center', mb: 2 }}>
                {isCorrect ? (
                  <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 1 }}>
                    <CheckCircle sx={{ color: 'success.main', fontSize: 32 }} />
                    <Typography variant="h6" color="success.main">答對了！🎉</Typography>
                  </Box>
                ) : (
                  <Box>
                    <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 1 }}>
                      <Cancel sx={{ color: 'error.main', fontSize: 32 }} />
                      <Typography variant="h6" color="error.main">答錯了</Typography>
                    </Box>
                    <Typography variant="body1" sx={{ mt: 0.5, fontWeight: 500 }}>
                      正確答案：{correctAnswer?.name}
                      {correctAnswer?.name_jp && ` (${correctAnswer.name_jp})`}
                    </Typography>
                  </Box>
                )}
              </Box>
            )}

            {/* 選項按鈕 */}
            <Box sx={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 1.5 }}>
              {choices.map((choice, idx) => (
                <Button
                  key={choice.id}
                  variant={
                    showResult && (choice.id === correctPersonId || (selectedChoice && choice.id === selectedChoice.id))
                      ? 'contained'
                      : 'outlined'
                  }
                  onClick={() => handleChoiceClick(choice)}
                  disabled={showResult}
                  fullWidth
                  sx={getChoiceButtonSx(choice)}
                >
                  <Typography component="span" sx={{ mr: 1, fontWeight: 700, minWidth: '1.4em' }}>
                    {String.fromCharCode(65 + idx)}.
                  </Typography>
                  <Box sx={{ textAlign: 'left' }}>
                    <Typography component="span" sx={{ fontSize: 'inherit', fontWeight: 500 }}>
                      {choice.name}
                    </Typography>
                    {choice.name_jp && (
                      <Typography component="span" sx={{ ml: 0.5, fontSize: '0.8em', opacity: 0.85 }}>
                        ({choice.name_jp})
                      </Typography>
                    )}
                  </Box>
                </Button>
              ))}
            </Box>
          </CardContent>

          {showResult && (
            <CardActions sx={{ justifyContent: 'center', p: { xs: 2, sm: 2 }, pt: 0 }}>
              <Button
                variant="contained"
                onClick={startReview}
                disabled={loading}
                fullWidth
                size="large"
                sx={{ py: 1.5 }}
              >
                {loading ? <CircularProgress size={24} /> : '下一題'}
              </Button>
            </CardActions>
          )}
        </Card>
      )}
    </Box>
  );
}

export default Review;
