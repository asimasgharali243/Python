import React, { useState } from "react";
import Upload from "./components/Upload";
import Preview from "./components/Preview";
import Summary from "./components/Summary";
import NullcheckandFill from "./components/NullcheckandFill";
import CheckDuplicationAndRemove from "./components/CheckDuplicationAndRemove";
import CheckDataTypeAndConvert from "./components/CheckDataTypeAndConvert";
import OutlierDetectionAndRemoval from "./components/OutlierDetectionAndRemoval";
import DataTransformation from "./components/DataTransformation";
import CategoricalEncoding from "./components/CategoricalEncoding";
import ColumnSelector from "./components/ColumnSelector";
import RegressionModels from "./components/RegressionModels";

export default function App() {
  const [fileId, setFileId] = useState(null);
  const [trainCols, setTrainCols] = useState([]);
  const [targetCol, setTargetCol] = useState("");

  return (
    <div style={{ padding: 20, fontFamily: "Arial" }}>
      <h2>Exploratory Data Analysis Web App</h2>
      <Upload onUploaded={(id) => setFileId(id)} />
      {fileId && (
        <div>
          <Preview fileId={fileId} />
          <CheckDataTypeAndConvert fileId={fileId} />
          <NullcheckandFill fileId={fileId} />
          <CheckDuplicationAndRemove fileId={fileId} />
          <OutlierDetectionAndRemoval fileId={fileId} />
          <DataTransformation fileId={fileId} />
          <CategoricalEncoding fileId={fileId} />
          {/* Pass state setters to ColumnSelector */}
          <ColumnSelector
            fileId={fileId}
            trainCols={trainCols}
            setTrainCols={setTrainCols}
            targetCol={targetCol}
            setTargetCol={setTargetCol}
          />
          {/* Pass selected columns to RegressionModels */}
          <RegressionModels
            fileId={fileId}
            trainCols={trainCols}
            targetCol={targetCol}
          />
        </div>
      )}
    </div>
  );
}
