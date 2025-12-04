import React from 'react';
import { AuthProvider } from '../contexts/AuthContext';
import Chatbot from '../components/Chatbot';

export default function Root({ children }) {
  return (
    <AuthProvider>
      {children}
      <Chatbot />
    </AuthProvider>
  );
}
