import React, { useState, useRef, useEffect } from 'react';
import Content from '@theme-original/Navbar/Content';
import { useAuth } from '../../../contexts/AuthContext';
import AuthModal from '../../../components/Auth/AuthModal';
import styles from './styles.module.css';

export default function ContentWrapper(props) {
  const { isAuthenticated, user, signOut } = useAuth();
  const [authModalOpen, setAuthModalOpen] = useState(false);
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setDropdownOpen(false);
      }
    }

    if (dropdownOpen) {
      document.addEventListener('mousedown', handleClickOutside);
      return () => {
        document.removeEventListener('mousedown', handleClickOutside);
      };
    }
  }, [dropdownOpen]);

  const handleSignOut = async () => {
    await signOut();
    setDropdownOpen(false);
    window.location.href = '/hackathon/';
  };

  return (
    <>
      <Content {...props} />
      <div className={styles.authButtons}>
        {isAuthenticated && user ? (
          <>
            <a href="/hackathon/dashboard" className={styles.dashboardLink}>
              Dashboard
            </a>
            <div className={styles.userMenu} ref={dropdownRef}>
              <button
                className={styles.userButton}
                onClick={() => setDropdownOpen(!dropdownOpen)}
              >
                <span className={styles.userIcon}>👤</span>
                {user.name}
              </button>
              {dropdownOpen && (
                <div className={styles.dropdown}>
                  <a href="/hackathon/dashboard" className={styles.dropdownItem}>
                    Dashboard
                  </a>
                  <button
                    onClick={handleSignOut}
                    className={styles.dropdownItem}
                  >
                    Sign Out
                  </button>
                </div>
              )}
            </div>
          </>
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
