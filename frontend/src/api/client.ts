import axios from 'axios';
import type {
  EmployeeInput,
  PredictionResult,
  AgentResult,
  Outcome,
  OutcomeInput,
  RiskTrend,
  UploadResult,
} from '../types';

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Health check
export const healthCheck = async (): Promise<{ status: string }> => {
  const response = await api.get('/health');
  return response.data;
};

// Prediction endpoints
export const predictEmployee = async (
  employee: EmployeeInput
): Promise<PredictionResult> => {
  const response = await api.post('/predict', employee);
  return response.data;
};

export const uploadCSV = async (file: File): Promise<UploadResult> => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await api.post('/predict/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
};

// Agent action endpoints
export const triggerAgent = async (
  prediction: PredictionResult
): Promise<AgentResult> => {
  const response = await api.post('/act', prediction);
  return response.data;
};

// Outcome endpoints
export const getOutcomes = async (): Promise<Outcome[]> => {
  const response = await api.get('/outcomes');
  return response.data;
};

export const createOutcome = async (
  outcome: OutcomeInput
): Promise<Outcome> => {
  const response = await api.post('/outcomes', outcome);
  return response.data;
};

export const getEmployeeTrend = async (
  employeeId: string
): Promise<RiskTrend | null> => {
  const response = await api.get(`/outcomes/trend/${employeeId}`);
  return response.data;
};

export default api;
