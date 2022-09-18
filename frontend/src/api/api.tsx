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
  return await request<LoginResponseType>(`${host}/account/login/`, {
    username,
    password,
  });
}

export async function logout() {
  return await request<LogoutResponseType>(`${host}/account/logout/`, {});
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
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    };
  } else {
    return undefined;
  }
}
