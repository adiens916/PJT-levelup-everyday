import React from 'react';
import {
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Typography,
} from '@mui/material';
import { ExpandMore } from '@mui/icons-material';
import { LoadingCircle } from '../style';

export default function HabitListContainer(props: HabitListContainerType) {
  const [expanded, setExpanded] = React.useState(props.expanded ? true : false);

  const handleChange = () => {
    setExpanded(!expanded);
  };

  return (
    <Accordion
      expanded={expanded}
      onChange={handleChange}
      sx={{ opacity: props.opacity ? props.opacity : 1 }}
    >
      <AccordionSummary expandIcon={<ExpandMore />}>
        <Typography>{props.summary}</Typography>
      </AccordionSummary>

      <AccordionDetails>
        {props.details ? props.details : <LoadingCircle />}
      </AccordionDetails>
    </Accordion>
  );
}

interface HabitListContainerType {
  summary: string;
  details: JSX.Element[];
  expanded?: boolean;
  opacity?: number;
}
