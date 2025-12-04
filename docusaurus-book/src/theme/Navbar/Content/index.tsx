import React, { useState } from 'react';
import Content from '@theme-original/Navbar/Content';
import { useAuth } from '../../../contexts/AuthContext';
import AuthModal from '../../../components/Auth/AuthModal';
import styles from './styles.module.css';

export default function ContentWrapper(props) {
  const { isAuthenticated, user } = useAuth();
  const [authModalOpen, setAuthModalOpen] = useState(false);

  return (
    <>
      <Content {...props} />
      <div className={styles.authButtons}>
        {isAuthenticated && user ? (
          <a href="/profile" className={styles.profileLink}>
            <span className={styles.userIcon}>👤</span>
            {user.name}
          </a>
        ) : (
          <button
            className={styles.signInButton}
            onClick={() => setAuthModalOpen(true)}
          >
            Sign In
          </button>
        )}
      </div>
      <AuthModal
        isOpen={authModalOpen}
        onClose={() => setAuthModalOpen(false)}
        initialMode="signin"
      />
    </>
  );
}
