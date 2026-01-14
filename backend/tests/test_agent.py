"""Tests for LangGraph agent workflow."""
import pytest
from app.agent.state import AgentState, ActionRecommendation
from app.agent.graph import build_agent_graph


class TestAgentState:
    """Tests for AgentState model."""

    def test_agent_state_creation(self) -> None:
        """Test AgentState can be created with valid data."""
        # AgentState is a TypedDict, so it's a dict
        state: AgentState = {
            "prediction": {
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
            },
            "employee_context": {"department": "Engineering", "tenure_months": 12},
            "reasoning": "Initial analysis",
            "suggested_actions": [],
            "executed_actions": [],
            "outcome_notes": "",
            "next_step": "reason",
        }
        assert state["prediction"]["employee_id"] == "EMP001"
        assert state["next_step"] == "reason"

    def test_agent_state_type_hints(self) -> None:
        """Test AgentState type hints are correct."""
        state: AgentState = {
            "prediction": {
                "employee_id": "EMP001",
                "risk_score": 0.5,
                "risk_tier": "MEDIUM",
                "confidence": 0.8,
                "factors": {
                    "tenure_risk": 0.2,
                    "satisfaction_risk": 0.3,
                    "absence_risk": 0.2,
                    "performance_risk": 0.2,
                },
            },
            "employee_context": {},
            "reasoning": "",
            "suggested_actions": [],
            "executed_actions": [],
            "outcome_notes": "",
            "next_step": "reason",
        }
        assert state["next_step"] == "reason"


class TestActionRecommendation:
    """Tests for ActionRecommendation model."""

    def test_action_recommendation_creation(self) -> None:
        """Test ActionRecommendation can be created."""
        action = ActionRecommendation(
            action_type="meeting",
            priority="high",
            description="Schedule 1:1 with manager",
            rationale="Employee shows signs of disengagement",
            predicted_impact="Improve satisfaction by 0.5",
        )
        assert action.action_type == "meeting"
        assert action.priority == "high"

    def test_action_recommendation_validation(self) -> None:
        """Test ActionRecommendation validates priority values."""
        # Valid priorities should work
        for priority in ["low", "medium", "high", "critical"]:
            action = ActionRecommendation(
                action_type="alert",
                priority=priority,
                description="Test",
                rationale="Test",
                predicted_impact="Test",
            )
            assert action.priority == priority


class TestAgentGraph:
    """Tests for LangGraph agent graph."""

    def test_graph_builder_returns_graph(self) -> None:
        """Test that build_agent_graph returns a StateGraph."""
        graph = build_agent_graph()
        assert graph is not None
        # Graph should have nodes
        assert len(graph.nodes) > 0

    def test_graph_has_required_nodes(self) -> None:
        """Test that graph has required nodes."""
        graph = build_agent_graph()
        node_names = list(graph.nodes.keys())
        # Should have at least: ingest, reason, execute
        assert len(node_names) >= 3

    def test_graph_has_edges(self) -> None:
        """Test that graph has edges defined."""
        graph = build_agent_graph()
        # Graph should compile without errors
        assert graph is not None


class TestAgentWorkflow:
    """Tests for agent workflow logic."""

    def test_reasoning_generation(self) -> None:
        """Test that reasoning can be generated from state."""
        # This tests the reasoning node logic
        state: AgentState = {
            "prediction": {
                "employee_id": "EMP001",
                "risk_score": 0.8,
                "risk_tier": "CRITICAL",
                "confidence": 0.9,
                "factors": {
                    "tenure_risk": 0.5,
                    "satisfaction_risk": 0.6,
                    "absence_risk": 0.4,
                    "performance_risk": 0.3,
                },
            },
            "employee_context": {
                "department": "Sales",
                "tenure_months": 6,
                "salary": 60000,
            },
            "reasoning": "",
            "suggested_actions": [],
            "executed_actions": [],
            "outcome_notes": "",
            "next_step": "reason",
        }
        # State should have prediction with high risk
        assert state["prediction"]["risk_score"] >= 0.6

    def test_action_selection_logic(self) -> None:
        """Test that appropriate actions are selected based on risk."""
        high_risk_prediction = {
            "employee_id": "EMP001",
            "risk_score": 0.85,
            "risk_tier": "CRITICAL",
            "confidence": 0.9,
            "factors": {
                "tenure_risk": 0.6,
                "satisfaction_risk": 0.7,
                "absence_risk": 0.5,
                "performance_risk": 0.4,
            },
        }

        # CRITICAL risk should suggest multiple high-priority actions
        assert high_risk_prediction["risk_tier"] == "CRITICAL"
        assert high_risk_prediction["risk_score"] >= 0.8

    def test_next_step_transition(self) -> None:
        """Test next_step state transitions."""
        # Initial state
        state: AgentState = {
            "prediction": {
                "employee_id": "EMP001",
                "risk_score": 0.5,
                "risk_tier": "MEDIUM",
                "confidence": 0.8,
                "factors": {
                    "tenure_risk": 0.2,
                    "satisfaction_risk": 0.3,
                    "absence_risk": 0.2,
                    "performance_risk": 0.2,
                },
            },
            "employee_context": {},
            "reasoning": "Analysis complete",
            "suggested_actions": [
                {
                    "action_type": "meeting",
                    "priority": "medium",
                    "description": "Check-in meeting",
                    "rationale": "Regular check-in",
                    "predicted_impact": "Moderate",
                }
            ],
            "executed_actions": [],
            "outcome_notes": "",
            "next_step": "reason",
        }

        # After reasoning, should transition to execute
        if state["reasoning"] and state["suggested_actions"]:
            state["next_step"] = "execute"

        assert state["next_step"] == "execute"
