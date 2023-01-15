export interface DailyRecordsForChartType {
  labels: string[];
  level_now: number[];
  xp_now: number[];
  xp_change: number[];
}

export const initialState: DailyRecordsForChartType = {
  labels: [],
  level_now: [],
  xp_now: [],
  xp_change: [],
};
