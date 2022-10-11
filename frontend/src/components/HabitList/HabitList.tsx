import React from 'react';
import { Link } from 'react-router-dom';
import { CircularProgress, Container, Typography } from '@mui/material';

import useDocumentTitle from '../../hook/useDocumentTitle';
import useHabitList from './useHabitList';
import HabitListContainerGroup from './HabitListContainerGroup/HabitListContainerGroup';
import { formatDateMmDd } from '../../utils/utils';

export default function HabitList() {
  useDocumentTitle('습관 목록');
  const { habits, loading, isError, errorCode } = useHabitList();

  return (
    <>
      <Container
        maxWidth="sm"
        sx={{ display: 'flex', flexDirection: 'column' }}
      >
        {/* 오늘 날짜 */}
        <Typography textAlign="center" fontSize="1.25rem">
          {formatDateMmDd()}
        </Typography>

        {/* 안내 메시지 */}
        {loading ? (
          <CircularProgress sx={{ alignSelf: 'center', marginTop: '1.5rem' }} />
        ) : errorCode === 403 || (!isError && habits && habits.length === 0) ? (
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
        {!loading && habits && habits.length && (
          <HabitListContainerGroup habits={habits} />
        )}
      </Container>
    </>
  );
}
