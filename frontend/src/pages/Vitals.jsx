import { useState, useEffect } from "react";
import { apiFetch } from "../api";

export default function Vitals({ token }) {
  const [vitals, setVitals] = useState([]);
  const [form, setForm] = useState({ temp: "", pulse: "", oxygen: "" });
  const [msg, setMsg] = useState("");

  useEffect(() => {
    apiFetch("/vitals/vitals", {}, token).then(setVitals);
  }, [token]);

  const submit = async () => {
    await apiFetch("/vitals/vitals", {
      method: "POST",
      body: JSON.stringify(form),
    }, token);
    setMsg("Vitals recorded!");
    const latest = await apiFetch("/vitals/vitals", {}, token);
    setVitals(latest);
  };

  return (
    <div>
      <h2>My Vitals</h2>
      <input
        placeholder="Temperature °C"
        value={form.temp}
        onChange={e => setForm({ ...form, temp: e.target.value })}
      /><br />
      <input
        placeholder="Pulse (bpm)"
        value={form.pulse}
        onChange={e => setForm({ ...form, pulse: e.target.value })}
      /><br />
      <input
        placeholder="Oxygen %"
        value={form.oxygen}
        onChange={e => setForm({ ...form, oxygen: e.target.value })}
      /><br />
      <button onClick={submit}>Submit</button>
      <p>{msg}</p>

      <h3>Recent Records</h3>
      <ul>
        {vitals.map((v, i) => (
          <li key={i}>
            {v.temp}°C, {v.pulse} bpm, {v.oxygen}% (Recorded at {v.when})
          </li>
        ))}
      </ul>
    </div>
  );
}