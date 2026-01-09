"""
Validator Agent

Responsibility:
- Validate jurisdiction (England/Wales)
- Validate basic eligibility rules
- Reject unserviceable cases early
- Provide clear rejection explanations and next steps
"""

from typing import Dict


class ValidatorAgent:
    def __init__(self):
        self.name = "ValidatorAgent"

    def run(self, state: Dict) -> Dict:
        state.setdefault("explanation", [])
        state.setdefault("steps", [])

        message = state.get("message", "").lower()

        # Jurisdiction check
        if any(country in message for country in ["usa", "india", "canada", "australia"]):
            state["validation"] = {
                "eligible": False,
                "rejection_reason": "Outside England and Wales jurisdiction"
            }

            state["explanation"].append(
                "This case was rejected because the legal issue appears to fall outside "
                "the jurisdiction of England and Wales, which this service is limited to."
            )

            state["steps"].extend([
                "Contact a legal advice service or lawyer in the country where the issue occurred.",
                "If the matter later involves England or Wales, you may resubmit with updated details."
            ])

            return state

        # Passed validation
        state["validation"] = {
            "eligible": True
        }

        state["explanation"].append(
            "The case falls within England and Wales jurisdiction and is eligible to proceed "
            "to further legal triage."
        )

        state["steps"].append(
            "Your case will now be analysed to determine the relevant legal area and next actions."
        )

        return state
