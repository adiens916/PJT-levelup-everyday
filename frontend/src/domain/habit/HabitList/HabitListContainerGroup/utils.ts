import { HabitType } from '../../types';

export function splitHabitsByStatus(habits: HabitType[]) {
  const habitsDone = habits.filter((habit) => isDone(habit));
  const habitsDoneSet = new Set(habitsDone);
  const habitsNotDone = habits.filter((e) => !habitsDoneSet.has(e));

  const habitsToDo = habitsNotDone.filter((habit) => isToDo(habit));
  const habitsToDoSet = new Set(habitsToDo);

  const habitsNotDue = habitsNotDone.filter((e) => !habitsToDoSet.has(e));
  return { habitsToDo, habitsDone, habitsNotDue };
}

function isDone(habit: HabitType) {
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

function isToDo(habit: HabitType) {
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
