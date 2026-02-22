// api.ts - FIXED VERSION
import axios, { AxiosInstance, AxiosResponse, AxiosError } from 'axios';

// Define types
export interface UploadedFile {
  path: string;
  content: string;
  language: string;
  size: number;
}

export interface AnalysisResponse {
  analysis_id: string;
  status: string;
}

export interface AnalysisStatus {
  status: string;
  progress?: number;
  error?: string;
}

export interface Issue {
  file_path: string;
  rule_id: string;
  message: string;
  severity: string;
  line_start: number;
  line_end: number;
  column_start: number;
  column_end: number;
  suggestion: string;
}

export interface AnalysisResults {
  analysis_id: string;
  total_issues: number;
  issues: Issue[];
  summary: {
    critical: number;
    high: number;
    medium: number;
    low: number;
  };
}

export interface DashboardStats {
  totalIssues: number;
  criticalIssues: number;
  filesAnalyzed: number;
  avgTime: string;
  issueChange: number;
  criticalChange: number;
  filesChange: number;
  timeChange: number;
  trendData: any[];
  distribution: any[];
}

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';  // ✅ Using import.meta.env instead of process.env

// Create axios instance
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds
});

// Request interceptor for logging
apiClient.interceptors.request.use(
  (config) => {
    console.log(`📡 ${config.method?.toUpperCase()} request to ${config.url}`);
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
    console.log(`✅ Response from ${response.config.url}:`, response.status);
    return response;
  },
  (error: AxiosError) => {
    if (error.response) {
      // The request was made and the server responded with a status code
      console.error('❌ Server error:', error.response.status, error.response.data);
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

export const api = {
  async startAnalysis(projectId: string, files: UploadedFile[]): Promise<AnalysisResponse> {
    const response = await apiClient.post<AnalysisResponse>(`/analysis/start/${projectId}`, {
      files,
    });
    return response.data;
  },

  async getAnalysisStatus(analysisId: string): Promise<AnalysisStatus> {
    const response = await apiClient.get<AnalysisStatus>(`/analysis/status/${analysisId}`);
    return response.data;
  },

  async getAnalysisResults(analysisId: string): Promise<AnalysisResults> {
    const response = await apiClient.get<AnalysisResults>(`/analysis/results/${analysisId}`);
    return response.data;
  },

  async getDashboardStats(projectId: string | null): Promise<DashboardStats> {
    const params = projectId ? { projectId } : {};
    const response = await apiClient.get<DashboardStats>('/dashboard/stats', { params });
    return response.data;
  },

  async getRecentAnalyses(): Promise<any[]> {
    const response = await apiClient.get<any[]>('/analyses/recent');
    return response.data;
  },

  async healthCheck(): Promise<any> {
    const response = await apiClient.get('/health');
    return response.data;
  },

  async uploadFiles(files: File[]): Promise<{ files: UploadedFile[] }> {
    const formData = new FormData();
    files.forEach((file) => {
      formData.append('files', file);
    });

    const response = await apiClient.post<{ files: UploadedFile[] }>('/analysis/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }
};

export default api;