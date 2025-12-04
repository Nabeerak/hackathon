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
    return "https://your-backend-url.com";
  }
};

export const authClient = createAuthClient({
  baseURL: getBaseURL(),
});

export const { signIn, signUp, signOut, useSession } = authClient;
