import React from 'react';
import { Typography } from '@mui/material';

import HabitListContainer from '../HabitListContainer/HabitListContainer';
import HabitItem from '../HabitItem/HabitItem';
import { HabitDerivative } from 'utils/habitDerivative';
import { HabitType } from 'api/types';

export default function HabitListContainerGroup(
  props: HabitListContainerGroupType,
) {
  const { habitsToDo, habitsDone, habitsNotDue } =
    HabitDerivative.splitHabitsByStatus(props.habits);

  return (
    <>
      <HabitListContainer
        expanded={true}
        summary={'✨ 오늘의 습관'}
        details={habitsToDo.map((habit, index) => (
          <HabitItem
            habit={habit}
            opacity={1 - 0.7 * (index / habitsToDo.length)}
            key={index}
          />
        ))}
        detailsIfEmpty={
          <Typography textAlign="center" color="GrayText">
            전부 끝! 　(๑˃̵ᴗ˂̵)و
          </Typography>
        }
      />
      <HabitListContainer
        opacity={0.5}
        summary="🎉 달성한 습관"
        details={habitsDone.map((habit, index) => (
          <HabitItem habit={habit} key={index} />
        ))}
        detailsIfEmpty={
          <Typography textAlign="center" color="GrayText">
            없음 　(:3) ×)〆～～～
          </Typography>
        }
      />
      <HabitListContainer
        opacity={0.5}
        summary="🎵 나중에 할 습관"
        details={habitsNotDue.map((habit, index) => (
          <HabitItem habit={habit} key={index} />
        ))}
        detailsIfEmpty={
          <Typography textAlign="center" color="GrayText">
            없음 　(:3) ×)〆～～～
          </Typography>
        }
      />
    </>
  );
}

interface HabitListContainerGroupType {
  habits: HabitType[];
}
