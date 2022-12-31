import axios from 'axios';
import { host, axiosInstance, request, requestPostByAxios } from 'common/api';
import {
  SignUpResponseType,
  LoginResponseType,
  LogoutResponseType,
} from './types';

export async function signUp(username: string, password: string) {
  return await request<SignUpResponseType>(`${host}/account/signup/`, {
    username,
    password,
  });
}

export async function login(username: string, password: string) {
  const response = await axiosInstance.post<LoginResponseType>(
    '/account/login/',
    {
      username,
      password,
    },
  );
  saveUserToken(response.data.token);
  return response.data;
}

export async function logout() {
  let data: LogoutResponseType | null = null;
  try {
    data = await requestPostByAxios(`${host}/account/logout/`, {});
  } finally {
    clearUserToken();
    location.replace('/');
    return data;
  }
}

export async function checkConnection() {
  const response = await axios.get(`${host}/account/check-conn/`);
  // 'connected'
  return response.data;
}

export async function checkPostAvailability() {
  const response = await axios.post(`${host}/account/check-post/`);
  // 'post available'
  return response.data;
}

export function saveUserToken(token: string) {
  localStorage.setItem('token', token);
}

export function getUserToken() {
  return localStorage.getItem('token');
}

export function clearUserToken() {
  localStorage.removeItem('token');
}
