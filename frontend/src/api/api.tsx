import axios from 'axios';
import {
  SignUpResponseType,
  LoginResponseType,
  LogoutResponseType,
  HabitResponseType,
  HabitType,
  StartTimerType,
  FinishTimerType,
} from './types';

const host = 'http://127.0.0.1:8000/api';

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
  const data = await requestGetByAxios<HabitResponseType[]>(`${host}/habit/`);
  return extractFields(data);
}

export async function getHabit(habitId: number) {
  const data = await requestGetByAxios<HabitResponseType[]>(
    `${host}/habit/${habitId}/`,
  );
  return data;
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
  return response.data;
}

function extractFields(querySet: HabitResponseType[]): HabitType[] {
  return querySet.map((instance) => ({
    id: instance.pk,
    ...instance.fields,
  }));
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
