import React from 'react';
import { Box, CircularProgress, CircularProgressProps } from '@mui/material';
import InnerText from '../InnerText/InnerText';

export default function CircularProgressWithLabel(
  props: CircularProgressProps & { value: number; progress: string },
) {
  return (
    <Box sx={{ position: 'relative', display: 'inline-flex' }}>
      <CircularProgress
        variant="determinate"
        size="40vh"
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
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        <InnerText ratio={props.value} progress={props.progress} />
      </Box>
    </Box>
  );
}
