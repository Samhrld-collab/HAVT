import { useEffect, useState } from "react";
import { apiFetch } from "../api";

export default function MyAppointments({ token }) {
  const [appts, setAppts] = useState([]);

  useEffect(() => {
    apiFetch("/appointments/my", {}, token).then(setAppts);
  }, [token]);

  return (
    <div>
      <h2>My Appointments</h2>
      {appts.length === 0 ? (
        <p>No appointments booked yet.</p>
      ) : (
        <ul>
          {appts.map((a) => (
            <li key={a.id}>
              {a.when} with {a.clinician_name} — <b>{a.status}</b>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}