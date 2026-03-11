import React, { useState } from 'react';
import { 
  AppBar, Toolbar, Typography, Container, Box, Tabs, Tab,
  ThemeProvider, createTheme, CssBaseline 
} from '@mui/material';
import { FaceRetouchingNatural, Upload, Quiz, People } from '@mui/icons-material';
import UploadPhoto from './components/UploadPhoto';
import Review from './components/Review';
import PersonList from './components/PersonList';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function TabPanel({ children, value, index }) {
  return (
    <div hidden={value !== index}>
      {value === index && (
        <Box sx={{ p: { xs: 1, sm: 2, md: 3 } }}>
          {children}
        </Box>
      )}
    </div>
  );
}

function App() {
  const [tabValue, setTabValue] = useState(0);

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ flexGrow: 1, minHeight: '100vh', bgcolor: '#f5f5f5' }}>
        <AppBar position="sticky">
          <Toolbar>
            <FaceRetouchingNatural sx={{ mr: { xs: 1, sm: 2 } }} />
            <Typography 
              variant="h6" 
              component="div" 
              sx={{ 
                flexGrow: 1,
                fontSize: { xs: '0.9rem', sm: '1.25rem' },
                display: { xs: 'none', sm: 'block' }
              }}
            >
              Sensei Face Recognition - 日本老師人臉辨識系統
            </Typography>
            <Typography 
              variant="h6" 
              component="div" 
              sx={{ 
                flexGrow: 1,
                fontSize: '0.9rem',
                display: { xs: 'block', sm: 'none' }
              }}
            >
              人臉辨識系統
            </Typography>
          </Toolbar>
        </AppBar>

        <Container 
          maxWidth="lg" 
          sx={{ 
            mt: { xs: 2, sm: 3, md: 4 },
            px: { xs: 1, sm: 2, md: 3 },
            pb: { xs: 2, sm: 3, md: 4 }
          }}
        >
          <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
            <Tabs 
              value={tabValue} 
              onChange={handleTabChange} 
              variant="fullWidth"
              sx={{
                '& .MuiTab-root': {
                  minHeight: { xs: 60, sm: 72 },
                  fontSize: { xs: '0.75rem', sm: '0.875rem' }
                }
              }}
            >
              <Tab icon={<Upload />} label="上傳照片" iconPosition="top" />
              <Tab icon={<People />} label="人物列表" iconPosition="top" />
              <Tab icon={<Quiz />} label="開始複習" iconPosition="top" />
            </Tabs>
          </Box>

          <TabPanel value={tabValue} index={0}>
            <UploadPhoto />
          </TabPanel>

          <TabPanel value={tabValue} index={1}>
            <PersonList />
          </TabPanel>

          <TabPanel value={tabValue} index={2}>
            <Review />
          </TabPanel>
        </Container>
      </Box>
    </ThemeProvider>
  );
}

export default App;
