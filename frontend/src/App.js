import { useEffect, useMemo, useState } from "react";
import "@/App.css";
import {
  baseUrl,
  clearStoredTokens,
  getHealth,
  getStoredToken,
  login,
  logout,
  me,
  register,
  sendCommand,
  setStoredTokens,
} from "@/services/api";

const initialAuth = {
  name: "",
  email: "",
  password: "",
};

function AuthPanel({ mode, onModeChange, form, onFormChange, onSubmit, busy, error }) {
  return (
    <section className="card">
      <div className="card-header">
        <h2>{mode === "login" ? "Login" : "Create Account"}</h2>
        <p>{mode === "login" ? "Sign in to run commands." : "Register a new assistant user."}</p>
      </div>
      <form onSubmit={onSubmit} className="stack">
        {mode === "register" ? (
          <label className="field">
            <span>Name</span>
            <input
              value={form.name}
              onChange={(e) => onFormChange("name", e.target.value)}
              required
              placeholder="Sai Rolotech"
            />
          </label>
        ) : null}
        <label className="field">
          <span>Email</span>
          <input
            type="email"
            value={form.email}
            onChange={(e) => onFormChange("email", e.target.value)}
            required
            placeholder="user@example.com"
          />
        </label>
        <label className="field">
          <span>Password</span>
          <input
            type="password"
            value={form.password}
            onChange={(e) => onFormChange("password", e.target.value)}
            required
            placeholder="Minimum 12 chars with symbols"
          />
        </label>
        {error ? <p className="error">{error}</p> : null}
        <button type="submit" disabled={busy}>
          {busy ? "Please wait..." : mode === "login" ? "Login" : "Register"}
        </button>
      </form>
      <div className="inline-actions">
        <small>
          {mode === "login" ? "New user?" : "Already registered?"}
        </small>
        <button
          className="link-btn"
          onClick={() => onModeChange(mode === "login" ? "register" : "login")}
          type="button"
        >
          {mode === "login" ? "Create account" : "Go to login"}
        </button>
      </div>
    </section>
  );
}

function CommandPanel({
  user,
  commandInput,
  onCommandInput,
  onRunCommand,
  commandBusy,
  messages,
  statusText,
  onLogout,
  health,
}) {
  return (
    <section className="card">
      <div className="card-header">
        <h2>Assistant Console</h2>
        <p>
          Logged in as <strong>{user?.email}</strong>
        </p>
      </div>
      <div className="meta">
        <span>Backend: {baseUrl}</span>
        <span>Health: {health}</span>
        <span>Status: {statusText}</span>
      </div>
      <form
        className="row"
        onSubmit={(e) => {
          e.preventDefault();
          onRunCommand();
        }}
      >
        <input
          value={commandInput}
          onChange={(e) => onCommandInput(e.target.value)}
          placeholder="Try: open chrome, weather in Mumbai, schedule meeting tomorrow"
          required
        />
        <button type="submit" disabled={commandBusy}>
          {commandBusy ? "Running..." : "Run"}
        </button>
      </form>
      <div className="message-list">
        {messages.length === 0 ? (
          <p className="muted">No commands yet.</p>
        ) : (
          messages.map((m) => (
            <article key={m.id} className={`msg ${m.role}`}>
              <strong>{m.role === "user" ? "You" : "Assistant"}</strong>
              <p>{m.text}</p>
            </article>
          ))
        )}
      </div>
      <div className="inline-actions">
        <button className="secondary" type="button" onClick={onLogout}>
          Logout
        </button>
      </div>
    </section>
  );
}

