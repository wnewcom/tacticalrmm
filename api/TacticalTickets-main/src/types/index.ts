export interface User {
  id: number
  username: string
  email: string
  first_name: string
  last_name: string
}

export interface Category {
  id: number
  name: string
  description: string
  color: string
  created_at: string
}

export interface Comment {
  id: number
  content: string
  author: User
  created_at: string
  is_internal: boolean
}

export interface Ticket {
  id: number
  title: string
  description: string
  priority: 'low' | 'medium' | 'high' | 'urgent'
  status: 'open' | 'in_progress' | 'pending' | 'resolved' | 'closed'
  category: Category
  created_by: User
  assigned_to: User | null
  created_at: string
  updated_at: string
  due_date: string | null
  is_overdue: boolean
  comments?: Comment[]
  comments_count?: number
}

export interface TicketCreate {
  title: string
  description: string
  priority: string
  category_id: number
  assigned_to_id?: number | null
  due_date?: string | null
}

export interface DashboardStats {
  total_tickets: number
  open_tickets: number
  in_progress_tickets: number
  resolved_tickets: number
  my_tickets: number
  assigned_to_me: number
  high_priority: number
  urgent_priority: number
}

export interface ApiResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}