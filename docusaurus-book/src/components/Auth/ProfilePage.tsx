import React, { useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import styles from './Auth.module.css';

export default function ProfilePage() {
  const { user, signOut, updateProfile } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    software_background: user?.software_background || '',
    hardware_background: user?.hardware_background || '',
    learning_goals: user?.learning_goals || '',
    experience_level: user?.experience_level || 'beginner',
    personalization_enabled: user?.personalization_enabled ?? true,
    preferred_language: user?.preferred_language || 'en',
  });
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  if (!user) {
    return <div>Please sign in to view your profile.</div>;
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const value = e.target.type === 'checkbox' ? (e.target as HTMLInputElement).checked : e.target.value;
    setFormData({
      ...formData,
      [e.target.name]: value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setMessage('');

    try {
      await updateProfile(formData);
      setMessage('Profile updated successfully!');
      setIsEditing(false);
      setTimeout(() => setMessage(''), 3000);
    } catch (error: any) {
      setMessage('Failed to update profile: ' + (error.message || 'Unknown error'));
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.profilePage}>
      <div className={styles.profileHeader}>
        <h1>My Profile</h1>
        <button onClick={() => signOut()} className={styles.logoutButton}>
          Logout
        </button>
      </div>

      {message && (
        <div className={message.includes('success') ? styles.success : styles.error}>
          {message}
        </div>
      )}

      <div className={styles.profileSection}>
        <h2>Account Information</h2>
        <div className={styles.profileInfo}>
          <div className={styles.profileField}>
            <strong>Username:</strong>
            <span>{user.username}</span>
          </div>
          <div className={styles.profileField}>
            <strong>Email:</strong>
            <span>{user.email}</span>
          </div>
          <div className={styles.profileField}>
            <strong>Member Since:</strong>
            <span>{new Date(user.created_at).toLocaleDateString()}</span>
          </div>
        </div>
      </div>

      <div className={styles.profileSection}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h2>Learning Profile</h2>
          {!isEditing && (
            <button onClick={() => setIsEditing(true)} className={styles.submitButton} style={{ width: 'auto', padding: '0.5rem 1rem' }}>
              Edit Profile
            </button>
          )}
        </div>

        {isEditing ? (
          <form onSubmit={handleSubmit} className={styles.authForm} style={{ boxShadow: 'none', padding: 0 }}>
            <div className={styles.formGroup}>
              <label htmlFor="experience_level">Experience Level</label>
              <select
                id="experience_level"
                name="experience_level"
                value={formData.experience_level}
                onChange={handleChange}
              >
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
              </select>
            </div>

            <div className={styles.formGroup}>
              <label htmlFor="software_background">Software Background</label>
              <textarea
                id="software_background"
                name="software_background"
                value={formData.software_background}
                onChange={handleChange}
                placeholder="e.g., Python, JavaScript, C++, ROS"
                rows={3}
              />
            </div>

            <div className={styles.formGroup}>
              <label htmlFor="hardware_background">Hardware Background</label>
              <textarea
                id="hardware_background"
                name="hardware_background"
                value={formData.hardware_background}
                onChange={handleChange}
                placeholder="e.g., Arduino, Raspberry Pi, 3D Printing, Electronics"
                rows={3}
              />
            </div>

            <div className={styles.formGroup}>
              <label htmlFor="learning_goals">Learning Goals</label>
              <textarea
                id="learning_goals"
                name="learning_goals"
                value={formData.learning_goals}
                onChange={handleChange}
                placeholder="What do you want to learn from this course?"
                rows={3}
              />
            </div>

            <div className={styles.formGroup}>
              <label htmlFor="preferred_language">Preferred Language</label>
              <select
                id="preferred_language"
                name="preferred_language"
                value={formData.preferred_language}
                onChange={handleChange}
              >
                <option value="en">English</option>
                <option value="ur">Urdu (اردو)</option>
              </select>
            </div>

            <div className={styles.formGroup}>
              <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <input
                  type="checkbox"
                  name="personalization_enabled"
                  checked={formData.personalization_enabled}
                  onChange={handleChange}
                  style={{ width: 'auto' }}
                />
                Enable personalized content based on my background
              </label>
            </div>

            <div style={{ display: 'flex', gap: '1rem' }}>
              <button type="submit" className={styles.submitButton} disabled={isLoading}>
                {isLoading ? 'Saving...' : 'Save Changes'}
              </button>
              <button
                type="button"
                onClick={() => {
                  setIsEditing(false);
                  setFormData({
                    software_background: user?.software_background || '',
                    hardware_background: user?.hardware_background || '',
                    learning_goals: user?.learning_goals || '',
                    experience_level: user?.experience_level || 'beginner',
                    personalization_enabled: user?.personalization_enabled ?? true,
                    preferred_language: user?.preferred_language || 'en',
                  });
                }}
                className={styles.submitButton}
                style={{ background: 'var(--ifm-color-gray-500)' }}
              >
                Cancel
              </button>
            </div>
          </form>
        ) : (
          <div className={styles.profileInfo}>
            <div className={styles.profileField}>
              <strong>Experience Level:</strong>
              <span style={{ textTransform: 'capitalize' }}>{user.experience_level || 'Not set'}</span>
            </div>
            <div className={styles.profileField}>
              <strong>Software Background:</strong>
              <span>{user.software_background || 'Not provided'}</span>
            </div>
            <div className={styles.profileField}>
              <strong>Hardware Background:</strong>
              <span>{user.hardware_background || 'Not provided'}</span>
            </div>
            <div className={styles.profileField}>
              <strong>Learning Goals:</strong>
              <span>{user.learning_goals || 'Not provided'}</span>
            </div>
            <div className={styles.profileField}>
              <strong>Preferred Language:</strong>
              <span>{user.preferred_language === 'ur' ? 'Urdu (اردو)' : 'English'}</span>
            </div>
            <div className={styles.profileField}>
              <strong>Personalization:</strong>
              <span>{user.personalization_enabled ? 'Enabled' : 'Disabled'}</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
