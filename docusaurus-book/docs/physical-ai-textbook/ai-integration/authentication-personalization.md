---
title: Authentication and Personalization
sidebar_label: Authentication & Personalization
sidebar_position: 2
description: User authentication system with personalized content delivery
keywords: [authentication, better-auth, personalization, user profiles]
---

# Authentication and Personalization

## Introduction

This chapter covers implementing user authentication and personalized content delivery for your Physical AI textbook. Using better-auth.com, we'll create a system that collects user background information and provides personalized content based on their experience level and learning goals.

## Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │───▶│   Better Auth    │───▶│   Neon DB       │
│   (Docusaurus)  │    │   Authentication │    │   (User Data)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  Personalization │
                    │  Service         │
                    └──────────────────┘
```

## Technology Stack

### Better Auth
- **Purpose**: Authentication and user management
- **Features**:
  - OAuth providers (Google, GitHub, etc.)
  - Email/password authentication
  - Session management
  - User metadata storage
  - TypeScript support

### Neon Serverless Postgres
- **Purpose**: Store user profiles, preferences, and learning progress
- **Features**:
  - Serverless scaling
  - Branching for development
  - PostgreSQL compatibility
  - Connection pooling

## Better Auth Setup

### Installation

```bash
npm install better-auth
```

### Configuration

```ts
// src/auth/auth.config.ts
import { defineConfig } from "better-auth";

export const auth = defineConfig({
  database: {
    provider: "postgresql",
    url: process.env.DATABASE_URL!,
  },
  secret: process.env.AUTH_SECRET!,
  socialProviders: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    },
    github: {
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!,
    },
  },
  user: {
    // Additional user fields for learning profiles
    additionalFields: {
      background: {
        type: "string",
        required: true,
      },
      experience_level: {
        type: "string",
        required: true,
      },
      learning_goals: {
        type: "json",
        required: false,
      },
      current_chapter: {
        type: "string",
        required: false,
      },
      progress: {
        type: "json",
        required: false,
      },
      preferred_language: {
        type: "string",
        required: false,
        defaultValue: "en",
      },
    },
  },
});
```

### API Route Setup

```ts
// src/pages/api/auth/[...auth].ts
import { auth } from "@/auth/auth.config";

export default auth.$handle;
```

## Registration with Background Collection

### Registration Form Component

```tsx
// src/components/RegistrationForm.tsx
import { useState } from 'react';
import { signIn } from 'better-auth/react';
import { useNavigate } from 'react-router-dom';

