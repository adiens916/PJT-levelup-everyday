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

function convertRecordsForChart(dailyRecords: DailyRecordType[]) {
  const labels = [];
  const goals = [];
  const progresses = [];
  const excesses = [];

  for (const record of dailyRecords) {
    labels.push(record.date);
    goals.push(record.goal);
    progresses.push(record.progress);
    excesses.push(record.excess);
  }

  const dailyRecordsForChart = {
    labels,
    goals,
    progresses,
    excesses,
  };

  return dailyRecordsForChart;
}
