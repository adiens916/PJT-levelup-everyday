import { initialState } from '../../HabitTimer/reducer';
import { HabitType } from '../../../api/types';

export class HabitDerivative {
  habit = initialState;

  constructor(habit: HabitType) {
    this.habit = habit;
  }

  get currentProgress() {
    return this.habit.today_progress + this.habit.temporary_progress;
  }

  get ratio() {
    if (this.habit.today_goal === 0) return 0;
    return Math.floor((this.currentProgress / this.habit.today_goal) * 100);
  }

  get level() {
    if (this.habit.final_goal === 0) return 0;
    return Math.floor((this.habit.today_goal / this.habit.final_goal) * 100);
  }

  get currentProgressWithUnit() {
    return this.getValueWithUnit(this.habit, this.currentProgress);
  }

  get goalWithUnit() {
    return this.getValueWithUnit(this.habit, this.habit.today_goal);
  }

  get goalLeftWithUnit() {
    return this.getValueWithUnit(
      this.habit,
      this.habit.today_goal - this.currentProgress,
    );
  }

  get goalLeftWithUnitAndMessage() {
    if (this.currentProgress === 0 || this.ratio >= 100) {
      return '';
    }
    return ` (${this.goalLeftWithUnit} 남음)`;
  }

  getValueWithUnit(habit: HabitType, value: number) {
    if (habit.estimate_type === 'COUNT') {
      return `${value}${habit.estimate_unit}`;
    } else {
      return this.getTimeWithUnit(value);
    }
  }

  getTimeWithUnit(seconds: number): string {
    if (seconds < 60) {
      return `${seconds}초`;
    } else if (seconds < 3600) {
      const minutes = Math.floor(seconds / 60);
      return `${minutes}분 ${seconds % 60}초`;
    } else {
      const hours = Math.floor(seconds / 3600);
      const minutes = Math.floor((seconds % 3600) / 60);
      return `${hours}시간 ${minutes}분 ${seconds % 60}초`;
    }
  }
}
