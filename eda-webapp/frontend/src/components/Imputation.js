import React, { useState, useEffect } from "react";
import API from "../api";

export default function Imputation({ fileId }) {
  const [suggestions, setSuggestions] = useState(null);

  useEffect(() => {
    API.get(`/suggest_imputation/${fileId}`).then((res) => setSuggestions(res.data));
  }, [fileId]);

  if (!suggestions) return null;

  return (
    <div className="mb-4">
      <h4>🧩 Imputation Suggestions</h4>
      <table className="table table-bordered table-sm">
        <thead>
          <tr>
            <th>Column</th>
            <th>Suggested Strategy</th>
            <th>Reason</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(suggestions).map(([col, val]) => (
            <tr key={col}>
              <td>{col}</td>
              <td>{val.suggested}</td>
              <td>{val.reason}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
