from typing import Dict, List


class PlannerAgent:
    def __init__(self):
        self.name = "PlannerAgent"

    def run(self, state: Dict) -> Dict:
        """
        Produces a deterministic execution plan.
        Legal intake must always reason and explain.
        """

        plan: List[str] = [
            "validator",
            "reasoner",
            "router",
            "explainer",
            "memory"
        ]

        return {
            **state,
            "plan": plan,
            "planner_metadata": {
                "agent": self.name,
                "confidence": "high",
                "policy": "always_reason_and_explain"
            }
        }
