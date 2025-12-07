import React from 'react';
import { AuthProvider, useAuth } from '../contexts/AuthContext';
import Chatbot from '../components/Chatbot';

function RootContent({ children }) {
  const { backendReady, backendError } = useAuth();

  // Show loading state while backend initializes
  if (!backendReady && !backendError) {
    return (
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
        fontFamily: 'system-ui, -apple-system, sans-serif'
      }}>
        <div style={{ marginBottom: '1rem' }}>Initializing backend services...</div>
        <div style={{
          border: '4px solid #f3f3f3',
          borderTop: '4px solid #3498db',
          borderRadius: '50%',
          width: '40px',
          height: '40px',
          animation: 'spin 1s linear infinite'
        }} />
        <style>{`
          @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }
        `}</style>
      </div>
    );
  }

  // Show error state if backend fails
  if (backendError) {
    return (
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
        fontFamily: 'system-ui, -apple-system, sans-serif',
        padding: '2rem'
      }}>
        <div style={{ color: '#e74c3c', fontSize: '1.2rem', marginBottom: '1rem' }}>
          Backend Connection Failed
        </div>
        <div style={{ color: '#666', marginBottom: '1rem' }}>
          {backendError}
        </div>
        <button
          onClick={() => window.location.reload()}
          style={{
            padding: '0.5rem 1rem',
            backgroundColor: '#3498db',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          Retry
        </button>
      </div>
    );
  }

  // Backend ready - render app
  return (
    <>
      {children}
      <Chatbot />
    </>
  );
}

export default function Root({ children }) {
  return (
    <AuthProvider>
      <RootContent>{children}</RootContent>
    </AuthProvider>
  );
}
