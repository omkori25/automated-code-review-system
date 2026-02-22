// src/pages/Projects.tsx
import React, { useState } from 'react';
import { FolderIcon, PlusIcon, MagnifyingGlassIcon } from '@heroicons/react/24/outline';

interface Project {
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
}

const Projects: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  
  // Mock data - replace with actual API data
  const projects: Project[] = [
    {
      id: '1',
      name: 'backend-api',
      description: 'Main backend API for the application',
      language: 'Python',
      files: 45,
      lastAnalyzed: '2024-02-20',
      issues: {
        critical: 2,
        high: 5,
        medium: 12,
        low: 8
      }
    },
    {
      id: '2',
      name: 'frontend-dashboard',
      description: 'React frontend dashboard',
      language: 'TypeScript',
      files: 67,
      lastAnalyzed: '2024-02-19',
      issues: {
        critical: 0,
        high: 3,
        medium: 15,
        low: 21
      }
    }
  ];

  const filteredProjects = projects.filter(project =>
    project.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    project.description.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getLanguageColor = (language: string) => {
    const colors: Record<string, string> = {
      'Python': 'bg-blue-100 text-blue-800',
      'TypeScript': 'bg-green-100 text-green-800',
      'JavaScript': 'bg-yellow-100 text-yellow-800',
      'Java': 'bg-red-100 text-red-800'
    };
    return colors[language] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Projects</h1>
        <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center">
          <PlusIcon className="w-5 h-5 mr-2" />
          New Project
        </button>
      </div>

      {/* Search Bar */}
      <div className="relative">
        <MagnifyingGlassIcon className="w-5 h-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
        <input
          type="text"
          placeholder="Search projects..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:border-gray-600"
        />
      </div>

      {/* Projects Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredProjects.map((project) => (
          <div key={project.id} className="bg-white dark:bg-gray-800 rounded-lg shadow hover:shadow-lg transition-shadow">
            <div className="p-6">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center">
                  <FolderIcon className="w-10 h-10 text-blue-500" />
                  <div className="ml-3">
                    <h3 className="font-semibold text-lg">{project.name}</h3>
                    <span className={`text-xs px-2 py-1 rounded ${getLanguageColor(project.language)}`}>
                      {project.language}
                    </span>
                  </div>
                </div>
              </div>
              
              <p className="text-gray-600 dark:text-gray-300 text-sm mb-4">
                {project.description}
              </p>
              
              <div className="flex justify-between text-sm text-gray-500 mb-4">
                <span>{project.files} files</span>
                <span>Last analyzed: {project.lastAnalyzed}</span>
              </div>
              
              {/* Issues Summary */}
              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-sm">Critical</span>
                  <span className="text-sm font-semibold text-red-600">{project.issues.critical}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm">High</span>
                  <span className="text-sm font-semibold text-orange-600">{project.issues.high}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm">Medium</span>
                  <span className="text-sm font-semibold text-yellow-600">{project.issues.medium}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm">Low</span>
                  <span className="text-sm font-semibold text-blue-600">{project.issues.low}</span>
                </div>
              </div>
              
              <button className="mt-4 w-full px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
                View Details
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Projects;