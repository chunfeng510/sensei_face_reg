import React, { useState, useEffect } from 'react';
import {
  Box, Typography, List, ListItem, ListItemText, ListItemButton,
  CircularProgress, Alert, Chip, IconButton, Dialog, DialogTitle,
  DialogContent, DialogActions, Button
} from '@mui/material';
import { Delete, Person } from '@mui/icons-material';
import { apiService } from '../services/api';

function PersonList() {
  const [persons, setPersons] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedPerson, setSelectedPerson] = useState(null);
  const [detailDialog, setDetailDialog] = useState(false);

  useEffect(() => {
    loadPersons();
  }, []);

  const loadPersons = async () => {
    try {
      setLoading(true);
      const result = await apiService.getPersons();
      if (result.success) {
        setPersons(result.persons);
      } else {
        setError(result.error);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handlePersonClick = async (person) => {
    try {
      const result = await apiService.getPerson(person.id);
      if (result.success) {
        setSelectedPerson(result);
        setDetailDialog(true);
      }
    } catch (err) {
      alert(`載入失敗：${err.message}`);
    }
  };

  const handleDelete = async (personId, event) => {
    event.stopPropagation();
    
    if (!window.confirm('確定要刪除此人物及其所有人臉資料嗎？')) {
      return;
    }

    try {
      await apiService.deletePerson(personId);
      loadPersons();
    } catch (err) {
      alert(`刪除失敗：${err.message}`);
    }
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return <Alert severity="error">{error}</Alert>;
  }

  return (
    <Box>
      <Typography 
        variant="h5" 
        gutterBottom
        sx={{ fontSize: { xs: '1.25rem', sm: '1.5rem' } }}
      >
        人物列表
      </Typography>

      {persons.length === 0 ? (
        <Alert severity="info" sx={{ fontSize: { xs: '0.875rem', sm: '1rem' } }}>
          尚未建立任何人物資料
        </Alert>
      ) : (
        <List sx={{ bgcolor: 'white', borderRadius: 1 }}>
          {persons.map((person) => (
            <ListItem
              key={person.id}
              secondaryAction={
                <IconButton
                  edge="end"
                  onClick={(e) => handleDelete(person.id, e)}
                  sx={{ 
                    mr: { xs: -1, sm: 0 },
                    color: 'error.main'
                  }}
                >
                  <Delete />
                </IconButton>
              }
              sx={{
                borderBottom: '1px solid #f0f0f0',
                '&:last-child': { borderBottom: 'none' }
              }}
            >
              <ListItemButton 
                onClick={() => handlePersonClick(person)}
                sx={{ 
                  py: { xs: 1.5, sm: 1 },
                  pr: { xs: 6, sm: 7 }
                }}
              >
                <Person sx={{ mr: { xs: 1.5, sm: 2 }, color: 'primary.main' }} />
                <ListItemText
                  primary={person.name}
                  secondary={
                    <>
                      {person.name_jp && `${person.name_jp} • `}
                      {person.face_count} 張人臉
                    </>
                  }
                  primaryTypographyProps={{
                    fontSize: { xs: '1rem', sm: '1rem' },
                    fontWeight: 500
                  }}
                  secondaryTypographyProps={{
                    fontSize: { xs: '0.875rem', sm: '0.875rem' }
                  }}
                />
              </ListItemButton>
            </ListItem>
          ))}
        </List>
      )}

      {/* 人物詳情對話框 */}
      <Dialog
        open={detailDialog}
        onClose={() => setDetailDialog(false)}
        maxWidth="md"
        fullWidth
        PaperProps={{
          sx: {
            m: { xs: 2, sm: 3 },
            maxHeight: { xs: '90vh', sm: 'auto' }
          }
        }}
      >
        {selectedPerson && (
          <>
            <DialogTitle sx={{ fontSize: { xs: '1.1rem', sm: '1.25rem' } }}>
              {selectedPerson.person.name}
              {selectedPerson.person.name_jp && ` (${selectedPerson.person.name_jp})`}
            </DialogTitle>
            <DialogContent sx={{ pt: { xs: 2, sm: 3 } }}>
              <Typography 
                variant="body2" 
                color="text.secondary" 
                gutterBottom
                sx={{ fontSize: { xs: '0.875rem', sm: '0.875rem' } }}
              >
                人臉數量：{selectedPerson.faces.length} 張
              </Typography>
              {selectedPerson.person.notes && (
                <Typography 
                  variant="body2" 
                  sx={{ 
                    mt: 2,
                    fontSize: { xs: '0.875rem', sm: '0.875rem' }
                  }}
                >
                  備註：{selectedPerson.person.notes}
                </Typography>
              )}
            </DialogContent>
            <DialogActions sx={{ p: { xs: 2, sm: 3 } }}>
              <Button 
                onClick={() => setDetailDialog(false)}
                variant="contained"
                fullWidth={window.innerWidth < 600}
              >
                關閉
              </Button>
            </DialogActions>
          </>
        )}
      </Dialog>
    </Box>
  );
}

export default PersonList;