function App() {
  const [health, setHealth] = useState("checking");
  const [authMode, setAuthMode] = useState("login");
  const [authForm, setAuthForm] = useState(initialAuth);
  const [authBusy, setAuthBusy] = useState(false);
  const [authError, setAuthError] = useState("");
  const [user, setUser] = useState(null);

  const [commandInput, setCommandInput] = useState("");
  const [commandBusy, setCommandBusy] = useState(false);
  const [statusText, setStatusText] = useState("idle");
  const [messages, setMessages] = useState([]);
  const [conversationId, setConversationId] = useState(null);

  const isLoggedIn = useMemo(() => Boolean(user && getStoredToken()), [user]);

  useEffect(() => {
    let active = true;
    getHealth()
      .then((res) => {
        if (active) setHealth(res?.status || "ok");
      })
      .catch(() => {
        if (active) setHealth("offline");
      });
    return () => {
      active = false;
    };
  }, []);

  useEffect(() => {
    const token = getStoredToken();
    if (!token) return;
    me()
      .then((res) => {
        if (res?.success) {
          setUser(res.user);
          setStatusText("session restored");
        }
      })
      .catch(() => {
        clearStoredTokens();
      });
  }, []);

  const updateAuthField = (key, value) => {
    setAuthForm((prev) => ({ ...prev, [key]: value }));
  };

  const pushMessage = (role, text) => {
    setMessages((prev) => [...prev, { id: `${role}-${Date.now()}-${Math.random()}`, role, text }]);
  };

  const submitAuth = async (e) => {
    e.preventDefault();
    setAuthBusy(true);
    setAuthError("");
    try {
      const payload =
        authMode === "login"
          ? { email: authForm.email.trim(), password: authForm.password }
          : {
              name: authForm.name.trim(),
              email: authForm.email.trim(),
              password: authForm.password,
            };
      const result = authMode === "login" ? await login(payload) : await register(payload);
      if (!result?.success) {
        throw new Error(result?.error || "Auth failed");
      }
      setStoredTokens(result.token, result.refresh_token);
      const meResult = await me();
      if (meResult?.success) {
        setUser(meResult.user);
        setAuthForm(initialAuth);
        setStatusText(authMode === "login" ? "logged in" : "registered and logged in");
      } else {
        throw new Error("Could not load profile");
      }
    } catch (error) {
      setAuthError(error?.response?.data?.detail || error?.response?.data?.error || error.message || "Auth error");
    } finally {
      setAuthBusy(false);
    }
  };

  const runCommand = async (confirmed = false) => {
    if (!commandInput.trim()) return;
    const command = commandInput.trim();
    setCommandBusy(true);
    setStatusText("running command");
    pushMessage("user", command);
    setCommandInput("");
    try {
      const result = await sendCommand(command, conversationId, confirmed);
      if (result?.conversation_id) {
        setConversationId(result.conversation_id);
      }
      const text =
        result?.response?.text ||
        result?.error ||
        "No response text received.";
      pushMessage("assistant", text);
      setStatusText("completed");
    } catch (error) {
      const data = error?.response?.data || {};
      const detail = data?.detail || data?.error || error.message;
      pushMessage("assistant", `Error: ${detail}`);
      setStatusText("failed");
    } finally {
      setCommandBusy(false);
    }
  };

  const handleLogout = async () => {
    try {
      await logout();
    } catch {
      // ignore logout API failure, clear local session anyway
    } finally {
      clearStoredTokens();
      setUser(null);
      setConversationId(null);
      setMessages([]);
      setStatusText("logged out");
    }
  };

  return (
    <main className="app-shell">
      <header className="topbar">
        <h1>BUDDY AUTO MODE</h1>
        <p>OpenClaw-style assistant MVP console</p>
      </header>
      {!isLoggedIn ? (
        <AuthPanel
          mode={authMode}
          onModeChange={setAuthMode}
          form={authForm}
          onFormChange={updateAuthField}
          onSubmit={submitAuth}
          busy={authBusy}
          error={authError}
        />
      ) : (
        <CommandPanel
          user={user}
          commandInput={commandInput}
          onCommandInput={setCommandInput}
          onRunCommand={runCommand}
          commandBusy={commandBusy}
          messages={messages}
          statusText={statusText}
          onLogout={handleLogout}
          health={health}
        />
      )}
    </main>
  );
}

export default App;
