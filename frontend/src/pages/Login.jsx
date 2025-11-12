import { useState } from "react";
import { apiFetch } from "../api";

export default function Login({ onLogin }) {
  const [email, setEmail] = useState("");
  const [pw, setPw] = useState("");
  const [message, setMessage] = useState("");

  const handleLogin = async () => {
    // ✅ Frontend email validation
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      setMessage("Please enter a valid email address.");
      return;
    }

    const res = await apiFetch("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password: pw }),
    });

    if (res.access_token) onLogin(res.access_token);
    else setMessage(res.detail || "Login failed");
  };

  const handleRegister = async () => {
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      setMessage("Please enter a valid email address.");
      return;
    }

    await apiFetch("/auth/register", {
      method: "POST",
      body: JSON.stringify({ email, password: pw }),
    });

    setMessage("Registered! Now log in.");
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>Login / Register</h2>
      <input
        type="email" // ✅ built-in HTML5 email check
        placeholder="Email"
        onChange={(e) => setEmail(e.target.value)}
      /><br />
      <input
        type="password"
        placeholder="Password"
        onChange={(e) => setPw(e.target.value)}
      /><br />
      <button onClick={handleLogin}>Login</button>
      <button onClick={handleRegister}>Register</button>
      <p>{message}</p>
    </div>
  );
}
