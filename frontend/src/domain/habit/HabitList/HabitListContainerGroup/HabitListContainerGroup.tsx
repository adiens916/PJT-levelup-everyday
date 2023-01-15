import React from 'react';

import { Typography } from '@mui/material';

import HabitListContainer from '../HabitListContainer/HabitListContainer';
import HabitItem from '../HabitItem/HabitItem';
import { splitHabitsByStatus } from './utils';
import { HabitType } from '../../types';

export default function HabitListContainerGroup({
  habits,
}: {
  habits: HabitType[];
}) {
  const { habitsToDo, habitsDone, habitsNotDue } = splitHabitsByStatus(habits);

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
