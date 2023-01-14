import { axiosInstance } from 'common/api';
import { setAxiosInterceptorForHeader } from 'domain/account/api';
import { DailyRecordType, OldDailyRecordType } from 'domain/habit/types';

setAxiosInterceptorForHeader();

export async function getDailyRecords(habitId: number) {
  const response = await axiosInstance.get<DailyRecordType[]>(
    `/habit/${habitId}/record/`,
  );
  return response.data;
}

export function convertRecordsForChart(dailyRecords: OldDailyRecordType[]) {
  return {
    labels: dailyRecords.map((record) => record.date),
    goals: dailyRecords.map((record) => record.goal),
    progresses: dailyRecords.map((record) => record.progress),
    excesses: dailyRecords.map((record) => record.excess),
  };
}
