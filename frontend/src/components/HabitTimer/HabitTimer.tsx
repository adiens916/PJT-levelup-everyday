import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Box, Button, Typography } from '@mui/material';

import CircularProgressWithLabel from './CircularProgress/CircularProgress';
import { getHabit } from '../../api/api';
import { HabitResponseType } from '../../api/types';

export default function HabitTimer() {
  const { id: habitId } = useParams();
  const [habit, setHabit] = useState<HabitResponseType>();

  const [progress, setProgress] = useState(0);
  const [running, setRunning] = useState(false);

  useEffect(() => {
    if (habitId) {
      getHabit(Number(habitId)).then((data) => setHabit(data[0]));
    }
  }, []);

  useEffect(() => {
    if (running) {
      const timer = setInterval(() => {
        setProgress((prevProgress) =>
          prevProgress >= 100 ? 0 : prevProgress + 10,
        );
      }, 800);
      return () => {
        clearInterval(timer);
      };
    }
  }, [running]);

  return (
    <>
      <Typography variant="h4" textAlign="center" marginY={7}>
        {habit?.fields.name}
      </Typography>
      <Box display="flex" justifyContent="center">
        <CircularProgressWithLabel value={progress} />
      </Box>
      <Button
        onClick={() => setRunning(!running)}
        variant="contained"
        sx={{
          display: 'block',
          marginLeft: 'auto',
          marginRight: 'auto',
          marginTop: '5rem',
        }}
      >
        시작 / 중지
      </Button>
    </>
  );
}
