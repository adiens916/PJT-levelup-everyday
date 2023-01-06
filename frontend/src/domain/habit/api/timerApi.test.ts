import { login } from 'domain/account/api';
import { getHabit } from './crudApi';
import { finishTimer, startTimer } from './timerApi';

const HABIT_ID = 16;

beforeAll(async () => {
  const USERNAME = 'john';
  const PASSWORD = 'johnjohn';
  await login(USERNAME, PASSWORD);
});

test('start timer', async () => {
  const result = await startTimer(HABIT_ID);
  expect(result.success).toBe(true);

  const habit = await getHabit(HABIT_ID);
  expect(habit.is_running).toBe(true);

  if (habit.start_datetime) {
    const start_datetime = new Date(habit.start_datetime);
    const now_datetime = new Date();
    expect(start_datetime < now_datetime).toBe(true);
  }
});

test('finish timer', async () => {
  const habit = await getHabit(HABIT_ID);
  expect(habit.is_running).toBe(true);

  // when 60 seconds passed
  const CURRENT_PROGRESS = 60;

  const result = await finishTimer(HABIT_ID, CURRENT_PROGRESS);
  expect(result.id).toBeTruthy();
  expect(result.progress).toBe(60);
});
