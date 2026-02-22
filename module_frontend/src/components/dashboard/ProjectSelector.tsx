// src/components/dashboard/ProjectSelector.tsx
import React from 'react';

interface ProjectSelectorProps {
  selected: string | null;
  onSelect: (projectId: string | null) => void;
}

const ProjectSelector: React.FC<ProjectSelectorProps> = ({ selected, onSelect }) => {
  // Mock projects - replace with actual data from API
  const projects = [
    { id: '1', name: 'All Projects' },
    { id: '2', name: 'Backend API' },
    { id: '3', name: 'Frontend Dashboard' },
  ];

  return (
    <select
      value={selected || '1'}
      onChange={(e) => onSelect(e.target.value === '1' ? null : e.target.value)}
      className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:border-gray-600"
    >
      {projects.map(project => (
        <option key={project.id} value={project.id}>
          {project.name}
        </option>
      ))}
    </select>
  );
};

export default ProjectSelector;