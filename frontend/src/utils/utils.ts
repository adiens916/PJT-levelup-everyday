export function get<T>(a: T | undefined, b: T) {
  return a ? a : b;
}

export function customMediaQuery(point: number) {
  return `@media (max-width: ${point}px)`;
}

const breakpoints = [0, 360, 500];
export const mediaQueries = breakpoints.map((point) => customMediaQuery(point));
