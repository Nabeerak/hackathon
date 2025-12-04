import React, { useState } from 'react';
import SignupForm from './SignupForm';
import SigninForm from './SigninForm';
import styles from './Auth.module.css';

interface AuthModalProps {
  isOpen: boolean;
  onClose: () => void;
  initialMode?: 'signin' | 'signup';
}

export default function AuthModal({ isOpen, onClose, initialMode = 'signin' }: AuthModalProps) {
  const [mode, setMode] = useState<'signin' | 'signup'>(initialMode);

  if (!isOpen) return null;

  const handleSuccess = () => {
    onClose();
  };

  return (
    <div className={styles.authModal} onClick={onClose}>
      <div className={styles.authModalContent} onClick={(e) => e.stopPropagation()}>
        <button className={styles.closeButton} onClick={onClose}>
          &times;
        </button>

        {mode === 'signin' ? (
          <>
            <SigninForm onSuccess={handleSuccess} />
            <div className={styles.authToggle}>
              <p>
                Don't have an account?{' '}
                <button onClick={() => setMode('signup')}>Sign Up</button>
              </p>
            </div>
          </>
        ) : (
          <>
            <SignupForm onSuccess={handleSuccess} />
            <div className={styles.authToggle}>
              <p>
                Already have an account?{' '}
                <button onClick={() => setMode('signin')}>Sign In</button>
              </p>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
