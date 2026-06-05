import React, { useState } from "react";
import axios from "axios";

export default function Upload({ onUploaded }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const submit = async (e) => {
    e.preventDefault();
    if (!file) return;
    setLoading(true);
    const fd = new FormData();
    fd.append("file", file);
    try {
      const res = await axios.post("http://localhost:5000/api/upload", fd);
      onUploaded(res.data.file_id);
    } catch (err) {
      alert("Upload failed");
    } finally {
      setLoading(false);
    }
  };
  return (
    <form onSubmit={submit}>
      <input
        type="file"
        accept=".csv,.xlsx,.xls"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <button type="submit" disabled={loading}>
        {loading ? "Uploading..." : "Upload"}
      </button>
    </form>
  );
}
