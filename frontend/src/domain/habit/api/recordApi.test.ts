import { login } from 'domain/account/api';
import { getDailyRecords } from './recordApi';

beforeAll(async () => {
  const USERNAME = 'john';
  const PASSWORD = 'johnjohn';
  await login(USERNAME, PASSWORD);
});

const HABIT_ID = 16;

test('get daily records', async () => {
  const dailyRecords = await getDailyRecords(HABIT_ID);
  expect(dailyRecords).toHaveProperty('date');
  expect(dailyRecords).toHaveProperty('success');
  expect(dailyRecords).toHaveProperty('level_now');
  expect(dailyRecords).toHaveProperty('level_change');
  expect(dailyRecords).toHaveProperty('xp_now');
  expect(dailyRecords).toHaveProperty('xp_change');
});
