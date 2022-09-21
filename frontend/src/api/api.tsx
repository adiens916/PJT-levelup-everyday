import axios from 'axios';

import {
  SignUpResponseType,
  LoginResponseType,
  LogoutResponseType,
} from './types';

const host = 'http://127.0.0.1:8000/api';

export async function signUp(username: string, password: string) {
  return await request<SignUpResponseType>(`${host}/account/signup/`, {
    username,
    password,
  });
}

export async function login(username: string, password: string) {
  const data = await requestPostByAxios(`${host}/account/login/`, {
    username,
    password,
  });
  saveUserId(data.id);
  return data;
}

export async function logout() {
  const data = await requestPostByAxios(`${host}/account/logout/`, {});
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
  const data = await requestGetByAxios(`${host}/habit/`);
  console.log(data);
  return data;
}

async function requestGetByAxios(url: string) {
  const response = await axios({
    method: 'GET',
    headers: {
      'Access-Control-Allow-Origin': 'http://localhost:3000',
      // 'Access-Control-Allow-Credentials': true,
    },
    withCredentials: true,
    url,
  });
  return response.data;
}

async function requestPostByAxios(url: string, data?: object) {
  const response = await axios({
    method: 'post',
    headers: {
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
