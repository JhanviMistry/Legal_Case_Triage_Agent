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
from backend.agents.explainer import ExplainerAgent



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
        self.explainer = ExplainerAgent()


        # Agent registry
        self.agent_registry = {
            "validator": self.validator,
            "reasoner": self.reasoner,
            "router": self.router,
            "explainer": self.explainer,
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
        Shape final API response.
        Assumes ExplainerAgent has already produced user-facing output.
        """

        validation = state.get("validation", {})
        reasoning = state.get("reasoning")

        if not reasoning:
            raise RuntimeError("Final response missing reasoning")

        explanation_list = state.get("explanation")
        steps = state.get("steps")

        if explanation_list is None or steps is None:
            raise RuntimeError("Final response missing explainer input")

        if not isinstance(explanation_list, list):
            raise RuntimeError("Explanation must be a list")

        explanation = " ".join(explanation_list)

        if explanation is None or steps is None:
            raise RuntimeError("Final response missing explainer output")

        confidence = reasoning.get("confidence")
        if confidence is None:
            raise RuntimeError("Final response missing confidence score")

        # Rejected case
        if not validation.get("eligible"):
            return {
                "status": "REJECTED",
                "route": None,
                "domain": reasoning.get("domain"),
                "confidence": float(confidence),
                "explanation": explanation,
                "steps": steps,
            }

        # Accepted case
        return {
            "status": "ACCEPTED",
            "route": state.get("route"),
            "domain": reasoning.get("domain"),
            "confidence": float(confidence),
            "explanation": explanation,
            "steps": steps,
        }



_engine = TriageEngine()


def run_triage(message: str) -> Dict:
    return _engine.run(message)
