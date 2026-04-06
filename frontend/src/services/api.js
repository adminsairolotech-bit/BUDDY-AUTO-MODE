import axios from "axios";

const baseUrl =
  (process.env.REACT_APP_BACKEND_URL || "").replace(/\/+$/, "") ||
  "http://localhost:8001";

const api = axios.create({
  baseURL: `${baseUrl}/api`,
  timeout: 15000,
});

const TOKEN_KEY = "buddy_auto_mode_access_token";
const REFRESH_TOKEN_KEY = "buddy_auto_mode_refresh_token";

export function getStoredToken() {
  return localStorage.getItem(TOKEN_KEY) || "";
}

export function getStoredRefreshToken() {
  return localStorage.getItem(REFRESH_TOKEN_KEY) || "";
}

export function setStoredTokens(accessToken, refreshToken) {
  if (accessToken) {
    localStorage.setItem(TOKEN_KEY, accessToken);
  }
  if (refreshToken) {
    localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
  }
}

export function clearStoredTokens() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
}

api.interceptors.request.use((config) => {
  const token = getStoredToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export async function getHealth() {
  const response = await api.get("/health");
  return response.data;
}

export async function register(payload) {
  const response = await api.post("/auth/register", payload);
  return response.data;
}

export async function login(payload) {
  const response = await api.post("/auth/login", payload);
  return response.data;
}

export async function me() {
  const response = await api.get("/auth/me");
  return response.data;
}

export async function logout() {
  const refreshToken = getStoredRefreshToken();
  const headers = refreshToken ? { "x-refresh-token": refreshToken } : undefined;
  const response = await api.post("/auth/logout", {}, { headers });
  return response.data;
}

export async function sendCommand(command, conversationId = null, confirmed = false) {
  const headers = confirmed ? { "x-confirm-action": "true" } : undefined;
  const response = await api.post("/command", {
    command,
    type: "text",
    context: conversationId ? { conversation_id: conversationId, previous_messages: [] } : undefined,
  }, { headers });
  return response.data;
}

export { baseUrl };
