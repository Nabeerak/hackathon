import React, { useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import AuthModal from '../Auth/AuthModal';
import styles from './PersonalizeButton.module.css';

interface PersonalizeButtonProps {
  chapterTitle: string;
}

export default function PersonalizeButton({ chapterTitle }: PersonalizeButtonProps) {
  const { isAuthenticated, user } = useAuth();
  const [authModalOpen, setAuthModalOpen] = useState(false);
  const [isPersonalized, setIsPersonalized] = useState(false);

  const handlePersonalize = () => {
    if (!isAuthenticated) {
      setAuthModalOpen(true);
      return;
    }

    if (!user?.personalization_enabled) {
      alert('Personalization is disabled. Enable it in your profile settings.');
      return;
    }

    // Toggle personalization
    setIsPersonalized(!isPersonalized);
  };

  if (!isAuthenticated) {
    return (
      <>
        <div className={styles.personalizeContainer}>
          <div className={styles.personalizeInfo}>
            <h3>📚 Personalize Your Learning Experience</h3>
            <p>
              Sign in to get content tailored to your background and experience level.
              Our AI will adapt examples and explanations based on your software and hardware knowledge.
            </p>
            <button className={styles.personalizeButton} onClick={() => setAuthModalOpen(true)}>
              Sign In to Personalize
            </button>
          </div>
        </div>
        <AuthModal
          isOpen={authModalOpen}
          onClose={() => setAuthModalOpen(false)}
          initialMode="signup"
        />
      </>
    );
  }

  if (!user?.personalization_enabled) {
    return (
      <div className={styles.personalizeContainer}>
        <div className={styles.personalizeInfo}>
          <h3>📚 Personalized Content</h3>
          <p>
            Personalization is currently disabled.{' '}
            <a href="/profile">Enable it in your profile</a> to get content tailored to your background.
          </p>
        </div>
      </div>
    );
  }

  return (
    <>
      <div className={styles.personalizeContainer}>
        <div className={styles.personalizeInfo}>
          <h3>📚 {isPersonalized ? 'Personalized Content Active' : 'Personalize This Chapter'}</h3>
          <p>
            {isPersonalized ? (
              <>
                Content is tailored for <strong>{user.experience_level}</strong> level.
                {user.software_background && (
                  <> Examples adapted for your background in <strong>{user.software_background}</strong>.</>
                )}
              </>
            ) : (
              <>
                Click below to adapt this chapter's content to your experience level ({user.experience_level})
                and background.
              </>
            )}
          </p>
          <button
            className={`${styles.personalizeButton} ${isPersonalized ? styles.activeButton : ''}`}
            onClick={handlePersonalize}
          >
            {isPersonalized ? '✓ Personalization Active' : 'Personalize Content'}
          </button>
          {isPersonalized && user.preferred_language === 'ur' && (
            <button
              className={styles.translateButton}
              onClick={() => alert('Translation feature coming soon!')}
            >
              🌐 Translate to Urdu (اردو)
            </button>
          )}
        </div>
      </div>
      {isPersonalized && (
        <div className={styles.personalizedBadge}>
          ✨ Content personalized for you
        </div>
      )}
    </>
  );
}
