import React from "react";

function ResultDisplay({ result }) {
  if (!result) return null;

  if (result.error) {
    return <div className="error">{result.error}</div>;
  }

  return (
    <div className="result-display">
      <h2>Result</h2>
      <div className="verdict">
        <strong>Verdict:</strong> {result.isTrue ? "True" : "False"}
      </div>
      {result.certaintyScore && (
        <div className="certainty">
          <strong>Certainty:</strong> {result.certaintyScore}%
        </div>
      )}
      {!result.isTrue && result.correctedFact && (
        <div className="corrected-fact">
          <h3>Corrected Fact:</h3>
          <p>{result.correctedFact}</p>
        </div>
      )}
    </div>
  );
}

export default ResultDisplay;
