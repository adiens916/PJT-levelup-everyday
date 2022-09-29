import React from 'react';
import { useParams } from 'react-router-dom';
import { Box, Typography } from '@mui/material';

import useTimer from './useTimer';
import CircularProgressWithLabel from './CircularProgress/CircularProgress';
import { ratio } from '../../utils/utils';

export default function HabitTimer() {
  const { id: habitId } = useParams();
  const { habit, StartStopButton } = useTimer(Number(habitId));

  return (
    <>
      <Typography variant="h4" textAlign="center" marginY={7}>
        {habit.name}
      </Typography>
      <Box display="flex" justifyContent="center">
        <CircularProgressWithLabel
          value={ratio(
            habit.today_progress + habit.temporary_progress,
            habit.today_goal,
          )}
          progress={habit.today_progress + habit.temporary_progress}
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
