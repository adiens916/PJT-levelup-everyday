import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ChartData,
  ChartOptions,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
);

const options: ChartOptions<'bar'> = {
  responsive: true,
  plugins: {
    legend: {
      position: 'top' as const,
    },
    title: {
      display: true,
      text: 'Chart.js Bar Chart',
    },
  },
  scales: {
    x: { stacked: true },
    y: { beginAtZero: true },
  },
};

const labels = Array.from(Array(10).keys());
const goals = [10, 12, 14, 16, 18, 20, 22, 24, 26, 28];
const progresses = [10, 10, 14, 16, 18, 20, 22, 24, 26, 28];
const excesses = [12, 0, 18, 24, 18, 20, 22, 30, 26, 28];

const data: ChartData<'bar'> = {
  labels,
  datasets: [
    {
      label: 'Progress',
      data: progresses,
      backgroundColor: '#00FFFF80', // Aqua
      // backgroundColor: '#6495ED80', // CornflowerBlue
      // backgroundColor: '#00BFFF80', // DeepSkyBlue
    },
    {
      label: 'Goal',
      data: goals,
      backgroundColor: 'rgba(255, 255, 255, 0.5)', // White, transparent
      borderColor: 'blue',
      borderWidth: { top: 1, left: 1, right: 1 },
    },
    {
      label: 'Excess',
      data: excesses,
      backgroundColor: '#FF149366', // DeepPink, transparent
      borderColor: '#FF1493',
      borderWidth: 1,
    },
  ],
};

export function DailyGraph() {
  return <Bar options={options} data={data} />;
}
