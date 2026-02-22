// src/components/dashboard/MetricsCard.tsx
import React from 'react';

interface MetricsCardProps {
  title: string;
  value: number | string;
  icon: React.ForwardRefExoticComponent<any>;
  color: string;
  bgColor: string;
  change?: number;
}

const MetricsCard: React.FC<MetricsCardProps> = ({ 
  title, 
  value, 
  icon: Icon, 
  color, 
  bgColor,
  change = 0 
}) => {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-600 dark:text-gray-400">{title}</p>
          <p className="text-2xl font-bold mt-2">{value}</p>
          {change !== 0 && (
            <p className={`text-sm mt-2 ${change > 0 ? 'text-green-600' : 'text-red-600'}`}>
              {change > 0 ? '+' : ''}{change}% from last month
            </p>
          )}
        </div>
        <div className={`p-3 rounded-full ${bgColor}`}>
          <Icon className={`w-6 h-6 ${color}`} />
        </div>
      </div>
    </div>
  );
};

export default MetricsCard;