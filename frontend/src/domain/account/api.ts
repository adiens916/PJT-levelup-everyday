import { axiosInstance } from 'common/api';
import {
  SignUpResponseType,
  LoginResponseType,
  LogoutResponseType,
} from './types';

axiosInstance.interceptors.request.use((config) => {
  if (getUserToken()) {
    config.headers = { Authorization: `Token ${getUserToken()}` };
    config.withCredentials = true;
  }
  return config;
});

export async function signUp(username: string, password: string) {
  const response = await axiosInstance.post<SignUpResponseType>(
    '/account/signup/',
    { username, password },
  );
  return response.data;
}

export async function login(username: string, password: string) {
  const response = await axiosInstance.post<LoginResponseType>(
    '/account/login/',
    { username, password },
  );
  saveUserToken(response.data.token);
  return response.data;
}

export async function logout() {
  try {
    const response = await axiosInstance.post<LogoutResponseType>(
      `/account/logout/`,
    );
    return response.data;
  } catch (error) {
    console.log(error);
  } finally {
    clearUserToken();
    location.replace('/');
  }
}

export async function checkConnection() {
  const response = await axiosInstance.get('/account/check-conn/');
  // 'connected'
  return response.data;
}

export async function checkPostAvailability() {
  const response = await axiosInstance.post('/account/check-post/');
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
