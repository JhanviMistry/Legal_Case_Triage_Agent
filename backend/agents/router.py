"""
Router Agent

Responsibility:
- Decide final routing destination
- Respect validation and reasoning output
- Produce explainable routing decisions
"""

from typing import Dict


class RouterAgent:
    def __init__(self):
        self.name = "RouterAgent"

        self.ROUTE_MAP = {
            "HOUSING": "Housing Legal Advice",
            "EMPLOYMENT": "Employment Legal Advice",
            "IMMIGRATION": "Immigration Legal Advice",
            "UNKNOWN": "General Legal Advice"
        }

    def run(self, state: Dict) -> Dict:
        state.setdefault("explanation", [])
        state.setdefault("steps", [])

        validation = state.get("validation", {})
        reasoning = state.get("reasoning", {})

        # If case is not eligible, do not route
        if not validation.get("eligible"):
            state["route"] = None

            state["explanation"].append(
                "The case was not routed because it did not meet eligibility requirements."
            )

            state["routing_metadata"] = {
                "agent": self.name,
                "status": "not_routed",
                "reason": validation.get("rejection_reason")
            }

            return state

        domain = reasoning.get("domain", "UNKNOWN")
        route = self.ROUTE_MAP.get(domain, "General Legal Advice")

        state["route"] = route

        state["explanation"].append(
            f"The case was routed to {route} based on the identified {domain.lower()} legal domain."
        )

        # Actionable next steps based on route
        if domain == "HOUSING":
            state["steps"].extend([
                "Contact a housing legal aid clinic or council housing service.",
                "Prepare your tenancy agreement, eviction notice, and rent records."
            ])
        elif domain == "EMPLOYMENT":
            state["steps"].extend([
                "Gather your employment contract and dismissal correspondence.",
                "Seek advice from an employment law advisor or ACAS."
            ])
        elif domain == "IMMIGRATION":
            state["steps"].extend([
                "Collect your visa and immigration documents.",
                "Consult an immigration advisor or solicitor."
            ])
        else:
            state["steps"].append(
                "Seek initial guidance from a general legal advice clinic."
            )

        state["routing_metadata"] = {
            "agent": self.name,
            "status": "routed",
            "domain": domain
        }

        return state
