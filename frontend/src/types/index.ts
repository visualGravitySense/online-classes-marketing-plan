// API Response types
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

// Authentication types
export interface User {
  id: number;
  username: string;
  email?: string;
  role: string;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

// Dashboard types
export interface DashboardSummary {
  financials: {
    totalRevenue: number;
    profitMargin: number;
    monthly: {
      grossRevenue: number;
      expenses: number;
      netProfit: number;
    };
  };
  courses: {
    total: number;
    active: number;
    completed: number;
  };
  students: {
    total: number;
    active: number;
    newThisMonth: number;
  };
  campaigns: {
    total: number;
    active: number;
    totalSpent: number;
  };
}

// Course types
export interface Course {
  id: number;
  name: string;
  description: string;
  price: number;
  start_date: string;
  status: 'draft' | 'active' | 'completed' | 'cancelled';
}

export interface CreateCourseData {
  name: string;
  description: string;
  price: number;
  start_date: string;
  status: string;
}

// Transaction types
export interface Transaction {
  id: number;
  type: 'income' | 'expense';
  amount: number;
  description: string;
  date: string;
  category: string;
  course_id?: number;
}

export interface CreateTransactionData {
  type: 'income' | 'expense';
  amount: number;
  description: string;
  date: string;
  category: string;
  course_id?: number;
}

// Team types
export interface TeamMember {
  id: number;
  name: string;
  role: string;
  email: string;
  status: 'active' | 'inactive';
}

export interface CreateTeamMemberData {
  name: string;
  role: string;
  email: string;
  status: string;
}

// Campaign types
export interface Campaign {
  id: number;
  name: string;
  source: string;
  budget: number;
  start_date: string;
  end_date: string;
  status: 'active' | 'paused' | 'finished';
}

export interface CreateCampaignData {
  name: string;
  source: string;
  budget: number;
  start_date: string;
  end_date: string;
  status: string;
}

// Student types
export interface Student {
  id: number;
  name: string;
  email: string;
  registration_date: string;
}

export interface CreateStudentData {
  name: string;
  email: string;
  registration_date: string;
}

// Partner types
export interface Partner {
  id: number;
  name: string;
  email: string;
  promo_code: string;
  status: 'active' | 'inactive';
}

export interface CreatePartnerData {
  name: string;
  email: string;
  promo_code: string;
  status: string;
}

// Telegram Bot types
export interface TelegramGroup {
  id: number;
  name: string;
  chat_id: string;
}

export interface TelegramStats {
  totalGroups: number;
  totalPosts: number;
  scheduledPosts: number;
  engagementRate: number;
}

// Content Generator types
export interface ContentRequest {
  topic: string;
  platform: string;
  tone: string;
  length: string;
  targetAudience: string;
}

export interface GeneratedContent {
  id: string;
  content: string;
  platform: string;
  created_at: string;
  status: 'draft' | 'published' | 'scheduled';
} 