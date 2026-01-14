"""
API routes for Agentic Case Triage AI.

This module exposes a clean HTTP interface over the
agentic triage engine. It contains NO business logic.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

from backend.services.triage_engine import run_triage

router = APIRouter()


# ======================================================
# Request / Response Schemas
# ======================================================

class TriageRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=10,
        description="User-submitted case description"
    )


class TriageResponse(BaseModel):
    status: str
    route: Optional[str]
    confidence: float
    explanation: str
    steps: List[str]


# ======================================================
# Routes
# ======================================================

@router.post(
    "/triage",
    response_model=TriageResponse,
    summary="Run agentic case triage",
    tags=["Triage"]
)
def triage_case(payload: TriageRequest):
    """
    Runs the multi-agent triage engine on a user case.

    Returns:
    - status (ACCEPTED / REJECTED / NEEDS_MORE_INFO)
    - route (if accepted)
    - confidence score
    - explanation
    - agent reasoning trace
    """
    try:
        result = run_triage(payload.message)
        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)   # 👈 TEMPORARY
        )

