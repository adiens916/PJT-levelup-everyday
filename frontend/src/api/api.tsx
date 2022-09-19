import {
  SignUpResponseType,
  LoginResponseType,
  LogoutResponseType,
} from './types';

const host = 'http://localhost:8000/api';

export async function signUp(username: string, password: string) {
  return await request<SignUpResponseType>(`${host}/account/signup/`, {
    username,
    password,
  });
}

export async function login(username: string, password: string) {
  const data = await request<LoginResponseType>(`${host}/account/login/`, {
    username,
    password,
  });
  saveUserId(data.id);
  return data;
}

export async function logout() {
  const data = await request<LogoutResponseType>(`${host}/account/logout/`, {});
  clearUserId();
  return data;
}

export function saveUserId(userId: number) {
  localStorage.setItem('userId', userId.toString());
}

export function clearUserId() {
  localStorage.removeItem('userId');
}

export function getUserId() {
  return Number(localStorage.getItem('userId'));
}

export async function getHabits() {
  return await request(`${host}/habit/`);
}

async function request<T>(url: string, body?: object): Promise<T> {
  const options: RequestInit | undefined = getOption(body);

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

function getOption(body?: object) {
  if (body) {
    return {
      method: 'POST',
      headers: {
        // Content-Type은 굳이 지정하지 않아도 됨.
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({ ...body }),
    };
  } else {
    return undefined;
  }
}
