import React, { useEffect, useState } from 'react';
import {
  Box,
  Button,
  CircularProgress,
  CircularProgressProps,
  Typography,
} from '@mui/material';

export default function CircularStatic() {
  const [progress, setProgress] = useState(10);
  const [running, setRunning] = useState(true);

  useEffect(() => {
    if (running) {
      const timer = setInterval(() => {
        setProgress((prevProgress) =>
          prevProgress >= 100 ? 0 : prevProgress + 10,
        );
      }, 800);
      return () => {
        clearInterval(timer);
      };
    }
  }, [running]);

  return (
    <>
      <Typography variant="h4" textAlign="center" marginY={7}>
        독서
      </Typography>
      <Box display="flex" justifyContent="center">
        <CircularProgressWithLabel value={progress} />
      </Box>
      <Button
        onClick={() => setRunning(!running)}
        variant="contained"
        sx={{
          display: 'block',
          marginLeft: 'auto',
          marginRight: 'auto',
          marginTop: '5rem',
        }}
      >
        시작 / 중지
      </Button>
    </>
  );
}

function CircularProgressWithLabel(
  props: CircularProgressProps & { value: number },
) {
  return (
    <Box sx={{ position: 'relative', display: 'inline-flex' }}>
      <CircularProgress
        variant="determinate"
        size="70vw"
        thickness={2}
        {...props}
      />
      <Box
        sx={{
          position: 'absolute',
          top: 0,
          left: 0,
          bottom: 0,
          right: 0,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        <Typography variant="h4" color="text.secondary">
          {`${Math.round(props.value)}%`}
        </Typography>
      </Box>
    </Box>
  );
}

// export default function HabitTimer() {
//   return (
//     <div>HabitTimer</div>
//   )
// }
