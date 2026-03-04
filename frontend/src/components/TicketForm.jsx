import { useState } from "react";
import axios from "axios";

export default function TicketForm({ setResult }) {

  const [text, setText] = useState("");

  const handleSubmit = async () => {

    const response = await axios.post(
      "http://127.0.0.1:8000/predict",
      null,
      {
        params: { ticket_text: text }
      }
    );

    setResult(response.data);
  };

  return (
    <div>
      <h2>Support Ticket</h2>

      <textarea
        rows="5"
        placeholder="Describe your issue..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <br />

      <button onClick={handleSubmit}>
        Analyze Ticket
      </button>
    </div>
  );
}