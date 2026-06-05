import React, { useEffect, useState } from "react";
import {
  Card,
  Button,
  Spinner,
  Dropdown,
  DropdownButton,
  Row,
  Col,
  Table,
  Form,
  Alert,
} from "react-bootstrap";

export default function CategoricalEncoding({ fileId }) {
  const [categoricalColumns, setCategoricalColumns] = useState([]);
  const [selectedColumn, setSelectedColumn] = useState("");
  const [encodingMethod, setEncodingMethod] = useState("");
  const [mapping, setMapping] = useState({});
  const [preview, setPreview] = useState([]);
  const [beforeImg, setBeforeImg] = useState("");
  const [afterImg, setAfterImg] = useState("");
  const [dtypes, setDtypes] = useState({});
  const [message, setMessage] = useState(null);
  const [loading, setLoading] = useState(false);

  // Load available categorical columns from backend
  useEffect(() => {
    if (!fileId) return;
    setLoading(true);
    fetch(`http://127.0.0.1:5000/api/label_options/${fileId}`)
      .then((res) => res.json())
      .then((data) => {
        setCategoricalColumns(data.categorical_columns || []);
      })
      .catch((err) => console.error("Error:", err))
      .finally(() => setLoading(false));
  }, [fileId]);

  const handleApplyEncoding = async () => {
    if (!selectedColumn || !encodingMethod) {
      setMessage("Please select a column and encoding method.");
      return;
    }

    setLoading(true);
    setMessage(null);
    setBeforeImg("");
    setAfterImg("");

    try {
      const res = await fetch(
        `http://127.0.0.1:5000/api/label_encode/${fileId}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            column: selectedColumn,
            method: encodingMethod,
            mapping: encodingMethod === "custom" ? mapping : {},
          }),
        }
      );

      const json = await res.json();
      if (!res.ok) throw new Error(json.error || "Encoding failed");

      setMessage(json.message || "Encoding applied successfully.");
      setBeforeImg(json.before_img || "");
      setAfterImg(json.after_img || "");
      setPreview(json.preview || []);
      setDtypes(json.dtypes || {});
    } catch (error) {
      setMessage(error.message);
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleMappingChange = (key, value) => {
    setMapping((prev) => ({ ...prev, [key]: value }));
  };

  return (
    <Card className="p-3 mt-4 shadow-sm">
      <h3 className="text-center mb-3">Categorical Column Labeling</h3>

      {message && <Alert variant="info">{message}</Alert>}

      {loading ? (
        <div className="text-center mt-3">
          <Spinner animation="border" />
        </div>
      ) : (
        <>
          <Row className="mb-3">
            <Col md={4}>
              <DropdownButton
                title={selectedColumn || "Select Categorical Column"}
                variant="info"
                onSelect={(val) => setSelectedColumn(val)}
              >
                {categoricalColumns.map((col) => (
                  <Dropdown.Item key={col} eventKey={col}>
                    {col}
                  </Dropdown.Item>
                ))}
              </DropdownButton>
            </Col>

            <Col md={4}>
              <DropdownButton
                title={encodingMethod || "Select Encoding Method"}
                variant="warning"
                onSelect={(val) => setEncodingMethod(val)}
              >
                <Dropdown.Item eventKey="label">Label Encoding</Dropdown.Item>
                <Dropdown.Item eventKey="onehot">
                  One-Hot Encoding
                </Dropdown.Item>
                <Dropdown.Item eventKey="custom">Custom Mapping</Dropdown.Item>
              </DropdownButton>
            </Col>

            <Col md={4} className="text-center">
              <Button
                variant="primary"
                disabled={!selectedColumn || !encodingMethod}
                onClick={handleApplyEncoding}
              >
                Apply Encoding
              </Button>
            </Col>
          </Row>

          {/* Custom Mapping Input */}
          {encodingMethod === "custom" && (
            <Card className="p-3 mb-3">
              <h5>Define Custom Mapping</h5>
              <Form.Group>
                <Form.Label>Format: category → label</Form.Label>
                <Form.Control
                  as="textarea"
                  rows={3}
                  placeholder={`Example:\nMale: 1\nFemale: 0`}
                  onChange={(e) => {
                    const lines = e.target.value.split("\n");
                    const map = {};
                    lines.forEach((line) => {
                      const [key, value] = line.split(":").map((s) => s.trim());
                      if (key && value) map[key] = value;
                    });
                    setMapping(map);
                  }}
                />
              </Form.Group>
            </Card>
          )}

          {/* Before / After visual comparison */}
          <Row>
            <Col md={6} className="text-center">
              <h5>Before Encoding</h5>
              {beforeImg ? (
                <img
                  src={`data:image/png;base64,${beforeImg}`}
                  alt="Before Encoding"
                  style={{
                    maxWidth: "100%",
                    borderRadius: 6,
                    boxShadow: "0 0 8px #ccc",
                  }}
                />
              ) : (
                <p className="text-muted">No image available</p>
              )}
            </Col>

            <Col md={6} className="text-center">
              <h5>After Encoding</h5>
              {afterImg ? (
                <img
                  src={`data:image/png;base64,${afterImg}`}
                  alt="After Encoding"
                  style={{
                    maxWidth: "100%",
                    borderRadius: 6,
                    boxShadow: "0 0 8px #ccc",
                  }}
                />
              ) : (
                <p className="text-muted">No image available</p>
              )}
            </Col>
          </Row>

          {/* Preview Table */}
          <div className="mt-4" style={{ overflowX: "auto" }}>
            <h5>Preview of Transformed Data</h5>
            <Table striped bordered size="sm">
              <thead>
                <tr>
                  {preview.length > 0 ? (
                    Object.keys(preview[0]).map((col) => (
                      <th key={col}>{col}</th>
                    ))
                  ) : (
                    <th>No Data</th>
                  )}
                </tr>
              </thead>
              <tbody>
                {preview.map((row, i) => (
                  <tr key={i}>
                    {Object.values(row).map((val, j) => (
                      <td key={j}>{String(val)}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </Table>
          </div>

          {/* Data Types */}
          <div className="mt-2">
            <strong>Data Types:</strong>{" "}
            {Object.keys(dtypes).length === 0 ? (
              <span className="text-muted">No info</span>
            ) : (
              Object.entries(dtypes).map(([k, v]) => (
                <span key={k} style={{ marginRight: 10 }}>
                  <code>{k}</code>: <small>{v}</small>
                </span>
              ))
            )}
          </div>
        </>
      )}
    </Card>
  );
}
