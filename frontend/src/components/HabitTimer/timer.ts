import { HabitResponseType } from '../../api/types';

export class Counter {
  goal = 0;
  progress = 0;
  ratio = 0.0;
  timer = setInterval(() => {
    return;
  });

  constructor(habit?: HabitResponseType) {
    if (habit) {
      this.goal = habit.fields.today_goal;
      this.progress = habit.fields.today_progress;
      this.ratio = this.getRatio();
      // habit.fields.estimate_type
      // habit.fields.growth_type
      // habit.fields.is_paused
      // habit.fields.is_running
      // habit.fields.start_datetime
      // habit.fields.paused_datetime
    }
  }

  start(setter?: (progress: number) => void) {
    this.timer = setInterval(() => {
      this.progress += 1;
      if (setter) {
        setter(this.progress);
      }
    }, 1000);
  }

  stop() {
    clearInterval(this.timer);
  }

  getRatio() {
    if (this.goal !== 0) {
      return Math.round((this.progress / this.goal) * 100);
    } else {
      return 100;
    }
  }
}
