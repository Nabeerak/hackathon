const API_BASE_URL = (typeof process !== 'undefined' && process.env?.REACT_APP_API_URL) || '/api';

export interface Conversation {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
  message_count: number;
}

export interface Message {
  id: string;
  role: string;
  content: string;
  timestamp: string;
}

export interface ConversationDetail {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
  messages: Message[];
}

export interface CreateConversationRequest {
  title?: string;
}

export interface ConversationExportData {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
  message_count: number;
  messages: Message[];
}

export class ConversationAPI {
  private baseURL: string;

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL;
  }

  async getConversations(userId: number = 1, skip: number = 0, limit: number = 20): Promise<Conversation[]> {
    const response = await fetch(`${this.baseURL}/conversations?user_id=${userId}&skip=${skip}&limit=${limit}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include', // Include cookies for authentication
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch conversations: ${response.statusText}`);
    }

    return response.json();
  }

  async getConversation(conversationId: string, userId: number = 1): Promise<ConversationDetail> {
    const response = await fetch(`${this.baseURL}/conversations/${conversationId}?user_id=${userId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include', // Include cookies for authentication
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch conversation: ${response.statusText}`);
    }

    return response.json();
  }

  async createConversation(request: CreateConversationRequest, userId: number = 1): Promise<Conversation> {
    const response = await fetch(`${this.baseURL}/conversations?user_id=${userId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include', // Include cookies for authentication
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`Failed to create conversation: ${response.statusText}`);
    }

    return response.json();
  }

  async deleteConversation(conversationId: string, userId: number = 1): Promise<void> {
    const response = await fetch(`${this.baseURL}/conversations/${conversationId}?user_id=${userId}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include', // Include cookies for authentication
    });

    if (!response.ok) {
      throw new Error(`Failed to delete conversation: ${response.statusText}`);
    }
  }

  async searchConversations(query: string, userId: number = 1): Promise<Conversation[]> {
    const response = await fetch(`${this.baseURL}/conversations/search?query=${encodeURIComponent(query)}&user_id=${userId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include', // Include cookies for authentication
    });

    if (!response.ok) {
      throw new Error(`Failed to search conversations: ${response.statusText}`);
    }

    return response.json();
  }

  async exportConversation(conversationId: string, userId: number = 1): Promise<ConversationExportData> {
    const response = await fetch(`${this.baseURL}/conversations/${conversationId}/export?user_id=${userId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include', // Include cookies for authentication
    });

    if (!response.ok) {
      throw new Error(`Failed to export conversation: ${response.statusText}`);
    }

    return response.json();
  }

  async downloadConversation(conversationId: string, filename: string): Promise<void> {
    const response = await fetch(`${this.baseURL}/conversations/${conversationId}/export`, {
      method: 'GET',
      credentials: 'include', // Include cookies for authentication
    });

    if (!response.ok) {
      throw new Error(`Failed to download conversation: ${response.statusText}`);
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename || `conversation_${conversationId}.json`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  }
}

export const conversationAPI = new ConversationAPI();