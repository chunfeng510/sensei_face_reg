import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:9453/api';

// 建立axios實例
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API 服務
export const apiService = {
  // 照片相關
  uploadPhoto: async (file) => {
    const formData = new FormData();
    formData.append('photo', file);
    const response = await api.post('/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },

  detectFaces: async (photoId) => {
    const response = await api.post('/detect-faces', { photo_id: photoId });
    return response.data;
  },

  getPhotos: async () => {
    const response = await api.get('/photos');
    return response.data;
  },

  deletePhoto: async (photoId) => {
    const response = await api.delete(`/photos/${photoId}`);
    return response.data;
  },

  // 人臉與人物相關
  saveFace: async (faceData) => {
    const response = await api.post('/save-face', faceData);
    return response.data;
  },

  getPersons: async () => {
    const response = await api.get('/persons');
    return response.data;
  },

  getPerson: async (personId) => {
    const response = await api.get(`/persons/${personId}`);
    return response.data;
  },

  updatePerson: async (personId, data) => {
    const response = await api.put(`/persons/${personId}`, data);
    return response.data;
  },

  deletePerson: async (personId) => {
    const response = await api.delete(`/persons/${personId}`);
    return response.data;
  },

  // 複習相關
  getRandomFace: async (personId = null) => {
    const params = personId ? { person_id: personId } : {};
    const response = await api.get('/review/random', { params });
    return response.data;
  },

  submitReview: async (reviewData) => {
    const response = await api.post('/review/submit', reviewData);
    return response.data;
  },

  getStatistics: async () => {
    const response = await api.get('/review/statistics');
    return response.data;
  },

  getPersonStatistics: async (personId) => {
    const response = await api.get(`/review/statistics/${personId}`);
    return response.data;
  },
};

export default api;
