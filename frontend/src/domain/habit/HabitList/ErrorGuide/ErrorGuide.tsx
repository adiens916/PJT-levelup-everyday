import React from 'react';
import { CircularProgress, Typography } from '@mui/material';
import { HabitType } from '../../types';
import { Link } from 'react-router-dom';

export default function ErrorGuide({
  habits,
  loading,
  isError,
  errorCode,
}: ErrorGuideType) {
  if (loading) {
    return (
      <CircularProgress sx={{ alignSelf: 'center', marginTop: '1.5rem' }} />
    );
  }

  if (!isError && habits && habits.length === 0) {
    return <EmptyHabitList />;
  }

  if (!isError) {
    return <></>;
  }

  switch (errorCode) {
    case 500:
      return <ConnectionError />;
    case 401:
      return <LoginRequired />;
    case 403:
      return <EmptyHabitList />;
    default:
      return <UnexpectedError />;
  }
}

function ConnectionError() {
  return (
    <Typography textAlign="center" marginTop="2rem">
      서버 연결 불가 (´；ω；｀)
    </Typography>
  );
}

function LoginRequired() {
  return (
    <Typography textAlign="center" marginTop="2rem">
      <Link to="/login">로그인</Link>을 해주세요 (・-・)
    </Typography>
  );
}

function EmptyHabitList() {
  return (
    <Typography textAlign="center" marginTop="2rem">
      <Link to="/create">새로운 습관</Link>을 만들어봅시다 ٩(ˊᗜˋ*)و
    </Typography>
  );
}

function UnexpectedError() {
  return (
    <Typography textAlign="center" marginTop="2rem">
      모르는 에러 (＃°Д°)Σ
    </Typography>
  );
}

interface ErrorGuideType {
  habits: HabitType[] | null;
  loading: boolean;
  isError: boolean;
  errorCode: number;
}
