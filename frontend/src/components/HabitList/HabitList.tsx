import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, Container, Stack, Typography } from '@mui/material';

import { getHabits } from '../../api/api';
import { HabitType } from '../../api/types';
import { ratio } from '../../utils/utils';

export default function HabitList() {
  const navigate = useNavigate();
  const [habits, setHabits] = React.useState<HabitType[]>([]);

  React.useEffect(() => {
    getHabits().then((data) => setHabits(data));
  }, []);

  return (
    <>
      <Container
        sx={{ display: 'flex', flexDirection: 'column', width: '70%' }}
      >
        {/* 오늘 날짜 */}
        <Typography textAlign="center" fontSize="1.5rem">
          {new Date().toLocaleDateString('ko')}
        </Typography>

        {/* 습관 목록 */}
        {habits.map((habit, index) => {
          const level = Math.floor((habit.today_goal / habit.final_goal) * 100);
          const _ratio = ratio(habit.today_progress, habit.today_goal);
          return (
            <Button
              onClick={() => {
                navigate(`/timer/${habit.id}`);
              }}
              variant="outlined"
              sx={{
                display: 'flex',
                justifyContent: 'space-between',
                marginY: '1rem',
                padding: '0.5rem',
                background: `linear-gradient(90deg, ${
                  _ratio >= 50 ? 'dodgerblue' : 'aqua'
                } 0%, white ${_ratio}%)`,
              }}
              key={index}
            >
              <Stack direction="row" alignItems="center" spacing={2}>
                <Typography color={_ratio > 30 ? 'yellow' : 'turquoise'}>
                  Lv. {level}
                </Typography>
                {/* 습관 이름 */}
                <Typography
                  color={_ratio > 30 ? 'yellow' : 'turquoise'}
                  variant="h5"
                >
                  {habit.name}
                </Typography>
              </Stack>

              {/* 현재 달성률 */}
              <Typography
                color={_ratio >= 100 ? 'yellow' : 'aquamarine'}
                variant="h5"
              >
                {_ratio}%
              </Typography>
            </Button>
          );
        })}
      </Container>
    </>
  );
}
