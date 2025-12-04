import React, { createContext, useContext, ReactNode, useState, useEffect } from 'react';
import { authClient } from '../lib/auth-client';

const { useSession, signIn, signUp, signOut } = authClient;

interface AuthContextType {
  user: any;
  session: any;
  isAuthenticated: boolean;
  isPending: boolean;
  signIn: typeof signIn.email;
  signUp: typeof signUp.email;
  signOut: typeof signOut;
  updateProfile: (updates: any) => Promise<void>;
  refreshSession: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [isClient, setIsClient] = useState(false);

  // Always call hooks unconditionally
  const sessionResult = useSession();
  const sessionData = sessionResult?.data || null;
  const isPending = sessionResult?.isPending ?? true;

  useEffect(() => {
    setIsClient(true);
  }, []);

  const user = sessionData?.user || null;
  const isAuthenticated = isClient && !!sessionData?.user;

  const updateProfile = async (updates: any) => {
    const baseURL = typeof window !== 'undefined' &&
      (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
      ? 'http://localhost:8000'
      : 'https://your-backend-url.com';

    const response = await fetch(`${baseURL}/api/auth/profile`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
      body: JSON.stringify(updates),
    });

    if (!response.ok) {
      const data = await response.json();
      throw new Error(data.error?.message || 'Failed to update profile');
    }

    const result = await response.json();
    if (result.error) {
      throw new Error(result.error.message);
    }

    // Refresh session to get updated user data
    await refreshSession();
  };

  const refreshSession = async () => {
    // Trigger a session refresh by calling the useSession hook's refetch if available
    // For now, we'll rely on the session hook to auto-refresh
    window.location.reload();
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        session: sessionData,
        isAuthenticated,
        isPending,
        signIn: signIn.email,
        signUp: signUp.email,
        signOut,
        updateProfile,
        refreshSession,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
