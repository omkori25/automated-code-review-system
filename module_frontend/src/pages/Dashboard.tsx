// src/pages/Dashboard.tsx - FIXED VERSION
import React, { useState } from 'react';  // ✅ Removed unused useEffect
import { useQuery } from '@tanstack/react-query';
import { api } from '../services/api';
import MetricsCard from '../components/dashboard/MetricsCard';
import Charts from '../components/dashboard/Charts';
import ProjectSelector from '../components/dashboard/ProjectSelector';
import { 
  CodeBracketIcon, 
  BugAntIcon, 
  ShieldExclamationIcon,
  ClockIcon 
} from '@heroicons/react/24/outline';

// Define types
interface DashboardStats {
  totalIssues: number;
  criticalIssues: number;
  filesAnalyzed: number;
  avgTime: string;
  issueChange: number;
  criticalChange: number;
  filesChange: number;
  timeChange: number;
  trendData?: any[];
  distribution?: any[];
}

const Dashboard: React.FC = () => {
  const [selectedProject, setSelectedProject] = useState<string | null>(null);

  // Fetch dashboard stats
  const { data: stats, isLoading } = useQuery<DashboardStats>({
    queryKey: ['dashboard-stats', selectedProject],
    queryFn: () => api.getDashboardStats(selectedProject),
    refetchInterval: 30000, // Refresh every 30 seconds
    initialData: {
      totalIssues: 0,
      criticalIssues: 0,
      filesAnalyzed: 0,
      avgTime: '0s',
      issueChange: 0,
      criticalChange: 0,
      filesChange: 0,
      timeChange: 0
    }
  });

  // Fetch recent analyses
  const { data: recentAnalyses } = useQuery({
    queryKey: ['recent-analyses'],
    queryFn: () => api.getRecentAnalyses(),
    initialData: []
  });

  const metrics = [
    {
      title: 'Total Issues',
      value: stats?.totalIssues || 0,
      icon: BugAntIcon,
      color: 'text-red-600',
      bgColor: 'bg-red-100',
      change: stats?.issueChange || 0
    },
    {
      title: 'Critical Bugs',
      value: stats?.criticalIssues || 0,
      icon: ShieldExclamationIcon,
      color: 'text-orange-600',
      bgColor: 'bg-orange-100',
      change: stats?.criticalChange || 0
    },
    {
      title: 'Files Analyzed',
      value: stats?.filesAnalyzed || 0,
      icon: CodeBracketIcon,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100',
      change: stats?.filesChange || 0
    },
    {
      title: 'Avg Analysis Time',
      value: stats?.avgTime || '0s',
      icon: ClockIcon,
      color: 'text-green-600',
      bgColor: 'bg-green-100',
      change: stats?.timeChange || 0
    }
  ];

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
          Dashboard
        </h1>
        <ProjectSelector 
          selected={selectedProject}
          onSelect={setSelectedProject}
        />
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {metrics.map((metric, index) => (
          <MetricsCard key={index} {...metric} />
        ))}
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
          <h2 className="text-lg font-semibold mb-4">Issues Over Time</h2>
          <Charts.IssueTrend data={stats?.trendData} />
        </div>
        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
          <h2 className="text-lg font-semibold mb-4">Issues by Type</h2>
          <Charts.IssueDistribution data={stats?.distribution} />
        </div>
      </div>

      {/* Recent Analyses */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow">
        <div className="p-6 border-b border-gray-200 dark:border-gray-700">
          <h2 className="text-lg font-semibold">Recent Analyses</h2>
        </div>
        <div className="divide-y divide-gray-200 dark:divide-gray-700">
          {recentAnalyses.length === 0 ? (
            <div className="p-6 text-center text-gray-500">
              No recent analyses found
            </div>
          ) : (
            recentAnalyses.map((analysis: any) => (
              <div key={analysis.id} className="p-6 flex items-center justify-between">
                <div>
                  <p className="font-medium">{analysis.projectName}</p>
                  <p className="text-sm text-gray-500">
                    {new Date(analysis.createdAt).toLocaleString()}
                  </p>
                </div>
                <div className="flex items-center space-x-4">
                  <div className="flex space-x-2">
                    <span className="px-2 py-1 text-xs font-medium rounded bg-red-100 text-red-800">
                      {analysis.critical} critical
                    </span>
                    <span className="px-2 py-1 text-xs font-medium rounded bg-yellow-100 text-yellow-800">
                      {analysis.high} high
                    </span>
                  </div>
                  <button className="text-blue-600 hover:text-blue-800">
                    View Results
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;