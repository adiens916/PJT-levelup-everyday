import axios from 'axios';
import {
  SignUpResponseType,
  LoginResponseType,
  LogoutResponseType,
  HabitResponseType,
  HabitType,
  StartTimerType,
  FinishTimerType,
  HabitCreateType,
  DailyRecordResponseType,
  DailyRecordType,
} from './types';

// Set host by an environment variable.
let host = process.env.BACKEND_WITH_DOMAIN;
if (host) {
  // Add postfix
  host += '/api';
} else {
  host = 'http://127.0.0.1:8000/api';
}

export async function signUp(username: string, password: string) {
  return await request<SignUpResponseType>(`${host}/account/signup/`, {
    username,
    password,
  });
}

export async function login(username: string, password: string) {
  const data: LoginResponseType = await requestPostByAxios(
    `${host}/account/login/`,
    {
      username,
      password,
    },
  );
  saveUserToken(data.token);
  return data;
}

export async function logout() {
  const data: LogoutResponseType = await requestPostByAxios(
    `${host}/account/logout/`,
    {},
  );
  clearUserToken();
  return data;
}

export function saveUserToken(token: string) {
  localStorage.setItem('token', token);
}

export function clearUserToken() {
  localStorage.removeItem('token');
}

export function getUserToken() {
  return localStorage.getItem('token');
}

export async function getHabits() {
  const response = await requestGetByAxios<HabitResponseType[]>(
    `${host}/habit/`,
  );
  return response;
  // if (response.status === 200) {
  //   return extractFields(response.data);
  // } else {
  // }
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

async function requestGetByAxios<T>(url: string) {
  const response = await axios.get<T>(url, {
    headers: {
      Authorization: `Token ${getUserToken()}`,
    },
    withCredentials: true,
  });
  return response;
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

async function requestPostByAxios(url: string, data?: object) {
  const response = await axios({
    method: 'post',
    headers: {
      Authorization: getUserToken() ? `Token ${getUserToken()}` : '',
      'Content-Type': 'multipart/form-data',
    },
    withCredentials: true,
    url,
    data,
  });
  return response.data;
}

async function request<T>(url: string, body?: object): Promise<T> {
  const options = getOption(body);

  try {
    const response = await fetch(url, options);
    if (response.ok) {
      return response.json();
    } else {
      console.log('Response not okay: ', response);
      throw response;
    }
  } catch (error) {
    console.log('Server error: ', error);
    throw error;
  }
}

function getOption(body?: object): RequestInit | undefined {
  if (body) {
    return {
      method: 'POST',
      headers: {
        // Content-Type은 굳이 지정하지 않아도 됨.
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({ ...body }),
      credentials: 'same-origin',
    };
  } else {
    return undefined;
  }
}
