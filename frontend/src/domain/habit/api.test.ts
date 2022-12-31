import { getHabit, getHabits } from './api';
import { login } from 'domain/account/api';

const USERNAME = 'john';
const PASSWORD = 'johnjohn';
const HABIT_LENGTH = 3;
const HABIT_ID = 16;

beforeAll(async () => {
  await login(USERNAME, PASSWORD);
});

test('get habits', async () => {
  const data = await getHabits();
  expect(data).toHaveLength(HABIT_LENGTH);
});

test('get habit', async () => {
  const data = await getHabit(HABIT_ID);
  expect(data.name).toBe('new');
});
