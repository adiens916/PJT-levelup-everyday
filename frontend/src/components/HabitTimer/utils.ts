export function ratio(numerator: number, denominator: number): number {
  if (denominator !== 0) {
    return Math.floor((numerator / denominator) * 100);
  } else {
    return 0;
  }
}
