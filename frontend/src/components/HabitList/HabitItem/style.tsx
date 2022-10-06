import styled from '@emotion/styled';
import { Typography, Stack } from '@mui/material';
import { customMediaQuery, get, mediaQueryMin } from '../../../utils/utils';
import type * as CSS from 'csstype';

export const TypographyByRatio = styled(Typography)<TypographyByRatioType>(
  (props) => ({
    color:
      props.ratio > get(props.ratioThreshold, 30)
        ? get(props.colorAfter, 'yellow')
        : get(props.colorBefore, 'turquoise'),
  }),

  {
    wordBreak: 'keep-all',
    [mediaQueryMin(550)]: {
      fontSize: '1.25rem',
    },
    [customMediaQuery(550)]: {
      fontSize: '1.25rem',
      // 요소가 두 개인 경우, 첫 번째 요소 크기를 줄임
      ':nth-last-of-type(2)': {
        fontSize: '1rem',
      },
    },
    [customMediaQuery(400)]: {
      fontSize: '1rem',
      ':nth-last-of-type(2)': {
        fontSize: '0.75rem',
      },
    },
  },
);

interface TypographyByRatioType {
  ratio: number;
  ratioThreshold?: number;
  colorBefore?: CSS.Property.Color;
  colorAfter?: CSS.Property.Color;
}

export const ResponsiveStack = styled(Stack)<ResponsiveStackType>({
  flexDirection: 'row',
  alignItems: 'center',

  [customMediaQuery(550)]: {
    flexDirection: 'column',
    ':first-of-type': {
      alignItems: 'start',
      textAlign: 'start',
    },
    ':last-of-type': {
      alignItems: 'end',
      textAlign: 'end',
    },
  },

  // 현재 선택자(&)로부터, 하위 Typography 클래스 지정
  '& .MuiTypography-root': {
    marginRight: '0.5rem',
  },
});

interface ResponsiveStackType {
  spacing?: number;
}
