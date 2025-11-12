import { useEffect, useState } from "react";
import { apiFetch } from "../api";

export default function Profile({ token }) {
  const [profile, setProfile] = useState({ full_name: "", dob: "" });
  const [msg, setMsg] = useState("");

  useEffect(() => {
    apiFetch("/patients/me", {}, token).then(res => {
      if (res && res.full_name) setProfile(res);
    });
  }, [token]);

  const save = async () => {
    await apiFetch("/patients/me", {
      method: "POST",
      body: JSON.stringify(profile),
    }, token);
    setMsg("Profile saved!");
  };

  return (
    <div>
      <h2>My Profile</h2>
      <input
        value={profile.full_name}
        onChange={e => setProfile({ ...profile, full_name: e.target.value })}
        placeholder="Full Name"
      /><br />
      <input
        value={profile.dob}
        onChange={e => setProfile({ ...profile, dob: e.target.value })}
        placeholder="Date of Birth"
      /><br />
      <button onClick={save}>Save</button>
      <p>{msg}</p>
    </div>
  );
}