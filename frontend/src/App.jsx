import React, { useState } from "react";
import InputForm from "./components/inputForm";
import ResultDisplay from "./components/resultDisplay";
import GraphDisplay from "./components/graphDisplay";

function App() {
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (statement) => {
    setIsLoading(true);
    try {
      const response = await fetch("http://localhost:8000/mock", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ statement }),
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error("Error:", error);
      setResult({ error: "An error occurred while processing your request." });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <h1>AI FACT CHECKER</h1>
      <InputForm onSubmit={handleSubmit} />
      {isLoading && <p>Loading...</p>}
      <ResultDisplay result={result} />
      {result && result.graphData && (
        <GraphDisplay graphData={result.graphData} />
      )}
    </div>
  );
}

export default App;
