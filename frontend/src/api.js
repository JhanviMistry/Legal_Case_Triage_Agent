/**
 * API layer for Agentic Case Triage AI
 * -----------------------------------
 * This file is the single source of truth
 * for backend communication.
 */

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

/**
 * Run case triage
 * @param {string} message - user case description
 * @returns {Promise<Object>} triage result
 */
export async function runTriage(message) {
  if (!message || message.trim().length < 10) {
    throw new Error("Message must be at least 10 characters long.");
  }

  const response = await fetch(`${API_BASE_URL}/triage`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(
      `Triage request failed (${response.status}): ${errorText}`
    );
  }

  return response.json();
}
