import React, { useEffect, useState } from 'react';
import { Button, ButtonProps } from '@mui/material';
import { getHabit, startTimer, finishTimer } from '../../api/api';
import { Counter } from './timer';

export default function useTimer(habitId: number) {
  const [counter, setCounter] = useState(new Counter());
  const [running, setRunning] = useState(false);

  useEffect(() => {
    if (habitId) {
      getHabit(habitId).then((habit) => {
        setCounter(new Counter(habit));
        setRunning(habit.is_running);
      });
    }
  }, []);

  useEffect(() => {
    if (running) {
      counter.start();
      return () => {
        counter.stop();
      };
    }
  }, [running]);

  function StartStopButton(props: ButtonProps) {
    return (
      <Button
        onClick={() => {
          if (!running) {
            startTimer(habitId);
          } else {
            finishTimer(habitId, counter.progress);
          }
          setRunning(!running);
        }}
        {...props}
      >
        {props.children}
      </Button>
    );
  }

  return { counter, running, StartStopButton };
}
