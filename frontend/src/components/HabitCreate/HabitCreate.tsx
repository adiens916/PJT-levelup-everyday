import React, { useState } from 'react';
import { Button, MenuItem, Stack, TextField, Typography } from '@mui/material';
import { Container } from '@mui/system';

import { initialState } from '../HabitTimer/reducer';
import { HabitType } from '../../api/types';
import { createHabit } from '../../api/api';
import { useNavigate } from 'react-router-dom';
type HabitKeyType = keyof HabitType;
// interface HabitCreateType extends HabitType {
//   final_goal: number | null;
//   day_cycle: number | null;
// }

const defaultState: HabitType = {
  ...initialState,
  estimate_unit: 'SECOND',
  day_cycle: 1,
};

export default function HabitCreate() {
  const navigate = useNavigate();
  const [habit, setHabit] = useState(defaultState);

  function changeValue(keyword: HabitKeyType, value: string) {
    setHabit((habit) => ({ ...habit, [keyword]: value }));
  }

  const [open, setOpen] = useState(false);

  return (
    <Container sx={{ marginTop: '10vh' }}>
      <Stack direction="column" spacing={3}>
        <TextField
          label="습관 이름"
          value={habit.name}
          onChange={(event) => {
            changeValue('name', event.target.value);
          }}
          required
        />

        <TextField
          select
          label="측정 방식"
          onChange={(event) => {
            changeValue('estimate_type', event.target.value as string);
          }}
          value={habit.estimate_type}
          required
        >
          <MenuItem value="TIME">시간</MenuItem>
          <MenuItem value="COUNT">개수</MenuItem>
        </TextField>

        <Stack direction="row">
          <TextField
            label="최종 목표"
            value={habit.final_goal}
            onChange={(event) => {
              changeValue('final_goal', event.target.value);
            }}
            required
            sx={{ flex: 'auto' }}
          />

          {habit.estimate_type === 'TIME' && (
            <TextField
              select
              label="측정 단위"
              value={habit.estimate_unit}
              onChange={(event) => {
                changeValue('estimate_unit', event.target.value);
              }}
              required
              sx={{ width: '30%' }}
            >
              <MenuItem value="HOUR">시간</MenuItem>
              <MenuItem value="MINUTE">분</MenuItem>
              <MenuItem value="SECOND">초</MenuItem>
            </TextField>
          )}

          {habit.estimate_type === 'COUNT' && (
            <TextField
              label="측정 단위"
              value={habit.estimate_unit}
              onChange={(event) => {
                changeValue('estimate_unit', event.target.value);
              }}
              required
              sx={{ width: '30%' }}
            />
          )}
        </Stack>

        {/* <TextField
          label="초기치"
          value={parseInt(habit.final_goal) * 0.01}
          onChange={(event) => {
            changeValue('name', event.target.value);
          }}
          required
        /> */}

        <TextField
          select
          label="증감 유형"
          onChange={(event) => {
            changeValue('growth_type', event.target.value as string);
          }}
          value={habit.growth_type}
          required
        >
          <MenuItem value="INCREASE">증가</MenuItem>
          <MenuItem value="DECREASE">감소</MenuItem>
        </TextField>

        <Stack direction="row" alignItems="center">
          <TextField
            label="반복 주기"
            value={habit.day_cycle}
            onChange={(event) => {
              changeValue('day_cycle', event.target.value);
            }}
            sx={{ width: '70%' }}
          />
          <Typography>일마다</Typography>
        </Stack>

        <Button
          onClick={async () => {
            const isConfirmed = confirm('추가하시겠습니까?');
            if (isConfirmed) {
              const result = await createHabit(habit);
              if (result.id) {
                navigate('/');
              }
            }
          }}
          variant="contained"
          sx={{ fontSize: '1.5rem' }}
        >
          추가
        </Button>

        <Button
          onClick={() => {
            setOpen(!open);
          }}
          variant="contained"
          color={!open ? 'primary' : 'secondary'}
        >
          {!open ? '옵션 더 보기' : '옵션 닫기'}
        </Button>

        {open && (
          <>
            <TextField
              label="증감치"
              defaultValue={habit.final_goal * 0.01}
              value={habit.growth_amount}
              onChange={(event) => {
                changeValue('growth_amount', event.target.value);
              }}
              required
            />
            <Typography>
              처음 목표치는, 최종 목표치의 1% 부터 시작합니다. <br />
              (예: 100개가 최종 목표인 경우, 1개부터 시작) <br />
              목표 증감치도 1%부터 시작합니다. <br />
              (예: 1개씩 증가)
            </Typography>
          </>
        )}
      </Stack>
    </Container>
  );
}
