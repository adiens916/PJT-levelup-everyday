export interface DailyRecordsForChartType {
  labels: string[];
  level_now: number[];
  xp_accumulate: number[];
  xp_change: number[];
}

export const initialState: DailyRecordsForChartType = {
  labels: [],
  level_now: [],
  xp_accumulate: [],
  xp_change: [],
};
