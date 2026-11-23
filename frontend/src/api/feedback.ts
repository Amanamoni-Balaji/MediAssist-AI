import { apiClient } from './client';

export interface FeedbackData {
  conversation?: string;
  message?: string;
  is_helpful: boolean;
  rating: number;
  comment?: string;
}

export const feedbackApi = {
  submit: async (data: FeedbackData) => {
    const res = await apiClient.post('/feedback/submit/', data);
    return res.data;
  },

  list: async () => {
    const res = await apiClient.get('/feedback/list/');
    return res.data;
  },
};

