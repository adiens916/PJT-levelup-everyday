import { initialState } from '../../HabitTimer/reducer';
import { HabitType } from '../../../api/types';
import { getValueWithUnit, ratio as getRatio } from '../../../utils/utils';

export class HabitDerivative {
  habit = initialState;

  constructor(habit: HabitType) {
    this.habit = habit;
  }

  get level() {
    return Math.floor((this.habit.today_goal / this.habit.final_goal) * 100);
  }

  get currentProgress() {
    return this.habit.today_progress + this.habit.temporary_progress;
  }

  get ratio() {
    return getRatio(this.currentProgress, this.habit.today_goal);
  }

  get goalWithUnit() {
    return getValueWithUnit(this.habit, this.habit.today_goal);
  }

  get progressRemainingWithUnit() {
    if (this.currentProgress === 0 || this.ratio >= 100) {
      return '';
    } else {
      const remains = getValueWithUnit(
        this.habit,
        this.habit.today_goal - this.currentProgress,
      );
      return ` (${remains} 남음)`;
    }
  }
}
