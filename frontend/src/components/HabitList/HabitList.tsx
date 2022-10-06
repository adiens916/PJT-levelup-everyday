import React from 'react';
import { Link } from 'react-router-dom';
import { CircularProgress, Container, Typography } from '@mui/material';

import HabitItem from './HabitItem/HabitItem';
import useHabitList from './useHabitList';
import useDocumentTitle from '../../hook/useDocumentTitle';
import { HabitDerivative } from '../../utils/habitDerivative';
import HabitListContainer from './HabitListContainer/HabitListContainer';

export default function HabitList() {
  useDocumentTitle('습관 목록');
  const { habits, loading, isError, errorCode } = useHabitList();
  const { habitsToDo, habitsDone, habitsNotDue } =
    HabitDerivative.splitHabitsByStatus(habits);

  const formatDateMMDD = () => {
    const today = new Date();
    const formatted = `${today.getMonth() + 1}월 ${today.getDate()}일`;
    return formatted;
  };

  return (
    <>
      <Container
        maxWidth="sm"
        sx={{ display: 'flex', flexDirection: 'column' }}
      >
        {/* 오늘 날짜 */}
        <Typography textAlign="center" fontSize="1.25rem">
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

        {/* 상태별로 정렬 */}
        {!loading && (
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
        )}
      </Container>
    </>
  );
}
