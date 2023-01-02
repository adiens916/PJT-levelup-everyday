import { axiosInstance } from 'common/api';
import { setAxiosInterceptorForHeader } from 'domain/account/api';
import {
  HabitResponseType,
  HabitType,
  StartTimerType,
  FinishTimerType,
  HabitCreateRequestType,
  HabitCreateResponseType,
  DailyRecordResponseType,
  DailyRecordType,
} from 'domain/habit/types';

setAxiosInterceptorForHeader();

export async function getHabits() {
  const response = await axiosInstance.get<HabitType[]>('/habit/');
  return response.data;
}

export async function getHabit(habitId: number) {
  const response = await axiosInstance.get<HabitType>(`/habit/${habitId}/`);
  return response.data;
}

export async function createHabit(habit: HabitCreateRequestType) {
  const response = await axiosInstance.post<HabitCreateResponseType>(
    '/habit/',
    habit,
  );
  return response.data;
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
