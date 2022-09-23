import { HabitType } from '../../api/types';

export class Counter {
  goal = 0;
  progress = 0;
  timer = setInterval(() => {
    return;
  });

  constructor(habit?: HabitType) {
    if (habit) {
      this.goal = habit.today_goal;
      this.progress = habit.today_progress;
      if (habit.is_running && habit.start_datetime) {
        this.progress += this.getDiff(habit.start_datetime);
      }
      // habit.fields.estimate_type
      // habit.fields.growth_type
      // habit.fields.is_paused
      // habit.fields.paused_datetime
    }
  }

  start(onChange?: () => void) {
    this.timer = setInterval(() => {
      this.progress += 1;
      if (onChange) {
        onChange();
      }
    }, 1000);
  }

  stop() {
    clearInterval(this.timer);
  }

  getDiff(start_datetime: string) {
    const start = new Date(start_datetime);
    const now = new Date();
    const seconds = Math.floor((now.getTime() - start.getTime()) / 1000);
    return seconds;
  }

  get ratio() {
    if (this.goal !== 0) {
      return Math.floor((this.progress / this.goal) * 100);
    } else {
      return 100;
    }
  }
}
