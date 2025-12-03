const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

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

  async getConversations(skip: number = 0, limit: number = 20): Promise<Conversation[]> {
    const response = await fetch(`${this.baseURL}/conversations?skip=${skip}&limit=${limit}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch conversations: ${response.statusText}`);
    }

    return response.json();
  }

  async getConversation(conversationId: string): Promise<ConversationDetail> {
    const response = await fetch(`${this.baseURL}/conversations/${conversationId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch conversation: ${response.statusText}`);
    }

    return response.json();
  }

  async createConversation(request: CreateConversationRequest): Promise<Conversation> {
    const response = await fetch(`${this.baseURL}/conversations`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`Failed to create conversation: ${response.statusText}`);
    }

    return response.json();
  }

  async deleteConversation(conversationId: string): Promise<void> {
    const response = await fetch(`${this.baseURL}/conversations/${conversationId}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`Failed to delete conversation: ${response.statusText}`);
    }
  }

  async searchConversations(query: string): Promise<Conversation[]> {
    const response = await fetch(`${this.baseURL}/conversations/search?query=${encodeURIComponent(query)}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`Failed to search conversations: ${response.statusText}`);
    }

    return response.json();
  }

  async exportConversation(conversationId: string): Promise<ConversationExportData> {
    const response = await fetch(`${this.baseURL}/conversations/${conversationId}/export`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`Failed to export conversation: ${response.statusText}`);
    }

    return response.json();
  }

  async downloadConversation(conversationId: string, filename: string): Promise<void> {
    const response = await fetch(`${this.baseURL}/conversations/${conversationId}/export`, {
      method: 'GET',
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