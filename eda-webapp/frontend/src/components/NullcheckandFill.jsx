import React, { useEffect, useState } from "react";
import {
  Tabs,
  Tab,
  Spinner,
  Dropdown,
  Button,
  ButtonGroup,
} from "react-bootstrap";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  PieChart,
  Pie,
  Cell,
  Legend,
} from "recharts";

const COLORS = [
  "#0088FE",
  "#00C49F",
  "#FFBB28",
  "#FF8042",
  "#A28BFE",
  "#FEA8B8",
  "#82CA9D",
  "#8884D8",
];

export default function NullcheckandFill({ fileId }) {
  const [data, setData] = useState([]);
  const [total, setTotal] = useState(0);
  const [heatmap, setHeatmap] = useState("");
  const [loading, setLoading] = useState(true);
  const [filling, setFilling] = useState(false);

  useEffect(() => {
    if (!fileId) return;
    fetchMissingAnalysis();
  }, [fileId]);

  const fetchMissingAnalysis = () => {
    setLoading(true);
    fetch(`http://127.0.0.1:5000/api/missing_analysis/${fileId}`)
      .then((res) => res.json())
      .then((d) => {
        setData(d.missing_data);
        setTotal(d.total_missing);
        setHeatmap(d.heatmap);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  };

  const handleFill = (column, method) => {
    setFilling(true);
    fetch(`http://127.0.0.1:5000/api/impute/${fileId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ column, method }),
    })
      .then((res) => res.json())
      .then((d) => {
        alert(d.message);
        fetchMissingAnalysis(); // refresh data
        setFilling(false);
      })
      .catch((err) => {
        console.error(err);
        setFilling(false);
      });
  };

  if (loading) return <Spinner animation="border" variant="primary" />;

  return (
    <div style={{ marginTop: 20 }}>
      <h3 className="mb-3">Null Value Analysis</h3>

      {/* Dropdown to select column and fill method */}
      <div
        className="mb-3"
        style={{ display: "flex", gap: "10px", alignItems: "center" }}
      >
        <Dropdown as={ButtonGroup}>
          <Button variant="info">Fill Nulls</Button>
          <Dropdown.Toggle split variant="info" id="dropdown-split-basic" />
          <Dropdown.Menu>
            {data
              .filter((d) => d.nullCount > 0)
              .map((col, i) => (
                <Dropdown drop="end" key={i}>
                  <Dropdown.Toggle as="div" className="dropdown-item">
                    {col.column} ({col.nullCount})
                  </Dropdown.Toggle>
                  <Dropdown.Menu>
                    {[
                      "mean",
                      "median",
                      "mode",
                      "constant",
                      "knn",
                      "iterative",
                    ].map((method) => (
                      <Dropdown.Item
                        key={method}
                        onClick={() => handleFill(col.column, method)}
                      >
                        Fill with {method}
                      </Dropdown.Item>
                    ))}
                  </Dropdown.Menu>
                </Dropdown>
              ))}
          </Dropdown.Menu>
        </Dropdown>
        {filling && <Spinner animation="border" size="sm" />}
      </div>

      <Tabs defaultActiveKey="bar" id="null-tabs" className="mb-3">
        <Tab eventKey="bar" title="Bar Chart">
          <div style={{ display: "flex", justifyContent: "center" }}>
            <BarChart width={700} height={400} data={data}>
              <XAxis
                dataKey="column"
                angle={-45}
                textAnchor="end"
                interval={0}
                height={100}
              />
              <YAxis />
              <Tooltip />
              <Bar dataKey="nullCount" fill="#8884d8" />
            </BarChart>
          </div>
        </Tab>

        <Tab eventKey="pie" title="Pie Chart">
          <div style={{ display: "flex", justifyContent: "center" }}>
            <PieChart width={500} height={400}>
              <Pie
                data={data}
                dataKey="nullCount"
                nameKey="column"
                cx="50%"
                cy="50%"
                outerRadius={120}
                label
              >
                {data.map((entry, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={COLORS[index % COLORS.length]}
                  />
                ))}
              </Pie>
              <Legend />
              <Tooltip />
            </PieChart>
          </div>
        </Tab>

        <Tab eventKey="heatmap" title="Heatmap">
          <div style={{ textAlign: "center" }}>
            <img
              src={`data:image/png;base64,${heatmap}`}
              alt="Missing Values Heatmap"
              style={{
                maxWidth: "100%",
                borderRadius: "10px",
                boxShadow: "0 0 10px #ccc",
              }}
            />
          </div>
        </Tab>
      </Tabs>

      <p className="mt-3">
        <strong>Total Missing Values:</strong> {total}
      </p>
    </div>
  );
}
