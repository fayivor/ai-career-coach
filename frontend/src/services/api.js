import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Chatbot API
export const sendChatMessage = async (message) => {
  const response = await api.post('/api/chatbot/chat', { message });
  return response.data;
};

// Resume API
export const analyzeResume = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await api.post('/api/resume/analyze', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

// Skills API
export const analyzeSkillGap = async (currentSkills, targetRole) => {
  const response = await api.post('/api/skills/gap-analysis', {
    current_skills: currentSkills,
    target_role: targetRole,
  });
  return response.data;
};

export const getAvailableRoles = async () => {
  const response = await api.get('/api/skills/roles');
  return response.data;
};

export const getRoleRequirements = async (role) => {
  const response = await api.get(`/api/skills/role/${role}`);
  return response.data;
};

// Recommendations API
export const getCourseRecommendations = async (missingSkills, limit = 5) => {
  const response = await api.post(`/api/recommendations/courses?limit=${limit}`, missingSkills);
  return response.data;
};

export const getAllCourses = async () => {
  const response = await api.get('/api/recommendations/courses/all');
  return response.data;
};

// Tracker API
export const createGoal = async (goalData) => {
  const response = await api.post('/api/tracker/goals', goalData);
  return response.data;
};

export const getGoals = async () => {
  const response = await api.get('/api/tracker/goals');
  return response.data;
};

export const updateGoal = async (goalId, goalData) => {
  const response = await api.put(`/api/tracker/goals/${goalId}`, goalData);
  return response.data;
};

export const deleteGoal = async (goalId) => {
  const response = await api.delete(`/api/tracker/goals/${goalId}`);
  return response.data;
};

export const getTrackerStats = async () => {
  const response = await api.get('/api/tracker/stats');
  return response.data;
};

export default api;
