
export interface Source {
  id: string;
  title: string;
  url: string;
  snippet: string;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: Source[];
  isError?: boolean;
}

export interface RagApiResponse {
  answer: string;
  sources: Source[];
}