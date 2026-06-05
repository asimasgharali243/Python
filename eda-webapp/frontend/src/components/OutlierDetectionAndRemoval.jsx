import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  Table,
  Spinner,
  Dropdown,
  Button,
  Alert,
  Image,
} from "react-bootstrap";

export default function OutlierDetectionAndRemoval({ fileId }) {
  const [summary, setSummary] = useState([]);
  const [boxplot, setBoxplot] = useState("");
  const [hist, setHist] = useState("");
  const [loading, setLoading] = useState(false);
  const [selectedCols, setSelectedCols] = useState([]);
  const [message, setMessage] = useState(null);
  const [method, setMethod] = useState("iqr");
  const [preview, setPreview] = useState([]);

  useEffect(() => {
    fetchOutlierSummary();
  }, [fileId]);

  const fetchOutlierSummary = async () => {
    setLoading(true);
    try {
      const res = await axios.get(
        `http://127.0.0.1:5000/api/outlier_analysis/${fileId}`
      );
      setSummary(res.data.outlier_summary);
      setBoxplot(res.data.boxplot);
      setHist(res.data.histogram);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleToggleColumn = (col) => {
    setSelectedCols((prev) =>
      prev.includes(col) ? prev.filter((c) => c !== col) : [...prev, col]
    );
  };

  const handleRemoveOutliers = async () => {
    setLoading(true);
    setMessage(null);
    try {
      const res = await axios.post(
        `http://127.0.0.1:5000/api/remove_outliers/${fileId}`,
        { columns: selectedCols, method }
      );
      setMessage(res.data.message);
      setPreview(res.data.preview);
      fetchOutlierSummary();
    } catch (err) {
      console.error(err);
      setMessage("Error removing outliers.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-3">
      <h4 className="mb-3">📊 Outlier Detection & Removal</h4>

      {message && <Alert variant="info">{message}</Alert>}

      {loading ? (
        <div className="text-center p-4">
          <Spinner animation="border" />
        </div>
      ) : (
        <>
          <h5>Detected Outliers</h5>
          <Table bordered hover responsive>
            <thead className="table-primary">
              <tr>
                <th>Select</th>
                <th>Column</th>
                <th>IQR Outliers</th>
                <th>Z-score Outliers</th>
                <th>Total</th>
              </tr>
            </thead>
            <tbody>
              {summary.map((row, i) => (
                <tr key={i}>
                  <td>
                    <input
                      type="checkbox"
                      checked={selectedCols.includes(row.column)}
                      onChange={() => handleToggleColumn(row.column)}
                    />
                  </td>
                  <td>{row.column}</td>
                  <td>{row.iqr_outliers}</td>
                  <td>{row.z_outliers}</td>
                  <td>{row.total}</td>
                </tr>
              ))}
            </tbody>
          </Table>

          <div className="d-flex align-items-center mb-3">
            <label className="me-2 fw-bold">Select Method:</label>
            <Dropdown onSelect={(m) => setMethod(m)}>
              <Dropdown.Toggle variant="outline-secondary" size="sm">
                {method.toUpperCase()}
              </Dropdown.Toggle>
              <Dropdown.Menu>
                <Dropdown.Item eventKey="iqr">IQR</Dropdown.Item>
                <Dropdown.Item eventKey="zscore">Z-Score</Dropdown.Item>
                <Dropdown.Item eventKey="percentile">
                  Percentile Trimming
                </Dropdown.Item>
                <Dropdown.Item eventKey="isolation_forest">
                  Isolation Forest
                </Dropdown.Item>
              </Dropdown.Menu>
            </Dropdown>
            <Button
              variant="success"
              size="sm"
              className="ms-3"
              onClick={handleRemoveOutliers}
              disabled={!selectedCols.length}
            >
              Remove Outliers
            </Button>
          </div>

          <h5>Visualizations</h5>
          <div className="d-flex flex-wrap gap-4">
            <div>
              <h6>Boxplot</h6>
              <Image
                src={`data:image/png;base64,${boxplot}`}
                alt="Boxplot"
                fluid
                style={{ maxHeight: "300px" }}
              />
            </div>
            <div>
              <h6>Distribution</h6>
              <Image
                src={`data:image/png;base64,${hist}`}
                alt="Histogram"
                fluid
                style={{ maxHeight: "300px" }}
              />
            </div>
          </div>

          {preview.length > 0 && (
            <>
              <h5 className="mt-4">Cleaned Data Preview</h5>
              <Table striped bordered size="sm">
                <thead>
                  <tr>
                    {Object.keys(preview[0]).map((k) => (
                      <th key={k}>{k}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {preview.map((row, i) => (
                    <tr key={i}>
                      {Object.values(row).map((v, j) => (
                        <td key={j}>{String(v)}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </Table>
            </>
          )}
        </>
      )}
    </div>
  );
}
