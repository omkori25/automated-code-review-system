// src/pages/Analysis.tsx - FIXED VERSION
import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import CodeEditor from '../components/analysis/CodeEditor';
import FileUploader from '../components/analysis/FileUploader';
import IssueList from '../components/analysis/IssueList';
import { api } from '../services/api';
import toast from 'react-hot-toast';
import { Issue, AnalysisResults, UploadedFile } from '../types';

const Analysis: React.FC = () => {
  const params = useParams<{ id?: string }>();
  const id = params.id;
  
  const [files, setFiles] = useState<UploadedFile[]>([]);
  const [selectedFile, setSelectedFile] = useState<UploadedFile | null>(null);
  const [analysisResults, setAnalysisResults] = useState<AnalysisResults | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const handleFilesUploaded = async (uploadedFiles: UploadedFile[]) => {
    setFiles(uploadedFiles);
    setSelectedFile(uploadedFiles[0]);
    toast.success(`${uploadedFiles.length} files uploaded`);
  };

  const handleStartAnalysis = async () => {
    if (files.length === 0) {
      toast.error('Please upload files first');
      return;
    }

    setIsAnalyzing(true);
    try {
      // Start analysis
      const response = await api.startAnalysis(id || 'default-project', files);
      const analysisId = response.analysis_id;

      // Poll for results
      const checkInterval = setInterval(async () => {
        try {
          const status = await api.getAnalysisStatus(analysisId);
          
          if (status.status === 'completed') {
            clearInterval(checkInterval);
            const results = await api.getAnalysisResults(analysisId);
            setAnalysisResults(results);
            setIsAnalyzing(false);
            toast.success('Analysis completed!');
          } else if (status.status === 'failed') {
            clearInterval(checkInterval);
            setIsAnalyzing(false);
            toast.error('Analysis failed');
          }
        } catch (error) {
          console.error('Error checking status:', error);
        }
      }, 2000);
    } catch (error) {
      console.error('Analysis failed:', error);
      toast.error('Failed to start analysis');
      setIsAnalyzing(false);
    }
  };

  const handleIssueClick = (issue: Issue) => {
    console.log('Issue clicked:', issue);
    // You can add logic to scroll to the issue in editor
    // For example, if using monaco editor, you can:
    // editor.revealLineInCenter(issue.line_start);
    // editor.setPosition({ lineNumber: issue.line_start, column: issue.column_start });
    toast.success(`Navigated to issue at line ${issue.line_start}`);
  };

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
          Code Analysis {id ? `- Project ${id}` : ''}
        </h1>
        <div className="space-x-4">
          <button
            onClick={handleStartAnalysis}
            disabled={isAnalyzing || files.length === 0}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {isAnalyzing ? (
              <>
                <span className="animate-spin inline-block mr-2">⚪</span>
                Analyzing...
              </>
            ) : (
              'Start Analysis'
            )}
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex gap-4 min-h-0">
        {/* Left Panel - File List */}
        <div className="w-64 bg-white dark:bg-gray-800 rounded-lg shadow p-4 overflow-y-auto">
          <h2 className="font-semibold mb-4 text-gray-900 dark:text-white">
            Files ({files.length})
          </h2>
          {files.length === 0 ? (
            <p className="text-gray-500 text-sm">No files uploaded</p>
          ) : (
            <ul className="space-y-2">
              {files.map((file, index) => (
                <li
                  key={index}
                  onClick={() => setSelectedFile(file)}
                  className={`p-2 rounded cursor-pointer transition-colors ${
                    selectedFile?.path === file.path
                      ? 'bg-blue-50 dark:bg-blue-900 text-blue-600 dark:text-blue-300'
                      : 'hover:bg-gray-100 dark:hover:bg-gray-700'
                  }`}
                >
                  <div className="text-sm font-medium truncate">{file.path}</div>
                  <div className="text-xs text-gray-500">
                    {file.language} • {(file.size / 1024).toFixed(1)} KB
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>

        {/* Center Panel - Code Editor */}
        <div className="flex-1 bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
          {selectedFile ? (
            <CodeEditor
              code={selectedFile.content}
              language={selectedFile.language}
              issues={analysisResults?.issues?.filter(
                (i: Issue) => i.file_path === selectedFile.path
              )}
            />
          ) : (
            <div className="h-full flex items-center justify-center text-gray-500">
              {files.length === 0 ? 'Upload files to begin' : 'Select a file to view'}
            </div>
          )}
        </div>

        {/* Right Panel - Issues */}
        <div className="w-80 bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
          <IssueList
            issues={analysisResults?.issues || []}
            summary={analysisResults?.summary}
            onIssueClick={handleIssueClick}
          />
        </div>
      </div>

      {/* File Upload Area (shown when no files) */}
      {files.length === 0 && (
        <div className="mt-4">
          <FileUploader onFilesUploaded={handleFilesUploaded} />
        </div>
      )}
    </div>
  );
};

export default Analysis;