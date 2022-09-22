import React, { useEffect, useState } from 'react';
import { Button, ButtonProps } from '@mui/material';
import { getHabit } from '../../api/api';
import { HabitResponseType } from '../../api/types';
import { Counter } from './timer';

export default function useTimer(habitId: number) {
  const [habit, setHabit] = useState<HabitResponseType>();
  const [progress, setProgress] = useState(0);
  const [running, setRunning] = useState(false);

  useEffect(() => {
    if (habitId) {
      getHabit(habitId).then((data) => {
        setHabit(data[0]);
        console.log(data[0]);
      });
    }
  }, []);

  const counter = React.useRef(new Counter());

  useEffect(() => {
    if (running) {
      counter.current.start((p) => {
        setProgress(p);
      });
      return () => {
        counter.current.stop();
      };
    }
  }, [running]);

  const StartStopButton = (props: ButtonProps) => (
    <Button onClick={() => setRunning(!running)} {...props}>
      {props.children}
    </Button>
  );

  return { habit, progress, StartStopButton };
}
