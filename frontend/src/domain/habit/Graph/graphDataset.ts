import { ChartDataset } from 'chart.js';

export const whiteClearBar = (
  label: string,
  data: number[],
): ChartDataset<'bar'> => ({
  label,
  data,
  backgroundColor: 'rgba(255, 255, 255, 0.5)', // White, transparent
  borderColor: 'blue',
  borderWidth: { top: 1, left: 1, right: 1 },
});

export const blueBar = (
  label: string,
  data: number[],
): ChartDataset<'bar'> => ({
  label,
  data,
  backgroundColor: '#00FFFF80', // Aqua
  // backgroundColor: '#00BFFF80', // DeepSkyBlue
  // backgroundColor: '#6495ED80', // CornflowerBlue
});

export const redClearBar = (
  label: string,
  data: number[],
): ChartDataset<'bar'> => ({
  label,
  data,
  backgroundColor: '#FF149366', // DeepPink, transparent
  borderColor: '#FF1493', // DeepPink
  borderWidth: 1,
});
