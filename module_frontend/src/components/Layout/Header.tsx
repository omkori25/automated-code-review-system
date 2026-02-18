// module_frontend/src/components/Layout/Header.tsx
import React from 'react';
import { BellIcon, UserCircleIcon, MagnifyingGlassIcon } from '@heroicons/react/24/outline';

const Header: React.FC = () => {
  return (
    <header className="h-16 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-4">
      <div className="flex items-center justify-between h-full">
        {/* Search */}
        <div className="flex-1 max-w-xl">
          <div className="relative">
            <MagnifyingGlassIcon className="w-5 h-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
            <input
              type="text"
              placeholder="Search files, projects..."
              className="w-full pl-10 pr-4 py-2 border border-gray-200 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>

        {/* Right side icons */}
        <div className="flex items-center space-x-4">
          <button className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 relative">
            <BellIcon className="w-6 h-6" />
            <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
          </button>
          
          <button className="flex items-center space-x-2 p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700">
            <UserCircleIcon className="w-8 h-8" />
            <div className="text-left hidden md:block">
              <div className="text-sm font-medium">John Doe</div>
              <div className="text-xs text-gray-500">Developer</div>
            </div>
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;