export interface SignUpResponseType {
  id: number;
}

export interface LoginResponseType {
  id: number;
  name: string;
  last_login: string;
}

export interface LogoutResponseType {
  success: boolean;
  message: string;
}

export interface HabitResponseType {
  pk: number;
  model: string;
  fields: HabitType;
}

export interface HabitType {
  id?: number;
  user: number;
  name: string;
  description: string;
  estimate_type: 'TIME' | 'COUNT';
  estimate_unit?: string;
  final_goal: number;
  growth_amount: number;
  growth_type: 'INCREASE' | 'DECREASE';

  day_cycle: number;
  due_date: string | null;
  is_today_due_date: boolean;
  today_goal: number;
  today_progress: number;

  is_running: boolean;
  start_datetime: string | null;
  is_paused: boolean;
  paused_datetime: string | null;
  temporary_progress: number;
}
