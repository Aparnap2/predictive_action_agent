"""Pydantic models for API request/response schemas."""
from pydantic import BaseModel, Field


class EmployeeInput(BaseModel):
    """Input model for employee data."""

    employee_id: str = Field(..., min_length=1, max_length=50)
    department: str = Field(..., min_length=1, max_length=100)
    tenure_months: int = Field(..., ge=0, le=360)
    salary: float = Field(..., ge=0)
    satisfaction: float = Field(..., ge=0, le=5)
    absences: int = Field(..., ge=0)
    performance: float = Field(..., ge=0, le=5)


class RiskFactors(BaseModel):
    """Breakdown of risk factors contributing to overall score."""

    tenure_risk: float = Field(..., ge=0, le=1)
    satisfaction_risk: float = Field(..., ge=0, le=1)
    absence_risk: float = Field(..., ge=0, le=1)
    performance_risk: float = Field(..., ge=0, le=1)


class PredictionResult(BaseModel):
    """Output model for prediction results."""

    employee_id: str
    risk_score: float = Field(..., ge=0, le=1)
    risk_tier: str  # LOW, MEDIUM, HIGH, CRITICAL
    confidence: float = Field(..., ge=0, le=1)
    factors: RiskFactors
    suggested_actions: list["ActionRecommendation"] = []


class ActionRecommendation(BaseModel):
    """Recommended action from agent reasoning."""

    action_type: str = Field(..., description="Type of action: alert, task, meeting, compensation")
    priority: str = Field(..., description="Priority: low, medium, high, critical")
    description: str = Field(..., description="Human-readable action description")
    rationale: str = Field(..., description="Why this action is recommended")
    predicted_impact: str = Field(..., description="Expected outcome of this action")


class ActionExecution(BaseModel):
    """Record of action execution."""

    action_id: str
    status: str = Field(..., description="pending, executed, skipped")
    executed_at: str | None = None


class OutcomeInput(BaseModel):
    """Input for logging outcome results."""

    employee_id: str
    action_id: str | None = None
    pre_risk: float
    post_risk: float | None = None
    retention_months: int | None = None
    notes: str = ""


class OutcomeResult(BaseModel):
    """Output model for outcome records."""

    id: str
    employee_id: str
    pre_risk: float
    post_risk: float | None
    retention_months: int | None
    notes: str
    created_at: str


# Update forward references
PredictionResult.model_rebuild()
