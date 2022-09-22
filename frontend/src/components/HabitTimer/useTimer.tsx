import React, { useEffect, useState } from 'react';
import { Button, ButtonProps } from '@mui/material';
import { getHabit } from '../../api/api';
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
      <Button onClick={() => setRunning(!running)} {...props}>
        {props.children}
      </Button>
    );
  }

  return { habit, ratio, progress, StartStopButton };
}
