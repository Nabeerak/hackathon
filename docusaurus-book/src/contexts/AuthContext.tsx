import React, { createContext, useContext, ReactNode, useState, useEffect, useMemo } from 'react';
import { authClient, checkBackendHealth } from '../lib/auth-client';
import { BACKEND_URL } from '../config/env';

const { useSession, signIn, signUp, signOut } = authClient;

interface AuthContextType {
  user: any;
  session: any;
  isAuthenticated: boolean;
  isPending: boolean;
  backendReady: boolean;
  backendError: string | null;
  signIn: typeof signIn.email;
  signUp: typeof signUp.email;
  signOut: typeof signOut;
  updateProfile: (updates: any) => Promise<void>;
  refreshSession: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [isClient, setIsClient] = useState(false);
  const [backendReady, setBackendReady] = useState(false);
  const [backendError, setBackendError] = useState<string | null>(null);

  // Always call hooks unconditionally
  const sessionResult = useSession();
  const sessionData = sessionResult?.data || null;
  const isPending = sessionResult?.isPending ?? true;

  // Initialize backend on mount
  useEffect(() => {
    setIsClient(true);

    // Check backend health
    const initializeBackend = async () => {
      if (typeof window === 'undefined') return;

      try {
        const data = await checkBackendHealth();

        if (data.status === 'healthy' || data.status === 'degraded') {
          setBackendReady(true);
          setBackendError(null);
          console.log('Backend initialized:', data);
        } else {
          setBackendError('Backend is not ready');
        }
      } catch (error) {
        console.error('Backend initialization failed:', error);
        setBackendError(error instanceof Error ? error.message : 'Backend connection failed');
        setBackendReady(false);
      }
    };

    initializeBackend();
  }, []);

  const user = useMemo(() => sessionData?.user || null, [sessionData?.user]);
  const isAuthenticated = useMemo(() => isClient && !!sessionData?.user, [isClient, sessionData?.user]);

  const updateProfile = async (updates: any) => {
    const response = await fetch(`${BACKEND_URL}/api/auth/profile`, {
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

  const contextValue = useMemo(
    () => ({
      user,
      session: sessionData,
      isAuthenticated,
      isPending,
      backendReady,
      backendError,
      signIn: signIn.email,
      signUp: signUp.email,
      signOut,
      updateProfile,
      refreshSession,
    }),
    [user, sessionData, isAuthenticated, isPending, backendReady, backendError]
  );

  return (
    <AuthContext.Provider value={contextValue}>
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
