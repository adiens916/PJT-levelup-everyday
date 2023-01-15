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
  importance: number;

  level: number;
  goal_xp: number;
  current_xp: number;
  due_date: string | null;
  is_today_due_date: boolean;
  is_done: boolean;

  is_running: boolean;
  start_datetime: string | null;
  is_paused: boolean;
  paused_datetime: string | null;
  temporary_progress: number;
}

export type HabitCreateRequestType = Pick<
  HabitType,
  | 'name'
  | 'estimate_type'
  | 'estimate_unit'
  | 'final_goal'
  | 'growth_type'
  | 'day_cycle'
>;

export interface HabitCreateResponseType {
  id: number;
}

export interface StartTimerType {
  success: boolean;
  start_date: string;
  is_running: boolean;
}

export interface FinishTimerType {
  id: number;
  start_datetime: string;
  end_datetime: string;
  progress: number;
}

export interface DailyRecordType {
  id: number;
  habit: number;
  date: string;
  success: boolean;
  level_now: number;
  level_change: number;
  xp_now: number;
  xp_change: number;
}
