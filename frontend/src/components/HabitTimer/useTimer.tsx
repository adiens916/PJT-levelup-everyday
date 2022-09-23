import React, { useEffect, useState } from 'react';
import { Button, ButtonProps } from '@mui/material';
import { getHabit, startTimer, finishTimer } from '../../api/api';
import { HabitType } from '../../api/types';
import { Counter } from './timer';

export default function useTimer(habitId: number) {
  const [habit, setHabit] = useState<HabitType>();
  const [progress, setProgress] = useState(0);
  const [ratio, setRatio] = useState(0);
  const [running, setRunning] = useState(false);
  const counter = React.useRef(new Counter());

  const setProgressAndRatio = () => {
    setProgress(counter.current.progress);
    setRatio(counter.current.ratio);
  };

  useEffect(() => {
    if (habitId) {
      getHabit(habitId).then((habit) => {
        setHabit(habit);
        console.log(habit);
        counter.current = new Counter(habit);
        setProgressAndRatio();
        setRunning(habit.is_running);
      });
    }
  }, []);

  useEffect(() => {
    if (running) {
      counter.current.start(setProgressAndRatio);
      return () => {
        counter.current.stop();
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
            finishTimer(habitId, progress);
          }
          setRunning(!running);
        }}
        {...props}
      >
        {props.children}
      </Button>
    );
  }

  return { habit, ratio, progress, running, StartStopButton };
}
