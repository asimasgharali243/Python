import React, { useEffect, useState } from "react";
import {
  Table,
  Button,
  Spinner,
  Alert,
  Dropdown,
  DropdownButton,
} from "react-bootstrap";

export default function CheckDuplicationAndRemove({ fileId }) {
  const [duplicates, setDuplicates] = useState([]);
  const [count, setCount] = useState(0);
  const [percent, setPercent] = useState(0);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");
  const [method, setMethod] = useState("keep_first");

  // Fetch duplicate info
  useEffect(() => {
    if (!fileId) return;
    setLoading(true);
    fetch(`http://127.0.0.1:5000/api/duplicates/${fileId}`)
      .then((res) => res.json())
      .then((data) => {
        setCount(data.duplicate_count);
        setPercent(data.percent);
        setDuplicates(data.preview);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, [fileId]);

  const handleRemove = (selectedMethod) => {
    setLoading(true);
    setMessage("");
    fetch(`http://127.0.0.1:5000/api/remove_duplicates/${fileId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ method: selectedMethod }),
    })
      .then((res) => res.json())
      .then((data) => {
        setMessage(data.message);
        setCount(0); // assume duplicates removed
        setDuplicates([]);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  };

  if (loading) return <Spinner animation="border" variant="primary" />;

  return (
    <div style={{ marginTop: 20 }}>
      <h3 className="mb-3">Duplicate Data Check</h3>

      {count > 0 ? (
        <>
          <Alert variant="warning">
            Found <strong>{count}</strong> duplicate rows ({percent}% of
            dataset)
          </Alert>

          <DropdownButton
            as={Button.Group}
            title="Handle Duplicates"
            variant="primary"
            className="mb-3"
          >
            <Dropdown.Item onClick={() => handleRemove("keep_first")}>
              Remove Duplicates (Keep First)
            </Dropdown.Item>
            <Dropdown.Item onClick={() => handleRemove("keep_last")}>
              Remove Duplicates (Keep Last)
            </Dropdown.Item>
            <Dropdown.Item onClick={() => handleRemove("remove_all")}>
              Remove All Duplicates (Keep None)
            </Dropdown.Item>
          </DropdownButton>

          <h5>Preview of Duplicate Rows:</h5>
          <div style={{ overflowX: "auto" }}>
            <Table bordered striped hover size="sm">
              <thead>
                {duplicates.length > 0 && (
                  <tr>
                    {Object.keys(duplicates[0]).map((col) => (
                      <th key={col}>{col}</th>
                    ))}
                  </tr>
                )}
              </thead>
              <tbody>
                {duplicates.map((row, i) => (
                  <tr key={i}>
                    {Object.values(row).map((v, j) => (
                      <td key={j}>{String(v)}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </Table>
          </div>
        </>
      ) : (
        <Alert variant="success">No duplicate rows found ✅</Alert>
      )}

      {message && (
        <Alert variant="info" className="mt-3">
          {message}
        </Alert>
      )}
    </div>
  );
}
