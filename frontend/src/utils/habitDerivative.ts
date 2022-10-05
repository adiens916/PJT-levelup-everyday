import { initialState } from '../components/HabitTimer/reducer';
import { HabitType } from '../api/types';

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
    const ratio = (this.currentProgress / this.habit.today_goal) * 100;

    switch (this.habit.growth_type) {
      case 'INCREASE':
        return Math.floor(ratio);
      case 'DECREASE':
        return 100 - Math.ceil(ratio);
      default:
        return 0;
    }
  }

  get level() {
    switch (this.habit.growth_type) {
      case 'INCREASE':
        if (this.habit.final_goal === 0) return 0;
        return Math.floor(
          (this.habit.today_goal / this.habit.final_goal) * 100,
        );
      case 'DECREASE':
        const growth = this.habit.final_goal * 10 - this.habit.today_goal;
        const level = Math.floor(growth / this.habit.growth_amount) + 1;
        return level;
      default:
        return '';
    }
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
    switch (this.habit.growth_type) {
      case 'INCREASE':
        return ` (${this.goalLeftWithUnit} 남음)`;
      case 'DECREASE':
        return ` (${this.currentProgressWithUnit} 했음)`;
      default:
        return '';
    }
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
      return `${hours}시간 ${minutes}분`;
    }
  }
}