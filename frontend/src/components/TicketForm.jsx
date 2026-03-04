import { useState } from "react";
import { predictTicket } from "../services/api";

export default function TicketForm({ setResult }) {

  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {

    if (!text.trim()) return;

    setLoading(true);

    try {
      const data = await predictTicket(text);
      setResult(data);
    } catch (error) {
      console.error("Prediction failed:", error);
    }

    setLoading(false);
  };

  return (
    <div
      style={{
        width: "420px",
        background: "white",
        padding: "25px",
        borderRadius: "10px",
        boxShadow: "0 5px 15px rgba(0,0,0,0.1)",
        display: "flex",
        flexDirection: "column",
        gap: "15px",
      }}
    >
      <h2
        style={{
          margin: 0,
          color: "#444",
          textAlign: "center",
        }}
      >
        Submit Support Ticket
      </h2>

      <textarea
        rows="5"
        placeholder="Describe your issue..."
        value={text}
        onChange={(e) => setText(e.target.value)}
        style={{
          resize: "none",
          padding: "10px",
          borderRadius: "6px",
          border: "1px solid #ccc",
          fontSize: "14px",
          outline: "none",
        }}
      />

      <button
        onClick={handleSubmit}
        disabled={loading}
        style={{
          padding: "10px",
          backgroundColor: loading ? "#9ccc9c" : "#4CAF50",
          color: "white",
          border: "none",
          borderRadius: "6px",
          cursor: loading ? "not-allowed" : "pointer",
          fontSize: "15px",
          fontWeight: "bold",
        }}
      >
        {loading ? "Analyzing..." : "Analyze Ticket"}
      </button>

      {loading && (
        <p
          style={{
            textAlign: "center",
            color: "#666",
            fontSize: "14px",
          }}
        >
          AI is analyzing the ticket...
        </p>
      )}
    </div>
  );
}