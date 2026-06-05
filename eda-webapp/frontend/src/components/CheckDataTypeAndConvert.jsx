import React, { useEffect, useState } from "react";
import { Table, Dropdown, Spinner, Alert } from "react-bootstrap";
import axios from "axios";

const dtypeOptions = ["int", "float", "string", "datetime", "category"];

export default function CheckDataTypeAndConvert({ fileId }) {
  const [columns, setColumns] = useState([]);
  const [dtypes, setDtypes] = useState({});
  const [loading, setLoading] = useState(true);
  const [preview, setPreview] = useState([]);
  const [message, setMessage] = useState(null);

  useEffect(() => {
    fetchDtypes();
  }, [fileId]);

  const fetchDtypes = async () => {
    setLoading(true);
    setMessage(null);
    try {
      const res = await axios.get(`http://127.0.0.1:5000/api/dtypes/${fileId}`);
      setColumns(res.data.columns || []);
      setDtypes(res.data.dtypes || {});
      setPreview(res.data.preview || []);
    } catch (err) {
      console.error(err);
      setMessage("Failed to fetch data types.");
    } finally {
      setLoading(false);
    }
  };

  const handleChangeType = async (col, newType) => {
    setLoading(true);
    setMessage(null);
    try {
      const res = await axios.post(
        `http://127.0.0.1:5000/api/change_dtype/${fileId}`,
        { column: col, new_type: newType }
      );
      setDtypes(res.data.dtypes || {});
      setPreview(res.data.preview || []);
      setMessage(res.data.message || "Type changed successfully.");
    } catch (err) {
      console.error(err);
      setMessage("Error: " + (err.response?.data?.error || "Failed"));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-3">
      <h4 className="mb-3">🔍 Data Type Check & Conversion</h4>

      {message && <Alert variant="info">{message}</Alert>}

      {loading ? (
        <div className="text-center p-4">
          <Spinner animation="border" />
        </div>
      ) : (
        <Table bordered hover responsive>
          <thead>
            <tr className="table-primary">
              <th>Column Name</th>
              <th>Current Type</th>
              <th>Change To</th>
            </tr>
          </thead>
          <tbody>
            {columns.map((col, idx) => (
              <tr key={idx}>
                <td>{col}</td>
                <td>{dtypes[col] ?? "N/A"}</td>
                <td>
                  <Dropdown>
                    <Dropdown.Toggle variant="outline-secondary" size="sm">
                      Change Type
                    </Dropdown.Toggle>
                    <Dropdown.Menu>
                      {dtypeOptions.map((opt) => (
                        <Dropdown.Item
                          key={opt}
                          onClick={() => handleChangeType(col, opt)}
                        >
                          {opt}
                        </Dropdown.Item>
                      ))}
                    </Dropdown.Menu>
                  </Dropdown>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      )}

      <h5 className="mt-4">📋 Data Preview (Top 5 Rows)</h5>
      {preview.length === 0 ? (
        <p>No preview available.</p>
      ) : (
        <Table striped bordered size="sm" responsive>
          <thead>
            <tr>
              {Object.keys(preview[0]).map((key) => (
                <th key={key}>{key}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {preview.map((row, i) => (
              <tr key={i}>
                {Object.values(row).map((val, j) => (
                  <td key={j}>
                    {val !== undefined && val !== null ? String(val) : ""}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </Table>
      )}
    </div>
  );
}
