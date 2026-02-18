// module_frontend/src/components/Layout/Sidebar.tsx
import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  HomeIcon, 
  CodeBracketIcon, 
  FolderIcon, 
  Cog6ToothIcon,
  ChevronDoubleLeftIcon,
  ChevronDoubleRightIcon,
  ChartBarIcon
} from '@heroicons/react/24/outline';

interface SidebarProps {
  collapsed: boolean;
  onToggle: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ collapsed, onToggle }) => {
  const menuItems = [
    { path: '/dashboard', icon: HomeIcon, label: 'Dashboard' },
    { path: '/analysis', icon: CodeBracketIcon, label: 'Analysis' },
    { path: '/projects', icon: FolderIcon, label: 'Projects' },
    { path: '/reports', icon: ChartBarIcon, label: 'Reports' },
    { path: '/settings', icon: Cog6ToothIcon, label: 'Settings' },
  ];

  return (
    <div className={`bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 transition-all duration-300 ${
      collapsed ? 'w-20' : 'w-64'
    }`}>
      <div className="flex flex-col h-full">
        {/* Logo */}
        <div className="h-16 flex items-center justify-between px-4 border-b border-gray-200 dark:border-gray-700">
          {!collapsed && (
            <span className="text-xl font-bold text-blue-600 dark:text-blue-400">
              CodeReview
            </span>
          )}
          <button
            onClick={onToggle}
            className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
          >
            {collapsed ? (
              <ChevronDoubleRightIcon className="w-5 h-5" />
            ) : (
              <ChevronDoubleLeftIcon className="w-5 h-5" />
            )}
          </button>
        </div>

        {/* Menu Items */}
        <nav className="flex-1 py-4">
          {menuItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center px-4 py-3 my-1 mx-2 rounded-lg transition-colors ${
                  isActive
                    ? 'bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400'
                    : 'hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300'
                }`
              }
            >
              <item.icon className="w-6 h-6" />
              {!collapsed && <span className="ml-3">{item.label}</span>}
            </NavLink>
          ))}
        </nav>
      </div>
    </div>
  );
};

export default Sidebar;