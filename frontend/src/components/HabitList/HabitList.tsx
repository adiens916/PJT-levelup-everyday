import React from 'react';
import { CircularProgress, Container, Typography } from '@mui/material';

import HabitItem from './HabitItem/HabitItem';
import useHabitList from './useHabitList';
import useDocumentTitle from '../../hook/useDocumentTitle';
import { Link } from 'react-router-dom';

export default function HabitList() {
  useDocumentTitle('습관 목록');
  const { habits, loading, isError, errorCode } = useHabitList();

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

        {/* 안내 메시지 */}
        {loading ? (
          <CircularProgress sx={{ alignSelf: 'center', marginTop: '1.5rem' }} />
        ) : errorCode === 403 || (!isError && habits.length === 0) ? (
          <Typography textAlign="center" marginTop="2rem">
            <Link to="/create">새로운 습관</Link>을 만들어봅시다 ٩(ˊᗜˋ*)و
          </Typography>
        ) : errorCode === 401 ? (
          <Typography textAlign="center" marginTop="2rem">
            <Link to="/login">로그인</Link>을 해주세요 (・-・)
          </Typography>
        ) : (
          isError && (
            <Typography textAlign="center" marginTop="2rem">
              서버 연결 불가 (´；ω；｀)
            </Typography>
          )
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
