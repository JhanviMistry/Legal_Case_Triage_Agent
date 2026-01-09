"""
Reasoner Agent

Responsibility:
- Classify legal domain
- Provide structured reasoning
- Runs in deterministic mode by default
- Supports Gemini-backed reasoning via feature flag
"""

from typing import Dict
import os

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
except ImportError:
    ChatGoogleGenerativeAI = None


class ReasonerAgent:
    def __init__(self, use_llm: bool = False):
        self.name = "ReasonerAgent"
        self.use_llm = use_llm

        if self.use_llm:
            if ChatGoogleGenerativeAI is None:
                raise ImportError(
                    "langchain-google-genai is required for Gemini reasoning"
                )

            self.model = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                temperature=0.3,
                google_api_key=os.getenv("GEMINI_API_KEY")
            )

    def run(self, state: Dict) -> Dict:
        state.setdefault("explanation", [])
        state.setdefault("steps", [])

        message = state.get("message", "")

        if self.use_llm:
            reasoning = self._gemini_reasoning(message)
            mode = "gemini"
        else:
            reasoning = self._deterministic_reasoning(message)
            mode = "deterministic"

        # ✅ Explain reasoning
        state["explanation"].append(
            f"The case was classified under the {reasoning['domain']} domain "
            f"with confidence {reasoning['confidence']}."
        )

        # Optional guidance (NOT routing)
        if reasoning["domain"] == "UNKNOWN":
            state["steps"].append(
                "Provide more details to help classify the legal issue."
            )

        state["reasoning"] = reasoning
        state["reasoner_metadata"] = {
            "agent": self.name,
            "mode": mode
        }

        return state


    # -------------------------
    # Deterministic reasoning
    # -------------------------
    def _deterministic_reasoning(self, message: str) -> Dict:
        text = message.lower()

        if any(k in text for k in ["eviction", "landlord", "tenant", "rent"]):
            domain = "HOUSING"
            confidence = 0.85
        elif any(k in text for k in ["job", "fired", "employer", "work"]):
            domain = "EMPLOYMENT"
            confidence = 0.85
        elif any(k in text for k in ["visa", "immigration", "asylum"]):
            domain = "IMMIGRATION"
            confidence = 0.85
        else:
            domain = "UNKNOWN"
            confidence = 0.4

        return {
            "domain": domain,
            "confidence": confidence,
            "summary": f"Detected {domain.lower()} related issue"
        }

    # -------------------------
    # Gemini-backed reasoning
    # -------------------------
    def _gemini_reasoning(self, message: str) -> Dict:
        prompt = f"""
You are a legal intake reasoning agent.

Classify the user's issue into one of:
- HOUSING
- EMPLOYMENT
- IMMIGRATION
- UNKNOWN

Return STRICT JSON with:
- domain (string)
- confidence (number between 0 and 1)
- summary (one sentence)

User message:
\"\"\"{message}\"\"\"
"""

        response = self.model.invoke(prompt)

        try:
            import json
            return json.loads(response.content)
        except Exception:
            return {
                "domain": "UNKNOWN",
                "confidence": 0.0,
                "summary": "Gemini response could not be parsed"
            }
