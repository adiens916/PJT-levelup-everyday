import React from 'react';
import { useParams } from 'react-router-dom';
import { Box, CircularProgress, Typography } from '@mui/material';

import useTimer from './useTimer';
import CircularProgressWithLabel from './CircularProgress/CircularProgress';
import { getValueWithUnit, ratio } from '../../utils/utils';
import useDocumentTitle from '../../hook/useDocumentTitle';

export default function HabitTimer() {
  useDocumentTitle('습관 측정');

  const { id: habitId } = useParams();
  const { habit, StartStopButton } = useTimer(Number(habitId));

  const currentProgress = habit.today_progress + habit.temporary_progress;

  return (
    <>
      <Typography fontSize="2rem" textAlign="center" marginY={7}>
        {habit.name ? habit.name : <CircularProgress size="2rem" />}
      </Typography>
      <Box display="flex" justifyContent="center">
        <CircularProgressWithLabel
          value={ratio(currentProgress, habit.today_goal)}
          progress={getValueWithUnit(habit, currentProgress)}
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
