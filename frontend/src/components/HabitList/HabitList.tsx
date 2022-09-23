import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, Container, Typography } from '@mui/material';

import { getHabits } from '../../api/api';
import { HabitType } from '../../api/types';
import { ratio } from '../../utils/utils';

export default function HabitList() {
  const navigate = useNavigate();
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
            onClick={() => {
              navigate(`/timer/${habit.id}`);
            }}
            variant="outlined"
            sx={{
              display: 'flex',
              justifyContent: 'space-between',
              marginY: '1rem',
              padding: '0.5rem',
              // background: 'linear-gradient(90deg, blue 0%, white 30%)',
            }}
            key={index}
          >
            <Typography
              // color={getRatio(habit) > 10 ? 'yellow' : 'blue'}
              variant="h5"
            >
              {habit.name}
            </Typography>
            <Typography variant="h5">
              {ratio(habit.today_progress, habit.today_goal)}%
            </Typography>
          </Button>
        ))}
        <Button variant="contained" sx={{ fontSize: '1.5rem' }}>
          추가
        </Button>
      </Container>
    </>
  );
}
