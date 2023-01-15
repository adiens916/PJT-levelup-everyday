import { HabitType, initialState } from './types';

export class HabitDerivative {
  habit = initialState;

  constructor(habit: HabitType) {
    this.habit = habit;
  }

  get currentProgress() {
    return this.habit.current_xp + this.habit.temporary_progress;
  }

  get ratio() {
    if (this.habit.goal_xp === 0) return 0;
    const ratio = (this.currentProgress / this.habit.goal_xp) * 100;

    switch (this.habit.growth_type) {
      case 'INCREASE':
        return Math.floor(ratio);
      case 'DECREASE':
        return 100 - Math.ceil(ratio);
      default:
        return 0;
    }
  }

  get goalLeftWithUnitAndMessage() {
    if (this.currentProgress === 0 || this.ratio >= 100) {
      return '';
    }
    switch (this.habit.growth_type) {
      case 'INCREASE':
        return ` (${this.currentProgressWithUnit} 했음)`;
      case 'DECREASE':
        return ` (${this.goalLeftWithUnit} 남음)`;
      default:
        return '';
    }
  }

  get goalLeftWithUnit() {
    return this.getValueWithUnit(
      this.habit,
      this.habit.goal_xp - this.currentProgress,
    );
  }

  get goalWithUnit() {
    return this.getValueWithUnit(this.habit, this.habit.goal_xp);
  }

  get currentProgressWithUnit() {
    return this.getValueWithUnit(this.habit, this.currentProgress);
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
