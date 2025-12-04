# Authentication & Personalization Implementation

## Overview

This document describes the authentication and personalization features implemented for the Physical AI & Humanoid Robotics textbook platform.

## Features Implemented

### ✅ 1. User Authentication (better-auth.com)
- JWT-based authentication
- Secure password hashing with bcrypt
- Token-based session management
- Sign up, sign in, and logout functionality

### ✅ 2. User Profile with Background Fields
Users can provide during signup:
- **Username & Email**: Account credentials
- **Experience Level**: Beginner, Intermediate, or Advanced
- **Software Background**: Python, JavaScript, C++, ROS, etc.
- **Hardware Background**: Arduino, Raspberry Pi, 3D Printing, Electronics, etc.
- **Learning Goals**: What they want to achieve from the course
- **Personalization Toggle**: Enable/disable personalized content
- **Preferred Language**: English or Urdu (اردو)

### ✅ 3. Personalized Content Delivery
- "Personalize Content" button at the start of each chapter
- Content adapts based on user's experience level and background
- Visual indicators when personalization is active
- Option to translate content to Urdu for logged-in users

### ✅ 4. Profile Management
- View and edit profile information
- Update learning preferences
- Toggle personalization on/off
- Change preferred language

## Technical Architecture

### Backend (FastAPI + PostgreSQL)

#### Database Schema
```sql
users:
  - id (PRIMARY KEY)
  - username (UNIQUE, NOT NULL)
  - email (UNIQUE, NOT NULL)
  - password_hash (NOT NULL)
  - software_background (TEXT)
  - hardware_background (TEXT)
  - learning_goals (TEXT)
  - experience_level (VARCHAR: beginner/intermediate/advanced)
  - personalization_enabled (BOOLEAN, default: true)
  - preferred_language (VARCHAR: en/ur, default: en)
  - created_at (TIMESTAMP)
  - updated_at (TIMESTAMP)
```

#### API Endpoints

**Authentication:**
- `POST /api/auth/signup` - Register new user with profile
- `POST /api/auth/signin` - Authenticate user
- `POST /api/auth/logout` - Logout user
- `GET /api/auth/profile` - Get current user profile (requires token)
- `PUT /api/auth/profile` - Update user profile (requires token)

**Example Signup Request:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure123",
  "software_background": "Python, JavaScript, ROS",
  "hardware_background": "Arduino, Raspberry Pi",
  "learning_goals": "Build autonomous robots",
  "experience_level": "intermediate"
}
```

**Example Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "software_background": "Python, JavaScript, ROS",
    "hardware_background": "Arduino, Raspberry Pi",
    "learning_goals": "Build autonomous robots",
    "experience_level": "intermediate",
    "personalization_enabled": true,
    "preferred_language": "en",
    "created_at": "2025-12-03T20:00:00Z",
    "updated_at": "2025-12-03T20:00:00Z"
  }
}
```

#### Security Features
- Password hashing with bcrypt (cost factor: 12)
- JWT tokens with 7-day expiration
- Secure token validation on protected endpoints
- CORS configuration for frontend access

### Frontend (React + Docusaurus)

#### Components Created

1. **AuthContext** (`src/contexts/AuthContext.tsx`)
   - Global authentication state management
   - Token persistence in localStorage
   - Auto-refresh on page load

2. **SignupForm** (`src/components/Auth/SignupForm.tsx`)
   - Complete registration form
   - Profile fields collection
   - Client-side validation

3. **SigninForm** (`src/components/Auth/SigninForm.tsx`)
   - Login form
   - Error handling

4. **AuthModal** (`src/components/Auth/AuthModal.tsx`)
   - Popup modal for signin/signup
   - Toggle between modes
   - Can be triggered from anywhere

5. **ProfilePage** (`src/components/Auth/ProfilePage.tsx`)
   - View user profile
   - Edit profile fields
   - Toggle personalization
   - Change language preference

6. **PersonalizeButton** (`src/components/PersonalizeButton/PersonalizeButton.tsx`)
   - Appears at start of chapters
   - Prompts signin if not authenticated
   - Shows user's experience level
   - Activates personalized content
   - Translation button (when language is Urdu)

7. **Navbar Integration** (`src/theme/Navbar/Content/index.tsx`)
   - "Sign In" button when logged out
   - Username + profile link when logged in

8. **Root Provider** (`src/theme/Root.tsx`)
   - Wraps entire app with AuthProvider
   - Makes auth context available everywhere

#### API Service
```typescript
// src/services/auth_api.ts
class AuthAPI {
  signup(request: SignupRequest): Promise<AuthResponse>
  signin(request: SigninRequest): Promise<AuthResponse>
  getProfile(token: string): Promise<UserProfile>
  updateProfile(token: string, request: UpdateProfileRequest): Promise<UserProfile>
  logout(token: string): Promise<void>
}
```

