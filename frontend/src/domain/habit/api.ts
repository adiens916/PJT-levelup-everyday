import { axiosInstance } from 'common/api';
import { setAxiosInterceptorForHeader } from 'domain/account/api';
import {
  HabitResponseType,
  HabitType,
  StartTimerType,
  FinishTimerType,
  HabitCreateType,
  DailyRecordResponseType,
  DailyRecordType,
} from 'domain/habit/types';

setAxiosInterceptorForHeader();

export async function getHabits() {
  const response = await axiosInstance.get<HabitResponseType[]>('/habit/');
  return response.data;
}

export async function getHabit(habitId: number) {
  const response = await requestGetByAxios<HabitResponseType[]>(
    `${host}/habit/${habitId}/`,
  );
  return extractFields(response.data)[0];
}

export async function createHabit(habit: HabitType) {
  const body = {
    name: habit.name,
    estimate_type: habit.estimate_type,
    estimate_unit: habit.estimate_unit,
    final_goal: habit.final_goal,
    growth_type: habit.growth_type,
    day_cycle: habit.day_cycle,
  };

  if (body.estimate_type === 'TIME') {
    switch (body.estimate_unit) {
      case 'HOUR':
        body.final_goal *= 3600;
        break;
      case 'MINUTE':
        body.final_goal *= 60;
        break;
      default:
        break;
    }
    body.estimate_unit = '';
  }

  const data: HabitCreateType = await requestPostByAxios(
    `${host}/habit/`,
    body,
  );
  return data;
}

export async function deleteHabit(habitId: number) {
  return await requestPostByAxios(`${host}/habit/${habitId}/`);
}

export async function updateImportance(habitId: number, importance: number) {
  return await requestPostByAxios(`${host}/habit/${habitId}/importance`, {
    importance,
  });
}

export async function getRecords(habitId: number) {
  const response = await requestGetByAxios<DailyRecordResponseType[]>(
    `${host}/habit/${habitId}/record/`,
  );
  const records = extractRecordFields(response.data);
  return convertRecordsForChart(records);
}

export async function startTimer(habitId: number) {
  const data: StartTimerType = await requestPostByAxios(
    `${host}/habit/timer/start/`,
    {
      habit_id: habitId,
    },
  );
  return data;
}

export async function finishTimer(habitId: number, progress: number) {
  const data: FinishTimerType = await requestPostByAxios(
    `${host}/habit/timer/finish/`,
    {
      habit_id: habitId,
      progress: progress,
    },
  );
  return data;
}

export function extractFields(querySet: HabitResponseType[]): HabitType[] {
  return querySet.map((instance) => ({
    id: instance.pk,
    ...instance.fields,
  }));
}

function extractRecordFields(
  querySet: DailyRecordResponseType[],
): DailyRecordType[] {
  return querySet.map((instance) => ({
    ...instance.fields,
    id: instance.pk,
  }));
}

function convertRecordsForChart(dailyRecords: DailyRecordType[]) {
  const labels = [];
  const goals = [];
  const progresses = [];
  const excesses = [];

  for (const record of dailyRecords) {
    labels.push(record.date);
    goals.push(record.goal);
    progresses.push(record.progress);
    excesses.push(record.excess);
  }

  const dailyRecordsForChart = {
    labels,
    goals,
    progresses,
    excesses,
  };

  return dailyRecordsForChart;
}
