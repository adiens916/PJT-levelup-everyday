import React from 'react';
import { useParams } from 'react-router-dom';
import { Box, CircularProgress, Typography } from '@mui/material';

import CircularProgressWithLabel from './CircularProgress/CircularProgress';
import useDocumentTitle from 'hook/useDocumentTitle';
import useTimer from './useTimer';
import { HabitDerivative } from '../habitDerivative';

export default function HabitTimer() {
  useDocumentTitle('습관 측정');

  const { id: habitId } = useParams();
  const { habit, StartStopButton } = useTimer(Number(habitId));
  const habitDerivative = new HabitDerivative(habit);

  return (
    <>
      <Typography fontSize="2rem" textAlign="center" marginY={7}>
        {habit.name ? habit.name : <CircularProgress size="2rem" />}
      </Typography>
      <Box display="flex" justifyContent="center">
        <CircularProgressWithLabel
          value={habitDerivative.ratio}
          progress={habitDerivative.currentProgressWithUnit}
        />
      </Box>
      <StartStopButton
        variant="contained"
        color={!habit.is_running ? 'primary' : 'secondary'}
        sx={{
          display: 'block',
          marginLeft: 'auto',
          marginRight: 'auto',
          marginTop: '5rem',
        }}
      >
        {!habit.is_running ? '시작' : '중지'}
      </StartStopButton>
    </>
  );
}
