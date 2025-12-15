import { createAuthClient } from "better-auth/react";
import { BACKEND_URL } from "../config/env";

// Point better-auth client to FastAPI backend
// Better-auth will append /api/auth to this baseURL

export const authClient = createAuthClient({
  baseURL: BACKEND_URL,
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
  const response = await fetch(`${BACKEND_URL}/api/health`, {
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
