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
  const record = dailyRecords[0];

  expect(record).toHaveProperty('date');
  expect(record).toHaveProperty('success');
  expect(record).toHaveProperty('level_now');
  expect(record).toHaveProperty('level_change');
  expect(record).toHaveProperty('xp_now');
  expect(record).toHaveProperty('xp_change');
});
