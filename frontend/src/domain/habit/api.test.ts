import { createHabit, deleteHabit, getHabit, getHabits } from './api';
import { login } from 'domain/account/api';
import { HabitCreateRequestType } from './types';

const USERNAME = 'john';
const PASSWORD = 'johnjohn';
const HABIT_LENGTH = 3;
const HABIT_ID = 16;
let newHabitId = 0;

beforeAll(async () => {
  await login(USERNAME, PASSWORD);
});

test('get habits', async () => {
  const data = await getHabits();
  expect(data.length).toBe(HABIT_LENGTH);
});

test('get habit', async () => {
  const data = await getHabit(HABIT_ID);
  expect(data.name).toBe('new');
});

test('create habit', async () => {
  const HABIT_INFO: HabitCreateRequestType = {
    name: 'Reading a book',
    estimate_type: 'TIME',
    estimate_unit: '',
    final_goal: 3600,
    growth_type: 'INCREASE',
    day_cycle: 1,
  };

  const data = await createHabit(HABIT_INFO);
  expect(data.id).toBeTruthy();
  newHabitId = data.id;
});

test('delete habit', async () => {
  if (newHabitId) {
    const result = await deleteHabit(newHabitId);
    expect(result.success).toBe(true);

    const habits = await getHabits();
    expect(habits.length).toBe(HABIT_LENGTH);
  }
});
