import React from 'react';
import { Accordion, AccordionSummary, AccordionDetails } from '@mui/material';
import { ExpandMore } from '@mui/icons-material';
import { TypographyCentered } from '../style';

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
        <TypographyCentered fontWeight="bold">
          {props.summary}
        </TypographyCentered>
      </AccordionSummary>

      <AccordionDetails>
        {props.details.length ? props.details : props.detailsIfEmpty}
      </AccordionDetails>
    </Accordion>
  );
}

interface HabitListContainerType {
  summary: string;
  details: JSX.Element[];
  detailsIfEmpty?: JSX.Element;
  expanded?: boolean;
  opacity?: number;
}
