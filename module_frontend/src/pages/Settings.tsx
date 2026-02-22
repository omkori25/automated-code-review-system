// src/pages/Settings.tsx
import React, { useState } from 'react';
import { 
  UserIcon, 
  BellIcon, 
  ShieldCheckIcon, 
  PaintBrushIcon,
  GlobeAltIcon,
  KeyIcon,
  CloudIcon
} from '@heroicons/react/24/outline';

interface SettingsSection {
  id: string;
  name: string;
  icon: React.ForwardRefExoticComponent<any>;
}

interface NotificationSetting {
  id: string;
  label: string;
  enabled: boolean;
}

const Settings: React.FC = () => {
  const [activeSection, setActiveSection] = useState('profile');
  const [isSaving, setIsSaving] = useState(false);
  
  // Profile settings
  const [profile, setProfile] = useState({
    fullName: 'John Doe',
    email: 'john.doe@example.com',
    role: 'Developer',
    company: 'Tech Corp'
  });
  
  // Notification settings
  const [notifications, setNotifications] = useState<NotificationSetting[]>([
    { id: 'email', label: 'Email notifications', enabled: true },
    { id: 'desktop', label: 'Desktop notifications', enabled: false },
    { id: 'slack', label: 'Slack integration', enabled: true },
    { id: 'weekly', label: 'Weekly reports', enabled: true }
  ]);
  
  // Appearance settings
  const [appearance, setAppearance] = useState({
    theme: 'system', // light, dark, system
    fontSize: 'medium', // small, medium, large
    compactView: false
  });
  
  const sections: SettingsSection[] = [
    { id: 'profile', name: 'Profile', icon: UserIcon },
    { id: 'notifications', name: 'Notifications', icon: BellIcon },
    { id: 'security', name: 'Security', icon: ShieldCheckIcon },
    { id: 'appearance', name: 'Appearance', icon: PaintBrushIcon },
    { id: 'preferences', name: 'Preferences', icon: GlobeAltIcon },
    { id: 'api', name: 'API Keys', icon: KeyIcon },
    { id: 'integrations', name: 'Integrations', icon: CloudIcon },
  ];

  const handleSave = async () => {
    setIsSaving(true);
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000));
    setIsSaving(false);
    // Show success message
  };

  const toggleNotification = (id: string) => {
    setNotifications(notifications.map(n => 
      n.id === id ? { ...n, enabled: !n.enabled } : n
    ));
  };

  const renderSection = () => {
    switch (activeSection) {
      case 'profile':
        return (
          <div className="space-y-6">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Profile Settings</h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
                  Full Name
                </label>
                <input
                  type="text"
                  value={profile.fullName}
                  onChange={(e) => setProfile({ ...profile, fullName: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
                  Email
                </label>
                <input
                  type="email"
                  value={profile.email}
                  onChange={(e) => setProfile({ ...profile, email: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
                  Role
                </label>
                <select
                  value={profile.role}
                  onChange={(e) => setProfile({ ...profile, role: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                >
                  <option>Developer</option>
                  <option>Senior Developer</option>
                  <option>Team Lead</option>
                  <option>Manager</option>
                  <option>Admin</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
                  Company
                </label>
                <input
                  type="text"
                  value={profile.company}
                  onChange={(e) => setProfile({ ...profile, company: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                />
              </div>
            </div>
          </div>
        );
      
      case 'notifications':
        return (
          <div className="space-y-6">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Notification Preferences</h2>
            
            <div className="space-y-4">
              {notifications.map((item) => (
                <div key={item.id} className="flex items-center justify-between py-2">
                  <span className="text-gray-700 dark:text-gray-300">{item.label}</span>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={item.enabled}
                      onChange={() => toggleNotification(item.id)}
                      className="sr-only peer"
                    />
                    <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
                  </label>
                </div>
              ))}
            </div>
            
            <div className="pt-4">
              <h3 className="font-medium mb-3 text-gray-900 dark:text-white">Email Digest</h3>
              <select className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white">
                <option>Daily digest</option>
                <option>Weekly digest</option>
                <option>Monthly digest</option>
                <option>Real-time only</option>
              </select>
            </div>
          </div>
        );
      
      case 'appearance':
        return (
          <div className="space-y-6">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Appearance Settings</h2>
            
            <div>
              <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">Theme</label>
              <div className="grid grid-cols-3 gap-3">
                {['light', 'dark', 'system'].map((theme) => (
                  <button
                    key={theme}
                    onClick={() => setAppearance({ ...appearance, theme })}
                    className={`px-4 py-2 border rounded-lg capitalize ${
                      appearance.theme === theme
                        ? 'bg-blue-600 text-white border-blue-600'
                        : 'border-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700'
                    }`}
                  >
                    {theme}
                  </button>
                ))}
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">Font Size</label>
              <select
                value={appearance.fontSize}
                onChange={(e) => setAppearance({ ...appearance, fontSize: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              >
                <option value="small">Small</option>
                <option value="medium">Medium</option>
                <option value="large">Large</option>
              </select>
            </div>
            
            <div className="flex items-center justify-between">
              <span className="text-gray-700 dark:text-gray-300">Compact view</span>
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={appearance.compactView}
                  onChange={(e) => setAppearance({ ...appearance, compactView: e.target.checked })}
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
              </label>
            </div>
          </div>
        );
      
      default:
        return (
          <div className="text-center py-12 text-gray-500">
            Select a section from the sidebar
          </div>
        );
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Settings</h1>
      
      <div className="flex gap-6">
        {/* Sidebar */}
        <div className="w-64 bg-white dark:bg-gray-800 rounded-lg shadow p-4">
          <nav className="space-y-2">
            {sections.map((section) => {
              const Icon = section.icon;
              return (
                <button
                  key={section.id}
                  onClick={() => setActiveSection(section.id)}
                  className={`w-full flex items-center px-4 py-3 rounded-lg transition-colors ${
                    activeSection === section.id
                      ? 'bg-blue-50 text-blue-600 dark:bg-blue-900 dark:text-blue-300'
                      : 'hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300'
                  }`}
                >
                  <Icon className="w-5 h-5 mr-3" />
                  {section.name}
                </button>
              );
            })}
          </nav>
        </div>
        
        {/* Content */}
        <div className="flex-1 bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          {renderSection()}
          
          <div className="mt-6 pt-6 border-t border-gray-200 dark:border-gray-700 flex justify-end">
            <button
              onClick={handleSave}
              disabled={isSaving}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center"
            >
              {isSaving ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Saving...
                </>
              ) : (
                'Save Changes'
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Settings;