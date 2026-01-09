"""
Planner Agent

Responsibility:
- Analyze the incoming case
- Decide which steps / agents should run
- Output an execution plan (ordered steps)

This agent does NOT make decisions.
It only plans the reasoning workflow.
"""

from typing import Dict, List


class PlannerAgent:
    def __init__(self):
        self.name = "PlannerAgent"

    def run(self, state: Dict) -> Dict:
        state.setdefault("explanation", [])
        state.setdefault("steps", [])

        message = state.get("message", "").lower()

        plan: List[str] = []

        # Step 1: Always validate jurisdiction & eligibility
        plan.append("validator")

        # Step 2: Decide if deeper reasoning is needed
        if any(keyword in message for keyword in [
            "eviction", "fired", "visa", "asylum", "job", "rent"
        ]):
            plan.append("reasoner")

        # Step 3: Route only if eligible
        plan.append("router")

        # Step 4: Persist case for learning / audit
        plan.append("memory")

        state["plan"] = plan

        state["explanation"].append(
            f"The system planned the following steps to process the case: {', '.join(plan)}."
        )

        state["planner_metadata"] = {
            "agent": self.name,
            "confidence": "high" if len(plan) > 3 else "medium"
        }

        return state
