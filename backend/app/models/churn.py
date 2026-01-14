"""Churn prediction logic and risk scoring."""
from typing import Annotated

from pydantic import AfterValidator

from app.models.schemas import EmployeeInput, RiskFactors, PredictionResult


def classify_risk_tier(risk_score: float) -> str:
    """Classify risk score into tier categories."""
    if risk_score < 0.4:
        return "LOW"
    elif risk_score < 0.6:
        return "MEDIUM"
    elif risk_score < 0.8:
        return "HIGH"
    else:
        return "CRITICAL"


def validate_risk_score(v: float) -> float:
    """Ensure risk score is between 0 and 1."""
    if not 0 <= v <= 1:
        raise ValueError(f"Risk score must be between 0 and 1, got {v}")
    return v


ValidatedRiskScore = Annotated[float, AfterValidator(validate_risk_score)]


def calculate_tenure_risk(tenure_months: int) -> float:
    """Calculate risk based on tenure.

    New employees are higher risk. Risk decreases with tenure.
    - 0-6 months: 0.7-1.0
    - 6-12 months: 0.5-0.7
    - 12-24 months: 0.3-0.5
    - 24-60 months: 0.1-0.3
    - 60+ months: 0.0-0.1
    """
    if tenure_months <= 3:
        return 0.9
    elif tenure_months <= 6:
        return 0.75
    elif tenure_months <= 12:
        return 0.55
    elif tenure_months <= 24:
        return 0.4
    elif tenure_months <= 60:
        return 0.25
    else:
        return 0.1


def calculate_satisfaction_risk(satisfaction: float) -> float:
    """Calculate risk based on satisfaction score (0-5).

    Lower satisfaction = higher risk.
    """
    # Invert: low satisfaction (0) -> high risk (1)
    # high satisfaction (5) -> low risk (0)
    return 1.0 - (satisfaction / 5.0)


def calculate_absence_risk(absences: int) -> float:
    """Calculate risk based on number of absences.

    More absences = higher risk.
    """
    if absences <= 2:
        return 0.1
    elif absences <= 5:
        return 0.3
    elif absences <= 8:
        return 0.5
    elif absences <= 12:
        return 0.7
    else:
        return 0.9


def calculate_performance_risk(performance: float) -> float:
    """Calculate risk based on performance score (0-5).

    Lower performance = higher risk.
    """
    # Invert: low performance (0) -> high risk (1)
    # high performance (5) -> low risk (0)
    return 1.0 - (performance / 5.0)


def calculate_risk_score(
    tenure_months: int,
    satisfaction: float,
    absences: int,
    performance: float,
) -> float:
    """Calculate overall risk score from employee metrics.

    Uses weighted average of individual risk factors.
    """
    tenure_factor = calculate_tenure_risk(tenure_months)
    satisfaction_factor = calculate_satisfaction_risk(satisfaction)
    absence_factor = calculate_absence_risk(absences)
    performance_factor = calculate_performance_risk(performance)

    # Weighted average (adjust weights as needed)
    weights = {
        "tenure": 0.25,
        "satisfaction": 0.30,
        "absence": 0.20,
        "performance": 0.25,
    }

    risk_score = (
        weights["tenure"] * tenure_factor
        + weights["satisfaction"] * satisfaction_factor
        + weights["absence"] * absence_factor
        + weights["performance"] * performance_factor
    )

    # Ensure bounds
    return max(0.0, min(1.0, risk_score))


def predict_churn(employee: EmployeeInput) -> PredictionResult:
    """Generate churn prediction for an employee."""
    risk_score = calculate_risk_score(
        tenure_months=employee.tenure_months,
        satisfaction=employee.satisfaction,
        absences=employee.absences,
        performance=employee.performance,
    )

    factors = RiskFactors(
        tenure_risk=calculate_tenure_risk(employee.tenure_months),
        satisfaction_risk=calculate_satisfaction_risk(employee.satisfaction),
        absence_risk=calculate_absence_risk(employee.absences),
        performance_risk=calculate_performance_risk(employee.performance),
    )

    # Calculate confidence based on data quality (simplified)
    confidence = 0.85  # Base confidence

    return PredictionResult(
        employee_id=employee.employee_id,
        risk_score=risk_score,
        risk_tier=classify_risk_tier(risk_score),
        confidence=confidence,
        factors=factors,
        suggested_actions=[],
    )
