import { createAuthClient } from "better-auth/react";

// Point better-auth client to FastAPI backend (port 8000)
// Better-auth will append /api/auth to this baseURL
// Docusaurus doesn't support REACT_APP_ env vars, so we detect environment by hostname
const getBaseURL = () => {
  if (typeof window === 'undefined') {
    // Server-side rendering
    return "http://localhost:8000";
  }

  // Client-side
  const hostname = window.location.hostname;
  if (hostname === 'localhost' || hostname === '127.0.0.1') {
    return "http://localhost:8000";
  } else {
    // Production - adjust this URL for your deployed backend
    return "https://hackathon-docusaurus.onrender.com"; 

  }
};

export const authClient = createAuthClient({
  baseURL: getBaseURL(),
  fetchOptions: {
    credentials: 'include',
    mode: 'cors',
    onRequest: async (ctx) => {
      // Add session token from localStorage to headers as fallback
      const token = localStorage.getItem('auth_session_token');
      if (token) {
        ctx.headers.set('Authorization', `Bearer ${token}`);
      }
      return ctx;
    }
  }
});

export const { signIn, signUp, signOut, useSession } = authClient;

/**
 * Check backend health and initialization status
 * @returns Promise with health status or throws error
 */
export async function checkBackendHealth() {
  const baseURL = getBaseURL();

  const response = await fetch(`${baseURL}/api/health`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error(`Backend health check failed: ${response.status}`);
  }

  const data = await response.json();
  return data;
}
