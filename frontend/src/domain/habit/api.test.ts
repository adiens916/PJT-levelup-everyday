import { getHabits } from './api';
import { login } from 'domain/account/api';

const USERNAME = 'john';
const PASSWORD = 'johnjohn';
const HABIT_LENGTH = 3;

beforeAll(async () => {
  await login(USERNAME, PASSWORD);
});

test('get habits', async () => {
  const data = await getHabits();
  expect(data).toHaveLength(HABIT_LENGTH);
});
