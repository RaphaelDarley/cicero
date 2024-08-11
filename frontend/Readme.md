```AI Fact-Checking Tool~~~

***Overview***
    The AI Fact-Checking Tool is a web-based application designed to empower users with accurate information by analyzing and verifying the truthfulness of statements. By leveraging AI and machine learning models, the tool provides users with a detailed analysis of the input statement, including a verdict, certainty score, and any necessary corrections to false information. It also visualizes the logical process in a dynamic graph format.

***Features***
   Input Form: Users can input a statement they wish to fact-check.
   Result Display: The tool provides a clear and concise verdict on whether the statement is true or false. It also includes a certainty score and corrected facts if the statement is false.
   Graphical Representation: A dynamic graph is generated to visualize the logical process used in fact-checking, showing how different facts relate to the final conclusion.
   Responsive Design: The application is designed to be user-friendly and accessible on various devices.

Technology Stack

     Frontend:
React.js: For building the user interface.
react-d3-graph: For rendering the dynamic graph visualizations.
CSS: For styling the application.

     Backend:
FastAPI: For handling requests and processing data.
SurrealDB: For managing the database operations.
Python: For backend logic, including embedding, Wikipedia API integration, and AI model interactions.
AI Models:

Embedding model: Used to create vector representations of the input statement and facts.
Custom AI Flows: Used for splitting, analyzing, and verifying facts against known information.

***Usage***
Fact-Checking: Enter a statement in the input form and click "Check Fact." The tool will process the statement, interact with the backend, and display the results, including a dynamic graph showing the logical flow.
Graph Interaction: Click on any node in the graph to view additional details.
```
