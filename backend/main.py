"""
Main application entry point for Agentic Case Triage AI.

- Initializes FastAPI app
- Registers API routes
- Enables CORS for frontend
- Serves React static files (for Hugging Face / Docker)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from dotenv import load_dotenv

from backend.api import router as triage_router

load_dotenv()

# ======================================================
# App Initialization
# ======================================================

app = FastAPI(
    title="Agentic Case Triage AI",
    description="A multi-agent system for autonomous case triage",
    version="1.0.0"
)

# ======================================================
# CORS (for React / external frontends)
# ======================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================================================
# API Routes
# ======================================================

app.include_router(triage_router)

# ======================================================
# Static Frontend (React build)
# ======================================================

FRONTEND_DIST = "frontend/dist"

if os.path.isdir(FRONTEND_DIST):
    app.mount(
        "/",
        StaticFiles(directory=FRONTEND_DIST, html=True),
        name="frontend"
    )

    @app.get("/{full_path:path}")
    def serve_react_app(full_path: str):
        """
        Catch-all route to serve React SPA.
        """
        index_path = os.path.join(FRONTEND_DIST, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        return {"detail": "Frontend not built."}


# ======================================================
# Health Check
# ======================================================

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
