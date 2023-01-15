import React from 'react';
import { Typography } from '@mui/material';

import HabitItem from '../HabitItem/HabitItem';
import { HabitType } from '../../types';

export default function HabitListDueFirst({ habits }: { habits: HabitType[] }) {
  const is_exist_habit_due_date = () =>
    habits.some((habit) => habit.is_today_due_date);

  // 오늘의 습관을 모두 끝마쳐야 다른 습관들을 볼 수 있음
  const is_done_today_habits = () =>
    habits.every(
      (habit) => habit.is_today_due_date && habit.current_xp >= habit.goal_xp,
    );

  return (
    <>
      {is_exist_habit_due_date() ? (
        <>
          <Typography textAlign="center" fontSize="1.5rem">
            오늘의 습관
          </Typography>
          {habits.map((habit, index) => {
            if (habit.is_today_due_date)
              return <HabitItem habit={habit} key={index} />;
          })}

          {/* 오늘의 습관을 모두 끝내야 볼 수 있음 */}
          {is_done_today_habits() && (
            <>
              <Typography textAlign="center" fontSize="1.5rem" marginTop="5rem">
                내일의 습관
              </Typography>
              {habits.map((habit, index) => {
                if (!habit.is_today_due_date)
                  return <HabitItem habit={habit} key={index} />;
              })}
            </>
          )}
        </>
      ) : (
        <>
          {/* 습관 목록 */}
          {habits.map((habit, index) => (
            <HabitItem
              habit={habit}
              opacity={1 - 0.7 * (index / habits.length)}
              key={index}
            />
          ))}
        </>
      )}
    </>
  );
}
