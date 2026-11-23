import { apiClient } from './client';

export interface AdminAnalyticsData {
  kpis: {
    total_users: number;
    total_conversations: number;
    total_queries: number;
    emergency_alerts: number;
    satisfaction_percentage: number;
    average_rating: number;
    total_feedbacks: number;
  };
  intent_distribution: Array<{ name: string; value: number }>;
  top_topics: Array<{ topic: string; queries: number }>;
  activity_trend: Array<{ date: string; queries: number; emergencies: number }>;
  ml_model_metrics: {
    accuracy?: number;
    macro_precision?: number;
    macro_recall?: number;
    macro_f1?: number;
    weighted_f1?: number;
    test_sample_count?: number;
    train_sample_count?: number;
    intent_classes?: string[];
    confusion_matrix?: number[][];
    classification_report?: any;
  };
}

export const analyticsApi = {
  getDashboardAnalytics: async (): Promise<AdminAnalyticsData> => {
    const res = await apiClient.get('/analytics/dashboard/');
    return res.data;
  },
};

