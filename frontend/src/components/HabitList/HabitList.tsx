import React from 'react';
import { Container, Typography } from '@mui/material';

import HabitItem from './HabitItem/HabitItem';
import { getHabits } from '../../api/api';
import { HabitType } from '../../api/types';

export default function HabitList() {
  const [habits, setHabits] = React.useState<HabitType[]>([]);

  React.useEffect(() => {
    getHabits().then((data) => setHabits(data));
  }, []);

  return (
    <>
      <Container
        sx={{ display: 'flex', flexDirection: 'column', width: '70%' }}
      >
        {/* 오늘 날짜 */}
        <Typography textAlign="center" fontSize="1.5rem">
          {new Date().toLocaleDateString('ko')}
        </Typography>

        {/* 습관 목록 */}
        {habits.map((habit, index) => (
          <HabitItem habit={habit} key={index} />
        ))}
      </Container>
    </>
  );
}
