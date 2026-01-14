"""
Explainer Agent

Responsibility:
- Convert internal agent state into human-readable explanations
- Generate clear next steps
- Never change decisions or routing
"""

from typing import Dict, List


class ExplainerAgent:
    def __init__(self):
        self.name = "ExplainerAgent"

    def run(self, state: Dict) -> Dict:
        explanation: List[str] = []
        steps: List[str] = []

        validation = state.get("validation", {})
        reasoning = state.get("reasoning", {})
        route = state.get("route")

        domain = reasoning.get("domain", "UNKNOWN")
        confidence = reasoning.get("confidence", 0.5)

        # ----------------------------
        # Jurisdiction / eligibility
        # ----------------------------
        if not validation.get("eligible"):
            explanation.append(
                "The case cannot be progressed because it falls outside "
                "England and Wales jurisdiction or does not meet basic eligibility criteria."
            )

            reason = validation.get("rejection_reason")
            if reason:
                explanation.append(reason)

            steps.append(
                "Consider seeking legal advice within the appropriate country or jurisdiction."
            )

            return {
                **state,
                "explanation": explanation,
                "steps": steps,
                "explainer_metadata": {
                    "agent": self.name,
                    "status": "rejected"
                }
            }

        # ----------------------------
        # Accepted cases
        # ----------------------------
        explanation.append(
            "The case falls within England and Wales jurisdiction and is eligible for legal triage."
        )

        explanation.append(
            f"The issue appears to relate to {domain.lower()} law based on the information provided."
        )

        if route:
            explanation.append(
                f"The case has been routed to **{route}** for further handling."
            )
        else:
            explanation.append(
                "The system could not confidently determine a specialist legal route."
            )

        # ----------------------------
        # Confidence explanation
        # ----------------------------
        if confidence >= 0.8:
            explanation.append(
                "The system is highly confident in this assessment."
            )
        elif confidence >= 0.5:
            explanation.append(
                "The assessment was made with moderate confidence and may benefit from further details."
            )
        else:
            explanation.append(
                "The assessment has low confidence due to limited or unclear information."
            )

        # ----------------------------
        # Next steps
        # ----------------------------
        steps.append(
            "A legal advisor can now review your case using the provided summary."
        )

        if confidence < 0.6:
            steps.append(
                "You may be asked to provide additional details to improve the assessment."
            )

        steps.append(
            "Prepare any relevant documents (contracts, notices, correspondence) for review."
        )

        return {
            **state,
            "explanation": explanation,
            "steps": steps,
            "explainer_metadata": {
                "agent": self.name,
                "status": "explained"
            }
        }
