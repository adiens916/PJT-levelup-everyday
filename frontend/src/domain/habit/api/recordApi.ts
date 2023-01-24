import { axiosInstance } from 'common/api';
import { setAxiosInterceptorForHeader } from 'domain/account/api';
import { DailyRecordType } from 'domain/habit/types';

setAxiosInterceptorForHeader();

export async function getDailyRecords(habitId: number) {
  const response = await axiosInstance.get<DailyRecordType[]>(
    `/habit/${habitId}/record/`,
  );
  return response.data;
}

export function convertRecordsForChart(dailyRecords: DailyRecordType[]) {
  return {
    labels: dailyRecords.map((record) => record.date),
    level_now: dailyRecords.map((record) => record.level_now),
    xp_accumulate: dailyRecords.map((record) => record.xp_accumulate),
    xp_change: dailyRecords.map((record) => record.xp_change),
  };
}
