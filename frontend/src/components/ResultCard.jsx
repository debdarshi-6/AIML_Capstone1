export default function ResultCard({ result }) {
  if (!result) return null;

  const getPriorityColor = (priority) => {
    switch (priority?.toLowerCase()) {
      case "low":
        return "#28a745"; // green
      case "medium":
        return "#f0ad4e"; // orange
      case "high":
        return "#d9534f"; // red
      default:
        return "#333";
    }
  };

  return (
    <div
      style={{
        marginTop: "25px",
        width: "420px",
        background: "white",
        padding: "20px",
        borderRadius: "10px",
        boxShadow: "0 5px 15px rgba(0,0,0,0.1)",
      }}
    >
      <h3
        style={{
          marginTop: 0,
          marginBottom: "15px",
          color: "#333",
          textAlign: "center",
        }}
      >
        Prediction Result
      </h3>

      <p style={{ fontSize: "16px" }}>
        Department:{" "}
        <span style={{ fontWeight: "bold", color: "#0077cc" }}>
          {result.Department}
        </span>
      </p>

      <p style={{ fontSize: "16px" }}>
        Priority:{" "}
        <span
          style={{
            fontWeight: "bold",
            color: getPriorityColor(result.priority),
            textTransform: "capitalize",
          }}
        >
          {result.Priority}
        </span>
      </p>
    </div>
  );
}