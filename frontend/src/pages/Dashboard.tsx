import { useState, useEffect } from 'react';
import { getOutcomes } from '../api/client';
import { formatDate } from '../lib/utils';
import type { Outcome } from '../types';

function Dashboard() {
  const [outcomes, setOutcomes] = useState<Outcome[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchOutcomes = async () => {
      try {
        const data = await getOutcomes();
        setOutcomes(data);
      } catch (err) {
        setError('Failed to load outcomes');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchOutcomes();
  }, []);

  const getRiskColor = (score: number) => {
    if (score < 0.4) return 'text-green-600';
    if (score < 0.6) return 'text-yellow-600';
    if (score < 0.8) return 'text-orange-600';
    return 'text-red-600';
  };

  const avgPreRisk =
    outcomes.length > 0
      ? outcomes.reduce((sum, o) => sum + o.pre_risk, 0) / outcomes.length
      : 0;

  const avgPostRisk =
    outcomes.length > 0
      ? outcomes
          .filter((o) => o.post_risk)
          .reduce((sum, o) => sum + (o.post_risk || 0), 0) /
        outcomes.filter((o) => o.post_risk).length
      : 0;

  const riskImprovement = avgPreRisk - avgPostRisk;

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center">
        <h2 className="text-3xl font-bold text-slate-900">Outcome Dashboard</h2>
        <p className="mt-2 text-slate-600">
          Track retention actions and their impact on churn risk
        </p>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-600">{error}</p>
        </div>
      )}

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-sm text-slate-500">Total Outcomes</p>
          <p className="text-3xl font-bold text-slate-900">{outcomes.length}</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-sm text-slate-500">Avg Pre-Risk</p>
          <p className={`text-3xl font-bold ${getRiskColor(avgPreRisk)}`}>
            {(avgPreRisk * 100).toFixed(1)}%
          </p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-sm text-slate-500">Avg Post-Risk</p>
          <p className={`text-3xl font-bold ${getRiskColor(avgPostRisk)}`}>
            {avgPostRisk > 0 ? `${(avgPostRisk * 100).toFixed(1)}%` : 'N/A'}
          </p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-sm text-slate-500">Risk Improvement</p>
          <p
            className={`text-3xl font-bold ${
              riskImprovement > 0 ? 'text-green-600' : 'text-slate-900'
            }`}
          >
            {riskImprovement > 0 ? '+' : ''}
            {(riskImprovement * 100).toFixed(1)}%
          </p>
        </div>
      </div>

      {/* Outcomes Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="px-6 py-4 border-b border-slate-200">
          <h3 className="text-lg font-semibold text-slate-900">
            Outcome History
          </h3>
        </div>
        {loading ? (
          <div className="p-6 text-center text-slate-500">
            Loading outcomes...
          </div>
        ) : outcomes.length === 0 ? (
          <div className="p-6 text-center text-slate-500">
            No outcomes recorded yet. Use the Predict page to analyze employees.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-slate-200">
              <thead className="bg-slate-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                    Employee
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                    Pre-Risk
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                    Post-Risk
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                    Retention
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                    Date
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                    Notes
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-slate-200">
                {outcomes.map((outcome) => (
                  <tr key={outcome.id}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-slate-900">
                      {outcome.employee_id}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-900">
                      <span className={getRiskColor(outcome.pre_risk)}>
                        {(outcome.pre_risk * 100).toFixed(1)}%
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-900">
                      {outcome.post_risk ? (
                        <span className={getRiskColor(outcome.post_risk)}>
                          {(outcome.post_risk * 100).toFixed(1)}%
                        </span>
                      ) : (
                        <span className="text-slate-400">-</span>
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-900">
                      {outcome.retention_months ? (
                        `${outcome.retention_months} mo`
                      ) : (
                        <span className="text-slate-400">-</span>
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">
                      {formatDate(outcome.created_at)}
                    </td>
                    <td className="px-6 py-4 text-sm text-slate-500 max-w-xs truncate">
                      {outcome.notes || '-'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

export default Dashboard;
