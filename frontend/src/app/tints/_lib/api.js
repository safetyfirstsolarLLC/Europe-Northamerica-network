import axios from "axios";

// Next.js exposes browser-visible env vars via the NEXT_PUBLIC_ prefix.
// Add NEXT_PUBLIC_BACKEND_URL to your .env.local (see README).
const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL;
export const API = `${BACKEND_URL}/api`;

export const api = axios.create({ baseURL: API });

export function authHeader() {
  if (typeof window === "undefined") return {};
  const token = localStorage.getItem("mwt_admin_token");
  return token ? { Authorization: `Bearer ${token}` } : {};
}
