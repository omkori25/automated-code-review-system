@echo off
cd C:\Users\Om Kori\Desktop\automated-code-review-system\automated-code-review-system\module_frontend\src

echo Creating dashboard components directory...
mkdir components\dashboard 2>nul

echo Creating MetricsCard.tsx...
(
echo import React from 'react';
echo.
echo interface MetricsCardProps {
echo   title: string;
echo   value: number ^| string;
echo   icon: React.ForwardRefExoticComponent^<any^>;
echo   color: string;
echo   bgColor: string;
echo   change?: number;
echo }
echo.
echo const MetricsCard: React.FC^<MetricsCardProps^> = ({ 
echo   title, 
echo   value, 
echo   icon: Icon, 
echo   color, 
echo   bgColor,
echo   change = 0 
echo }) =^> {
echo   return (
echo     ^<div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6"^>
echo       ^<div className="flex items-center justify-between"^>
echo         ^<div^>
echo           ^<p className="text-sm text-gray-600 dark:text-gray-400"^>{title}^</p^>
echo           ^<p className="text-2xl font-bold mt-2"^>{value}^</p^>
echo           {change !== 0 ^&^& (
echo             ^<p className={`text-sm mt-2 ${change ^> 0 ? 'text-green-600' : 'text-red-600'}`^}>
echo               {change ^> 0 ? '+' : ''}{change}%% from last month
echo             ^</p^>
echo           )}
echo         ^</div^>
echo         ^<div className={`p-3 rounded-full ${bgColor}`}^>
echo           ^<Icon className={`w-6 h-6 ${color}`} /^>
echo         ^</div^>
echo       ^</div^>
echo     ^</div^>
echo   );
echo };
echo.
echo export default MetricsCard;
) > components\dashboard\MetricsCard.tsx

echo Creating Charts.tsx...
(
echo import React from 'react';
echo.
echo const IssueTrend: React.FC^<{ data?: any[] }^> = ({ data }) =^> {
echo   return (
echo     ^<div className="h-64 flex items-center justify-center bg-gray-50 dark:bg-gray-700 rounded"^>
echo       ^<p className="text-gray-500"^>Issue Trend Chart (Placeholder)^</p^>
echo       {data ^&^& ^<pre className="hidden"^>{JSON.stringify(data)}^</pre^>}
echo     ^</div^>
echo   );
echo };
echo.
echo const IssueDistribution: React.FC^<{ data?: any[] }^> = ({ data }) =^> {
echo   return (
echo     ^<div className="h-64 flex items-center justify-center bg-gray-50 dark:bg-gray-700 rounded"^>
echo       ^<p className="text-gray-500"^>Issue Distribution Chart (Placeholder)^</p^>
echo       {data ^&^& ^<pre className="hidden"^>{JSON.stringify(data)}^</pre^>}
echo     ^</div^>
echo   );
echo };
echo.
echo const Charts = {
echo   IssueTrend,
echo   IssueDistribution
echo };
echo.
echo export default Charts;
) > components\dashboard\Charts.tsx

echo Creating ProjectSelector.tsx...
(
echo import React from 'react';
echo.
echo interface ProjectSelectorProps {
echo   selected: string ^| null;
echo   onSelect: (projectId: string ^| null) =^> void;
echo }
echo.
echo const ProjectSelector: React.FC^<ProjectSelectorProps^> = ({ selected, onSelect }) =^> {
echo   const projects = [
echo     { id: '1', name: 'All Projects' },
echo     { id: '2', name: 'Backend API' },
echo     { id: '3', name: 'Frontend Dashboard' },
echo   ];
echo.
echo   return (
echo     ^<select
echo       value={selected ^|^| '1'}
echo       onChange={(e) =^> onSelect(e.target.value === '1' ? null : e.target.value)}
echo       className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:border-gray-600"
echo     ^>
echo       {projects.map(project =^> (
echo         ^<option key={project.id} value={project.id}^>
echo           {project.name}
echo         ^</option^>
echo       ))}
echo     ^</select^>
echo   );
echo };
echo.
echo export default ProjectSelector;
) > components\dashboard\ProjectSelector.tsx

echo ✅ All dashboard components created successfully!
echo.
echo Press any key to continue...
pause > nul