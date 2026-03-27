import React, { useState } from "react";
import PredictionForm from "./components/PredictionForm";
import PatientHistory from "./components/patient-history";
import { apiRequest } from "./api";
import "./App.css";

function App() {
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [username, setUsername] = useState(localStorage.getItem("username") || "");
  const [loginError, setLoginError] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    const userId = e.target.userId.value;

    try {
      const data = await apiRequest("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ userId }),
      });

      localStorage.setItem("token", data.token);
      localStorage.setItem("username", userId);
      setToken(data.token);
      setUsername(userId);
      setLoginError("");
    } catch (err) {
      console.error(err);
      setLoginError(err.message || "Login failed");
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    setToken(null);
    setUsername("");
    setLoginError("");
  };

  if (!token) {
    return (
      <div className="centered">
        <h2>Healthcare Risk Prediction Login</h2>
        <form onSubmit={handleLogin} className="loginForm">
          <input type="text" name="userId" placeholder="Enter User ID" required className="input" />
          <button type="submit" className="button">Login</button>
        </form>
        {loginError ? <p className="errorText">{loginError}</p> : null}
      </div>
    );
  }

  return (
    <div className="appShell">
      <div className="appFrame">
        <header className="header">
          <div>
            <p className="eyebrow">Healthcare AI</p>
            <h2>Risk Prediction Dashboard</h2>
          </div>
          <div className="headerActions">
            <span className="username">{username}</span>
            <button onClick={handleLogout} className="logoutBtn">Logout</button>
          </div>
        </header>
        <p className="subtleText">
          Assess diabetes and heart-disease risk with a calmer, clinician-friendly workflow.
        </p>
        <PredictionForm token={token} username={username} logout={handleLogout} />
        <PatientHistory token={token} />
      </div>
    </div>
  );
}

export default App;
