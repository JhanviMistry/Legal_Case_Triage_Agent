import { useState } from "react";
import { runTriage } from "./api";

import ChatInput from "./components/ChatInput";
import DecisionCard from "./components/DecisionCard";
import TriageSteps from "./components/TriageSteps";
import LoadingState from "./components/LoadingState";

import "./index.css";

function App() {
  const [message, setMessage] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async () => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await runTriage(message);
      setResult(response);
    } catch (err) {
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <h1>Agentic Case Triage AI</h1>

      <ChatInput
        value={message}
        onChange={setMessage}
        onSubmit={handleSubmit}
        disabled={loading}
      />

      {loading && <LoadingState />}

      {error && <div className="error-box">{error}</div>}

      {result && (
        <>
          <DecisionCard
            status={result.status}
            route={result.route}
            confidence={result.confidence}
          />

          <TriageSteps
            explanation={result.explanation}
            steps={result.steps}
          />
        </>
      )}
    </div>
  );
}

export default App;
