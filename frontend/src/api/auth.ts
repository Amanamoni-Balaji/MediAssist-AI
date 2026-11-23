import { apiClient } from './client';

export interface UserProfile {
  phone: string;
  date_of_birth: string | null;
  gender: string;
  blood_group: string;
  emergency_contact: string;
  medical_disclaimer_accepted: boolean;
  bio: string;
  created_at: string;
  updated_at: string;
}

export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  is_staff: boolean;
  is_superuser: boolean;
  profile: UserProfile;
}

export const authApi = {
  login: async (credentials: { username: string; password: string }) => {
    const res = await apiClient.post('/auth/login/', credentials);
    return res.data;
  },

  register: async (data: any) => {
    const res = await apiClient.post('/auth/register/', data);
    return res.data;
  },

  getProfile: async (): Promise<User> => {
    const res = await apiClient.get('/auth/profile/');
    return res.data;
  },

  updateProfile: async (data: any): Promise<User> => {
    const res = await apiClient.put('/auth/profile/', data);
    return res.data;
  },

  changePassword: async (data: { old_password: string; new_password: string }) => {
    const res = await apiClient.post('/auth/change-password/', data);
    return res.data;
  },
};

