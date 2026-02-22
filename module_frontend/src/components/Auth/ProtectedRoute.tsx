// src/components/Auth/ProtectedRoute.tsx
import React from 'react';
import { Navigate } from 'react-router-dom';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  // Check if user is authenticated
  // For demo, check if token exists in localStorage
  const isAuthenticated = localStorage.getItem('auth_token') !== null;
  
  // For development, you can set this to true to bypass authentication
  // const isAuthenticated = true;
  
  if (!isAuthenticated) {
    // Redirect to login page if not authenticated
    return <Navigate to="/login" replace />;
  }

  // Render children if authenticated
  return <>{children}</>;
};

export default ProtectedRoute;