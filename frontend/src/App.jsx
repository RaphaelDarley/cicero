import React, { useState } from "react";
import InputForm from "./components/inputForm";
import ResultDisplay from "./components/resultDisplay";
import GraphDisplay from "./components/graphDisplay";
import aiImage from "./assets/image.png";

function App() {
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (statement) => {
    setIsLoading(true);
    try {
      // Replace this with your actual API call
      const response = await fetch("https://cicero.darley.dev/api/newsletter_add", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: statement,
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
    <>
      <header className="header">
        <div className="black">
          <h4>Empowering you with accurate info</h4>
        </div>
        <div className="next"></div>
        <nav className="navbar">
          <ul className="navbar-list">
            <li className="navbar-item">Home</li>
            <li className="navbar-item">About</li>
            <li className="navbar-item">Check-Fact</li>
            <li className="navbar-item">Contact</li>
          </ul>
        </nav>
      </header>
      <div className="facts">Truth in an Age of Lies</div>
      <div className="content-wrapper">
        <div className="paragraph">
          <span>Fact-Check Your Statement with AI Precision</span>
          Enter any statement you want to verify, and let our AI tool give you
          an accurate verdict within seconds.
        </div>
        <div className="image">
          <img src={aiImage} alt="Apex" className="Ai" />
        </div>
      </div>
      <div className="heading1">
        <h1>Sign up for Updates</h1>
      </div>
      <div className="app-container">
        <InputForm onSubmit={handleSubmit} />
      </div>
    </>
  );
}

export default App;
