import React, { useState } from 'react';
import Layout from '@theme/Layout';
import { useAuth } from '../contexts/AuthContext';
import ChatHistory from '../components/Auth/ChatHistory';
import styles from './dashboard.module.css';

type TabType = 'overview' | 'history';

export default function Dashboard() {
  const { user, isAuthenticated, isPending } = useAuth();
  const [activeTab, setActiveTab] = useState<TabType>('overview');

  if (isPending) {
    return (
      <Layout title="Dashboard">
        <div className={styles.container}>
          <div className={styles.loading}>Loading...</div>
        </div>
      </Layout>
    );
  }

  if (!isAuthenticated) {
    return (
      <Layout title="Dashboard">
        <div className={styles.container}>
          <div className={styles.hero}>
            <h1>Welcome to Your Dashboard</h1>
            <p>Please sign in to view your personalized dashboard</p>
            <a href="/hackathon/" className={styles.homeButton}>Go to Home</a>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout title="Dashboard">
      <div className={styles.container}>
        <div className={styles.hero}>
          <h1>Welcome back, {user?.name}!</h1>
          <p className={styles.subtitle}>Your personalized learning dashboard</p>
        </div>

        <div className={styles.tabs}>
          <button
            className={`${styles.tabButton} ${activeTab === 'overview' ? styles.active : ''}`}
            onClick={() => setActiveTab('overview')}
          >
            Overview
          </button>
          <button
            className={`${styles.tabButton} ${activeTab === 'history' ? styles.active : ''}`}
            onClick={() => setActiveTab('history')}
          >
            Chat History
          </button>
        </div>

        <div className={styles.tabContent}>
          {activeTab === 'overview' && (
            <>
              <div className={styles.statsGrid}>
                <div className={styles.statCard}>
                  <div className={styles.statIcon}>📧</div>
                  <div className={styles.statContent}>
                    <h3>Email</h3>
                    <p>{user?.email}</p>
                  </div>
                </div>
                <div className={styles.statCard}>
                  <div className={styles.statIcon}>📊</div>
                  <div className={styles.statContent}>
                    <h3>Experience Level</h3>
                    <p>{user?.experience_level || 'Beginner'}</p>
                  </div>
                </div>
                <div className={styles.statCard}>
                  <div className={styles.statIcon}>💻</div>
                  <div className={styles.statContent}>
                    <h3>Software Background</h3>
                    <p>{user?.software_background || 'Not specified'}</p>
                  </div>
                </div>
                <div className={styles.statCard}>
                  <div className={styles.statIcon}>🔧</div>
                  <div className={styles.statContent}>
                    <h3>Hardware Background</h3>
                    <p>{user?.hardware_background || 'Not specified'}</p>
                  </div>
                </div>
              </div>

              {user?.learning_goals && (
                <section className={styles.section}>
                  <h2>Your Learning Goals</h2>
                  <div className={styles.goalsCard}>
                    <p>{user.learning_goals}</p>
                  </div>
                </section>
              )}

              <section className={styles.section}>
                <h2>Quick Links</h2>
                <div className={styles.linksGrid}>
                  <a href="/hackathon/physical-ai-textbook/intro" className={styles.linkCard}>
                    <span className={styles.linkIcon}>📚</span>
                    <h3>Documentation</h3>
                    <p>Start learning</p>
                  </a>
                </div>
              </section>
            </>
          )}

          {activeTab === 'history' && (
            <div className={styles.chatHistoryWrapper}>
              <ChatHistory />
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
}
