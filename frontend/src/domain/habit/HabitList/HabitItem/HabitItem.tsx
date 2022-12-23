import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, Button } from '@mui/material';

import HabitItemMenu from '../HabitItemMenu/HabitItemMenu';
import { HabitDerivative } from '../../habitDerivative';
import { HabitType } from '../../types';
import { ResponsiveStack, TypographyByRatio } from './style';

export default function HabitItem(props: HabitItemType) {
  const navigate = useNavigate();
  const habitDerivative = new HabitDerivative(props.habit);

  return (
    <Box
      sx={{
        display: 'flex',
        alignItems: 'center',
        opacity: props.opacity ? props.opacity : 1,
      }}
    >
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
        <ResponsiveStack>
          {/* 습관 숙련도 */}
          <TypographyByRatio ratio={habitDerivative.ratio}>
            Lv. {habitDerivative.level}
          </TypographyByRatio>

          {/* 습관 이름 */}
          <TypographyByRatio ratio={habitDerivative.ratio}>
            {props.habit.name}
          </TypographyByRatio>
        </ResponsiveStack>

        <ResponsiveStack>
          {/* 현재 목표 */}
          <TypographyByRatio
            ratio={habitDerivative.ratio}
            ratioThreshold={80}
            colorBefore="aquamarine"
          >
            {habitDerivative.goalWithUnit}
          </TypographyByRatio>
          {habitDerivative.goalLeftWithUnitAndMessage && (
            <TypographyByRatio
              ratio={habitDerivative.ratio}
              ratioThreshold={80}
              colorBefore="aquamarine"
            >
              {habitDerivative.goalLeftWithUnitAndMessage}
            </TypographyByRatio>
          )}
        </ResponsiveStack>
      </Button>
      <HabitItemMenu habit={props.habit} />
    </Box>
  );
}

interface HabitItemType {
  habit: HabitType;
  disabled?: boolean;
  opacity?: number;
}
