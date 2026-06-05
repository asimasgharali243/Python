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
  Alert,
} from "react-bootstrap";

export default function DataTransformation({ fileId }) {
  const [columns, setColumns] = useState([]);
  const [selectedColumn, setSelectedColumn] = useState("");
  const [loading, setLoading] = useState(false);
  const [preview, setPreview] = useState([]); // backend preview (has Index)
  const [dtypes, setDtypes] = useState({});
  const [method, setMethod] = useState("");
  const [transformationType, setTransformationType] = useState("");
  const [beforeImg, setBeforeImg] = useState("");
  const [afterImg, setAfterImg] = useState("");
  const [message, setMessage] = useState(null);

  // Load numeric columns and a preview from backend
  useEffect(() => {
    if (!fileId) return;
    setLoading(true);
    setMessage(null);
    fetch(`http://127.0.0.1:5000/api/transform_options/${fileId}`)
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch transform options");
        return res.json();
      })
      .then((d) => {
        setColumns(d.numeric_columns || []);
        // backend transform_options returns stats; fetch preview separately
        return fetch(`http://127.0.0.1:5000/api/preview/${fileId}`);
      })
      .then((res2) => {
        if (!res2.ok) throw new Error("Failed to fetch preview");
        return res2.json();
      })
      .then((pv) => {
        setPreview(pv.preview || []);
        setDtypes(pv.dtypes || {});
      })
      .catch((err) => {
        console.error(err);
        setMessage(err.message || "Error loading data");
      })
      .finally(() => setLoading(false));
  }, [fileId]);

  // Build payload for backend transform
  const buildTransformPayload = () => {
    // backend expects: { "columns": [...], "method": "minmax" ... }
    return {
      columns: [selectedColumn],
      method: method,
      // you may add clip_negative_for_log: true if you want to allow log on negatives
    };
  };

  const handleTransformation = async () => {
    if (!selectedColumn || !method) {
      setMessage("Select a column and a method first.");
      return;
    }

    setLoading(true);
    setMessage(null);
    setBeforeImg("");
    setAfterImg("");

    try {
      const res = await fetch(`http://127.0.0.1:5000/api/transform/${fileId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(buildTransformPayload()),
      });

      const json = await res.json();
      if (!res.ok) {
        throw new Error(json.error || json.message || "Transformation failed");
      }

      // Backend returns before_img, after_img, preview, dtypes, message
      setBeforeImg(json.before_img || "");
      setAfterImg(json.after_img || "");
      setPreview(json.preview || []);
      setDtypes(json.dtypes || {});
      setMessage(json.message || "Transformation applied");
    } catch (err) {
      console.error(err);
      setMessage(err.message || "Error applying transformation");
    } finally {
      setLoading(false);
    }
  };

  if (loading)
    return (
      <div style={{ textAlign: "center", marginTop: 30 }}>
        <Spinner animation="border" />
      </div>
    );

  return (
    <Card className="p-3 mt-4 shadow-sm">
      <h3 className="mb-3 text-center">Data Transformation</h3>

      {message && <Alert variant="info">{message}</Alert>}

      <Row className="mb-3">
        <Col md={4}>
          <DropdownButton
            variant="info"
            title={selectedColumn || "Select Column"}
            onSelect={(col) => setSelectedColumn(col)}
          >
            {columns.length === 0 && (
              <Dropdown.Item disabled>No numeric columns</Dropdown.Item>
            )}
            {columns.map((col) => (
              <Dropdown.Item key={col} eventKey={col}>
                {col}
              </Dropdown.Item>
            ))}
          </DropdownButton>
        </Col>

        <Col md={4}>
          <DropdownButton
            variant="warning"
            title={transformationType || "Select Transformation Type"}
            onSelect={(val) => {
              setTransformationType(val);
              setMethod(""); // reset method on type change
            }}
          >
            <Dropdown.Item eventKey="normalize">Normalization</Dropdown.Item>
            <Dropdown.Item eventKey="standardize">
              Standardization
            </Dropdown.Item>
            <Dropdown.Item eventKey="transform">Other Transforms</Dropdown.Item>
          </DropdownButton>
        </Col>

        <Col md={4}>
          <DropdownButton
            variant="secondary"
            title={method || "Select Method"}
            onSelect={(val) => setMethod(val)}
          >
            {transformationType === "normalize" && (
              <>
                <Dropdown.Item eventKey="minmax">Min-Max</Dropdown.Item>
                <Dropdown.Item eventKey="maxabs">MaxAbs</Dropdown.Item>
              </>
            )}
            {transformationType === "standardize" && (
              <>
                <Dropdown.Item eventKey="zscore">Z-Score</Dropdown.Item>
                <Dropdown.Item eventKey="robust">Robust Scaler</Dropdown.Item>
              </>
            )}
            {transformationType === "transform" && (
              <>
                <Dropdown.Item eventKey="log">Log (log1p)</Dropdown.Item>
                <Dropdown.Item eventKey="sqrt">Square Root</Dropdown.Item>
                <Dropdown.Item eventKey="boxcox">
                  Box-Cox / Yeo-Johnson
                </Dropdown.Item>
              </>
            )}
            {!transformationType && (
              <Dropdown.Item disabled>Choose type first</Dropdown.Item>
            )}
          </DropdownButton>
        </Col>
      </Row>

      <div className="text-center mb-4">
        <Button
          variant="primary"
          disabled={!selectedColumn || !method}
          onClick={handleTransformation}
        >
          Apply Transformation
        </Button>
      </div>

      {/* Before / After images returned by backend */}
      <Row>
        <Col md={6} style={{ textAlign: "center" }}>
          <h5>Before</h5>
          {beforeImg ? (
            <img
              src={`data:image/png;base64,${beforeImg}`}
              alt="before"
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

        <Col md={6} style={{ textAlign: "center" }}>
          <h5>After</h5>
          {afterImg ? (
            <img
              src={`data:image/png;base64,${afterImg}`}
              alt="after"
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

      {/* Preview table (has Index column from backend) */}
      <div className="mt-4" style={{ overflowX: "auto" }}>
        <h5>Preview (top rows)</h5>
        <Table striped bordered size="sm">
          <thead>
            <tr>
              {preview.length > 0 ? (
                Object.keys(preview[0]).map((k) => <th key={k}>{k}</th>)
              ) : (
                <th>No data</th>
              )}
            </tr>
          </thead>
          <tbody>
            {preview.map((row, i) => (
              <tr key={i}>
                {Object.values(row).map((val, j) => (
                  <td key={j}>
                    {val === null || val === undefined ? "" : String(val)}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </Table>
      </div>

      {/* Current dtypes */}
      <div className="mt-2">
        <strong>Data types:</strong>{" "}
        {Object.keys(dtypes).length === 0 ? (
          <span className="text-muted">no info</span>
        ) : (
          Object.entries(dtypes).map(([k, v]) => (
            <span key={k} style={{ marginRight: 10 }}>
              <code>{k}</code>: <small>{v}</small>
            </span>
          ))
        )}
      </div>
    </Card>
  );
}
