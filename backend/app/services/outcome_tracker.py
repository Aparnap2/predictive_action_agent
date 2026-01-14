"""Outcome tracking service (in-memory for MVP)."""
from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from app.models.schemas import OutcomeInput, OutcomeResult


class OutcomeTracker:
    """Simple in-memory outcome tracker for portfolio demo.

    In production, this would use PostgreSQL via Prisma.
    """

    def __init__(self) -> None:
        self._outcomes: list[dict] = []

    def create_outcome(self, input_data: OutcomeInput) -> OutcomeResult:
        """Create a new outcome record."""
        outcome = {
            "id": str(uuid4()),
            "employee_id": input_data.employee_id,
            "action_id": input_data.action_id,
            "pre_risk": input_data.pre_risk,
            "post_risk": input_data.post_risk,
            "retention_months": input_data.retention_months,
            "notes": input_data.notes,
            "created_at": datetime.now().isoformat(),
        }
        self._outcomes.append(outcome)
        return OutcomeResult(**outcome)

    def get_outcomes(self) -> list[OutcomeResult]:
        """Retrieve all outcomes."""
        return [OutcomeResult(**o) for o in self._outcomes]

    def get_outcomes_by_employee(self, employee_id: str) -> list[OutcomeResult]:
        """Get outcomes for a specific employee."""
        return [
            OutcomeResult(**o)
            for o in self._outcomes
            if o["employee_id"] == employee_id
        ]

    def get_employee_risk_trend(self, employee_id: str) -> Optional[dict]:
        """Get risk trend for an employee (pre vs post)."""
        employee_outcomes = self.get_outcomes_by_employee(employee_id)
        if not employee_outcomes:
            return None

        pre_risks = [o.pre_risk for o in employee_outcomes if o.pre_risk is not None]
        post_risks = [
            o.post_risk for o in employee_outcomes if o.post_risk is not None
        ]

        if not pre_risks or not post_risks:
            return None

        avg_pre = sum(pre_risks) / len(pre_risks)
        avg_post = sum(post_risks) / len(post_risks)
        improvement = avg_pre - avg_post

        return {
            "employee_id": employee_id,
            "avg_pre_risk": avg_pre,
            "avg_post_risk": avg_post,
            "risk_improvement": improvement,
            "outcome_count": len(employee_outcomes),
        }


# Global instance for demo
outcome_tracker = OutcomeTracker()
