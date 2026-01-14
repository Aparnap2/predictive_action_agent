"""API routes for the Predictive Action Engine."""
from io import StringIO
from typing import Any

import pandas as pd
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse

from app.models.churn import predict_churn
from app.models.schemas import (
    EmployeeInput,
    PredictionResult,
    ActionRecommendation,
    OutcomeInput,
)
from app.agent.graph import build_agent_graph
from app.services.outcome_tracker import outcome_tracker


router = APIRouter()


@router.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}


@router.post("/predict", response_model=PredictionResult)
async def predict_employee_risk(employee: EmployeeInput) -> PredictionResult:
    """Predict churn risk for a single employee."""
    result = predict_churn(employee)
    return result


@router.post("/predict/upload")
async def upload_csv_predict(
    file: UploadFile = File(...),
) -> dict[str, Any]:
    """Upload CSV file for batch prediction."""
    # Validate file type
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a CSV")

    content = await file.read()
    try:
        df = pd.read_csv(StringIO(content.decode("utf-8")))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid CSV: {str(e)}")

    # Validate required columns
    required_columns = [
        "employee_id",
        "department",
        "tenure_months",
        "salary",
        "satisfaction",
        "absences",
        "performance",
    ]
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"Missing columns: {', '.join(missing)}",
        )

    predictions = []
    for _, row in df.iterrows():
        try:
            employee = EmployeeInput(
                employee_id=str(row["employee_id"]),
                department=str(row["department"]),
                tenure_months=int(row["tenure_months"]),
                salary=float(row["salary"]),
                satisfaction=float(row["satisfaction"]),
                absences=int(row["absences"]),
                performance=float(row["performance"]),
            )
            result = predict_churn(employee)
            predictions.append(result.model_dump())
        except Exception as e:
            # Skip problematic rows but log them
            predictions.append({
                "employee_id": str(row.get("employee_id", "unknown")),
                "error": str(e),
            })

    return {"predictions": predictions}


@router.post("/act")
async def trigger_agent_actions(
    prediction: dict[str, Any],
) -> dict[str, Any]:
    """Trigger agent reasoning and action selection."""
    # Build and run the agent graph
    graph = build_agent_graph()
    compiled = graph.compile()

    initial_state = {
        "prediction": prediction,
        "employee_context": {},
        "reasoning": "",
        "suggested_actions": [],
        "executed_actions": [],
        "outcome_notes": "",
        "next_step": "reason",
    }

    # Run the graph
    result = compiled.invoke(initial_state)

    return {
        "reasoning": result.get("reasoning", ""),
        "suggested_actions": result.get("suggested_actions", []),
        "executed_actions": result.get("executed_actions", []),
    }


@router.get("/outcomes")
async def get_outcomes() -> list[dict]:
    """Retrieve all outcome records."""
    outcomes = outcome_tracker.get_outcomes()
    return [o.model_dump() for o in outcomes]


@router.post("/outcomes", response_model=dict)
async def create_outcome(data: OutcomeInput) -> dict:
    """Create a new outcome record."""
    result = outcome_tracker.create_outcome(data)
    return result.model_dump()


@router.get("/outcomes/trend/{employee_id}")
async def get_employee_trend(employee_id: str) -> dict | None:
    """Get risk trend for a specific employee."""
    trend = outcome_tracker.get_employee_risk_trend(employee_id)
    return trend
