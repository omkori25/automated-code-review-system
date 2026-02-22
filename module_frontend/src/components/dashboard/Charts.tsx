// src/components/dashboard/Charts.tsx
import React from 'react';

interface ChartsProps {
  IssueTrend?: React.FC<{ data?: any[] }>;
  IssueDistribution?: React.FC<{ data?: any[] }>;
}

// Issue Trend Chart Component
const IssueTrend: React.FC<{ data?: any[] }> = ({ data }) => {
  return (
    <div className="h-64 flex items-center justify-center bg-gray-50 dark:bg-gray-700 rounded">
      <p className="text-gray-500">Issue Trend Chart (Placeholder)</p>
      {data && <pre className="hidden">{JSON.stringify(data)}</pre>}
    </div>
  );
};

// Issue Distribution Chart Component
const IssueDistribution: React.FC<{ data?: any[] }> = ({ data }) => {
  return (
    <div className="h-64 flex items-center justify-center bg-gray-50 dark:bg-gray-700 rounded">
      <p className="text-gray-500">Issue Distribution Chart (Placeholder)</p>
      {data && <pre className="hidden">{JSON.stringify(data)}</pre>}
    </div>
  );
};

// Export as an object with both components
const Charts = {
  IssueTrend,
  IssueDistribution
};

export default Charts;