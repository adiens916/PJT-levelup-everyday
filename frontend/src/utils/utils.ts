export function get<T>(a: T | undefined, b: T) {
  return a ? a : b;
}

export function formatDateMmDd() {
  const today = new Date();
  const formatted = `${today.getMonth() + 1}월 ${today.getDate()}일`;
  return formatted;
}

export function customMediaQuery(point: number) {
  return `@media (max-width: ${point}px)`;
}

export function mediaQueryMin(point: number) {
  return `@media (min-width: ${point}px)`;
}

const breakpoints = [0, 360, 500];
export const mediaQueries = breakpoints.map((point) => customMediaQuery(point));
