import React, { useEffect, useState, useReducer } from 'react';

import { Button, ButtonProps } from '@mui/material';

import { getHabit } from '../api/crudApi';
import { startTimer, finishTimer } from '../api/timerApi';
import { initialState } from '../types';
import { reducer } from './reducer';

export default function useTimer(habitId: number) {
  const [habit, dispatch] = useReducer(reducer, initialState);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    if (habitId && !loaded) {
      getHabit(habitId).then((habit) => {
        dispatch({ type: 'LOAD', state: habit });
        dispatch({ type: 'CONTINUE' });
        setLoaded(true);
      });
    }
  }, []);

  useEffect(() => {
    if (habit.is_running) {
      const timer = setInterval(() => {
        dispatch({ type: 'PROCEED' });
      }, 1000);
      return () => {
        clearInterval(timer);
      };
    }
  }, [habit.is_running]);

  function StartStopButton(props: ButtonProps) {
    return (
      <Button
        onClick={() => {
          if (!habit.is_running) {
            startTimer(habitId);
          } else {
            finishTimer(habitId, habit.temporary_progress);
          }
          dispatch({ type: 'RUN_OR_STOP' });
        }}
        {...props}
      >
        {props.children}
      </Button>
    );
  }

  return { habit, StartStopButton };
}
