import { useState } from "react";
import TicketForm from "./components/TicketForm";
import ResultCard from "./components/ResultCard";

function App() {
  const [result, setResult] = useState(null);

  return (
    <div
      style={{
        height: "100vh",
        width: "100%",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "flex-start",
        backgroundColor: "#f4f6f8",
        fontFamily: "Arial, sans-serif",
        paddingTop: "80px",
      }}
    >
      <h1
        style={{
          marginBottom: "30px",
          color: "#333",
        }}
      >
        AI Ticket Routing System
      </h1>

      <TicketForm setResult={setResult} />

      <ResultCard result={result} />
    </div>
  );
}

export default App;
