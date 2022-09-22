import React from 'react';
import { IconButton, Stack, Typography } from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';

export default function InnerText(props: InnerTextType) {
  return (
    <>
      <Typography variant="h4" color="text.secondary">
        {`${Math.round(props.value)}%`}
      </Typography>
      <Stack direction="row" alignItems="center">
        <Typography variant="h5" color="text.secondary">
          {`${Math.round(props.value / 10)}분`}
        </Typography>
        <IconButton>
          <EditIcon />
        </IconButton>
      </Stack>
    </>
  );
}

interface InnerTextType {
  value: number;
}
