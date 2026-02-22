// src/components/analysis/IssueList.tsx
import React from 'react';
import { Issue, AnalysisSummary } from '../../types';

interface IssueListProps {
  issues: Issue[];
  summary?: AnalysisSummary;
  onIssueClick: (issue: Issue) => void;
}

const IssueList: React.FC<IssueListProps> = ({ issues, summary, onIssueClick }) => {
  const getSeverityColor = (severity: string) => {
    switch(severity) {
      case 'critical': return 'bg-red-100 text-red-800 border-red-200 dark:bg-red-900 dark:text-red-300';
      case 'high': return 'bg-orange-100 text-orange-800 border-orange-200 dark:bg-orange-900 dark:text-orange-300';
      case 'medium': return 'bg-yellow-100 text-yellow-800 border-yellow-200 dark:bg-yellow-900 dark:text-yellow-300';
      case 'low': return 'bg-blue-100 text-blue-800 border-blue-200 dark:bg-blue-900 dark:text-blue-300';
      default: return 'bg-gray-100 text-gray-800 border-gray-200 dark:bg-gray-700 dark:text-gray-300';
    }
  };

  return (
    <div className="h-full flex flex-col bg-white dark:bg-gray-800">
      {/* Summary Section */}
      {summary && (
        <div className="p-4 border-b border-gray-200 dark:border-gray-700">
          <h3 className="font-semibold mb-3 text-gray-900 dark:text-white">Summary</h3>
          <div className="grid grid-cols-2 gap-3">
            <div className="bg-red-50 dark:bg-red-900/20 p-3 rounded-lg text-center">
              <div className="text-xs text-gray-600 dark:text-gray-400">Critical</div>
              <div className="text-xl font-bold text-red-600 dark:text-red-400">{summary.critical}</div>
            </div>
            <div className="bg-orange-50 dark:bg-orange-900/20 p-3 rounded-lg text-center">
              <div className="text-xs text-gray-600 dark:text-gray-400">High</div>
              <div className="text-xl font-bold text-orange-600 dark:text-orange-400">{summary.high}</div>
            </div>
            <div className="bg-yellow-50 dark:bg-yellow-900/20 p-3 rounded-lg text-center">
              <div className="text-xs text-gray-600 dark:text-gray-400">Medium</div>
              <div className="text-xl font-bold text-yellow-600 dark:text-yellow-400">{summary.medium}</div>
            </div>
            <div className="bg-blue-50 dark:bg-blue-900/20 p-3 rounded-lg text-center">
              <div className="text-xs text-gray-600 dark:text-gray-400">Low</div>
              <div className="text-xl font-bold text-blue-600 dark:text-blue-400">{summary.low}</div>
            </div>
          </div>
        </div>
      )}

      {/* Issues List */}
      <div className="flex-1 overflow-y-auto p-4">
        <div className="flex justify-between items-center mb-3">
          <h3 className="font-semibold text-gray-900 dark:text-white">
            Issues ({issues.length})
          </h3>
          <span className="text-xs text-gray-500">
            Click to view in editor
          </span>
        </div>
        
        {issues.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-gray-400 dark:text-gray-600 text-6xl mb-4">✓</div>
            <p className="text-gray-500 dark:text-gray-400">No issues found</p>
          </div>
        ) : (
          <div className="space-y-3">
            {issues.map((issue, index) => (
              <div
                key={`${issue.file_path}-${issue.line_start}-${index}`}
                onClick={() => onIssueClick(issue)}
                className={`p-4 rounded-lg border cursor-pointer hover:shadow-md transition-all duration-200 ${getSeverityColor(issue.severity)}`}
              >
                <div className="flex justify-between items-start mb-2">
                  <span className="text-xs font-medium uppercase px-2 py-1 rounded bg-white dark:bg-gray-800 bg-opacity-50">
                    {issue.rule_id}
                  </span>
                  <span className="text-xs bg-white dark:bg-gray-800 px-2 py-1 rounded">
                    Line {issue.line_start}
                  </span>
                </div>
                <p className="text-sm mb-2">{issue.message}</p>
                {issue.suggestion && (
                  <div className="mt-2 text-xs bg-white dark:bg-gray-800 bg-opacity-50 p-2 rounded">
                    <span className="font-medium">Suggestion:</span> {issue.suggestion}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default IssueList;