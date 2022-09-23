import React from 'react';
import { useParams } from 'react-router-dom';
import { Box, Typography } from '@mui/material';
import useTimer from './useTimer';
import CircularProgressWithLabel from './CircularProgress/CircularProgress';

export default function HabitTimer() {
  const { id: habitId } = useParams();
  const { counter, running, StartStopButton } = useTimer(Number(habitId));

  return (
    <>
      <Typography variant="h4" textAlign="center" marginY={7}>
        달리기
      </Typography>
      <Box display="flex" justifyContent="center">
        <CircularProgressWithLabel
          value={counter.ratio}
          progress={counter.progress}
        />
      </Box>
      <StartStopButton
        variant="contained"
        color={!running ? 'primary' : 'secondary'}
        sx={{
          display: 'block',
          marginLeft: 'auto',
          marginRight: 'auto',
          marginTop: '5rem',
        }}
      >
        {!running ? '시작' : '중지'}
      </StartStopButton>
    </>
  );
}
