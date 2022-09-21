import React from 'react';
import { Button, Container, Typography } from '@mui/material';
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
        <Typography textAlign="center" fontSize="1.5rem">
          {new Date().toLocaleDateString('ko')}
        </Typography>
        {habits.map((habit, index) => (
          <Button
            variant="outlined"
            sx={{
              display: 'flex',
              justifyContent: 'space-between',
              marginY: '1rem',
              padding: '0.5rem',
            }}
            key={index}
          >
            <Typography variant="h5">{habit.name}</Typography>
            <Typography variant="h5">{habit.today_progress}%</Typography>
          </Button>
        ))}
        <Button variant="contained" sx={{ fontSize: '1.5rem' }}>
          추가
        </Button>
      </Container>
    </>
  );
}
