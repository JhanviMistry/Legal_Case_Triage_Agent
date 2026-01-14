import { useState } from "react";

function ChatInput({ value, onChange, onSubmit, disabled }) {
  const [error, setError] = useState(null);

  const handleSubmit = () => {
    if (!value || value.trim().length < 10) {
      setError("Please describe your situation in at least 10 characters.");
      return;
    }

    setError(null);
    onSubmit();
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="chat-input-container">
      <textarea
        placeholder="Describe your legal issue..."
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={handleKeyDown}
        disabled={disabled}
        rows={4}
      />

      {error && <div className="input-error">{error}</div>}

      <button onClick={handleSubmit} disabled={disabled}>
        {disabled ? "Processing..." : "Submit Case"}
      </button>
    </div>
  );
}

export default ChatInput;
