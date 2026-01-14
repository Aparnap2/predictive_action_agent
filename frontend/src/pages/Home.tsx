import { useState } from 'react';
import { predictEmployee, triggerAgent, uploadCSV } from '../api/client';
import type { PredictionResult, ActionRecommendation } from '../types';

function Home() {
  const [formData, setFormData] = useState({
    employee_id: '',
    department: 'Engineering',
    tenure_months: 12,
    salary: 75000,
    satisfaction: 3.5,
    absences: 5,
    performance: 3.5,
  });
  const [loading, setLoading] = useState(false);
  const [prediction, setPrediction] = useState<PredictionResult | null>(null);
  const [agentResult, setAgentResult] = useState<{
    reasoning: string;
    suggested_actions: ActionRecommendation[];
  } | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [file, setFile] = useState<File | null>(null);

  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name === 'department' ? value : Number(value),
    }));
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handlePredict = async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await predictEmployee(formData);
      setPrediction(result);
      setAgentResult(null);
    } catch (err) {
      setError('Failed to get prediction. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleAgentAction = async () => {
    if (!prediction) return;
    setLoading(true);
    try {
      const result = await triggerAgent(prediction);
      setAgentResult({
        reasoning: result.reasoning,
        suggested_actions: result.suggested_actions,
      });
    } catch (err) {
      setError('Failed to get agent actions. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);
    try {
      await uploadCSV(file);
      alert('File uploaded successfully!');
    } catch (err) {
      setError('Failed to upload file. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (tier: string) => {
    switch (tier) {
      case 'LOW':
        return 'bg-green-100 text-green-800';
      case 'MEDIUM':
        return 'bg-yellow-100 text-yellow-800';
      case 'HIGH':
        return 'bg-orange-100 text-orange-800';
      case 'CRITICAL':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-slate-100 text-slate-800';
    }
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center">
        <h2 className="text-3xl font-bold text-slate-900">
          Employee Churn Prediction
        </h2>
        <p className="mt-2 text-slate-600">
          Analyze employee risk and get AI-powered retention recommendations
        </p>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-600">{error}</p>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Input Form */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-slate-900 mb-4">
            Employee Data
          </h3>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-700">
                Employee ID
              </label>
              <input
                type="text"
                name="employee_id"
                value={formData.employee_id}
                onChange={handleInputChange}
                className="mt-1 block w-full rounded-md border-slate-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm border p-2"
                placeholder="EMP001"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700">
                Department
              </label>
              <select
                name="department"
                value={formData.department}
                onChange={handleInputChange}
                className="mt-1 block w-full rounded-md border-slate-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm border p-2"
              >
                <option value="Engineering">Engineering</option>
                <option value="Sales">Sales</option>
                <option value="Marketing">Marketing</option>
                <option value="HR">HR</option>
                <option value="Finance">Finance</option>
              </select>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-700">
                  Tenure (months)
                </label>
                <input
                  type="number"
                  name="tenure_months"
                  value={formData.tenure_months}
                  onChange={handleInputChange}
                  className="mt-1 block w-full rounded-md border-slate-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm border p-2"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700">
                  Salary ($)
                </label>
                <input
                  type="number"
                  name="salary"
                  value={formData.salary}
                  onChange={handleInputChange}
                  className="mt-1 block w-full rounded-md border-slate-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm border p-2"
                />
              </div>
            </div>
            <div className="grid grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-700">
                  Satisfaction (0-5)
                </label>
                <input
                  type="number"
                  step="0.1"
                  name="satisfaction"
                  min="0"
                  max="5"
                  value={formData.satisfaction}
                  onChange={handleInputChange}
                  className="mt-1 block w-full rounded-md border-slate-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm border p-2"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700">
                  Absences
                </label>
                <input
                  type="number"
                  name="absences"
                  value={formData.absences}
                  onChange={handleInputChange}
                  className="mt-1 block w-full rounded-md border-slate-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm border p-2"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700">
                  Performance (0-5)
                </label>
                <input
                  type="number"
                  step="0.1"
                  name="performance"
                  min="0"
                  max="5"
                  value={formData.performance}
                  onChange={handleInputChange}
                  className="mt-1 block w-full rounded-md border-slate-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm border p-2"
                />
              </div>
            </div>
            <button
              onClick={handlePredict}
              disabled={loading}
              className="w-full bg-primary-600 text-white py-2 px-4 rounded-md hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Analyzing...' : 'Analyze Risk'}
            </button>
          </div>
        </div>

        {/* CSV Upload */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-slate-900 mb-4">
            Batch Upload
          </h3>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-700">
                Upload CSV
              </label>
              <input
                type="file"
                accept=".csv"
                onChange={handleFileChange}
                className="mt-1 block w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-primary-50 file:text-primary-700 hover:file:bg-primary-100"
              />
            </div>
            <button
              onClick={handleFileUpload}
              disabled={loading || !file}
              className="w-full bg-slate-600 text-white py-2 px-4 rounded-md hover:bg-slate-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Uploading...' : 'Upload & Process'}
            </button>
          </div>
        </div>
      </div>

      {/* Results */}
      {prediction && (
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-semibold text-slate-900">
              Prediction Results
            </h3>
            <span
              className={`px-3 py-1 rounded-full text-sm font-semibold ${getRiskColor(
                prediction.risk_tier
              )}`}
            >
              {prediction.risk_tier} RISK
            </span>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <div className="bg-slate-50 rounded-lg p-4">
              <p className="text-sm text-slate-500">Risk Score</p>
              <p className="text-2xl font-bold text-slate-900">
                {(prediction.risk_score * 100).toFixed(1)}%
              </p>
            </div>
            <div className="bg-slate-50 rounded-lg p-4">
              <p className="text-sm text-slate-500">Confidence</p>
              <p className="text-2xl font-bold text-slate-900">
                {(prediction.confidence * 100).toFixed(1)}%
              </p>
            </div>
            <div className="bg-slate-50 rounded-lg p-4">
              <p className="text-sm text-slate-500">Tenure Risk</p>
              <p className="text-2xl font-bold text-slate-900">
                {(prediction.factors.tenure_risk * 100).toFixed(0)}%
              </p>
            </div>
            <div className="bg-slate-50 rounded-lg p-4">
              <p className="text-sm text-slate-500">Satisfaction Risk</p>
              <p className="text-2xl font-bold text-slate-900">
                {(prediction.factors.satisfaction_risk * 100).toFixed(0)}%
              </p>
            </div>
          </div>
          <button
            onClick={handleAgentAction}
            disabled={loading}
            className="bg-emerald-600 text-white py-2 px-4 rounded-md hover:bg-emerald-700 disabled:opacity-50"
          >
            {loading ? 'Processing...' : 'Get AI Recommendations'}
          </button>
        </div>
      )}

      {/* Agent Recommendations */}
      {agentResult && (
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-slate-900 mb-4">
            AI Recommendations
          </h3>
          <div className="bg-slate-50 rounded-lg p-4 mb-4">
            <p className="text-sm text-slate-500 mb-2">Reasoning</p>
            <p className="text-slate-700">{agentResult.reasoning}</p>
          </div>
          <div className="space-y-3">
            {agentResult.suggested_actions.map((action, index) => (
              <div
                key={index}
                className="border border-slate-200 rounded-lg p-4"
              >
                <div className="flex justify-between items-start">
                  <div>
                    <span
                      className={`inline-block px-2 py-1 text-xs font-semibold rounded mb-2 ${
                        action.priority === 'critical'
                          ? 'bg-red-100 text-red-800'
                          : action.priority === 'high'
                            ? 'bg-orange-100 text-orange-800'
                            : 'bg-blue-100 text-blue-800'
                      }`}
                    >
                      {action.priority.toUpperCase()}
                    </span>
                    <h4 className="font-medium text-slate-900">
                      {action.description}
                    </h4>
                    <p className="text-sm text-slate-600 mt-1">
                      {action.rationale}
                    </p>
                  </div>
                </div>
                <div className="mt-2 text-sm text-slate-500">
                  Expected Impact: {action.predicted_impact}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default Home;
