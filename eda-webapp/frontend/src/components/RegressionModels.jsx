import React, { useState } from "react";
import axios from "axios";

export default function RegressionModels({ fileId, trainCols, targetCol }) {
  const [model, setModel] = useState("linear");
  const [training, setTraining] = useState(false);
  const [result, setResult] = useState(null);

  const models = [
    { value: "linear", label: "Linear Regression" },
    { value: "ridge", label: "Ridge Regression" },
    { value: "lasso", label: "Lasso Regression" },
    { value: "decision_tree", label: "Decision Tree" },
    { value: "random_forest", label: "Random Forest" },
    { value: "logistic", label: "Logistic Regression" }, // Added
  ];

  const handleTrain = async () => {
    if (!trainCols.length || !targetCol) {
      alert("Please select training columns and a target column first.");
      return;
    }

    setTraining(true);
    setResult(null);

    try {
      // Save column selection in backend
      await axios.post(`http://localhost:5000/api/select_columns/${fileId}`, {
        train_columns: trainCols,
        target_column: targetCol,
      });

      // Train model
      const res = await axios.post(
        `http://localhost:5000/api/train_model/${fileId}`,
        { model }
      );

      setResult(res.data);
    } catch (err) {
      console.error(err);
      setResult({ error: err.response?.data?.error || "Training failed" });
    }

    setTraining(false);
  };

  return (
    <div style={{ marginTop: 20 }}>
      <h3>Train Regression / Classification Model</h3>

      {/* Model selector */}
      <select
        value={model}
        onChange={(e) => setModel(e.target.value)}
        style={{ padding: 5, marginRight: 10 }}
      >
        {models.map((m) => (
          <option key={m.value} value={m.value}>
            {m.label}
          </option>
        ))}
      </select>

      {/* Display selected columns */}
      <div style={{ margin: "10px 0" }}>
        <strong>Training Columns:</strong>{" "}
        {trainCols.length > 0 ? trainCols.join(", ") : "None selected"}
      </div>

      <div style={{ margin: "10px 0" }}>
        <strong>Target Column:</strong> {targetCol || "None selected"}
      </div>

      <button onClick={handleTrain} disabled={training}>
        {training ? "Training..." : "Train Model"}
      </button>

      {result && (
        <div style={{ marginTop: 20 }}>
          {result.error ? (
            <div style={{ color: "red" }}>Error: {result.error}</div>
          ) : (
            <div>
              <p>{result.message}</p>
              {result.score_type === "r2_score" && (
                <p>R² Score: {result.score}</p>
              )}
              {result.score_type === "accuracy" && (
                <p>Accuracy: {result.score}</p>
              )}
              <p>Train Columns: {result.train_columns.join(", ")}</p>
              <p>Target Column: {result.target_column}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
