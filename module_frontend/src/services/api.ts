// module_frontend/src/services/api.ts
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for auth
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Redirect to login
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const api = {
  // Health check
  async healthCheck() {
    const response = await apiClient.get('/health');
    return response.data;
  },

  // File upload
  async uploadFiles(files: File[]) {
    const formData = new FormData();
    files.forEach((file) => {
      formData.append('files', file);
    });

    const response = await apiClient.post('/analysis/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Analysis
  async startAnalysis(projectId: string, files: any[]) {
    const response = await apiClient.post(`/analysis/start/${projectId}`, {
      files,
    });
    return response.data;
  },

  async getAnalysisStatus(analysisId: string) {
    const response = await apiClient.get(`/analysis/status/${analysisId}`);
    return response.data;
  },

  async getAnalysisResults(analysisId: string) {
    const response = await apiClient.get(`/analysis/results/${analysisId}`);
    return response.data;
  },

  // Dashboard
  async getDashboardStats(projectId: string | null) {
    const params = projectId ? { projectId } : {};
    const response = await apiClient.get('/dashboard/stats', { params });
    return response.data;
  },

  async getRecentAnalyses() {
    const response = await apiClient.get('/analyses/recent');
    return response.data;
  },

  // Projects
  async getProjects() {
    const response = await apiClient.get('/projects');
    return response.data;
  },

  async createProject(projectData: any) {
    const response = await apiClient.post('/projects', projectData);
    return response.data;
  },

  // Issues
  async markFalsePositive(issueId: string) {
    const response = await apiClient.post(`/issues/${issueId}/false-positive`);
    return response.data;
  },

  async getIssueDetails(issueId: string) {
    const response = await apiClient.get(`/issues/${issueId}`);
    return response.data;
  },
};