import React, { useEffect, useState } from "react";
import { apiRequest } from "../api";
import ResultCard from "./ResultCard";

const PatientHistory = ({ token }) => {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const data = await apiRequest("/patient-history", { token });
        setHistory(data);
      } catch (err) {
        console.error(err);
      }
    };
    fetchHistory();
  }, [token]);

  if (!history.length) return null;

  return (
    <section className="panel historyPanel">
      <h3>Patient History</h3>
      <p className="sectionText">Previous assessments for the current signed-in user.</p>
      {history.map((item, idx) => (
        <ResultCard key={idx} result={item.result || item} title={item.disease ? `${item.disease} Assessment` : "Prediction Result"} />
      ))}
    </section>
  );
};

export default PatientHistory;
