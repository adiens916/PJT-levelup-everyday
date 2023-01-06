import { axiosInstance } from 'common/api';
import { setAxiosInterceptorForHeader } from 'domain/account/api';
import { StartTimerType, FinishTimerType } from '../types';

setAxiosInterceptorForHeader();

export async function startTimer(habitId: number) {
  const response = await axiosInstance.post<StartTimerType>(
    '/habit/timer/start/',
    {
      habit_id: habitId,
    },
  );
  return response.data;
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
