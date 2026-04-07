import React, { useState, useEffect } from 'react';
import './App.css';

const API_URL = process.env.REACT_APP_BACKEND_URL || '';

// Auth Context
const AuthContext = React.createContext();
const useAuth = () => React.useContext(AuthContext);

const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('buddy_token'));
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (token) {
      fetch(`${API_URL}/api/auth/me`, {
        headers: { Authorization: `Bearer ${token}` }
      })
        .then(res => res.json())
        .then(data => {
          if (data.success) setUser(data.user);
          else { localStorage.removeItem('buddy_token'); setToken(null); }
        })
        .catch(() => { localStorage.removeItem('buddy_token'); setToken(null); })
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, [token]);

  const login = async (email, password) => {
    const res = await fetch(`${API_URL}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    const data = await res.json();
    if (!data.success) throw new Error(data.error || 'Login failed');
    localStorage.setItem('buddy_token', data.token);
    setToken(data.token);
    setUser(data.user);
  };

  const register = async (name, email, password) => {
    const res = await fetch(`${API_URL}/api/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, password })
    });
    const data = await res.json();
    if (!data.success) throw new Error(data.error || 'Registration failed');
    localStorage.setItem('buddy_token', data.token);
    setToken(data.token);
    setUser(data.user);
  };

  const logout = () => {
    localStorage.removeItem('buddy_token');
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

// Login Page
const LoginPage = ({ onSwitch }) => {
  const { login } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      await login(email, password);
    } catch (err) {
      setError(err.message);
    }
    setLoading(false);
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <div className="logo">🤖</div>
          <h1>BUDDY AI</h1>
          <p>Welcome back! Login to continue</p>
        </div>
        <form onSubmit={handleSubmit}>
          {error && <div className="error-msg">{error}</div>}
          <div className="input-group">
            <label>Email</label>
            <input 
              type="email" 
              value={email} 
              onChange={e => setEmail(e.target.value)}
              placeholder="your@email.com"
              required
            />
          </div>
          <div className="input-group">
            <label>Password</label>
            <input 
              type="password" 
              value={password} 
              onChange={e => setPassword(e.target.value)}
              placeholder="••••••••"
              required
            />
          </div>
          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? 'Logging in...' : '🚀 Login'}
          </button>
        </form>
        <p className="switch-auth">
          Don't have an account? <span onClick={onSwitch}>Register</span>
        </p>
      </div>
    </div>
  );
};

// Register Page
const RegisterPage = ({ onSwitch }) => {
  const { register } = useAuth();
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      await register(name, email, password);
    } catch (err) {
      setError(err.message);
    }
    setLoading(false);
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <div className="logo">🤖</div>
          <h1>BUDDY AI</h1>
          <p>Create your account</p>
        </div>
        <form onSubmit={handleSubmit}>
          {error && <div className="error-msg">{error}</div>}
          <div className="input-group">
            <label>Name</label>
            <input 
              type="text" 
              value={name} 
              onChange={e => setName(e.target.value)}
              placeholder="John Doe"
              required
            />
          </div>
          <div className="input-group">
            <label>Email</label>
            <input 
              type="email" 
              value={email} 
              onChange={e => setEmail(e.target.value)}
              placeholder="your@email.com"
              required
            />
          </div>
          <div className="input-group">
            <label>Password (12+ chars, mix case, number, special)</label>
            <input 
              type="password" 
              value={password} 
              onChange={e => setPassword(e.target.value)}
              placeholder="••••••••••••"
              required
              minLength={12}
            />
          </div>
          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? 'Creating...' : '✨ Create Account'}
          </button>
        </form>
        <p className="switch-auth">
          Already have an account? <span onClick={onSwitch}>Login</span>
        </p>
      </div>
    </div>
  );
};

