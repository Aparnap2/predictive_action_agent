"""Tests for churn prediction models and logic."""
import pytest
from app.models.churn import (
    EmployeeInput,
    RiskFactors,
    PredictionResult,
    calculate_risk_score,
    classify_risk_tier,
)


class TestEmployeeInput:
    """Tests for EmployeeInput validation."""

    def test_valid_employee_input(self) -> None:
        """Test that valid employee data passes validation."""
        data = {
            "employee_id": "EMP001",
            "department": "Engineering",
            "tenure_months": 24,
            "salary": 75000.0,
            "satisfaction": 4.0,
            "absences": 3,
            "performance": 4.5,
        }
        employee = EmployeeInput(**data)
        assert employee.employee_id == "EMP001"
        assert employee.department == "Engineering"
        assert employee.tenure_months == 24

    def test_invalid_tenure_negative(self) -> None:
        """Test that negative tenure raises validation error."""
        data = {
            "employee_id": "EMP001",
            "department": "Engineering",
            "tenure_months": -5,
            "salary": 75000.0,
            "satisfaction": 4.0,
            "absences": 3,
            "performance": 4.5,
        }
        with pytest.raises(Exception):
            EmployeeInput(**data)

    def test_invalid_satisfaction_out_of_range(self) -> None:
        """Test that satisfaction > 5 raises validation error."""
        data = {
            "employee_id": "EMP001",
            "department": "Engineering",
            "tenure_months": 24,
            "salary": 75000.0,
            "satisfaction": 6.0,
            "absences": 3,
            "performance": 4.5,
        }
        with pytest.raises(Exception):
            EmployeeInput(**data)


class TestRiskFactors:
    """Tests for RiskFactors model."""

    def test_risk_factors_creation(self) -> None:
        """Test RiskFactors can be created with valid values."""
        factors = RiskFactors(
            tenure_risk=0.3,
            satisfaction_risk=0.5,
            absence_risk=0.2,
            performance_risk=0.4,
        )
        assert factors.tenure_risk == 0.3
        assert factors.satisfaction_risk == 0.5

    def test_risk_factors_default(self) -> None:
        """Test RiskFactors can use defaults for missing values."""
        factors = RiskFactors(
            tenure_risk=0.1,
            satisfaction_risk=0.1,
            absence_risk=0.1,
            performance_risk=0.1,
        )
        assert all(0 <= v <= 1 for v in factors.model_dump().values())


class TestRiskClassification:
    """Tests for risk tier classification."""

    def test_low_risk_tier(self) -> None:
        """Test LOW classification for low risk scores."""
        assert classify_risk_tier(0.2) == "LOW"
        assert classify_risk_tier(0.35) == "LOW"

    def test_medium_risk_tier(self) -> None:
        """Test MEDIUM classification for medium risk scores."""
        assert classify_risk_tier(0.4) == "MEDIUM"
        assert classify_risk_tier(0.55) == "MEDIUM"

    def test_high_risk_tier(self) -> None:
        """Test HIGH classification for high risk scores."""
        assert classify_risk_tier(0.6) == "HIGH"
        assert classify_risk_tier(0.75) == "HIGH"

    def test_critical_risk_tier(self) -> None:
        """Test CRITICAL classification for very high risk scores."""
        assert classify_risk_tier(0.8) == "CRITICAL"
        assert classify_risk_tier(0.95) == "CRITICAL"


class TestCalculateRiskScore:
    """Tests for risk score calculation."""

    def test_high_risk_employee(self) -> None:
        """Test calculation for high-risk employee profile."""
        # New employee, low satisfaction, high absences, low performance
        result = calculate_risk_score(
            tenure_months=3,
            satisfaction=1.5,
            absences=10,
            performance=2.0,
        )
        assert result >= 0.6  # Should be high risk

    def test_low_risk_employee(self) -> None:
        """Test calculation for low-risk employee profile."""
        # Senior employee, high satisfaction, low absences, high performance
        result = calculate_risk_score(
            tenure_months=60,
            satisfaction=4.5,
            absences=1,
            performance=4.5,
        )
        assert result <= 0.4  # Should be low risk

    def test_moderate_risk_employee(self) -> None:
        """Test calculation for moderate-risk employee profile."""
        result = calculate_risk_score(
            tenure_months=24,
            satisfaction=3.0,
            absences=5,
            performance=3.5,
        )
        assert 0.3 <= result <= 0.6  # Should be moderate

    def test_risk_score_bounds(self) -> None:
        """Test that risk score is always between 0 and 1."""
        # Test edge cases
        result = calculate_risk_score(
            tenure_months=0,
            satisfaction=0,
            absences=100,
            performance=0,
        )
        assert 0 <= result <= 1

        result = calculate_risk_score(
            tenure_months=120,
            satisfaction=5,
            absences=0,
            performance=5,
        )
        assert 0 <= result <= 1


class TestPredictionResult:
    """Tests for PredictionResult model."""

    def test_prediction_result_creation(self) -> None:
        """Test PredictionResult can be created with valid data."""
        factors = RiskFactors(
            tenure_risk=0.3,
            satisfaction_risk=0.4,
            absence_risk=0.2,
            performance_risk=0.3,
        )
        result = PredictionResult(
            employee_id="EMP001",
            risk_score=0.65,
            risk_tier="HIGH",
            confidence=0.85,
            factors=factors,
        )
        assert result.employee_id == "EMP001"
        assert result.risk_score == 0.65
        assert result.risk_tier == "HIGH"

    def test_prediction_result_serialization(self) -> None:
        """Test PredictionResult can be serialized to dict."""
        factors = RiskFactors(
            tenure_risk=0.3,
            satisfaction_risk=0.4,
            absence_risk=0.2,
            performance_risk=0.3,
        )
        result = PredictionResult(
            employee_id="EMP001",
            risk_score=0.65,
            risk_tier="HIGH",
            confidence=0.85,
            factors=factors,
        )
        data = result.model_dump()
        assert data["employee_id"] == "EMP001"
        assert data["risk_score"] == 0.65
