import React, { useEffect, useState } from "react";
import axios from "axios";

export default function Summary({ fileId }) {
  const [summary, setSummary] = useState(null);
  useEffect(() => {
    axios
      .get(`http://localhost:5000/api/summary/${fileId}`)
      .then((r) => setSummary(r.data));
  }, [fileId]);
  if (!summary) return null;
  return (
    <div style={{ marginTop: 20 }}>
      <h3>Summary</h3>
      <pre style={{ background: "#f5f5f5", padding: 10 }}>
        {JSON.stringify(summary, null, 2)}
      </pre>
    </div>
  );
}
