import { apiClient } from './client';

export interface MedicalTopic {
  id: number;
  topic: string;
  slug: string;
  category: string;
  description: string;
  symptoms: string[];
  causes: string;
  prevention: string;
  when_to_seek_care: string;
  references: Array<{ source: string; title: string; url: string }>;
  keywords: string;
  created_at: string;
  updated_at: string;
}

export interface SymptomAnalysisResult {
  is_emergency: boolean;
  emergency_message: string | null;
  input_symptoms: string[];
  identified_conditions: Array<{
    topic: string;
    slug: string;
    category: string;
    description: string;
    matching_symptoms: string[];
    all_associated_symptoms: string[];
    when_to_seek_care: string;
    overlap_score: number;
  }>;
  general_guidance: string;
  recommended_actions: string[];
  disclaimer: string;
}

export const medicalApi = {
  getTopics: async (search?: string, category?: string): Promise<MedicalTopic[]> => {
    const params: any = {};
    if (search) params.search = search;
    if (category) params.category = category;
    const res = await apiClient.get('/medical/topics/', { params });
    return res.data;
  },

  getTopic: async (slug: string): Promise<MedicalTopic> => {
    const res = await apiClient.get(`/medical/topics/${slug}/`);
    return res.data;
  },

  getSymptomDictionary: async (): Promise<{ symptoms: string[]; categories: string[] }> => {
    const res = await apiClient.get('/medical/symptoms/dictionary/');
    return res.data;
  },

  analyzeSymptoms: async (symptoms: string[], free_text?: string): Promise<SymptomAnalysisResult> => {
    const res = await apiClient.post('/medical/symptoms/analyze/', {
      symptoms,
      free_text,
    });
    return res.data;
  },
};

