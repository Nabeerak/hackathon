import { API_URL } from '../config/env';

const API_BASE_URL = API_URL;

export interface ChatRequest {
  conversation_id?: number;
  message: string;
  selected_text?: string;
  user_id?: number;
}

export interface ChatResponse {
  message: string;
  conversation_id: number;
  sources: string[];
  timestamp: string;
  processing_time: number;
  off_topic?: boolean;
  metadata?: {
    processing_time?: number;
    sources_count?: number;
    timestamp?: string;
    client_ip?: string;
    [key: string]: any;
  };
}

export class ChatAPI {
  private baseURL: string;

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL;
  }

  async sendMessage(request: ChatRequest): Promise<ChatResponse> {
    // Get the session token stored by better-auth
    const sessionToken = localStorage.getItem('auth_session_token');

    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };

    // Add Authorization header if we have a session token
    if (sessionToken) {
      headers['Authorization'] = `Bearer ${sessionToken}`;
    }

    const response = await fetch(`${this.baseURL}/chat`, {
      method: 'POST',
      headers,
      credentials: 'include', // Include cookies for authentication
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      if (response.status === 429) {
        throw new Error('Rate limit exceeded. Please try again later.');
      } else if (response.status === 400) {
        const errorData = await response.json();
        throw new Error(`Validation error: ${errorData.detail || response.statusText}`);
      } else if (response.status === 500) {
        throw new Error('Internal server error. Please try again later.');
      }
      throw new Error(`Failed to send message: ${response.statusText}`);
    }

    return response.json();
  }
}

export const chatAPI = new ChatAPI();
