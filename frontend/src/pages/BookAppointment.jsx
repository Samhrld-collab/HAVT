import { useEffect, useState } from "react";
import { apiFetch } from "../api";

export default function BookAppointment({ token }) {
  const [slots, setSlots] = useState([]);
  const [msg, setMsg] = useState("");

  useEffect(() => {
    // ✅ Just use the path; gateway prefix handled in apiFetch
    apiFetch("/appointments/slots", {}, token).then(setSlots);
  }, [token]);

  const book = async (slotId) => {
    const res = await apiFetch("/appointments/appointments", {
      method: "POST",
      body: JSON.stringify({ slot_id: slotId }),
    }, token);
    setMsg(`Booked appointment #${res.id} (${res.status})`);
  };

  return (
    <div>
      <h2>Book Appointment</h2>
      {slots.map((s) => (
        <div key={s.id}>
          {s.when} with {s.clinician_name}{" "}
          <button onClick={() => book(s.id)}>Book</button>
        </div>
      ))}
      <p>{msg}</p>
    </div>
  );
}