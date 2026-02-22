// src/types/index.ts
export interface Issue {
  file_path: string;
  rule_id: string;
  message: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  line_start: number;
  line_end: number;
  column_start: number;
  column_end: number;
  suggestion: string;
  code_snippet?: string;
  is_false_positive?: boolean;
  is_fixed?: boolean;
  metadata?: Record<string, any>;
}

export interface AnalysisSummary {
  critical: number;
  high: number;
  medium: number;
  low: number;
}

export interface AnalysisResults {
  analysis_id: string;
  total_issues: number;
  issues: Issue[];
  summary: AnalysisSummary;
  project_id?: string;
  created_at?: string;
  completed_at?: string;
}

export interface UploadedFile {
  path: string;
  content: string;
  language: string;
  size: number;
  encoding?: string;
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
  trendData?: Array<{ date: string; count: number }>;
  distribution?: Array<{ type: string; count: number }>;
}

export interface Project {
  id: string;
  name: string;
  description: string;
  language: string;
  files: number;
  lastAnalyzed: string;
  issues: {
    critical: number;
    high: number;
    medium: number;
    low: number;
  };
  owner_id?: string;
  created_at?: string;
  updated_at?: string;
}

export interface User {
  id: string;
  username: string;
  email: string;
  full_name?: string;
  role: 'admin' | 'manager' | 'developer';
  is_active: boolean;
  created_at?: string;
  updated_at?: string;
}

export interface LoginResponse {
  token: string;
  user: User;
}

export interface HealthCheckResponse {
  status: 'healthy' | 'unhealthy';
  timestamp: string;
  service: string;
  version: string;
  database?: 'connected' | 'disconnected';
  ml_service?: 'available' | 'unavailable';
}