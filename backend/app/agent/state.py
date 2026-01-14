"""LangGraph agent state definitions."""
from typing import TypedDict, Literal, NotRequired

from pydantic import BaseModel

from app.models.schemas import PredictionResult, ActionRecommendation


class AgentState(TypedDict):
    """State for the LangGraph agent workflow."""

    prediction: dict
    employee_context: dict
    reasoning: str
    suggested_actions: list[dict]
    executed_actions: list[dict]
    outcome_notes: str
    next_step: Literal["reason", "execute", "complete"]


class ActionToolInput(BaseModel):
    """Input for action execution tool."""

    action_type: str
    description: str
    priority: str
    employee_id: str
    rationale: str
    predicted_impact: str
