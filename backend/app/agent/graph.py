"""LangGraph agent workflow for churn prediction and actioning."""
from typing import Any

from langgraph.graph import StateGraph, END

from app.agent.state import AgentState


def create_action_suggestions(risk_tier: str, factors: dict[str, float]) -> list[dict[str, Any]]:
    """Generate action suggestions based on risk profile.

    Args:
        risk_tier: Risk tier classification
        factors: Individual risk factors

    Returns:
        List of action suggestions
    """
    actions = []

    # Always suggest a check-in for MEDIUM+ risk
    if risk_tier in ["MEDIUM", "HIGH", "CRITICAL"]:
        actions.append({
            "action_type": "meeting",
            "priority": "medium",
            "description": "Schedule 1:1 check-in with manager",
            "rationale": "Regular check-ins help identify issues early",
            "predicted_impact": "Improve satisfaction and engagement",
        })

    # High satisfaction risk -> engagement actions
    if factors.get("satisfaction_risk", 0) > 0.5:
        actions.append({
            "action_type": "task",
            "priority": "high",
            "description": "Conduct satisfaction survey and address concerns",
            "rationale": "Low satisfaction is a key churn indicator",
            "predicted_impact": "Identify and resolve pain points",
        })

    # High tenure risk -> onboarding/integration
    if factors.get("tenure_risk", 0) > 0.5:
        actions.append({
            "action_type": "task",
            "priority": "high",
            "description": "Review onboarding experience and mentorship",
            "rationale": "New employees need strong integration support",
            "predicted_impact": "Improve retention in first year",
        })

    # High absence risk -> wellness/check-in
    if factors.get("absence_risk", 0) > 0.5:
        actions.append({
            "action_type": "meeting",
            "priority": "medium",
            "description": "Discuss workload and wellness",
            "rationale": "High absence may indicate burnout or disengagement",
            "predicted_impact": "Address potential burnout",
        })

    # High performance risk -> performance support
    if factors.get("performance_risk", 0) > 0.5:
        actions.append({
            "action_type": "task",
            "priority": "medium",
            "description": "Provide performance coaching or training",
            "rationale": "Performance issues can lead to disengagement",
            "predicted_impact": "Improve performance and confidence",
        })

    # Critical risk -> HR alert
    if risk_tier == "CRITICAL":
        actions.append({
            "action_type": "alert",
            "priority": "critical",
            "description": "HR alert: High churn risk employee",
            "rationale": "Immediate attention required to prevent departure",
            "predicted_impact": "Enable proactive retention effort",
        })
        actions.append({
            "action_type": "compensation",
            "priority": "high",
            "description": "Evaluate compensation and benefits package",
            "rationale": "Competitive compensation can prevent departure",
            "predicted_impact": "Improve retention likelihood",
        })

    return actions


def generate_reasoning(prediction: dict, context: dict) -> str:
    """Generate agent reasoning for the prediction.

    Args:
        prediction: Prediction results
        context: Employee context

    Returns:
        Human-readable reasoning
    """
    risk_score = prediction.get("risk_score", 0)
    risk_tier = prediction.get("risk_tier", "UNKNOWN")
    factors = prediction.get("factors", {})

    reasoning_parts = [
        f"Employee {prediction.get('employee_id', 'Unknown')} has a churn risk score of {risk_score:.2f} ({risk_tier}).",
    ]

    # Explain key risk factors
    key_factors = []
    if factors.get("tenure_risk", 0) > 0.5:
        key_factors.append("tenure (new employee)")
    if factors.get("satisfaction_risk", 0) > 0.5:
        key_factors.append("satisfaction concerns")
    if factors.get("absence_risk", 0) > 0.5:
        key_factors.append("high absence rate")
    if factors.get("performance_risk", 0) > 0.5:
        key_factors.append("performance issues")

    if key_factors:
        reasoning_parts.append(f"Key risk drivers: {', '.join(key_factors)}.")
    else:
        reasoning_parts.append("No significant risk drivers identified.")

    # Add context if available
    if context:
        dept = context.get("department", "")
        if dept:
            reasoning_parts.append(f"Employee works in {dept}.")

    # Add recommendation summary
    if risk_tier in ["HIGH", "CRITICAL"]:
        reasoning_parts.append("Recommended actions focus on immediate intervention and retention.")
    elif risk_tier == "MEDIUM":
        reasoning_parts.append("Recommended actions focus on proactive engagement.")
    else:
        reasoning_parts.append("Standard retention practices recommended.")

    return " ".join(reasoning_parts)


def ingest_prediction_node(state: AgentState) -> AgentState:
    """Node: Ingest prediction data and prepare for reasoning."""
    prediction = state.get("prediction", {})
    context = state.get("employee_context", {})

    # Ensure prediction has required fields
    if not prediction.get("factors"):
        prediction["factors"] = {
            "tenure_risk": 0.3,
            "satisfaction_risk": 0.3,
            "absence_risk": 0.3,
            "performance_risk": 0.3,
        }

    return {
        **state,
        "prediction": prediction,
        "employee_context": context,
        "next_step": "reason",
    }


def reason_node(state: AgentState) -> AgentState:
    """Node: Generate reasoning and action suggestions."""
    prediction = state.get("prediction", {})
    context = state.get("employee_context", {})

    # Generate reasoning
    reasoning = generate_reasoning(prediction, context)

    # Generate action suggestions
    risk_tier = prediction.get("risk_tier", "MEDIUM")
    factors = prediction.get("factors", {})
    actions = create_action_suggestions(risk_tier, factors)

    return {
        **state,
        "reasoning": reasoning,
        "suggested_actions": actions,
        "next_step": "execute",
    }


def execute_node(state: AgentState) -> AgentState:
    """Node: Simulate action execution (auto-execute all actions)."""
    suggested = state.get("suggested_actions", [])
    executed = []

    for action in suggested:
        executed_action = {
            **action,
            "status": "executed",
            "executed_at": "auto",
        }
        executed.append(executed_action)

    return {
        **state,
        "executed_actions": executed,
        "outcome_notes": f"Auto-executed {len(executed)} actions",
        "next_step": "complete",
    }


def build_agent_graph() -> StateGraph:
    """Build the LangGraph agent workflow.

    Returns:
        Compiled StateGraph for the agent
    """
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("ingest", ingest_prediction_node)
    workflow.add_node("reason", reason_node)
    workflow.add_node("execute", execute_node)

    # Define edges
    workflow.set_entry_point("ingest")
    workflow.add_edge("ingest", "reason")
    workflow.add_edge("reason", "execute")
    workflow.add_edge("execute", END)

    return workflow
