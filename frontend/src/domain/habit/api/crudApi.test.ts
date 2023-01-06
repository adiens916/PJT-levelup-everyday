import {
  createHabit,
  deleteHabit,
  getHabit,
  getHabits,
  updateImportance,
} from './crudApi';
import { login } from 'domain/account/api';
import { HabitCreateRequestType } from '../types';

const SAMPLE_HABIT_COUNT = 3;
const SAMPLE_HABIT_ID = 16;
let newHabitId = 0;

beforeAll(async () => {
  const USERNAME = 'john';
  const PASSWORD = 'johnjohn';
  await login(USERNAME, PASSWORD);
});

test('get habits', async () => {
  const data = await getHabits();
  expect(data.length).toBe(SAMPLE_HABIT_COUNT);
});

test('get habit', async () => {
  const data = await getHabit(SAMPLE_HABIT_ID);
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
    expect(habits.length).toBe(SAMPLE_HABIT_COUNT);
  }
});

test('update habit importance', async () => {
  const result = await updateImportance(SAMPLE_HABIT_ID, 300);
  expect(result.success).toBe(true);

  const habit = await getHabit(SAMPLE_HABIT_ID);
  expect(habit.importance).toBe(300);

  await updateImportance(SAMPLE_HABIT_ID, 100);
});
