const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

export interface SearchResponseItem {
  id: string;
  content: string;
  source: string;
  score: number;
}

export interface SearchResponse {
  results: SearchResponseItem[];
  total: number;
}

export class SearchAPI {
  private baseURL: string;

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL;
  }

  async search(query: string, limit: number = 10): Promise<SearchResponse> {
    const response = await fetch(`${this.baseURL}/search?query=${encodeURIComponent(query)}&limit=${limit}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`Failed to search: ${response.statusText}`);
    }

    return response.json();
  }
}

export const searchAPI = new SearchAPI();