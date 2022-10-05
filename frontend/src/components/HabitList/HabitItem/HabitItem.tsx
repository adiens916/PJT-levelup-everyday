import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, Button, Stack } from '@mui/material';

import HabitItemMenu from '../HabitItemMenu/HabitItemMenu';
import { HabitDerivative } from '../../../utils/habitDerivative';
import { HabitType } from '../../../api/types';
import { TypographyByRatio } from './style';

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
          {/* 습관 숙련도 */}
          <TypographyByRatio ratio={habitDerivative.ratio}>
            Lv. {habitDerivative.level}
          </TypographyByRatio>

          {/* 습관 이름 */}
          <TypographyByRatio ratio={habitDerivative.ratio} variant="h5">
            {props.habit.name}
          </TypographyByRatio>
        </Stack>

        {/* 현재 목표 */}
        <TypographyByRatio
          ratio={habitDerivative.ratio}
          ratioThreshold={100}
          colorBefore="aquamarine"
          variant="h5"
        >
          {habitDerivative.goalWithUnit}
          {habitDerivative.goalLeftWithUnitAndMessage}
        </TypographyByRatio>
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
