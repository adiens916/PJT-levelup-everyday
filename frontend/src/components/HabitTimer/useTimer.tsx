import React, { useEffect, useState, useReducer } from 'react';
import { Button, ButtonProps } from '@mui/material';
import { getHabit, startTimer, finishTimer } from '../../api/api';
import { reducer, initialState } from './reducer';

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
            finishTimer(habitId, habit.today_progress);
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
