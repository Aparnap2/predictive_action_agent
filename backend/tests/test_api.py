"""Tests for FastAPI endpoints."""
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


class TestHealthEndpoint:
    """Tests for health check endpoint."""

    @pytest.mark.asyncio
    async def test_health_check(self) -> None:
        """Test health check returns 200."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestPredictEndpoint:
    """Tests for prediction endpoint."""

    @pytest.mark.asyncio
    async def test_predict_single_employee(self) -> None:
        """Test prediction for single employee."""
        payload = {
            "employee_id": "EMP001",
            "department": "Engineering",
            "tenure_months": 24,
            "salary": 75000.0,
            "satisfaction": 4.0,
            "absences": 3,
            "performance": 4.5,
        }
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post("/api/predict", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "employee_id" in data
        assert "risk_score" in data
        assert "risk_tier" in data
        assert "factors" in data
        assert 0 <= data["risk_score"] <= 1

    @pytest.mark.asyncio
    async def test_predict_high_risk(self) -> None:
        """Test prediction identifies high-risk employee."""
        payload = {
            "employee_id": "EMP002",
            "department": "Sales",
            "tenure_months": 3,
            "salary": 50000.0,
            "satisfaction": 1.5,
            "absences": 12,
            "performance": 2.0,
        }
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post("/api/predict", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["risk_tier"] in ["HIGH", "CRITICAL"]
        assert data["risk_score"] >= 0.5

    @pytest.mark.asyncio
    async def test_predict_low_risk(self) -> None:
        """Test prediction identifies low-risk employee."""
        payload = {
            "employee_id": "EMP003",
            "department": "Engineering",
            "tenure_months": 60,
            "salary": 120000.0,
            "satisfaction": 4.5,
            "absences": 1,
            "performance": 4.8,
        }
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post("/api/predict", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["risk_tier"] == "LOW"
        assert data["risk_score"] <= 0.35

    @pytest.mark.asyncio
    async def test_predict_invalid_data(self) -> None:
        """Test prediction rejects invalid data."""
        payload = {
            "employee_id": "EMP001",
            "department": "Engineering",
            "tenure_months": -5,  # Invalid
            "salary": 75000.0,
            "satisfaction": 4.0,
            "absences": 3,
            "performance": 4.5,
        }
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post("/api/predict", json=payload)
        assert response.status_code == 422  # Validation error


class TestActEndpoint:
    """Tests for agent action endpoint."""

    @pytest.mark.asyncio
    async def test_act_returns_suggestions(self) -> None:
        """Test act endpoint returns action suggestions."""
        payload = {
            "employee_id": "EMP001",
            "risk_score": 0.75,
            "risk_tier": "HIGH",
            "confidence": 0.85,
            "factors": {
                "tenure_risk": 0.3,
                "satisfaction_risk": 0.5,
                "absence_risk": 0.4,
                "performance_risk": 0.3,
            },
        }
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post("/api/act", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "reasoning" in data
        assert "suggested_actions" in data
        assert isinstance(data["suggested_actions"], list)

    @pytest.mark.asyncio
    async def test_act_returns_priority_actions(self) -> None:
        """Test high risk returns high priority actions."""
        payload = {
            "employee_id": "EMP002",
            "risk_score": 0.9,
            "risk_tier": "CRITICAL",
            "confidence": 0.95,
            "factors": {
                "tenure_risk": 0.7,
                "satisfaction_risk": 0.8,
                "absence_risk": 0.6,
                "performance_risk": 0.5,
            },
        }
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post("/api/act", json=payload)
        assert response.status_code == 200
        data = response.json()
        # CRITICAL risk should have at least one high-priority action
        actions = data["suggested_actions"]
        assert len(actions) > 0
        priorities = [a["priority"] for a in actions]
        assert "high" in priorities or "critical" in priorities


class TestOutcomesEndpoint:
    """Tests for outcomes endpoint."""

    @pytest.mark.asyncio
    async def test_outcomes_returns_list(self) -> None:
        """Test outcomes endpoint returns a list."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/outcomes")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_outcomes_accepts_new(self) -> None:
        """Test outcomes endpoint accepts new entries."""
        payload = {
            "employee_id": "EMP001",
            "pre_risk": 0.75,
            "post_risk": 0.45,
            "retention_months": 6,
            "notes": "Retention actions taken",
        }
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post("/api/outcomes", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["employee_id"] == "EMP001"
        assert "id" in data


class TestUploadEndpoint:
    """Tests for CSV upload endpoint."""

    @pytest.mark.asyncio
    async def test_upload_rejects_non_csv(self) -> None:
        """Test upload rejects non-CSV files."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/api/predict/upload",
                files={"file": ("test.txt", b"not csv", "text/plain")},
            )
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_upload_accepts_csv(self) -> None:
        """Test upload accepts valid CSV."""
        csv_content = """employee_id,department,tenure_months,salary,satisfaction,absences,performance
EMP001,Engineering,24,75000,4.0,3,4.5
EMP002,Sales,12,60000,3.5,5,3.8"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/api/predict/upload",
                files={"file": ("test.csv", csv_content, "text/csv")},
            )
        assert response.status_code == 200
        data = response.json()
        assert "predictions" in data
        assert len(data["predictions"]) == 2
