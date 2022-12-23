import React from 'react';
import { Accordion, AccordionSummary, AccordionDetails } from '@mui/material';
import { ExpandMore } from '@mui/icons-material';
import { TypographyCentered } from '../style';

export default function HabitListContainer(props: HabitListContainerType) {
  return (
    <Accordion
      defaultExpanded={props.expanded}
      sx={{ opacity: props.opacity ? props.opacity : 1 }}
    >
      <AccordionSummary expandIcon={<ExpandMore />}>
        <TypographyCentered fontWeight="bold">
          {props.summary}
        </TypographyCentered>
      </AccordionSummary>

      <AccordionDetails sx={{ padding: '0px 8px 8px' }}>
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
