import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, Button, Stack, Typography } from '@mui/material';

import HabitItemMenu from '../HabitItemMenu/HabitItemMenu';
import { HabitDerivative } from './habitDerivative';
import { HabitType } from '../../../api/types';

export default function HabitItem(props: HabitItemType) {
  const navigate = useNavigate();
  const habitDerivative = new HabitDerivative(props.habit);

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
            habitDerivative.ratio >= 50 ? 'dodgerblue' : 'aqua'
          } 0%, white ${habitDerivative.ratio}%)`,
          // opacity: props.disabled ? '0.2' : '1',
        }}
      >
        <Stack direction="row" alignItems="center" spacing={2}>
          <Typography
            color={habitDerivative.ratio > 30 ? 'yellow' : 'turquoise'}
          >
            Lv. {habitDerivative.level}
          </Typography>
          {/* 습관 이름 */}
          <Typography
            color={habitDerivative.ratio > 30 ? 'yellow' : 'turquoise'}
            variant="h5"
          >
            {props.habit.name}
          </Typography>
        </Stack>

        {/* 현재 목표 */}
        <Typography
          color={habitDerivative.ratio >= 100 ? 'yellow' : 'aquamarine'}
          variant="h5"
        >
          {habitDerivative.goalWithUnit}
          {habitDerivative.goalLeftWithUnitAndMessage}
        </Typography>

        {/* 현재 달성률 */}
        {/* <Typography color={ratio >= 100 ? 'yellow' : 'aquamarine'} variant="h5">
          {ratio}%
        </Typography> */}
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
