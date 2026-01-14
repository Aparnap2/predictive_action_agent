"""Action execution tools for the agent."""
from datetime import datetime
from typing import Any

from app.agent.state import ActionToolInput


def create_alert(
    employee_id: str,
    description: str,
    priority: str,
    rationale: str,
) -> dict[str, Any]:
    """Create a high-priority alert for HR/management.

    Args:
        employee_id: The employee to alert about
        description: Alert description
        priority: Alert priority level
        rationale: Why this alert is being created

    Returns:
        Dict containing alert details
    """
    return {
        "action_id": f"alert_{employee_id}_{datetime.now().timestamp()}",
        "action_type": "alert",
        "description": description,
        "priority": priority,
        "employee_id": employee_id,
        "rationale": rationale,
        "timestamp": datetime.now().isoformat(),
        "status": "executed",
    }


def create_task(
    employee_id: str,
    description: str,
    priority: str,
    assignee: str = "manager",
    due_days: int = 7,
) -> dict[str, Any]:
    """Create a follow-up task for managers.

    Args:
        employee_id: The employee the task is about
        description: Task description
        priority: Task priority
        assignee: Who should complete the task
        due_days: Days until task is due

    Returns:
        Dict containing task details
    """
    due_date = datetime.now().timestamp() + (due_days * 86400)
    return {
        "action_id": f"task_{employee_id}_{datetime.now().timestamp()}",
        "action_type": "task",
        "description": description,
        "priority": priority,
        "employee_id": employee_id,
        "assignee": assignee,
        "due_date": due_date,
        "timestamp": datetime.now().isoformat(),
        "status": "pending",
    }


def schedule_meeting(
    employee_id: str,
    meeting_type: str,
    priority: str,
    rationale: str,
) -> dict[str, Any]:
    """Schedule a meeting with the employee.

    Args:
        employee_id: Employee to meet with
        meeting_type: Type of meeting (1:1, exit interview, etc.)
        priority: Meeting priority
        rationale: Why this meeting is needed

    Returns:
        Dict containing meeting details
    """
    return {
        "action_id": f"meeting_{employee_id}_{datetime.now().timestamp()}",
        "action_type": "meeting",
        "description": f"{meeting_type} with {employee_id}",
        "priority": priority,
        "employee_id": employee_id,
        "meeting_type": meeting_type,
        "rationale": rationale,
        "timestamp": datetime.now().isoformat(),
        "status": "pending",
    }


def recommend_compensation_review(
    employee_id: str,
    current_salary: float,
    priority: str,
    rationale: str,
) -> dict[str, Any]:
    """Flag for compensation review.

    Args:
        employee_id: Employee to review
        current_salary: Current salary
        priority: Review priority
        rationale: Why compensation review is needed

    Returns:
        Dict containing compensation review request
    """
    return {
        "action_id": f"compensation_{employee_id}_{datetime.now().timestamp()}",
        "action_type": "compensation",
        "description": f"Compensation review for {employee_id}",
        "priority": priority,
        "employee_id": employee_id,
        "current_salary": current_salary,
        "rationale": rationale,
        "timestamp": datetime.now().isoformat(),
        "status": "pending",
    }


def execute_action(input_data: ActionToolInput) -> dict[str, Any]:
    """Execute an action based on type.

    Args:
        input_data: Action specification

    Returns:
        Executed action details
    """
    action_type = input_data.action_type

    if action_type == "alert":
        return create_alert(
            employee_id=input_data.employee_id,
            description=input_data.description,
            priority=input_data.priority,
            rationale=input_data.rationale,
        )
    elif action_type == "task":
        return create_task(
            employee_id=input_data.employee_id,
            description=input_data.description,
            priority=input_data.priority,
        )
    elif action_type == "meeting":
        return schedule_meeting(
            employee_id=input_data.employee_id,
            meeting_type="1:1 check-in",
            priority=input_data.priority,
            rationale=input_data.rationale,
        )
    elif action_type == "compensation":
        return recommend_compensation_review(
            employee_id=input_data.employee_id,
            current_salary=0,  # Would come from employee context
            priority=input_data.priority,
            rationale=input_data.rationale,
        )
    else:
        # Default task creation
        return create_task(
            employee_id=input_data.employee_id,
            description=input_data.description,
            priority=input_data.priority,
        )