const RegistrationForm = () => {
  const [background, setBackground] = useState('');
  const [experience, setExperience] = useState('beginner');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    
    try {
      // First, create the account with email/password
      const result = await signIn.email({
        email,
        password,
        callbackURL: '/dashboard',
        options: {
          // Additional user data
          background,
          experience_level: experience,
          learning_goals: ['understand ROS 2', 'build humanoid robot'],
          progress: {},
          preferred_language: 'en',
        },
      });
      
      if (result?.error) {
        console.error('Registration error:', result.error);
        alert(`Registration failed: ${result.error}`);
      }
    } catch (error) {
      console.error('Registration error:', error);
      alert('Registration failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };
  
  return (
    <form onSubmit={handleSubmit} className="auth-form">
      <div className="form-group">
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
      </div>
      
      <div className="form-group">
        <label htmlFor="password">Password</label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
      </div>
      
      <div className="form-group">
        <label htmlFor="background">Software/Hardware Background</label>
        <select
          id="background"
          value={background}
          onChange={(e) => setBackground(e.target.value)}
          required
        >
          <option value="">Select your background</option>
          <option value="software_engineer">Software Engineer</option>
          <option value="hardware_engineer">Hardware Engineer</option>
          <option value="robotics_researcher">Robotics Researcher</option>
          <option value="student">Student</option>
          <option value="hobbyist">Hobbyist</option>
          <option value="other">Other</option>
        </select>
      </div>
      
      <div className="form-group">
        <label htmlFor="experience">Experience Level</label>
        <select
          id="experience"
          value={experience}
          onChange={(e) => setExperience(e.target.value)}
          required
        >
          <option value="beginner">Beginner (0-1 years)</option>
          <option value="intermediate">Intermediate (1-3 years)</option>
          <option value="advanced">Advanced (3+ years)</option>
        </select>
      </div>
      
      <button type="submit" disabled={isLoading}>
        {isLoading ? 'Registering...' : 'Register'}
      </button>
    </form>
  );
};

export default RegistrationForm;
```

## Personalized Content Delivery

### User Profile Context Provider

```tsx
// src/contexts/UserProfileContext.tsx
import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { useSession } from 'better-auth/react';

interface UserPreferences {
  background: string;
  experience_level: string;
  learning_goals: string[];
  current_chapter: string;
  progress: Record<string, any>;
  preferred_language: string;
}

interface UserProfileContextType {
  preferences: UserPreferences | null;
  updatePreferences: (newPrefs: Partial<UserPreferences>) => Promise<void>;
  isPersonalized: boolean;
}

const UserProfileContext = createContext<UserProfileContextType | undefined>(undefined);

export const UserProfileProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [preferences, setPreferences] = useState<UserPreferences | null>(null);
  const { session } = useSession();
  
  useEffect(() => {
    if (session?.user) {
      loadPreferences();
    }
  }, [session]);
  
  const loadPreferences = async () => {
    try {
      const response = await fetch('/api/user/preferences');
      if (response.ok) {
        const data = await response.json();
        setPreferences(data);
      }
    } catch (error) {
      console.error('Error loading user preferences:', error);
    }
  };
  
  const updatePreferences = async (newPrefs: Partial<UserPreferences>) => {
    if (!session?.user) return;
    
    try {
      const response = await fetch('/api/user/preferences', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newPrefs),
      });
      
      if (response.ok) {
        setPreferences(prev => prev ? { ...prev, ...newPrefs } : null);
      }
    } catch (error) {
      console.error('Error updating preferences:', error);
    }
  };
  
  const isPersonalized = !!preferences && session?.user;
  
  return (
    <UserProfileContext.Provider value={{ preferences, updatePreferences, isPersonalized }}>
      {children}
    </UserProfileContext.Provider>
  );
};

export const useUserProfile = () => {
  const context = useContext(UserProfileContext);
  if (context === undefined) {
    throw new Error('useUserProfile must be used within a UserProfileProvider');
  }
  return context;
};
```

### Personalized Content Component

```tsx
// src/components/PersonalizedContent.tsx
import React from 'react';
import { useUserProfile } from '../contexts/UserProfileContext';

interface PersonalizedContentProps {
  children: React.ReactNode;
  difficulty?: 'beginner' | 'intermediate' | 'advanced';
  topic?: string;
  fallback?: React.ReactNode;
}

const PersonalizedContent: React.FC<PersonalizedContentProps> = ({ 
  children, 
  difficulty, 
  topic,
  fallback = null 
}) => {
  const { preferences, isPersonalized } = useUserProfile();
  
  // If not personalized, show default content
  if (!isPersonalized) {
    return <>{children}</>;
  }
  
  // Filter content based on user preferences
  if (difficulty && preferences?.experience_level) {
    const userLevel = preferences.experience_level;
    
    // For beginners, show only beginner or match content
    if (userLevel === 'beginner' && difficulty !== 'beginner' && difficulty !== 'intermediate') {
      return fallback;
    }
    
    // For intermediate users, show beginner, intermediate, or match content
    if (userLevel === 'intermediate' && difficulty === 'advanced') {
      // Show simplified version or redirect to appropriate content
      return (
        <div className="simplified-content">
          <p>This advanced content is available, but we recommend completing foundational topics first.</p>
          <button onClick={() => {
            // Logic to show simplified version
          }}>
            View Simplified Version
          </button>
        </div>
      );
    }
  }
  
  // Filter by user's learning goals
  if (topic && preferences?.learning_goals) {
    const userGoalMatches = preferences.learning_goals.some(goal => 
      goal.toLowerCase().includes(topic.toLowerCase())
    );
    
    if (userGoalMatches) {
      // Enhance content for goal-relevant topics
      return (
        <div className={`enhanced-content goal-relevant ${topic}`}>
          {children}
          <div className="goal-context">
            <p>This content aligns with your learning goal: "{topic}"</p>
          </div>
        </div>
      );
    }
  }
  
  return <>{children}</>;
};

