import { apiClient } from './client';

export interface ChatMessage {
  id: string;
  conversation: string;
  sender: 'user' | 'assistant';
  text: string;
  intent?: string;
  confidence?: number;
  entities?: {
    symptoms?: string[];
    conditions?: string[];
    body_parts?: string[];
    severity?: string[];
    durations?: string[];
    emergency_flag?: boolean;
  };
  is_emergency?: boolean;
  matched_topic?: string | null;
  suggested_questions?: string[];
  created_at: string;
}

export interface Conversation {
  id: string;
  user: number | null;
  title: string;
  is_active: boolean;
  message_count?: number;
  last_message?: {
    text: string;
    sender: string;
    created_at: string;
  } | null;
  created_at: string;
  updated_at: string;
}

export interface ConversationDetail extends Conversation {
  messages: ChatMessage[];
}

export interface SendMessageResponse {
  conversation_id: string;
  conversation_title: string;
  user_message: ChatMessage;
  assistant_message: ChatMessage;
  nlp_metadata: {
    intent: string;
    confidence: number;
    entities: any;
    is_emergency: boolean;
    matched_topic: string | null;
    suggested_questions: string[];
    similarity_score: number;
  };
}

export const chatApi = {
  getConversations: async (): Promise<Conversation[]> => {
    const res = await apiClient.get('/chat/conversations/');
    return res.data;
  },

  getConversation: async (id: string): Promise<ConversationDetail> => {
    const res = await apiClient.get(`/chat/conversations/${id}/`);
    return res.data;
  },

  createConversation: async (title?: string): Promise<Conversation> => {
    const res = await apiClient.post('/chat/conversations/', { title });
    return res.data;
  },

  deleteConversation: async (id: string) => {
    const res = await apiClient.delete(`/chat/conversations/${id}/`);
    return res.data;
  },

  clearConversation: async (id: string) => {
    const res = await apiClient.post(`/chat/conversations/${id}/clear/`);
    return res.data;
  },

  sendMessage: async (message: string, conversation_id?: string): Promise<SendMessageResponse> => {
    const res = await apiClient.post('/chat/chat/send/', {
      message,
      conversation_id,
    });
    return res.data;
  },
};

