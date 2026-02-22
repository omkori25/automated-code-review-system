// src/services/api.ts
import axios, { AxiosInstance, AxiosResponse, AxiosError } from 'axios';
import { 
  UploadedFile, 
  AnalysisResults, 
  DashboardStats,
  Issue,
  AnalysisSummary
} from '../types';

// API response types
interface StartAnalysisResponse {
  analysis_id: string;
  status: string;
}

interface AnalysisStatusResponse {
  status: string;
  progress?: number;
  error?: string;
}

interface UploadFilesResponse {
  files: UploadedFile[];
}

interface HealthCheckResponse {
  status: string;
  timestamp: string;
  service: string;
  version: string;
}

// Create axios instance with default config
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds
});

// Request interceptor for logging and auth
apiClient.interceptors.request.use(
  (config) => {
    // Log request in development
    if (import.meta.env.DEV) {
      console.log(`📡 ${config.method?.toUpperCase()} request to ${config.url}`);
    }
    
    // Add auth token if available
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    return config;
  },
  (error) => {
    console.error('❌ Request error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    // Log response in development
    if (import.meta.env.DEV) {
      console.log(`✅ Response from ${response.config.url}:`, response.status);
    }
    return response;
  },
  (error: AxiosError) => {
    // Handle different error types
    if (error.response) {
      // The request was made and the server responded with a status code
      console.error('❌ Server error:', {
        status: error.response.status,
        data: error.response.data,
        headers: error.response.headers
      });
      
      // Handle specific status codes
      switch (error.response.status) {
        case 401:
          // Unauthorized - redirect to login
          localStorage.removeItem('auth_token');
          window.location.href = '/login';
          break;
        case 403:
          console.error('Forbidden: You don\'t have permission to access this resource');
          break;
        case 404:
          console.error('Resource not found');
          break;
        case 500:
          console.error('Internal server error');
          break;
      }
    } else if (error.request) {
      // The request was made but no response was received
      console.error('❌ No response received:', error.request);
    } else {
      // Something happened in setting up the request
      console.error('❌ Request setup error:', error.message);
    }
    
    return Promise.reject(error);
  }
);

// API service object with all methods
export const api = {
  /**
   * Start a new code analysis
   * @param projectId - ID of the project to analyze
   * @param files - Array of files to analyze
   * @returns Analysis ID and status
   */
  async startAnalysis(projectId: string, files: UploadedFile[]): Promise<StartAnalysisResponse> {
    try {
      const response = await apiClient.post<StartAnalysisResponse>(`/analysis/start/${projectId}`, {
        files,
      });
      return response.data;
    } catch (error) {
      console.error('Failed to start analysis:', error);
      throw error;
    }
  },

  /**
   * Get analysis status
   * @param analysisId - ID of the analysis
   * @returns Current status of the analysis
   */
  async getAnalysisStatus(analysisId: string): Promise<AnalysisStatusResponse> {
    try {
      const response = await apiClient.get<AnalysisStatusResponse>(`/analysis/status/${analysisId}`);
      return response.data;
    } catch (error) {
      console.error('Failed to get analysis status:', error);
      throw error;
    }
  },

  /**
   * Get analysis results
   * @param analysisId - ID of the analysis
   * @returns Complete analysis results with issues
   */
  async getAnalysisResults(analysisId: string): Promise<AnalysisResults> {
    try {
      const response = await apiClient.get<AnalysisResults>(`/analysis/results/${analysisId}`);
      return response.data;
    } catch (error) {
      console.error('Failed to get analysis results:', error);
      throw error;
    }
  },

  /**
   * Get dashboard statistics
   * @param projectId - Optional project ID to filter stats
   * @returns Dashboard metrics and charts data
   */
  async getDashboardStats(projectId: string | null): Promise<DashboardStats> {
    try {
      const params = projectId ? { projectId } : {};
      const response = await apiClient.get<DashboardStats>('/dashboard/stats', { params });
      return response.data;
    } catch (error) {
      console.error('Failed to get dashboard stats:', error);
      // Return default empty stats
      return {
        totalIssues: 0,
        criticalIssues: 0,
        filesAnalyzed: 0,
        avgTime: '0s',
        issueChange: 0,
        criticalChange: 0,
        filesChange: 0,
        timeChange: 0
      };
    }
  },

  /**
   * Get recent analyses
   * @returns List of recent analyses
   */
  async getRecentAnalyses(): Promise<any[]> {
    try {
      const response = await apiClient.get<any[]>('/analyses/recent');
      return response.data;
    } catch (error) {
      console.error('Failed to get recent analyses:', error);
      return [];
    }
  },

  /**
   * Health check
   * @returns Health status of the API
   */
  async healthCheck(): Promise<HealthCheckResponse> {
    try {
      const response = await apiClient.get<HealthCheckResponse>('/health');
      return response.data;
    } catch (error) {
      console.error('Health check failed:', error);
      throw error;
    }
  },

  /**
   * Upload files for analysis
   * @param files - Array of File objects to upload
   * @returns Processed file information
   */
  async uploadFiles(files: File[]): Promise<UploadFilesResponse> {
    try {
      const formData = new FormData();
      files.forEach((file) => {
        formData.append('files', file);
      });

      const response = await apiClient.post<UploadFilesResponse>('/analysis/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      console.error('Failed to upload files:', error);
      throw error;
    }
  },

  /**
   * Mark an issue as false positive
   * @param issueId - ID of the issue
   * @returns Updated issue
   */
  async markFalsePositive(issueId: string): Promise<Issue> {
    try {
      const response = await apiClient.post<Issue>(`/issues/${issueId}/false-positive`);
      return response.data;
    } catch (error) {
      console.error('Failed to mark issue as false positive:', error);
      throw error;
    }
  },

  /**
   * Get detailed issue information
   * @param issueId - ID of the issue
   * @returns Detailed issue data
   */
  async getIssueDetails(issueId: string): Promise<Issue> {
    try {
      const response = await apiClient.get<Issue>(`/issues/${issueId}`);
      return response.data;
    } catch (error) {
      console.error('Failed to get issue details:', error);
      throw error;
    }
  },

  /**
   * Get all projects
   * @returns List of projects
   */
  async getProjects(): Promise<any[]> {
    try {
      const response = await apiClient.get<any[]>('/projects');
      return response.data;
    } catch (error) {
      console.error('Failed to get projects:', error);
      return [];
    }
  },

  /**
   * Create a new project
   * @param projectData - Project data
   * @returns Created project
   */
  async createProject(projectData: any): Promise<any> {
    try {
      const response = await apiClient.post('/projects', projectData);
      return response.data;
    } catch (error) {
      console.error('Failed to create project:', error);
      throw error;
    }
  },

  /**
   * Login user
   * @param email - User email
   * @param password - User password
   * @returns Auth token and user data
   */
  async login(email: string, password: string): Promise<{ token: string; user: any }> {
    try {
      const response = await apiClient.post('/auth/login', { email, password });
      const { token, user } = response.data;
      
      // Store token
      localStorage.setItem('auth_token', token);
      
      // Update default header
      apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      
      return { token, user };
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    }
  },

  /**
   * Logout user
   */
  logout(): void {
    localStorage.removeItem('auth_token');
    delete apiClient.defaults.headers.common['Authorization'];
    window.location.href = '/login';
  },

  /**
   * Check if user is authenticated
   * @returns True if authenticated
   */
  isAuthenticated(): boolean {
    return !!localStorage.getItem('auth_token');
  },

  /**
   * Get current auth token
   * @returns Auth token or null
   */
  getToken(): string | null {
    return localStorage.getItem('auth_token');
  }
};

// Export individual methods for direct use
export const {
  startAnalysis,
  getAnalysisStatus,
  getAnalysisResults,
  getDashboardStats,
  getRecentAnalyses,
  healthCheck,
  uploadFiles,
  markFalsePositive,
  getIssueDetails,
  getProjects,
  createProject,
  login,
  logout,
  isAuthenticated,
  getToken
} = api;

// Default export for convenience
export default api;