import { initialState } from 'domain/habit/HabitTimer/reducer';
import { HabitType } from './types';

export class HabitDerivative {
  habit = initialState;

  constructor(habit: HabitType) {
    this.habit = habit;
  }

  static splitHabitsByStatus(habits: HabitType[]) {
    const habitsDone = habits.filter((habit) => this.isDone(habit));
    const habitsDoneSet = new Set(habitsDone);
    const habitsNotDone = habits.filter((e) => !habitsDoneSet.has(e));

    const habitsToDo = habitsNotDone.filter((habit) => this.isToDo(habit));
    const habitsToDoSet = new Set(habitsToDo);

    const habitsNotDue = habitsNotDone.filter((e) => !habitsToDoSet.has(e));
    return { habitsToDo, habitsDone, habitsNotDue };
  }

  static isDone(habit: HabitType) {
    if (habit.is_running) {
      return false;
    }

    switch (habit.growth_type) {
      case 'INCREASE':
        return habit.current_xp >= habit.goal_xp;
      case 'DECREASE':
        return habit.current_xp === 0;
      default:
        return;
    }
  }

  static isToDo(habit: HabitType) {
    if (habit.is_running) {
      return true;
    }

    switch (habit.growth_type) {
      case 'INCREASE':
        return (
          habit.is_today_due_date ||
          habit.current_xp + habit.temporary_progress > 0
        );
      case 'DECREASE':
        return habit.current_xp !== 0;
      default:
        return;
    }
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

  get level() {
    switch (this.habit.growth_type) {
      case 'INCREASE':
        if (this.habit.final_goal === 0) return 0;
        return Math.floor((this.habit.goal_xp / this.habit.final_goal) * 100);
      case 'DECREASE':
        const growth = this.habit.final_goal * 10 - this.habit.goal_xp;
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
    return this.getValueWithUnit(this.habit, this.habit.goal_xp);
  }

  get goalLeftWithUnit() {
    return this.getValueWithUnit(
      this.habit,
      this.habit.goal_xp - this.currentProgress,
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
