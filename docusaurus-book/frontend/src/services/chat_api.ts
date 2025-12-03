const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

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
    const response = await fetch(`${this.baseURL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
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
