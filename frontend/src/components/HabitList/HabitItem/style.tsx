import styled from '@emotion/styled';
import { Typography } from '@mui/material';
import type * as CSS from 'csstype';

export const TypographyByRatio = styled(Typography)<TypographyByRatioType>(
  (props) => ({
    color:
      props.ratio > get(props.ratioThreshold, 30)
        ? get(props.colorAfter, 'yellow')
        : get(props.colorBefore, 'turquoise'),
  }),
);

function get<T>(a: T | undefined, b: T) {
  return a ? a : b;
}

interface TypographyByRatioType {
  ratio: number;
  ratioThreshold?: number;
  colorBefore?: CSS.Property.Color;
  colorAfter?: CSS.Property.Color;
}
