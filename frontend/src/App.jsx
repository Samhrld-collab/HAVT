import { useState } from "react";
import Login from "./pages/Login";
import Profile from "./pages/Profile";
import BookAppointment from "./pages/BookAppointment";
import MyAppointments from "./pages/MyAppointments";
import Vitals from "./pages/Vitals";

export default function App() {
  const [token, setToken] = useState(null);
  const [page, setPage] = useState("login");

  if (!token) return <Login onLogin={setToken} />;

  return (
    <div style={{ padding: 20 }}>
      <h1>Healthcare Appointment & Vitals Tracker</h1>
      <nav style={{ marginBottom: 10 }}>
        <button onClick={() => setPage("profile")}>Profile</button>
        <button onClick={() => setPage("book")}>Book Appointment</button>
        <button onClick={() => setPage("my")}>My Appointments</button>
        <button onClick={() => setPage("vitals")}>Vitals</button>
        <button onClick={() => setToken(null)}>Logout</button>
      </nav>
      <hr />

      {page === "profile" && <Profile token={token} />}
      {page === "book" && <BookAppointment token={token} />}
      {page === "my" && <MyAppointments token={token} />}
      {page === "vitals" && <Vitals token={token} />}
    </div>
  );
}
