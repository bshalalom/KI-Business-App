import './App.css';
import React, { useState } from "react";

export default function BusinessIdeaGenerator() {
  const [prompt, setPrompt] = useState("");
  const [idea, setIdea] = useState("");
  const [validation, setValidation] = useState("Noch keine Validierung durchgeführt.");
  const [sources, setSources] = useState("Noch keine Quellen verfügbar.");
  const [activeTab, setActiveTab] = useState("validierung");

  const handleGenerate = async () => {
    // Wir senden nur noch den Prompt. Den Rest erledigt das Backend.
    const formData = new FormData();
    formData.append('prompt', prompt);

    try {
      const res = await fetch("http://127.0.0.1:8000/analyze-all", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const errorData = await res.json();
        const errorMessage = errorData.detail ? JSON.stringify(errorData.detail) : `HTTP-Fehler! Status: ${res.status}`;
        throw new Error(errorMessage);
      }

      const data = await res.json();

      setIdea(data.final_analysis || "Keine Analyse zurückgegeben.");
      setValidation(
        data.feedback_iterations?.join("\n") || "Keine Validierung durchgeführt."
      );
      // Die Quellen kommen jetzt automatisch vom Backend
      setSources(
        data.urls_used?.join("\n") || "Keine Quellen zurückgegeben."
      );
    } catch (err) {
      setIdea("Fehler bei der Analyse: " + err.message);
      setValidation("Fehler beim Laden der Validierung.");
      setSources("Fehler beim Laden der Quellen.");
    }
  };

  return (
    <div className="container">
      <div className="menu-icon">☰</div>
      <h1 className="title">Generate Business Idea</h1>

      <div className="input-group">
        <input
          type="text"
          placeholder="Enter a prompt"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
        />
        <button onClick={handleGenerate}>Generate</button>
      </div>

      <h2 className="label">Generated Idea</h2>
      <textarea
        className="idea-box"
        readOnly
        value={idea}
      />

      <div className="tabs">
        <span
          className={`tab ${activeTab === "validierung" ? "active" : "inactive"}`}
          onClick={() => setActiveTab("validierung")}
        >
          Validierung
        </span>
        <span
          className={`tab ${activeTab === "quellen" ? "active" : "inactive"}`}
          onClick={() => setActiveTab("quellen")}
        >
          Quellen
        </span>
      </div>

      <div className="tab-content">
        <textarea
          className="info-box"
          readOnly
          value={activeTab === "validierung" ? validation : sources}
        />
      </div>
    </div>
  );
}