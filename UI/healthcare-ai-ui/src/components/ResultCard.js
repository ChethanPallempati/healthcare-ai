import React from "react";

const formatFactor = (factor) => factor.replaceAll("_", " ");

const ResultCard = ({ result, title = "Prediction Result" }) => {
  const { disease, risk, probability, topFactors = [], recommendations = [], prediction } = result;

  return (
    <div className="resultCard">
      <div className="resultHeader">
        <div>
          <h3>{title}</h3>
          {disease ? <p className="resultDisease">{disease}</p> : null}
        </div>
        <div className="riskPill">{risk}</div>
      </div>
      <div className="resultStats">
        <div className="statBlock">
          <span className="statLabel">Probability</span>
          <strong>{(probability * 100).toFixed(0)}%</strong>
        </div>
        {typeof prediction === "number" ? (
          <div className="statBlock">
            <span className="statLabel">Prediction</span>
            <strong>{prediction}</strong>
          </div>
        ) : null}
      </div>
      {topFactors.length ? <p><strong>Top factors:</strong> {topFactors.map(formatFactor).join(", ")}</p> : null}
      {recommendations.length ? <p><strong>Recommendations:</strong> {recommendations.join(" ")}</p> : null}
    </div>
  );
};

export default ResultCard;