export default PersonalizedContent;
```

## Backend API for User Preferences

### Express.js API Routes

```ts
// src/server/routes/user.ts
import express from 'express';
import { auth } from '../../auth/auth.config';

const router = express.Router();

// Get user preferences
router.get('/preferences', auth.withSession(), async (req, res) => {
  try {
    const user = req.session?.user;
    if (!user) {
      return res.status(401).json({ error: 'Unauthorized' });
    }
    
    // Return user preferences from the database
    res.json({
      background: user.background,
      experience_level: user.experience_level,
      learning_goals: user.learning_goals,
      current_chapter: user.current_chapter,
      progress: user.progress,
      preferred_language: user.preferred_language,
    });
  } catch (error) {
    console.error('Error fetching user preferences:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Update user preferences
router.put('/preferences', auth.withSession(), async (req, res) => {
  try {
    const user = req.session?.user;
    if (!user) {
      return res.status(401).json({ error: 'Unauthorized' });
    }
    
    const updates = req.body;
    
    // Update user preferences in the database
    await auth.user.updateUser(user.id, updates);
    
    res.json({ message: 'Preferences updated successfully' });
  } catch (error) {
    console.error('Error updating user preferences:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Track chapter progress
router.post('/progress/:chapter', auth.withSession(), async (req, res) => {
  try {
    const user = req.session?.user;
    if (!user) {
      return res.status(401).json({ error: 'Unauthorized' });
    }
    
    const { chapter } = req.params;
    const { progress, timestamp } = req.body;
    
    // Update user's progress
    const updatedProgress = {
      ...user.progress,
      [chapter]: {
        progress,
        timestamp,
        completed: progress === 100
      }
    };
    
    await auth.user.updateUser(user.id, { 
      progress: updatedProgress,
      current_chapter: chapter
    });
    
    res.json({ message: 'Progress updated' });
  } catch (error) {
    console.error('Error updating progress:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

export default router;
```

## Docusaurus Integration

### Custom Login Page

```tsx
// src/pages/login.tsx
import { useState } from 'react';
import { signIn } from 'better-auth/react';
import { useNavigate, useSearchParams } from 'react-router-dom';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  
  const callbackURL = searchParams.get('callbackUrl') || '/dashboard';
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    
    try {
      const result = await signIn.email({
        email,
        password,
        callbackURL,
      });
      
      if (result?.error) {
        setError(result.error);
      }
    } catch (err) {
      setError('Login failed. Please try again.');
      console.error('Login error:', err);
    } finally {
      setIsLoading(false);
    }
  };
  
  return (
    <div className="login-page">
      <div className="login-container">
        <h2>Login to Your Physical AI Account</h2>
        
        {error && <div className="error-message">{error}</div>}
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          
          <button type="submit" disabled={isLoading}>
            {isLoading ? 'Logging in...' : 'Login'}
          </button>
        </form>
        
        <div className="social-login">
          <button onClick={() => signIn.social('google', { callbackURL })}>
            Sign in with Google
          </button>
          <button onClick={() => signIn.social('github', { callbackURL })}>
            Sign in with GitHub
          </button>
        </div>
        
        <p className="signup-link">
          Don't have an account? <a href="/register">Register here</a>
        </p>
      </div>
    </div>
  );
};

export default LoginPage;
```

### Profile Page Component

```tsx
// src/pages/profile.tsx
import { useSession } from 'better-auth/react';
import { useUserProfile } from '../contexts/UserProfileContext';
import { useState } from 'react';

const ProfilePage = () => {
  const { session } = useSession();
  const { preferences, updatePreferences } = useUserProfile();
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState(preferences || {});

  if (!session) {
    return (
      <div className="profile-page">
        <p>Please <a href="/login">log in</a> to view your profile.</p>
      </div>
    );
  }

  const handleSave = async () => {
    await updatePreferences(formData);
    setIsEditing(false);
  };

  return (
    <div className="profile-page">
      <h1>Your Profile</h1>
      
      <div className="profile-info">
        <h2>Basic Information</h2>
        <p><strong>Name:</strong> {session.user.name}</p>
        <p><strong>Email:</strong> {session.user.email}</p>
      </div>
      
      <div className="learning-profile">
        <h2>Learning Profile</h2>
        
        {isEditing ? (
          <div className="edit-form">
            <div className="form-group">
              <label>Background:</label>
              <input
                type="text"
                value={formData.background || ''}
                onChange={(e) => setFormData({...formData, background: e.target.value})}
              />
            </div>
            
            <div className="form-group">
              <label>Experience Level:</label>
              <select
                value={formData.experience_level || 'beginner'}
                onChange={(e) => setFormData({...formData, experience_level: e.target.value})}
              >
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
              </select>
            </div>
            
            <div className="form-group">
              <label>Learning Goals:</label>
              <textarea
                value={JSON.stringify(formData.learning_goals || [])}
                onChange={(e) => setFormData({...formData, learning_goals: JSON.parse(e.target.value)})}
              />
            </div>
            
            <div className="form-actions">
              <button onClick={handleSave}>Save Changes</button>
              <button onClick={() => setIsEditing(false)}>Cancel</button>
            </div>
          </div>
        ) : (
          <div className="profile-display">
            <p><strong>Background:</strong> {preferences?.background}</p>
            <p><strong>Experience:</strong> {preferences?.experience_level}</p>
            <p><strong>Goals:</strong> {preferences?.learning_goals?.join(', ')}</p>
            <p><strong>Current Chapter:</strong> {preferences?.current_chapter}</p>
            <button onClick={() => setIsEditing(true)}>Edit Profile</button>
          </div>
        )}
      </div>
    </div>
  );
};

export default ProfilePage;
```

## Personalized Learning Paths

### Learning Path Component

```tsx
// src/components/LearningPath.tsx
import { useUserProfile } from '../contexts/UserProfileContext';

interface LearningPathProps {
  topic: string;
  content: any[]; // Array of chapter/section objects
}

const LearningPath: React.FC<LearningPathProps> = ({ topic, content }) => {
  const { preferences } = useUserProfile();
  
  // Filter content based on user level
  const filteredContent = content.filter(item => {
    if (!preferences?.experience_level) return true;
    
    if (preferences.experience_level === 'beginner') {
      return item.difficulty === 'beginner' || item.difficulty === 'intermediate';
    } else if (preferences.experience_level === 'intermediate') {
      return item.difficulty !== 'advanced' || item.has_beginner_fallback;
    }
    
    return true; // Advanced users see all
  });
  
  // Sort by progress and prerequisite completion
  const orderedContent = filteredContent.sort((a, b) => {
    const aCompleted = preferences?.progress?.[a.id]?.completed || false;
    const bCompleted = preferences?.progress?.[b.id]?.completed || false;
    
    // Completed items go last
    if (aCompleted && !bCompleted) return 1;
    if (!aCompleted && bCompleted) return -1;
    
    return 0;
  });
  
  return (
    <div className="learning-path">
      <h2>Your Learning Path: {topic}</h2>
      <ol>
        {orderedContent.map((item, index) => {
          const isCompleted = preferences?.progress?.[item.id]?.completed || false;
          const progress = preferences?.progress?.[item.id]?.progress || 0;
          
          return (
            <li key={item.id} className={isCompleted ? 'completed' : 'incomplete'}>
              <a href={item.url}>
                {index + 1}. {item.title}
              </a>
              <div className="progress-bar">
                <div className="progress-fill" style={{ width: `${progress}%` }}></div>
              </div>
              <span className="progress-text">{progress}% complete</span>
            </li>
          );
        })}
      </ol>
    </div>
  );
};

export default LearningPath;
```

## Progress Tracking and Analytics

### Progress Tracking Hook

```ts
// src/hooks/useProgressTracking.ts
import { useState, useEffect } from 'react';
import { useUserProfile } from '../contexts/UserProfileContext';

export const useProgressTracking = (chapterId: string) => {
  const { preferences, updatePreferences } = useUserProfile();
  const [progress, setProgress] = useState(0);
  
  useEffect(() => {
    if (preferences?.progress?.[chapterId]) {
      setProgress(preferences.progress[chapterId].progress || 0);
    }
  }, [chapterId, preferences]);
  
  const updateProgress = async (newProgress: number) => {
    setProgress(newProgress);
    
    if (newProgress > (preferences?.progress?.[chapterId]?.progress || 0)) {
      const updatedProgress = {
        ...preferences?.progress,
        [chapterId]: {
          progress: newProgress,
          timestamp: new Date().toISOString(),
          completed: newProgress === 100
        }
      };
      
      await updatePreferences({ 
        progress: updatedProgress,
        current_chapter: chapterId
      });
    }
  };
  
  const markComplete = () => updateProgress(100);
  
  return { progress, updateProgress, markComplete };
};
```

## Security Considerations

### Secure Authentication Practices

```ts
// src/middleware/auth-guard.ts
import { NextApiRequest, NextApiResponse } from 'next';
import { auth } from '../auth/auth.config';

export const withAuth = (handler: any) => {
  return async (req: NextApiRequest, res: NextApiResponse) => {
    // Verify session
    const session = await auth.getSession({
      headers: req.headers,
    });
    
    if (!session) {
      return res.status(401).json({ error: 'Unauthorized' });
    }
    
    // Add user to request object
    (req as any).user = session.user;
    
    return handler(req, res);
  };
};
```

## Privacy and Data Protection

### Data Handling Best Practices

```ts
// src/utils/data-privacy.ts
export class DataPrivacy {
  static sanitizeUserData(userData: any) {
    // Remove sensitive information before logging or processing
    return {
      id: userData.id,
      background: userData.background,
      experience_level: userData.experience_level,
      learning_goals: userData.learning_goals,
      current_chapter: userData.current_chapter,
      progress: userData.progress,
      preferred_language: userData.preferred_language,
      // Do not include email, name, or other PII in analytics
    };
  }
  
  static async anonymizeForAnalytics(userData: any) {
    // Create anonymized version for analytics
    return {
      user_id: this.hash(userData.id), // Hashed ID
      background: userData.background,
      experience_level: userData.experience_level,
      learning_path: userData.learning_goals,
      progress_stats: this.getProgressStats(userData.progress),
    };
  }
  
  private static hash(str: string): string {
    // Simple hash function (use crypto in production)
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
    }
    return Math.abs(hash).toString(16);
  }
  
  private static getProgressStats(progress: any) {
    // Extract aggregate stats without individual chapter data
    const completed = Object.values(progress).filter((p: any) => p.completed).length;
    const total = Object.keys(progress).length;
    return {
      overall_completion: total > 0 ? Math.round((completed / total) * 100) : 0,
      completion_rate: completed,
      total_chapters: total
    };
  }
}
```

## Summary

This authentication and personalization system provides:

- ✅ Better Auth integration for secure user authentication
- ✅ Collection of user background and experience information
- ✅ Personalized content delivery based on user profile
- ✅ Progress tracking and learning path customization
- ✅ Privacy-conscious data handling
- ✅ Docusaurus-friendly implementation
- ✅ TypeScript support throughout

## Implementation Steps

1. **Setup Better Auth**: Configure authentication with your database
2. **Create Registration Flow**: Collect user background information
3. **Implement Context System**: Manage user preferences in frontend
4. **Build Personalization Logic**: Filter content based on user profile
5. **Add Progress Tracking**: Monitor user learning progress
6. **Test Security**: Ensure proper authentication and authorization
7. **Deploy**: Set up in production environment

## Next Steps

- Implement the multilingual support system
- Integrate with the RAG chatbot for personalized responses
- Add Claude Code subagents for automated content personalization
- Connect to the full Physical AI textbook content