function DecisionCard({ status, route, confidence }) {
    const confidencePercent = Math.round(confidence * 100);
  
    const statusColor =
      status === "ACCEPTED"
        ? "status-accepted"
        : status === "REJECTED"
        ? "status-rejected"
        : "status-neutral";
  
    return (
      <div className={`decision-card ${statusColor}`}>
        <h2>Decision</h2>
  
        <div className="decision-row">
          <strong>Status:</strong>
          <span>{status}</span>
        </div>
  
        {route && (
          <div className="decision-row">
            <strong>Recommended Route:</strong>
            <span>{route}</span>
          </div>
        )}
  
        <div className="decision-row">
          <strong>Confidence:</strong>
          <span>{confidencePercent}%</span>
        </div>
      </div>
    );
  }
  
  export default DecisionCard;
  