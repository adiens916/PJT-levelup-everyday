import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ChartOptions,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';
import { useParams } from 'react-router-dom';
import { useDailyRecords } from './useDailyRecords';
import useDocumentTitle from '../../hook/useDocumentTitle';

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

export function DailyGraph() {
  useDocumentTitle('기록');

  const { id: habitId } = useParams();
  const data = useDailyRecords(Number(habitId));

  return <Bar options={options} data={data} />;
}
