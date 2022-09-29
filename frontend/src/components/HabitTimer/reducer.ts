import { HabitType } from '../../api/types';

export const initialState: HabitType = {
  id: 0,
  user: 0,
  name: '',
  description: '',
  estimate_type: 'TIME',
  final_goal: 0,
  growth_amount: 0,
  growth_type: 'INCREASE',
  day_cycle: 0,

  due_date: null,
  is_today_due_date: false,
  today_goal: 0,
  today_progress: 0,

  is_running: false,
  start_datetime: null,
  is_paused: false,
  paused_datetime: null,
  temporary_progress: 0,
};

export function reducer(state = initialState, action: ActionType): HabitType {
  switch (action.type) {
    case 'LOAD':
      if (action.state) {
        return { ...action.state };
      } else {
        return state;
      }

    case 'CONTINUE':
      if (!state.start_datetime) return state;

      if (state.estimate_type === 'TIME') {
        const start = new Date(state.start_datetime);
        const now = new Date();
        const seconds = Math.floor((now.getTime() - start.getTime()) / 1000);
        return { ...state, temporary_progress: seconds };
      } else {
        return state;
      }

    case 'RUN_OR_STOP':
      return { ...state, is_running: !state.is_running };

    case 'PROCEED':
      if (state.growth_type === 'INCREASE') {
        return { ...state, temporary_progress: state.temporary_progress + 1 };
      } else {
        return { ...state, temporary_progress: state.temporary_progress - 1 };
      }

    default:
      throw new Error('Unsupported action type: ' + action.type);
  }
}

interface ActionType {
  type: 'LOAD' | 'CONTINUE' | 'RUN_OR_STOP' | 'PROCEED';
  payload?: object;
  state?: HabitType;
}
