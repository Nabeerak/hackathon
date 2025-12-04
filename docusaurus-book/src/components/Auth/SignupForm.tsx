import React, { useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import styles from './Auth.module.css';

export default function SignupForm({ onSuccess }: { onSuccess?: () => void }) {
  const { signUp } = useAuth();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    software_background: '',
    hardware_background: '',
    learning_goals: '',
    experience_level: 'beginner' as 'beginner' | 'intermediate' | 'advanced',
  });
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
    setError('');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (formData.password.length < 8) {
      setError('Password must be at least 8 characters');
      return;
    }

    setIsLoading(true);

    try {
      // Make direct API call to our backend with custom fields
      const baseURL = typeof window !== 'undefined' &&
        (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
        ? 'http://localhost:8000'
        : 'https://your-backend-url.com';

      const response = await fetch(`${baseURL}/api/auth/sign-up/email`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({
          name: formData.name,
          email: formData.email,
          password: formData.password,
          software_background: formData.software_background || null,
          hardware_background: formData.hardware_background || null,
          learning_goals: formData.learning_goals || null,
          experience_level: formData.experience_level,
        }),
      });

      const result = await response.json();

      if (result.error) {
        setError(result.error.message || 'Signup failed');
        return;
      }

      if (result.data?.access_token) {
        localStorage.setItem('jwt_token', result.data.access_token);
        onSuccess?.();
      } else if (result.data?.user) {
        // Fallback for cases where access_token might not be directly in data, but user is present
        onSuccess?.();
      } else {
        setError('Signup failed');
      }
    } catch (err: any) {
      setError(err.message || 'Signup failed');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form className={styles.authForm} onSubmit={handleSubmit}>
      <h2>Sign Up</h2>
      {error && <div className={styles.error}>{error}</div>}

      <div className={styles.formGroup}>
        <label htmlFor="name">Name *</label>
        <input
          type="text"
          id="name"
          name="name"
          value={formData.name}
          onChange={handleChange}
          required
          minLength={3}
          maxLength={50}
        />
      </div>

      <div className={styles.formGroup}>
        <label htmlFor="email">Email *</label>
        <input
          type="email"
          id="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          required
        />
      </div>

      <div className={styles.formGroup}>
        <label htmlFor="password">Password * (min 8 characters)</label>
        <input
          type="password"
          id="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          required
          minLength={8}
        />
      </div>

      <div className={styles.formGroup}>
        <label htmlFor="confirmPassword">Confirm Password *</label>
        <input
          type="password"
          id="confirmPassword"
          name="confirmPassword"
          value={formData.confirmPassword}
          onChange={handleChange}
          required
        />
      </div>

      <div className={styles.formGroup}>
        <label htmlFor="experience_level">Experience Level *</label>
        <select
          id="experience_level"
          name="experience_level"
          value={formData.experience_level}
          onChange={handleChange}
          required
        >
          <option value="beginner">Beginner</option>
          <option value="intermediate">Intermediate</option>
          <option value="advanced">Advanced</option>
        </select>
      </div>

      <div className={styles.formGroup}>
        <label htmlFor="software_background">Software Background (Optional)</label>
        <textarea
          id="software_background"
          name="software_background"
          value={formData.software_background}
          onChange={handleChange}
          placeholder="e.g., Python, JavaScript, C++, ROS"
          rows={2}
        />
      </div>

      <div className={styles.formGroup}>
        <label htmlFor="hardware_background">Hardware Background (Optional)</label>
        <textarea
          id="hardware_background"
          name="hardware_background"
          value={formData.hardware_background}
          onChange={handleChange}
          placeholder="e.g., Arduino, Raspberry Pi, 3D Printing, Electronics"
          rows={2}
        />
      </div>

      <div className={styles.formGroup}>
        <label htmlFor="learning_goals">Learning Goals (Optional)</label>
        <textarea
          id="learning_goals"
          name="learning_goals"
          value={formData.learning_goals}
          onChange={handleChange}
          placeholder="What do you want to learn from this course?"
          rows={3}
        />
      </div>

      <button type="submit" className={styles.submitButton} disabled={isLoading}>
        {isLoading ? 'Creating Account...' : 'Sign Up'}
      </button>
    </form>
  );
}
