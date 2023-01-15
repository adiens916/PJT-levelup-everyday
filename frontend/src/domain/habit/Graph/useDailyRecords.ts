import { useEffect, useState } from 'react';

import { ChartData } from 'chart.js';

import { getDailyRecords, convertRecordsForChart } from '../api/recordApi';
import { DailyRecordsForChartType, initialState } from './types';
import { blueBar, redClearBar, whiteClearBar } from './graphDataset';

export function useDailyRecords(habitId: number) {
  const [dailyRecords, setDailyRecords] =
    useState<DailyRecordsForChartType>(initialState);

  const data: ChartData<'bar'> = {
    labels: dailyRecords.labels,
    datasets: [
      blueBar('XP Change', dailyRecords.xp_change),
      whiteClearBar('XP Now', dailyRecords.xp_now),
      redClearBar('Level', dailyRecords.level_now),
    ],
  };

  useEffect(() => {
    getDailyRecords(habitId).then((data) =>
      setDailyRecords(convertRecordsForChart(data)),
    );
  }, []);

  return data;
}
