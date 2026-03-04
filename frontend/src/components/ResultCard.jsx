export default function ResultCard({ result }) {

  if (!result) return null;

  return (
    <div style={{marginTop: "20px"}}>
      <h3>Prediction</h3>

      <p>
        Department: <b>{result.department}</b>
      </p>

      <p>
        Priority: <b>{result.priority}</b>
      </p>
    </div>
  );
}