import React, { useState } from "react";
import ResultCard from "./ResultCard";
import { apiRequest } from "../api";
import "../App.css";

const PredictionForm = ({ token }) => {
  const [disease, setDisease] = useState("heart");
  const [formData, setFormData] = useState({});
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    const url = disease === "heart" ? "/predict-heart" : "/predict-risk";
    try {
      const data = await apiRequest(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        token,
        body: JSON.stringify(formData),
      });

      setResult(data);
      setError("");
    } catch (err) {
      console.error(err);
      setError(err.message || "Server error");
    }
  };

  const heartFields = [
    { label: "Gender", name: "Gender", type: "select", options: ["Male", "Female"] },
    { label: "Age", name: "Age", type: "number" },
    { label: "Chest Pain", name: "Chest_pain", type: "select", options: ["Yes", "No"] },
    { label: "Shortness of Breath", name: "Shortness_of_breath", type: "select", options: ["Yes", "No"] },
    { label: "Fatigue", name: "Fatigue", type: "select", options: ["Yes", "No"] },
    { label: "Systolic BP", name: "Systolic", type: "number" },
    { label: "Diastolic BP", name: "Diastolic", type: "number" },
    { label: "Heart Rate", name: "Heart_rate_bpm", type: "number" },
    { label: "Cholesterol", name: "Cholesterol_level_mg_dL", type: "number" },
    { label: "Diabetes", name: "Diabetes", type: "select", options: ["Yes", "No"] },
    { label: "Hypertension", name: "Hypertension", type: "select", options: ["Yes", "No"] },
    { label: "Smoking", name: "Smoking", type: "select", options: ["Yes", "No"] },
    { label: "Obesity", name: "Obesity", type: "select", options: ["Yes", "No"] },
  ];

  const diabetesFields = [
    { label: "Pregnancies", name: "pregnancies", type: "number" },
    { label: "Glucose", name: "glucose", type: "number" },
    { label: "Blood Pressure", name: "blood_pressure", type: "number" },
    { label: "Skin Thickness", name: "skin_thickness", type: "number" },
    { label: "Insulin", name: "insulin", type: "number" },
    { label: "BMI", name: "bmi", type: "number" },
    { label: "Diabetes Pedigree Function", name: "diabetes_pedigree", type: "number" },
    { label: "Age", name: "age", type: "number" },
  ];

  const fields = disease === "heart" ? heartFields : diabetesFields;

  return (
    <section className="panel">
      <h2>Predict Your Health Risk</h2>
      <p className="sectionText">Choose a condition, enter the patient inputs, and review the risk summary below.</p>

      <label className="fieldLabel">Disease</label>
      <select value={disease} onChange={(e) => setDisease(e.target.value)} className="select">
        <option value="heart">Heart Disease</option>
        <option value="diabetes">Diabetes</option>
      </select>

      <form onSubmit={handleSubmit} className="formGrid">
        {fields.map(f => (
          <div key={f.name} className="fieldGroup">
            <label className="fieldLabel">{f.label}</label>
            {f.type === "select"
              ? <select name={f.name} onChange={handleChange} className="select" required>
                  <option value="">Select</option>
                  {f.options.map(opt => <option key={opt} value={opt}>{opt}</option>)}
                </select>
              : <input type={f.type} name={f.name} onChange={handleChange} className="input" required />}
          </div>
        ))}
        <button type="submit" className="button">Predict</button>
      </form>

      {result && <ResultCard result={result} />}
      {error ? <p className="errorText">{error}</p> : null}
    </section>
  );
};

export default PredictionForm;
