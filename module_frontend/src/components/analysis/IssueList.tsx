// IssueList.tsx
import React from 'react';

interface Issue {
  file_path: string;
  rule_id: string;
  message: string;
  severity: string;
  line_start: number;
}

interface IssueListProps {
  issues: Issue[];
  summary?: {
    critical: number;
    high: number;
    medium: number;
    low: number;
  };
  onIssueClick: (issue: Issue) => void;
}

const IssueList: React.FC<IssueListProps> = ({ issues, summary, onIssueClick }) => {
  const getSeverityColor = (severity: string) => {
    switch(severity) {
      case 'critical': return 'bg-red-100 text-red-800 border-red-200';
      case 'high': return 'bg-orange-100 text-orange-800 border-orange-200';
      case 'medium': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'low': return 'bg-blue-100 text-blue-800 border-blue-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  return (
    <div className="h-full flex flex-col">
      {/* Summary Section */}
      {summary && (
        <div className="p-4 border-b border-gray-200">
          <h3 className="font-semibold mb-2">Summary</h3>
          <div className="grid grid-cols-2 gap-2">
            <div className="bg-red-50 p-2 rounded text-center">
              <div className="text-sm text-gray-600">Critical</div>
              <div className="text-xl font-bold text-red-600">{summary.critical}</div>
            </div>
            <div className="bg-orange-50 p-2 rounded text-center">
              <div className="text-sm text-gray-600">High</div>
              <div className="text-xl font-bold text-orange-600">{summary.high}</div>
            </div>
            <div className="bg-yellow-50 p-2 rounded text-center">
              <div className="text-sm text-gray-600">Medium</div>
              <div className="text-xl font-bold text-yellow-600">{summary.medium}</div>
            </div>
            <div className="bg-blue-50 p-2 rounded text-center">
              <div className="text-sm text-gray-600">Low</div>
              <div className="text-xl font-bold text-blue-600">{summary.low}</div>
            </div>
          </div>
        </div>
      )}

      {/* Issues List */}
      <div className="flex-1 overflow-y-auto p-4">
        <h3 className="font-semibold mb-3">Issues ({issues.length})</h3>
        {issues.length === 0 ? (
          <p className="text-gray-500 text-center py-8">No issues found</p>
        ) : (
          <div className="space-y-3">
            {issues.map((issue, index) => (
              <div
                key={index}
                onClick={() => onIssueClick(issue)}
                className={`p-3 rounded-lg border cursor-pointer hover:shadow-md transition-shadow ${getSeverityColor(issue.severity)}`}
              >
                <div className="flex justify-between items-start mb-1">
                  <span className="text-xs font-medium uppercase px-2 py-1 rounded bg-white bg-opacity-50">
                    {issue.rule_id}
                  </span>
                  <span className="text-xs">
                    Line {issue.line_start}
                  </span>
                </div>
                <p className="text-sm">{issue.message}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default IssueList;