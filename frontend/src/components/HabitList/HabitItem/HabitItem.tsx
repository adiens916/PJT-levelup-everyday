import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, Stack, Typography } from '@mui/material';

import { HabitType } from '../../../api/types';
import { ratio as getRatio } from '../../../utils/utils';

export default function HabitItem({ habit }: { habit: HabitType }) {
  const navigate = useNavigate();
  const level = Math.floor((habit.today_goal / habit.final_goal) * 100);
  const ratio = getRatio(habit.today_progress, habit.today_goal);

  return (
    <>
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
          background: `linear-gradient(90deg, ${
            ratio >= 50 ? 'dodgerblue' : 'aqua'
          } 0%, white ${ratio}%)`,
        }}
      >
        <Stack direction="row" alignItems="center" spacing={2}>
          <Typography color={ratio > 30 ? 'yellow' : 'turquoise'}>
            Lv. {level}
          </Typography>
          {/* 습관 이름 */}
          <Typography color={ratio > 30 ? 'yellow' : 'turquoise'} variant="h5">
            {habit.name}
          </Typography>
        </Stack>

        {/* 현재 달성률 */}
        <Typography color={ratio >= 100 ? 'yellow' : 'aquamarine'} variant="h5">
          {ratio}%
        </Typography>
      </Button>
    </>
  );
}
