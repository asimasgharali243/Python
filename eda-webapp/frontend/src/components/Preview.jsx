import React, { useEffect, useState } from "react";
import axios from "axios";
import { Container, Card, Table, Spinner } from "react-bootstrap";

export default function Preview({ fileId }) {
  const [preview, setPreview] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!fileId) return;
    setLoading(true);
    axios
      .get(`http://localhost:5000/api/preview/${fileId}`)
      .then((r) => {
        setPreview(r.data.preview);
        console.log(r.data);
      })
      .catch((err) => console.error("Error fetching preview:", err))
      .finally(() => setLoading(false));
  }, [fileId]);

  if (loading)
    return (
      <div className="d-flex justify-content-center mt-4">
        <Spinner animation="border" variant="primary" />
      </div>
    );

  if (!preview.length) return null;

  const cols = Object.keys(preview[0]);

  return (
    <Container className="mt-4">
      <Card className="shadow-sm border-0">
        <Card.Body>
          <Card.Title className="mb-3 text-center">📊 Data Preview</Card.Title>
          <div className="table-responsive">
            <Table striped bordered hover size="sm" className="align-middle">
              <thead className="table-light">
                <tr>
                  {cols.map((c) => (
                    <th
                      key={c}
                      style={{ whiteSpace: "nowrap" }}
                      className="align-middle p-3"
                    >
                      {c}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {preview.map((row, i) => (
                  <tr key={i}>
                    {cols.map((c) => (
                      <td key={c}>{String(row[c] ?? "")}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </Table>
          </div>
        </Card.Body>
      </Card>
    </Container>
  );
}
