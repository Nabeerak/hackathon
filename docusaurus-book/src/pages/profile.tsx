import React, { useEffect, useState } from 'react';
import Layout from '@theme/Layout';
import { useAuth } from '../contexts/AuthContext';
import ProfilePage from '../components/Auth/ProfilePage';
import ChatHistory from '../components/Auth/ChatHistory';
import { useHistory } from '@docusaurus/router';

export default function Profile() {
  const { isAuthenticated, isPending } = useAuth();
  const history = useHistory();
  const [activeTab, setActiveTab] = useState<'profile' | 'history'>('profile');

  useEffect(() => {
    if (!isPending && !isAuthenticated) {
      history.push('/');
    }
  }, [isAuthenticated, isPending, history]);

  if (isPending) {
    return (
      <Layout title="Profile">
        <div style={{ padding: '4rem 2rem', textAlign: 'center' }}>
          Loading...
        </div>
      </Layout>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  return (
    <Layout title="Profile">
      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '2rem' }}>
        <div style={{ display: 'flex', gap: '1rem', marginBottom: '2rem', borderBottom: '2px solid var(--ifm-color-emphasis-200)' }}>
          <button
            onClick={() => setActiveTab('profile')}
            style={{
              padding: '1rem 2rem',
              background: 'transparent',
              border: 'none',
              borderBottom: activeTab === 'profile' ? '3px solid var(--ifm-color-primary)' : 'none',
              color: activeTab === 'profile' ? 'var(--ifm-color-primary)' : 'var(--ifm-color-emphasis-700)',
              cursor: 'pointer',
              fontSize: '1.1rem',
              fontWeight: activeTab === 'profile' ? 'bold' : 'normal'
            }}
          >
            Profile
          </button>
          <button
            onClick={() => setActiveTab('history')}
            style={{
              padding: '1rem 2rem',
              background: 'transparent',
              border: 'none',
              borderBottom: activeTab === 'history' ? '3px solid var(--ifm-color-primary)' : 'none',
              color: activeTab === 'history' ? 'var(--ifm-color-primary)' : 'var(--ifm-color-emphasis-700)',
              cursor: 'pointer',
              fontSize: '1.1rem',
              fontWeight: activeTab === 'history' ? 'bold' : 'normal'
            }}
          >
            Chat History
          </button>
        </div>
        {activeTab === 'profile' ? <ProfilePage /> : <ChatHistory />}
      </div>
    </Layout>
  );
}
