import React, { useEffect, useState } from 'react';
import {
  Box,
  CircularProgress,
  CircularProgressProps,
  Typography,
} from '@mui/material';

export default function CircularStatic() {
  const [progress, setProgress] = useState(10);

  useEffect(() => {
    const timer = setInterval(() => {
      setProgress((prevProgress) =>
        prevProgress >= 100 ? 0 : prevProgress + 10,
      );
    }, 800);
    return () => {
      console.log('unmount');

      clearInterval(timer);
    };
  }, []);

  return <CircularProgressWithLabel value={progress} />;
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
