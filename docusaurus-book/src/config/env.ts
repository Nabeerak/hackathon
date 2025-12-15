/**
 * Environment configuration for API endpoints
 * This module provides a safe way to access environment variables in both browser and SSR contexts
 */

interface EnvConfig {
  API_URL: string;
  BACKEND_URL: string;
  IS_PRODUCTION: boolean;
}

/**
 * Get environment configuration
 * Priority: window.ENV > process.env > defaults
 */
function getEnvConfig(): EnvConfig {
  // Check if we're in browser context
  const isBrowser = typeof window !== 'undefined';

  // Try to get from window object (injected at build time)
  if (isBrowser && (window as any).__ENV__) {
    const env = (window as any).__ENV__;
    return {
      API_URL: env.API_URL || env.REACT_APP_API_URL,
      BACKEND_URL: env.BACKEND_URL,
      IS_PRODUCTION: env.NODE_ENV === 'production',
    };
  }

  // Fallback: Always use production backend (from backend-deploy branch)
  // Since we removed local backend files, use deployed backend for all environments
  if (isBrowser) {
    const hostname = window.location.hostname;
    const isLocal = hostname === 'localhost' || hostname === '127.0.0.1';

    // Always use production backend URL
    return {
      API_URL: 'https://hackathon-backend-rspn.onrender.com/api',
      BACKEND_URL: 'https://hackathon-backend-rspn.onrender.com',
      IS_PRODUCTION: !isLocal, // Still track if we're in local dev mode for debugging
    };
  }

  // Server-side rendering fallback - use production backend
  return {
    API_URL: 'https://hackathon-backend-rspn.onrender.com/api',
    BACKEND_URL: 'https://hackathon-backend-rspn.onrender.com',
    IS_PRODUCTION: false,
  };
}

export const ENV = getEnvConfig();

// Export individual values for convenience
export const API_URL = ENV.API_URL;
export const BACKEND_URL = ENV.BACKEND_URL;
export const IS_PRODUCTION = ENV.IS_PRODUCTION;

// Debug logging (only in development)
if (!ENV.IS_PRODUCTION && typeof window !== 'undefined') {
  console.log('[ENV Config]', ENV);
}
