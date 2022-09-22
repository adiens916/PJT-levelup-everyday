import React, { useEffect, useState } from 'react';
import { Button, ButtonProps } from '@mui/material';
import { getHabit, startTimer, finishTimer } from '../../api/api';
import { HabitResponseType } from '../../api/types';
import { Counter } from './timer';

export default function useTimer(habitId: number) {
  const [habit, setHabit] = useState<HabitResponseType>();
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
      getHabit(habitId).then((habits) => {
        setHabit(habits[0]);
        console.log(habits[0]);
        counter.current = new Counter(habits[0]);
        setProgressAndRatio();
        setRunning(habits[0].fields.is_running);
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
