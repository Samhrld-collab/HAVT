export const API_BASE = "http://localhost:8000/api";

export async function apiFetch(path, options = {}, token = null) {
  return fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(options.headers || {}),
    },
  }).then(res => res.json());
}
