"""
Memory Agent (SQLite)

Responsibility:
- Persist triage cases for audit & learning
- Store only structured, explainable metadata
- Never affect routing or decisions
"""

import sqlite3
import os
from typing import Dict
from datetime import datetime


class MemoryAgent:
    def __init__(self, db_path: str = None):
        self.name = "MemoryAgent"

        if db_path is None:
            db_path = os.path.join(
                os.path.dirname(__file__),
                "..",
                "data",
                "triage.db"
            )

        self.db_path = os.path.abspath(db_path)
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        self._init_db()

    def _init_db(self):
        """Create table if it doesn't exist"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cases (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    message TEXT,
                    domain TEXT,
                    eligible BOOLEAN,
                    route TEXT,
                    confidence REAL,
                    reasoning_mode TEXT,
                    created_at TEXT
                )
            """)
            conn.commit()

    def run(self, state: Dict) -> Dict:
        """Persist case metadata and return state unchanged"""

        state.setdefault("explanation", [])
        state.setdefault("steps", [])

        reasoning = state.get("reasoning", {})
        validation = state.get("validation", {})

        record = (
            state.get("message"),
            reasoning.get("domain"),
            validation.get("eligible"),
            state.get("route"),
            reasoning.get("confidence"),
            state.get("reasoner_metadata", {}).get("mode"),
            datetime.utcnow().isoformat()
        )

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO cases (
                    message,
                    domain,
                    eligible,
                    route,
                    confidence,
                    reasoning_mode,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, record)
            conn.commit()

        state["explanation"].append(
            "The case information was securely stored for audit and future improvement purposes."
        )

        state["memory_metadata"] = {
            "agent": self.name,
            "status": "persisted",
            "db_path": self.db_path
        }

        return state
