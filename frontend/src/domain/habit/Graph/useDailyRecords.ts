import { ChartData, ChartDataset } from 'chart.js';
import { useEffect, useState } from 'react';
import { getDailyRecords, convertRecordsForChart } from '../api/recordApi';

const initialState: DailyRecordsForChartType = {
  labels: [],
  goals: [],
  progresses: [],
  excesses: [],
};

export function useDailyRecords(habitId: number) {
  const [dailyRecords, setDailyRecords] =
    useState<DailyRecordsForChartType>(initialState);

  const datasetOfGoal: ChartDataset<'bar'> = {
    label: 'Goal',
    data: dailyRecords.goals,
    backgroundColor: 'rgba(255, 255, 255, 0.5)', // White, transparent
    borderColor: 'blue',
    borderWidth: { top: 1, left: 1, right: 1 },
  };

  const datasetOfProgress: ChartDataset<'bar'> = {
    label: 'Progress',
    data: dailyRecords.progresses,
    backgroundColor: '#00FFFF80', // Aqua
    // backgroundColor: '#6495ED80', // CornflowerBlue
    // backgroundColor: '#00BFFF80', // DeepSkyBlue
  };

  const datasetOfExcess: ChartDataset<'bar'> = {
    label: 'Excess',
    data: dailyRecords.excesses,
    backgroundColor: '#FF149366', // DeepPink, transparent
    borderColor: '#FF1493',
    borderWidth: 1,
  };

  const data: ChartData<'bar'> = {
    labels: dailyRecords.labels,
    datasets: [datasetOfProgress, datasetOfGoal, datasetOfExcess],
  };

  useEffect(() => {
    getDailyRecords(habitId).then((data) =>
      setDailyRecords(convertRecordsForChart(data)),
    );
  }, []);

  return data;
}

interface DailyRecordsForChartType {
  labels: string[];
  goals: number[];
  progresses: number[];
  excesses: number[];
}
