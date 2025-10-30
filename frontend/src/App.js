import React, { useState } from "react";

function App() {
  const [state1, setState1] = useState("");
  const [state2, setState2] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleCompare = async () => {
    if (!state1 || !state2) {
      setError("Please enter both states");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/compare?state1=${state1}&state2=${state2}`
      );
      if (!response.ok) throw new Error("Error fetching data");
      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError("Failed to fetch data. Please check backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px", fontFamily: "Arial" }}>
      <h1>🌾 Rainfall & Crop Production Comparison</h1>
      <p>Compare average rainfall and top crops between two Indian states</p>

      <input
        type="text"
        placeholder="Enter State 1"
        value={state1}
        onChange={(e) => setState1(e.target.value)}
        style={{ marginRight: "10px", padding: "8px" }}
      />
      <input
        type="text"
        placeholder="Enter State 2"
        value={state2}
        onChange={(e) => setState2(e.target.value)}
        style={{ marginRight: "10px", padding: "8px" }}
      />
      <button onClick={handleCompare} style={{ padding: "8px 16px" }}>
        Compare
      </button>

      {loading && <p>Loading...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {result && (
        <div style={{ marginTop: "30px" }}>
          <h2>📊 Comparison Results</h2>
          {result.states &&
            result.states.map((s, idx) => (
              <div
                key={idx}
                style={{
                  border: "1px solid #ddd",
                  borderRadius: "10px",
                  margin: "10px auto",
                  padding: "10px",
                  width: "400px",
                  textAlign: "left",
                }}
              >
                <h3>{s.name}</h3>
                <p>
                  <strong>Average Rainfall:</strong> {s.avg_rainfall} mm
                </p>
                <p>
                  <strong>Top Crops:</strong> {s.top_crops.join(", ")}
                </p>
              </div>
            ))}

          <p style={{ marginTop: "20px", fontSize: "14px", color: "gray" }}>
            Source: data.gov.in/agriculture | data.gov.in/IMD
          </p>
        </div>
      )}
    </div>
  );
}

export default App;
