import axios, { AxiosInstance, AxiosResponse } from 'axios';
import { 
  ApiResponse, 
  DashboardSummary, 
  Course, 
  CreateCourseData,
  Transaction,
  CreateTransactionData,
  TeamMember,
  CreateTeamMemberData,
  Campaign,
  CreateCampaignData,
  Student,
  CreateStudentData,
  Partner,
  CreatePartnerData,
  TelegramGroup,
  TelegramStats,
  ContentRequest,
  GeneratedContent
} from '@/types';

class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: '/api',
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor
    this.api.interceptors.request.use(
      (config) => {
        // Add auth token if available
        const token = localStorage.getItem('authToken');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.api.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          // Handle unauthorized access
          localStorage.removeItem('authToken');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // Generic request methods
  private async get<T>(url: string): Promise<T> {
    const response: AxiosResponse<T> = await this.api.get(url);
    return response.data;
  }

  private async post<T>(url: string, data?: any): Promise<T> {
    const response: AxiosResponse<T> = await this.api.post(url, data);
    return response.data;
  }

  private async put<T>(url: string, data?: any): Promise<T> {
    const response: AxiosResponse<T> = await this.api.put(url, data);
    return response.data;
  }

  private async delete<T>(url: string): Promise<T> {
    const response: AxiosResponse<T> = await this.api.delete(url);
    return response.data;
  }

  // Authentication
  async login(username: string, password: string): Promise<ApiResponse<any>> {
    try {
      const response = await this.post<ApiResponse<any>>('/login', {
        username,
        password
      });
      return response;
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.message || 'Login failed'
      };
    }
  }

  // Dashboard
  async getDashboardSummary(): Promise<DashboardSummary> {
    return this.get<DashboardSummary>('/owner/summary');
  }

  // Courses
  async getCourses(): Promise<Course[]> {
    return this.get<Course[]>('/courses');
  }

  async createCourse(data: CreateCourseData): Promise<Course> {
    return this.post<Course>('/courses', data);
  }

  async updateCourse(id: number, data: Partial<CreateCourseData>): Promise<Course> {
    return this.put<Course>(`/courses/${id}`, data);
  }

  async deleteCourse(id: number): Promise<void> {
    return this.delete<void>(`/courses/${id}`);
  }

  // Transactions
  async getTransactions(): Promise<Transaction[]> {
    return this.get<Transaction[]>('/transactions');
  }

  async createTransaction(data: CreateTransactionData): Promise<Transaction> {
    return this.post<Transaction>('/transactions', data);
  }

  // Team
  async getTeamMembers(): Promise<TeamMember[]> {
    return this.get<TeamMember[]>('/team');
  }

  async createTeamMember(data: CreateTeamMemberData): Promise<TeamMember> {
    return this.post<TeamMember>('/team', data);
  }

  async updateTeamMember(id: number, data: Partial<CreateTeamMemberData>): Promise<TeamMember> {
    return this.put<TeamMember>(`/team/${id}`, data);
  }

  async deleteTeamMember(id: number): Promise<void> {
    return this.delete<void>(`/team/${id}`);
  }

  // Campaigns
  async getCampaigns(): Promise<Campaign[]> {
    return this.get<Campaign[]>('/campaigns');
  }

  async createCampaign(data: CreateCampaignData): Promise<Campaign> {
    return this.post<Campaign>('/campaigns', data);
  }

  async updateCampaign(id: number, data: Partial<CreateCampaignData>): Promise<Campaign> {
    return this.put<Campaign>(`/campaigns/${id}`, data);
  }

  async deleteCampaign(id: number): Promise<void> {
    return this.delete<void>(`/campaigns/${id}`);
  }

  // Students
  async getStudents(): Promise<Student[]> {
    return this.get<Student[]>('/students');
  }

  async createStudent(data: CreateStudentData): Promise<Student> {
    return this.post<Student>('/students', data);
  }

  async updateStudent(id: number, data: Partial<CreateStudentData>): Promise<Student> {
    return this.put<Student>(`/students/${id}`, data);
  }

  async deleteStudent(id: number): Promise<void> {
    return this.delete<void>(`/students/${id}`);
  }

  // Partners
  async getPartners(): Promise<Partner[]> {
    return this.get<Partner[]>('/partners');
  }

  async createPartner(data: CreatePartnerData): Promise<Partner> {
    return this.post<Partner>('/partners', data);
  }

  async updatePartner(id: number, data: Partial<CreatePartnerData>): Promise<Partner> {
    return this.put<Partner>(`/partners/${id}`, data);
  }

  async deletePartner(id: number): Promise<void> {
    return this.delete<void>(`/partners/${id}`);
  }

  // Telegram Bot
  async getTelegramGroups(): Promise<TelegramGroup[]> {
    return this.get<TelegramGroup[]>('/telegram/groups');
  }

  async createTelegramGroup(data: { name: string; chat_id: string }): Promise<TelegramGroup> {
    return this.post<TelegramGroup>('/telegram/groups', data);
  }

  async deleteTelegramGroup(id: number): Promise<void> {
    return this.delete<void>(`/telegram/groups/${id}`);
  }

  async getTelegramStats(): Promise<TelegramStats> {
    return this.get<TelegramStats>('/telegram/stats');
  }

  async getScheduledPosts(): Promise<any[]> {
    return this.get<any[]>('/telegram/scheduled_posts');
  }

  // Content Generator
  async generateContent(data: ContentRequest): Promise<GeneratedContent> {
    return this.post<GeneratedContent>('/content/generate', data);
  }

  async getContentSummary(): Promise<any> {
    return this.get<any>('/content/summary');
  }
}

export const apiService = new ApiService();
export default apiService; 