// Dashboard
const Dashboard = () => {
  const { user, logout, token } = useAuth();
  const [command, setCommand] = useState('');
  const [messages, setMessages] = useState([
    { type: 'bot', text: 'Hello! I\'m BUDDY, your AI assistant. How can I help you today?' }
  ]);
  const [loading, setLoading] = useState(false);
  const [skills, setSkills] = useState([]);
  const [activeTab, setActiveTab] = useState('chat');

  useEffect(() => {
    fetch(`${API_URL}/api/skills`, {
      headers: { Authorization: `Bearer ${token}` }
    })
      .then(res => res.json())
      .then(data => data.success && setSkills(data.skills || []));
  }, [token]);

  const sendCommand = async () => {
    if (!command.trim()) return;
    const userMsg = command;
    setMessages(prev => [...prev, { type: 'user', text: userMsg }]);
    setCommand('');
    setLoading(true);

    try {
      const res = await fetch(`${API_URL}/api/command`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({ command: userMsg, type: 'text' })
      });
      const data = await res.json();
      setMessages(prev => [...prev, { 
        type: 'bot', 
        text: data.success ? data.response?.text : 'Sorry, I couldn\'t process that.'
      }]);
    } catch {
      setMessages(prev => [...prev, { type: 'bot', text: 'Error processing request.' }]);
    }
    setLoading(false);
  };

  const skillIcons = {
    weather: '🌤️',
    news: '📰',
    calculator: '🧮',
    translator: '🌐',
    notes: '📝'
  };

  return (
    <div className="dashboard">
      <aside className="sidebar">
        <div className="sidebar-logo">
          <span className="logo-icon">🤖</span>
          <div>
            <h2>BUDDY</h2>
            <small>Automation</small>
          </div>
        </div>
        <nav>
          <button className={activeTab === 'chat' ? 'active' : ''} onClick={() => setActiveTab('chat')}>
            💬 Chat
          </button>
          <button className={activeTab === 'skills' ? 'active' : ''} onClick={() => setActiveTab('skills')}>
            ⚡ Skills
          </button>
          <button className={activeTab === 'settings' ? 'active' : ''} onClick={() => setActiveTab('settings')}>
            ⚙️ Settings
          </button>
        </nav>
        <div className="sidebar-user">
          <div className="user-avatar">{user?.name?.[0]?.toUpperCase() || 'U'}</div>
          <div className="user-info">
            <span>{user?.name || 'User'}</span>
            <small>{user?.email || ''}</small>
          </div>
          <button className="logout-btn" onClick={logout}>🚪</button>
        </div>
      </aside>

      <main className="main-content">
        {activeTab === 'chat' && (
          <div className="chat-container">
            <div className="chat-header">
              <h1>👋 Hello, {user?.name?.split(' ')[0] || 'there'}!</h1>
              <p>How can I assist you today?</p>
            </div>
            <div className="chat-messages">
              {messages.map((msg, i) => (
                <div key={i} className={`message ${msg.type}`}>
                  {msg.type === 'bot' && <span className="bot-icon">🤖</span>}
                  <div className="message-content">{msg.text}</div>
                </div>
              ))}
              {loading && <div className="message bot"><span className="bot-icon">🤖</span><div className="typing">...</div></div>}
            </div>
            <div className="chat-input">
              <input
                value={command}
                onChange={e => setCommand(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && sendCommand()}
                placeholder="Type your command..."
              />
              <button onClick={sendCommand} disabled={loading}>➤</button>
            </div>
            <div className="quick-skills">
              {skills.slice(0, 5).map(skill => (
                <button key={skill.id} onClick={() => setCommand(`Use ${skill.name.toLowerCase()}`)} className="skill-chip">
                  {skillIcons[skill.id] || '⚡'} {skill.name}
                </button>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'skills' && (
          <div className="skills-page">
            <h1>⚡ Skills</h1>
            <p>Available AI capabilities</p>
            <div className="skills-grid">
              {skills.map(skill => (
                <div key={skill.id} className="skill-card">
                  <span className="skill-icon">{skillIcons[skill.id] || '⚡'}</span>
                  <h3>{skill.name}</h3>
                  <p>{skill.description}</p>
                  <div className="triggers">
                    {(skill.trigger_phrases || []).slice(0, 3).map((t, i) => (
                      <span key={i} className="trigger">{t}</span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'settings' && (
          <div className="settings-page">
            <h1>⚙️ Settings</h1>
            <div className="settings-section">
              <h2>👤 Profile</h2>
              <div className="profile-info">
                <div className="avatar-large">{user?.name?.[0]?.toUpperCase() || 'U'}</div>
                <div>
                  <h3>{user?.name}</h3>
                  <p>{user?.email}</p>
                </div>
              </div>
            </div>
            <div className="settings-section">
              <h2>🔐 Security</h2>
              <button className="btn-secondary" onClick={logout}>🚪 Logout</button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

// Main App
function App() {
  const [isLogin, setIsLogin] = useState(true);

  return (
    <AuthProvider>
      <AppContent isLogin={isLogin} setIsLogin={setIsLogin} />
    </AuthProvider>
  );
}

const AppContent = ({ isLogin, setIsLogin }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="loading-screen">
        <div className="loader">🤖</div>
        <p>Loading BUDDY AI...</p>
      </div>
    );
  }

  if (user) {
    return <Dashboard />;
  }

  return isLogin 
    ? <LoginPage onSwitch={() => setIsLogin(false)} />
    : <RegisterPage onSwitch={() => setIsLogin(true)} />;
};

export default App;
