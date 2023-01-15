import { HabitType, initialState } from '../types';

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
      return { ...state, temporary_progress: state.temporary_progress + 1 };
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
