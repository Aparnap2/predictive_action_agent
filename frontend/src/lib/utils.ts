import type { Outcome } from '../types';

export const getRiskTrend = (outcomes: Outcome[]) => {
  if (outcomes.length === 0) return null;

  const sorted = [...outcomes].sort(
    (a, b) =>
      new Date(a.created_at).getTime() - new Date(b.created_at).getTime()
  );

  const first = sorted[0];
  const last = sorted[sorted.length - 1];

  if (first.pre_risk && last.post_risk) {
    return last.post_risk - first.pre_risk;
  }
  return null;
};

export const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
};

export const formatNumber = (num: number, decimals = 1) => {
  return num.toFixed(decimals);
};
