function TriageSteps({ explanation, steps }) {
    return (
      <div className="triage-steps">
        <h2>Explanation</h2>
        <p className="explanation-text">{explanation}</p>
  
        {steps && steps.length > 0 && (
          <>
            <h3>Next Steps</h3>
            <ul className="steps-list">
              {steps.map((step, index) => (
                <li key={index}>{step}</li>
              ))}
            </ul>
          </>
        )}
      </div>
    );
  }
  
  export default TriageSteps;
  