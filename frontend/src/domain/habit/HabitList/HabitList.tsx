import React from 'react';
import { Container, Typography } from '@mui/material';

import useDocumentTitle from 'common/hook';
import useHabitList from './useHabitList';
import ErrorGuide from './ErrorGuide/ErrorGuide';
import HabitListContainerGroup from './HabitListContainerGroup/HabitListContainerGroup';
import { formatDateMmDd } from 'utils/utils';

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
        <ErrorGuide
          habits={habits}
          loading={loading}
          isError={isError}
          errorCode={errorCode}
        />

        {/* 상태별로 정렬 */}
        {!loading && habits && habits.length !== 0 && (
          <HabitListContainerGroup habits={habits} />
        )}
      </Container>
    </>
  );
}
