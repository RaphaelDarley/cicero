import React, { useState } from "react";

function InputForm({ onSubmit }) {
  const [statement, setStatement] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(statement); // Pass data to the App component
    setStatement(""); // Clear input field
  };

  return (
    <form onSubmit={handleSubmit} className="input-form">
      <input
        type="text"
        name="text"
        className="input"
        value={statement}
        onChange={(e) => setStatement(e.target.value)}
        placeholder="Enter statement to fact check..."
        required
      />
      <button type="submit">Check Fact</button>
    </form>
  );
}

export default InputForm;
