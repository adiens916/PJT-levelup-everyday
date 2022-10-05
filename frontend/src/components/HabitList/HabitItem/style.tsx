import styled from '@emotion/styled';
import { Typography } from '@mui/material';
import type * as CSS from 'csstype';
import { customMediaQuery, get } from '../../../utils/utils';

export const TypographyByRatio = styled(Typography)<TypographyByRatioType>(
  (props) => ({
    color:
      props.ratio > get(props.ratioThreshold, 30)
        ? get(props.colorAfter, 'yellow')
        : get(props.colorBefore, 'turquoise'),

    [customMediaQuery(500)]: {
      fontSize: '1rem',
    },
  }),
);

interface TypographyByRatioType {
  ratio: number;
  ratioThreshold?: number;
  colorBefore?: CSS.Property.Color;
  colorAfter?: CSS.Property.Color;
}
