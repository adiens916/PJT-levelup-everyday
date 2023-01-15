import React, { useEffect, useState, useReducer } from 'react';

import { Button, ButtonProps } from '@mui/material';

import { reducer } from './reducer';
import { getHabit } from '../api/crudApi';
import { startTimer, finishTimer } from '../api/timerApi';
import { FinishTimerType, initialState, StartTimerType } from '../types';
import { Toast } from 'domain/layout/Alert/Toast';

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
    function isSuccessful(result: StartTimerType | FinishTimerType) {
      if ('success' in result && result.success) {
        return true;
      } else if ('id' in result && result.id) {
        return true;
      } else {
        return false;
      }
    }

    return (
      <Button
        onClick={async () => {
          let result = null;
          if (!habit.is_running) {
            result = await startTimer(habitId);
            if (isSuccessful(result)) {
              Toast.fire({ icon: 'success', title: 'started recording' });
            } else {
              Toast.fire({ icon: 'error', title: 'failed recording' });
            }
          } else {
            result = await finishTimer(habitId, habit.temporary_progress);
            if (isSuccessful(result)) {
              Toast.fire({ icon: 'success', title: 'finished recording' });
            } else {
              Toast.fire({ icon: 'error', title: 'failed recording' });
            }
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
