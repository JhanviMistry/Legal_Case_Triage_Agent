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
    """
    LLM-FIRST legal reasoning agent.
    """

    def __init__(self, use_llm: bool = True):
        self.name = "ReasonerAgent"
        self.use_llm = use_llm

        if not os.getenv("GEMINI_API_KEY"):
            raise RuntimeError("GEMINI_API_KEY is required for reasoning")

        self.model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.2,
            google_api_key=os.getenv("GEMINI_API_KEY")
        )

    def run(self, state: Dict) -> Dict:
        message = state.get("message", "")

        reasoning = self._llm_reasoning(message)

        return {
            **state,
            "reasoning": reasoning,
            "reasoner_metadata": {
                "agent": self.name,
                "mode": "gemini"
            }
        }

    def _llm_reasoning(self, message: str) -> Dict:
        prompt = f"""
You are a legal intake reasoning agent for a UK legal advice clinic.

Your task:
- Identify the legal domain of the issue
- Assess confidence in classification
- Explain why the issue belongs to that domain
- Identify any missing information

Allowed domains:
HOUSING, EMPLOYMENT, IMMIGRATION, FAMILY, DEBT, BENEFITS, UNKNOWN

Rules:
- Do NOT give legal advice
- Do NOT suggest outcomes
- Do NOT cite laws
- ONLY classify and explain reasoning

Return STRICT JSON:
{{
  "domain": string,
  "confidence": number between 0 and 1,
  "why": string,
  "missing_info": [string]
}}

User message:
\"\"\"{message}\"\"\"
"""

        response = self.model.invoke(prompt)

        try:
            return json.loads(response.content)
        except Exception:
            return {
                "domain": "UNKNOWN",
                "confidence": 0.0,
                "why": "The system could not reliably classify the issue.",
                "missing_info": ["Clarify the legal issue and location"]
            }