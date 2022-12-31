import axios from 'axios';

// Set host by an environment variable.
export let host = process.env.REACT_APP_BACKEND_HOST;
if (host) {
  host += '/api';
} else {
  host = 'http://127.0.0.1:8000/api';
}

export const axiosInstance = axios.create({
  baseURL: host,
});