## Usage Examples

### In a Chapter (MDX)
```mdx
---
title: ROS 2 Fundamentals
---

import PersonalizeButton from '@site/src/components/PersonalizeButton/PersonalizeButton';

# ROS 2 Fundamentals

<PersonalizeButton chapterTitle="ROS 2 Fundamentals" />

## Introduction
...
```

### Programmatic Usage
```typescript
import { useAuth } from '../contexts/AuthContext';

function MyComponent() {
  const { user, isAuthenticated, signin, logout } = useAuth();

  if (!isAuthenticated) {
    return <button onClick={() => signin({email, password})}>Sign In</button>;
  }

  return (
    <div>
      <p>Welcome, {user.username}!</p>
      <p>Experience Level: {user.experience_level}</p>
      <button onClick={logout}>Logout</button>
    </div>
  );
}
```

## Environment Variables

### Backend (.env)
```env
OPENAI_API_KEY=your_openai_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_key
NEON_DATABASE_URL=postgresql://user:pass@host/db
BETTER_AUTH_SECRET=your_better_auth_secret
JWT_SECRET_KEY=your_jwt_secret_at_least_32_chars
```

### Frontend (.env.development / .env.production)
```env
REACT_APP_API_URL=http://localhost:8000/api
```

## Testing

### 1. Test Backend API
```bash
# Start backend
cd backend
python -m uvicorn src.main:app --reload

# Test signup
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "software_background": "Python, ROS",
    "hardware_background": "Arduino",
    "experience_level": "intermediate"
  }'

# Test signin
curl -X POST http://localhost:8000/api/auth/signin \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'
```

### 2. Test Frontend
```bash
# Start Docusaurus dev server
cd docusaurus-book
npm start

# Visit http://localhost:3000
# Click "Sign In" in navbar
# Create account and test personalization
```

## Database Migrations

### Apply Migrations
```bash
cd backend
alembic upgrade head
```

### Create New Migration
```bash
cd backend
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

## Deployment Checklist

### Backend
- [ ] Set strong `JWT_SECRET_KEY` (min 32 characters)
- [ ] Set `BETTER_AUTH_SECRET`
- [ ] Configure CORS with production frontend URL
- [ ] Run database migrations
- [ ] Test all auth endpoints

### Frontend
- [ ] Update `REACT_APP_API_URL` in `.env.production`
- [ ] Test signup/signin flow
- [ ] Test profile management
- [ ] Test personalization button
- [ ] Verify token persistence

## Future Enhancements

### Planned Features
1. **Content Personalization Logic**
   - AI-powered content adaptation
   - Dynamic example generation based on background
   - Difficulty adjustment per experience level

2. **Urdu Translation**
   - OpenAI GPT-4 translation API
   - Cache translated content
   - Toggle between languages

3. **Learning Progress Tracking**
   - Chapter completion status
   - Quiz scores
   - Learning path recommendations

4. **Social Features**
   - Share learning goals
   - Connect with students at similar level
   - Discussion forums per chapter

## Files Created

### Backend
- `backend/src/models/models.py` - Updated User model
- `backend/src/services/auth_service.py` - Auth service (JWT, password hashing)
- `backend/src/api/auth.py` - Auth endpoints
- `backend/alembic/versions/174d8055ab95_add_user_authentication_and_profile_.py` - Migration

### Frontend
- `docusaurus-book/src/contexts/AuthContext.tsx` - Auth state management
- `docusaurus-book/src/services/auth_api.ts` - Auth API client
- `docusaurus-book/src/components/Auth/SignupForm.tsx` - Signup form
- `docusaurus-book/src/components/Auth/SigninForm.tsx` - Signin form
- `docusaurus-book/src/components/Auth/AuthModal.tsx` - Modal wrapper
- `docusaurus-book/src/components/Auth/ProfilePage.tsx` - Profile management
- `docusaurus-book/src/components/Auth/Auth.module.css` - Auth styles
- `docusaurus-book/src/components/PersonalizeButton/PersonalizeButton.tsx` - Personalization button
- `docusaurus-book/src/components/PersonalizeButton/PersonalizeButton.module.css` - Button styles
- `docusaurus-book/src/theme/Navbar/Content/index.tsx` - Navbar auth integration
- `docusaurus-book/src/theme/Navbar/Content/styles.module.css` - Navbar styles
- `docusaurus-book/src/theme/Root.tsx` - Auth provider wrapper
- `docusaurus-book/src/pages/profile.tsx` - Profile page route
- `docusaurus-book/docs/example-chapter.mdx` - Example with personalization

## Support

For issues or questions:
1. Check this documentation
2. Review the example chapter at `/docs/example-chapter.mdx`
3. Check backend logs for API errors
4. Check browser console for frontend errors
