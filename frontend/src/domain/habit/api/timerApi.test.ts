import { login } from 'domain/account/api';
import { getHabit } from './crudApi';
import { startTimer } from './timerApi';

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
