export const API = import.meta.env.VITE_API_URL || "/api";

async function request(path, options = {}) {
  const headers = new Headers(options.headers || {});
  const token = localStorage.getItem("token");
  if (token) headers.set("Authorization", `Bearer ${token}`);
  if (!(options.body instanceof FormData)) headers.set("Content-Type", "application/json");

  const response = await fetch(`${API}${path}`, { ...options, headers });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    let message = "Request failed";
    if (Array.isArray(data.detail)) {
        message = data.detail.map(x =>
            typeof x === "object" ? (x.msg || JSON.stringify(x)) : String(x)
        ).join(", ");
    } else if (typeof data.detail === "object" && data.detail !== null) {
        message = data.detail.msg || JSON.stringify(data.detail);
    } else if (data.detail) {
        message = String(data.detail);
    }
    throw new Error(message);
}
  return data;
}

export const api = {
  services: (q = "") => request(`/services?q=${encodeURIComponent(q)}`),
  login: (body) => request("/auth/login", { method: "POST", body: JSON.stringify(body) }),
  register: (body) => request("/auth/register", { method: "POST", body: JSON.stringify(body) }),
  me: () => request("/auth/me"),
  ocr: (form) => request("/ocr/receipt", { method: "POST", body: form }),
  report: (body) => request("/reports/fee", { method: "POST", body: JSON.stringify(body) }),
  myReports: () => request("/reports/mine"),
  reportSummary: () => request("/reports/summary"),
  adminStats: () => request("/admin/stats"),
  adminCreate: (body) => request("/admin/services", { method: "POST", body: JSON.stringify(body) }),
  adminUpdate: (id, body) => request(`/admin/services/${id}`, { method: "PUT", body: JSON.stringify(body) }),
  adminDelete: (id) => request(`/admin/services/${id}`, { method: "DELETE" })
};

