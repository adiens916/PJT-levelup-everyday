import { axiosInstance } from 'common/api';
import { setAxiosInterceptorForHeader } from 'domain/account/api';
import {
  HabitType,
  HabitCreateRequestType,
  HabitCreateResponseType,
} from 'domain/habit/types';

setAxiosInterceptorForHeader();

export async function getHabits() {
  const response = await axiosInstance.get<HabitType[]>('/habit/');
  return response.data;
}

export async function getHabit(habitId: number) {
  const response = await axiosInstance.get<HabitType>(`/habit/${habitId}/`);
  return response.data;
}

export async function createHabit(habit: HabitCreateRequestType) {
  const response = await axiosInstance.post<HabitCreateResponseType>(
    '/habit/',
    habit,
  );
  return response.data;
}

export async function deleteHabit(habitId: number) {
  const response = await axiosInstance.delete(`/habit/${habitId}/`);
  return response.data;
}

export async function updateImportance(habitId: number, importance: number) {
  const response = await axiosInstance.patch(`/habit/${habitId}/importance/`, {
    importance,
  });
  return response.data;
}
