import { HabitType } from '../api/types';

export function ratio(numerator: number, denominator: number): number {
  if (denominator !== 0) {
    return Math.floor((numerator / denominator) * 100);
  } else {
    return 0;
  }
}

export function getValueWithUnit(habit: HabitType, value: number) {
  if (habit.estimate_type === 'TIME') {
    return getTimeWithUnit(value);
  } else {
    return `${value}${habit.estimate_unit}`;
  }
}

export function getTimeWithUnit(seconds: number): string {
  if (seconds < 60) {
    return `${seconds}초`;
  } else if (seconds < 3600) {
    const minutes = Math.floor(seconds / 60);
    return `${minutes}분 ${seconds % 60}초`;
  } else {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor(seconds / 60);
    return `${hours}시간 ${minutes}분 ${seconds % 60}초`;
  }
}
