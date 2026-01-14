// Types for the Predictive Action Engine

export interface EmployeeInput {
  employee_id: string;
  department: string;
  tenure_months: number;
  salary: number;
  satisfaction: number;
  absences: number;
  performance: number;
}

export interface RiskFactors {
  tenure_risk: number;
  satisfaction_risk: number;
  absence_risk: number;
  performance_risk: number;
}

export interface PredictionResult {
  employee_id: string;
  risk_score: number;
  risk_tier: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  confidence: number;
  factors: RiskFactors;
  suggested_actions: ActionRecommendation[];
}

export interface ActionRecommendation {
  action_type: string;
  priority: string;
  description: string;
  rationale: string;
  predicted_impact: string;
}

export interface ActionExecution {
  action_id: string;
  status: 'pending' | 'executed' | 'skipped';
  executed_at?: string;
}

export interface AgentResult {
  reasoning: string;
  suggested_actions: ActionRecommendation[];
  executed_actions: ActionExecution[];
}

export interface Outcome {
  id: string;
  employee_id: string;
  pre_risk: number;
  post_risk?: number;
  retention_months?: number;
  notes: string;
  created_at: string;
}

export interface OutcomeInput {
  employee_id: string;
  action_id?: string;
  pre_risk: number;
  post_risk?: number;
  retention_months?: number;
  notes: string;
}

export interface RiskTrend {
  employee_id: string;
  avg_pre_risk: number;
  avg_post_risk: number;
  risk_improvement: number;
  outcome_count: number;
}

export interface UploadResult {
  predictions: PredictionResult[];
}
