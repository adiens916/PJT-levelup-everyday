import { HabitResponseType } from '../../api/types';

export class Counter {
  goal = 0;
  progress = 0;
  timer = setInterval(() => {
    return;
  });

  constructor(habit?: HabitResponseType) {
    if (habit) {
      this.goal = habit.fields.today_goal;
      this.progress = habit.fields.today_progress;
      if (habit.fields.is_running && habit.fields.start_datetime) {
        this.progress += this.getDiff(habit.fields.start_datetime);
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
    const seconds = (now.getTime() - start.getTime()) / 1000;
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
