// frontend/src/App.jsx

import React, { useState, useEffect } from "react";
import axios from "axios";
import shellPoof from "./assets/shell-poof.gif";
import "./index.css";

const API_URL = "http://localhost:5000/chat";

export default function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [showShell, setShowShell] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;
    setMessages((prev) => [...prev, { sender: "user", text: input }]);
    setInput("");
    setShowShell(true);

    try {
      const res = await axios.post(API_URL, { message: input });
      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: res.data.reply,
          confidence: res.data.confidence,
        },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "⚠️ Server error. Try again." },
      ]);
    }

    setTimeout(() => setShowShell(false), 800);
  };

  useEffect(() => {
    const handleKey = (e) => {
      if (e.key === "Enter") sendMessage();
    };
    window.addEventListener("keydown", handleKey);
    return () => window.removeEventListener("keydown", handleKey);
  }, [input]);

  return (
    <div className="mario-container">
      <h1 className="mario-title">👨‍⚖️ Legal Chat Mario</h1>
      <div className="mario-chat">
        {messages.map((msg, i) => (
          <div key={i} className={`bubble ${msg.sender}`}>
            <p>{msg.text}</p>
            {msg.confidence !== undefined && (
              <span className="conf">Confidence: {msg.confidence}%</span>
            )}
          </div>
        ))}
        {showShell && <img src={shellPoof} alt="shell" className="shell" />}
      </div>
      <div className="mario-input">
        <input
          type="text"
          placeholder="Type your legal question..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}
