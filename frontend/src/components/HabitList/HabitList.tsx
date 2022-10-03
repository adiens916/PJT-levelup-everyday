import React from 'react';
import { Container, Typography } from '@mui/material';

import HabitItem from './HabitItem/HabitItem';
import useHabitList from './useHabitList';

export default function HabitList() {
  const { habits, isError, errorCode } = useHabitList();

  const formatDateMMDD = () => {
    const today = new Date();
    const formatted = `${today.getMonth() + 1}월 ${today.getDate()}일`;
    return formatted;
  };

  const is_exist_habit_due_date = () =>
    habits.some((habit) => habit.is_today_due_date);

  // 오늘의 습관을 모두 끝마쳐야 다른 습관들을 볼 수 있음
  const is_done_today_habits = () =>
    habits.every(
      (habit) =>
        habit.is_today_due_date && habit.today_progress >= habit.today_goal,
    );

  return (
    <>
      <Container
        maxWidth="sm"
        sx={{ display: 'flex', flexDirection: 'column' }}
      >
        {/* 오늘 날짜 */}
        <Typography textAlign="center" fontSize="1.5rem">
          {formatDateMMDD()}
        </Typography>

        {isError && errorCode === 401 ? (
          <Typography textAlign="center" marginTop="2rem">
            로그인을 해주세요 (・-・)
          </Typography>
        ) : errorCode === 403 ? (
          <Typography textAlign="center" marginTop="2rem">
            새로운 습관을 만들어봅시다 ٩(ˊᗜˋ*)و
          </Typography>
        ) : (
          <>서버 접속 불량 (´；ω；｀)</>
        )}

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
                <Typography
                  textAlign="center"
                  fontSize="1.5rem"
                  marginTop="5rem"
                >
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
              <HabitItem habit={habit} key={index} />
            ))}
          </>
        )}
      </Container>
    </>
  );
}
