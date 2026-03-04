import { useState } from "react";
import TicketForm from "./components/TicketForm";
import ResultCard from "./components/ResultCard";

function App() {

  const [result, setResult] = useState(null);

  return (
    <div style={{padding: "40px"}}>

      <h1>AI Ticket Routing System</h1>

      <TicketForm setResult={setResult} />

      <ResultCard result={result} />

    </div>
  );
}

export default App;