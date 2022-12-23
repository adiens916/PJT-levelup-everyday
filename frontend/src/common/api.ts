import axios from 'axios';

// Set host by an environment variable.
let host = process.env.REACT_APP_BACKEND_HOST;
if (host) {
  host += '/api';
} else {
  host = 'http://127.0.0.1:8000/api';
}

export async function requestGetByAxios<T>(url: string) {
  const response = await axios.get<T>(url, {
    headers: {
      Authorization: `Token ${getUserToken()}`,
    },
    withCredentials: true,
  });
  return response;
}

export async function requestPostByAxios(url: string, data?: object) {
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

export async function request<T>(url: string, body?: object): Promise<T> {
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

export function getUserToken() {
  return localStorage.getItem('token');
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
