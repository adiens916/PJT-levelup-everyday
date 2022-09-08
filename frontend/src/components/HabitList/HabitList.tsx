import React from 'react';
import { Button, Container, Typography } from '@mui/material';

const sampleHabits = [
  {
    name: '독서',
    progress: 0,
  },
  {
    name: '푸시업',
    progress: 0,
  },
];

export default function HabitList() {
  const [habits] = React.useState(sampleHabits);

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
            <Typography fontSize="1.5rem">{habit.name}</Typography>
            <Typography fontSize="1.5rem">{habit.progress}%</Typography>
          </Button>
        ))}
        <Button variant="contained" sx={{ fontSize: '1.5rem' }}>
          추가
        </Button>
      </Container>
    </>
  );
}
