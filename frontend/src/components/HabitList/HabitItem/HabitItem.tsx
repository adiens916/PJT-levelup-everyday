import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, Button, Stack, Typography } from '@mui/material';

import { HabitType } from '../../../api/types';
import { ratio as getRatio } from '../../../utils/utils';
import HabitItemMenu from '../HabitItemMenu/HabitItemMenu';

export default function HabitItem(props: HabitItemType) {
  const navigate = useNavigate();
  const level = Math.floor(
    (props.habit.today_goal / props.habit.final_goal) * 100,
  );
  const ratio = getRatio(props.habit.today_progress, props.habit.today_goal);

  return (
    <Box sx={{ display: 'flex', alignItems: 'center' }}>
      <Button
        onClick={() => {
          navigate(`/timer/${props.habit.id}`);
        }}
        // disabled={props.disabled}
        variant="outlined"
        sx={{
          display: 'flex',
          justifyContent: 'space-between',
          flexGrow: 1,
          marginY: '1rem',
          padding: '0.5rem',
          background: `linear-gradient(90deg, ${
            ratio >= 50 ? 'dodgerblue' : 'aqua'
          } 0%, white ${ratio}%)`,
          // opacity: props.disabled ? '0.2' : '1',
        }}
      >
        <Stack direction="row" alignItems="center" spacing={2}>
          <Typography color={ratio > 30 ? 'yellow' : 'turquoise'}>
            Lv. {level}
          </Typography>
          {/* 습관 이름 */}
          <Typography color={ratio > 30 ? 'yellow' : 'turquoise'} variant="h5">
            {props.habit.name}
          </Typography>
        </Stack>

        {/* 현재 달성률 */}
        <Typography color={ratio >= 100 ? 'yellow' : 'aquamarine'} variant="h5">
          {ratio}%
        </Typography>
      </Button>
      <HabitItemMenu habit={props.habit} />
    </Box>
  );
}

interface HabitItemType {
  habit: HabitType;
  transparent?: boolean;
  disabled?: boolean;
}
