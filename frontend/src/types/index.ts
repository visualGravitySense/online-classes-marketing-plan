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
  telegramBot: {
    totalCampaigns: number;
    activeCampaigns: number;
    totalPosts: number;
    scheduledPosts: number;
    totalChannels: number;
    activeChannels: number;
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

// ===== НОВЫЕ ТИПЫ ДЛЯ УНИВЕРСАЛЬНОГО БОТА =====

// Campaign types для универсального бота
export interface BotCampaign {
  id: string;
  name: string;
  description?: string;
  status: 'active' | 'inactive' | 'paused';
  channels: BotChannel[];
  posts_count: number;
  scheduled_posts: number;
  created_at: string;
  updated_at: string;
}

export interface CreateBotCampaignData {
  name: string;
  description?: string;
  channels?: string[];
}

// Channel types
export interface BotChannel {
  id: string;
  name: string;
  chat_id: string;
  campaign: string;
  status: 'active' | 'inactive';
  posts_count: number;
  last_post_date?: string;
}

export interface CreateBotChannelData {
  name: string;
  chat_id: string;
  campaign: string;
}

// Post types
export interface BotPost {
  id: string;
  content: string;
  media_urls?: string[];
  campaign: string;
  channels: string[];
  status: 'draft' | 'scheduled' | 'published' | 'failed';
  scheduled_time?: string;
  published_time?: string;
  created_at: string;
  updated_at: string;
}

export interface CreateBotPostData {
  content: string;
  media_urls?: string[];
  campaign: string;
  channels: string[];
  scheduled_time?: string;
}

export interface ScheduleBotPostData {
  post_id: string;
  scheduled_time: string;
  channels: string[];
}

// Content Generator types для универсального бота
export interface BotContentRequest {
  topic: string;
  campaign: string;
  tone: 'professional' | 'casual' | 'friendly' | 'formal';
  length: 'short' | 'medium' | 'long';
  target_audience: string;
  platform: 'telegram' | 'instagram' | 'facebook' | 'linkedin';
  include_hashtags?: boolean;
  include_call_to_action?: boolean;
}

export interface BotGeneratedContent {
  id: string;
  content: string;
  hashtags?: string[];
  call_to_action?: string;
  campaign: string;
  platform: string;
  created_at: string;
  status: 'draft' | 'saved' | 'published';
}

// Analytics types
export interface BotAnalytics {
  campaigns: {
    total: number;
    active: number;
    inactive: number;
  };
  posts: {
    total: number;
    published: number;
    scheduled: number;
    failed: number;
  };
  channels: {
    total: number;
    active: number;
    inactive: number;
  };
  engagement: {
    total_views: number;
    total_likes: number;
    total_shares: number;
    average_engagement_rate: number;
  };
  performance: {
    posts_today: number;
    posts_this_week: number;
    posts_this_month: number;
    best_performing_post?: BotPost;
  };
}

// System Status types
export interface BotSystemStatus {
  schedulers: {
    [campaign: string]: {
      status: 'running' | 'stopped' | 'error';
      last_run?: string;
      next_run?: string;
      error_message?: string;
    };
  };
  content_generator: {
    status: 'available' | 'unavailable' | 'error';
    last_generation?: string;
    error_message?: string;
  };
  database: {
    status: 'connected' | 'disconnected' | 'error';
    last_backup?: string;
  };
  telegram_api: {
    status: 'connected' | 'disconnected' | 'error';
    last_check?: string;
  };
} 