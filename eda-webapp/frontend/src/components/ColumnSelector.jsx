import React, { useEffect, useState } from "react";
import {
  Card,
  Spinner,
  Row,
  Col,
  DropdownButton,
  Dropdown,
  Button,
  Alert,
  ListGroup,
  Badge,
} from "react-bootstrap";

export default function ColumnSelector({
  fileId,
  trainCols,
  setTrainCols,
  targetCol,
  setTargetCol,
}) {
  const [columns, setColumns] = useState([]);
  const [dtypes, setDtypes] = useState({});
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  // Fetch columns and data types
  useEffect(() => {
    if (!fileId) return;
    setLoading(true);
    fetch(`http://127.0.0.1:5000/api/column_selection/${fileId}`)
      .then((res) => res.json())
      .then((data) => {
        if (data.error) throw new Error(data.error);
        setColumns(data.columns || []);
        setDtypes(data.dtypes || {});
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error:", err);
        setError("Failed to load columns");
        setLoading(false);
      });
  }, [fileId]);

  // Add a column to training columns
  const handleAddTrainCol = (col) => {
    if (col === targetCol) {
      setError("You cannot add the target column to training columns.");
      return;
    }
    if (!trainCols.includes(col)) {
      setTrainCols([...trainCols, col]);
      setError("");
    }
  };

  const handleRemoveTrainCol = (col) =>
    setTrainCols(trainCols.filter((c) => c !== col));

  // Select a single target column
  const handleSelectTarget = (col) => {
    if (trainCols.includes(col)) {
      setError("Target column cannot be one of the training columns.");
      return;
    }
    setTargetCol(col);
    setError("");
  };

  const handleRemoveTarget = () => setTargetCol("");

  // Submit selected columns
  const handleSubmit = async () => {
    if (!targetCol || trainCols.length === 0) {
      setError("Please select both training columns and a target column.");
      return;
    }

    setLoading(true);
    setMessage("");
    setError("");

    try {
      const res = await fetch(
        `http://127.0.0.1:5000/api/select_columns/${fileId}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            train_columns: trainCols,
            target_column: targetCol,
          }),
        }
      );
      const data = await res.json();
      if (data.error) throw new Error(data.error);
      setMessage("Training and target columns saved successfully.");
      setLoading(false);
    } catch (err) {
      console.error("Error saving selection:", err);
      setError(err.message);
      setLoading(false);
    }
  };

  if (loading)
    return (
      <div className="text-center mt-4">
        <Spinner animation="border" variant="primary" />
      </div>
    );

  return (
    <Card className="p-4 mt-4 shadow-sm">
      <h3 className="mb-3 text-center">Column Selection for Training</h3>

      {error && (
        <Alert variant="danger" onClose={() => setError("")} dismissible>
          {error}
        </Alert>
      )}
      {message && (
        <Alert variant="success" onClose={() => setMessage("")} dismissible>
          {message}
        </Alert>
      )}

      <Row className="mb-3">
        {/* Training Columns */}
        <Col md={6}>
          <h5>Select Training Columns</h5>
          <DropdownButton
            variant="info"
            title="Add Training Column"
            onSelect={handleAddTrainCol}
            className="mb-2"
          >
            {columns.map((col, i) => (
              <Dropdown.Item key={i} eventKey={col}>
                {col} <small>({dtypes[col]})</small>
              </Dropdown.Item>
            ))}
          </DropdownButton>

          {trainCols.length > 0 ? (
            <ListGroup>
              {trainCols.map((col) => (
                <ListGroup.Item
                  key={col}
                  className="d-flex justify-content-between align-items-center"
                >
                  {col}{" "}
                  <Badge
                    bg="danger"
                    style={{ cursor: "pointer" }}
                    onClick={() => handleRemoveTrainCol(col)}
                  >
                    Remove
                  </Badge>
                </ListGroup.Item>
              ))}
            </ListGroup>
          ) : (
            <p className="text-muted">No training columns selected</p>
          )}
        </Col>

        {/* Target Column */}
        <Col md={6}>
          <h5>Select Target Column</h5>
          <DropdownButton
            variant="warning"
            title={targetCol || "Choose Target Column"}
            onSelect={handleSelectTarget}
            className="mb-2"
          >
            {columns.map((col, i) => (
              <Dropdown.Item key={i} eventKey={col}>
                {col} <small>({dtypes[col]})</small>
              </Dropdown.Item>
            ))}
          </DropdownButton>

          {targetCol && (
            <Alert variant="secondary">
              <strong>
                {targetCol} ({dtypes[targetCol]})
              </strong>
              <Badge
                bg="danger"
                style={{ cursor: "pointer" }}
                onClick={handleRemoveTarget}
                className="float-end"
              >
                Remove
              </Badge>
            </Alert>
          )}
        </Col>
      </Row>

      <div className="text-center">
        <Button variant="primary" onClick={handleSubmit}>
          Save Selection
        </Button>
      </div>
    </Card>
  );
}
