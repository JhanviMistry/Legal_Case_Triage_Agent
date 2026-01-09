"""
Triage Engine

Responsibility:
- Orchestrate agent execution
- Respect planner-generated execution plan
- Maintain shared state
- Return final, explainable output
"""

import os
from typing import Dict, List

from backend.agents.planner import PlannerAgent
from backend.agents.validator import ValidatorAgent
from backend.agents.reasoner import ReasonerAgent
from backend.agents.router import RouterAgent
from backend.agents.memory import MemoryAgent


class TriageEngine:
    def __init__(self):
        # Feature flags
        use_llm_reasoner = os.getenv("USE_LLM_REASONER", "false").lower() == "true"

        # Initialize agents
        self.planner = PlannerAgent()
        self.validator = ValidatorAgent()
        self.reasoner = ReasonerAgent(use_llm=use_llm_reasoner)
        self.router = RouterAgent()
        self.memory = MemoryAgent()

        # Agent registry
        self.agent_registry = {
            "validator": self.validator,
            "reasoner": self.reasoner,
            "router": self.router,
            "memory": self.memory,
        }

    def run(self, message: str) -> Dict:
        """
        Execute the full triage workflow.
        """

        # Initial shared state
        state: Dict = {
            "message": message,
            "explanation": [],
            "steps": []
        }

        # 1️⃣ Planner decides execution steps
        state = self.planner.run(state)
        plan = state.get("plan", [])

        # 2️⃣ Execute planned agents in order
        for step in plan:
            agent = self.agent_registry.get(step)
            if not agent:
                continue

            state = agent.run(state)

            # Early stop if validation fails
            if step == "validator":
                validation = state.get("validation", {})
                if not validation.get("eligible"):
                    if "memory" in plan:
                        state = self.memory.run(state)
                    return self._final_response(state)

        # 3️⃣ Final response
        return self._final_response(state)

    def _final_response(self, state: Dict) -> Dict:
        """
        Normalize and shape final API response.
        """

        validation = state.get("validation", {})
        reasoning = state.get("reasoning", {})

        explanation: List[str] = state.get("explanation", [])
        steps: List[str] = state.get("steps", [])

        # Safety defaults
        confidence = reasoning.get("confidence")
        if confidence is None:
            confidence = 0.5

        if not explanation:
            explanation.append(
                "The case was reviewed by the triage system based on the information provided."
            )

        if not steps:
            steps.append(
                "Proceed with the recommended legal route or provide more details if needed."
            )

        # Rejected case
        if not validation.get("eligible"):
            explanation.append(
                validation.get("rejection_reason", "The case is not eligible for triage.")
            )

            return {
                "status": "REJECTED",
                "route": None,
                "confidence": float(confidence),
                "explanation": " ".join(explanation),
                "steps": steps,
            }

        # Accepted case
        return {
            "status": "ACCEPTED",
            "route": state.get("route"),
            "confidence": float(confidence),
            "explanation": " ".join(explanation),
            "steps": steps,
        }


_engine = TriageEngine()


def run_triage(message: str) -> Dict:
    return _engine.run(message)
