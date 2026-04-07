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
              data-testid="login-email"
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
              data-testid="login-password"
            />
          </div>
          <button type="submit" className="btn-primary" disabled={loading} data-testid="login-submit">
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
              data-testid="register-name"
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
              data-testid="register-email"
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
              data-testid="register-password"
            />
          </div>
          <button type="submit" className="btn-primary" disabled={loading} data-testid="register-submit">
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
    { type: 'bot', text: 'Hello! I\'m BUDDY, your AI-powered personal assistant. I can help you with weather, news, calculations, translations, and more. Try asking me something!' }
  ]);
  const [loading, setLoading] = useState(false);
  const [skills, setSkills] = useState([]);
  const [integrations, setIntegrations] = useState([]);
  const [desktopStatus, setDesktopStatus] = useState('offline');
  const [activeTab, setActiveTab] = useState('chat');

  useEffect(() => {
    // Fetch skills
    fetch(`${API_URL}/api/skills`, {
      headers: { Authorization: `Bearer ${token}` }
    })
      .then(res => res.json())
      .then(data => data.success && setSkills(data.skills || []));

    // Fetch integrations
    fetch(`${API_URL}/api/integrations`, {
      headers: { Authorization: `Bearer ${token}` }
    })
      .then(res => res.json())
      .then(data => data.success && setIntegrations(data.integrations || []));

    // Fetch desktop status
    fetch(`${API_URL}/api/desktop/status`, {
      headers: { Authorization: `Bearer ${token}` }
    })
      .then(res => res.json())
      .then(data => data.success && setDesktopStatus(data.status || 'offline'));
  }, [token]);

  const sendCommand = async () => {
    if (!command.trim() || loading) return;
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
        text: data.success ? data.response?.text : 'Sorry, I couldn\'t process that request.'
      }]);
    } catch {
      setMessages(prev => [...prev, { type: 'bot', text: 'Error connecting to server. Please try again.' }]);
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

  const integrationIcons = {
    telegram: '📱',
    gmail: '📧',
    calendar: '📅',
    notion: '📓',
    github: '🐙',
    gemini: '🤖'
  };

  return (
    <div className="dashboard" data-testid="dashboard">
      <aside className="sidebar">
        <div className="sidebar-logo">
          <span className="logo-icon">🤖</span>
          <div>
            <h2>BUDDY</h2>
            <small>AI Assistant</small>
          </div>
        </div>
        <nav>
          <button className={activeTab === 'chat' ? 'active' : ''} onClick={() => setActiveTab('chat')} data-testid="nav-chat">
            💬 Chat
          </button>
          <button className={activeTab === 'skills' ? 'active' : ''} onClick={() => setActiveTab('skills')} data-testid="nav-skills">
            ⚡ Skills
          </button>
          <button className={activeTab === 'integrations' ? 'active' : ''} onClick={() => setActiveTab('integrations')} data-testid="nav-integrations">
            🔗 Integrations
          </button>
          <button className={activeTab === 'desktop' ? 'active' : ''} onClick={() => setActiveTab('desktop')} data-testid="nav-desktop">
            🖥️ Desktop
          </button>
          <button className={activeTab === 'settings' ? 'active' : ''} onClick={() => setActiveTab('settings')} data-testid="nav-settings">
            ⚙️ Settings
          </button>
        </nav>
        <div className="sidebar-user">
          <div className="user-avatar">{user?.name?.[0]?.toUpperCase() || 'U'}</div>
          <div className="user-info">
            <span>{user?.name || 'User'}</span>
            <small>{user?.email || ''}</small>
          </div>
          <button className="logout-btn" onClick={logout} data-testid="logout-btn">🚪</button>
        </div>
      </aside>

      <main className="main-content">
        {/* Chat Tab */}
        {activeTab === 'chat' && (
          <div className="chat-container" data-testid="chat-container">
            <div className="chat-header">
              <h1>👋 Hello, {user?.name?.split(' ')[0] || 'there'}!</h1>
              <p>How can I assist you today?</p>
            </div>
            <div className="chat-messages" data-testid="chat-messages">
              {messages.map((msg, i) => (
                <div key={i} className={`message ${msg.type}`}>
                  {msg.type === 'bot' && <span className="bot-icon">🤖</span>}
                  <div className="message-content">{msg.text}</div>
                </div>
              ))}
              {loading && <div className="message bot"><span className="bot-icon">🤖</span><div className="typing">Thinking...</div></div>}
            </div>
            <div className="chat-input">
              <input
                value={command}
                onChange={e => setCommand(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && !loading && sendCommand()}
                placeholder="Type your command... (e.g., 'What's the weather?', 'Translate hello to Hindi')"
                data-testid="chat-input"
              />
              <button onClick={sendCommand} disabled={loading} data-testid="send-btn">➤</button>
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

        {/* Skills Tab */}
        {activeTab === 'skills' && (
          <div className="skills-page" data-testid="skills-page">
            <h1>⚡ Skills</h1>
            <p>AI-powered capabilities at your service</p>
            <div className="skills-grid">
              {skills.map(skill => (
                <div key={skill.id} className="skill-card" data-testid={`skill-${skill.id}`}>
                  <span className="skill-icon">{skillIcons[skill.id] || '⚡'}</span>
                  <h3>{skill.name}</h3>
                  <p>{skill.description}</p>
                  <div className="skill-status active">✓ Active</div>
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

        {/* Integrations Tab */}
        {activeTab === 'integrations' && (
          <div className="integrations-page" data-testid="integrations-page">
            <h1>🔗 Integrations</h1>
            <p>Connect your favorite services</p>
            <div className="integrations-grid">
              {integrations.map(integration => (
                <div key={integration.id} className="integration-card" data-testid={`integration-${integration.id}`}>
                  <span className="integration-icon">{integrationIcons[integration.id] || '🔌'}</span>
                  <div className="integration-info">
                    <h3>{integration.name}</h3>
                    <p>{integration.description || `Connect your ${integration.name} account`}</p>
                  </div>
                  <div className={`integration-status ${integration.status}`}>
                    {integration.status === 'connected' ? '🟢 Connected' : '⚪ Not Connected'}
                  </div>
                  <button className="btn-secondary">
                    {integration.status === 'connected' ? 'Disconnect' : 'Connect'}
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Desktop Tab */}
        {activeTab === 'desktop' && (
          <div className="desktop-page" data-testid="desktop-page">
            <h1>🖥️ Desktop Agent</h1>
            <p>Control your computer remotely</p>
            
            <div className="desktop-status-card">
              <div className="status-indicator">
                <div className={`status-dot ${desktopStatus}`}></div>
                <span>Status: <strong>{desktopStatus === 'online' ? 'Connected' : 'Offline'}</strong></span>
              </div>
              {desktopStatus === 'offline' && (
                <p className="status-message">Desktop agent is not connected. Download and install the agent on your Windows PC to enable remote control.</p>
              )}
            </div>

            <div className="desktop-actions">
              <h2>📥 Download Desktop Agent</h2>
              <p>Install BUDDY Desktop Agent on your Windows PC to enable remote automation and ChatGPT-Codex auto-reply.</p>
              <div className="download-options">
                <a href="/BUDDY_Desktop_Agent.zip" download className="btn-primary download-btn">
                  💻 Download for Windows
                </a>
              </div>
              <div className="automation-note">
                <h4>🤖 ChatGPT + Codex Auto-Reply Features:</h4>
                <ul>
                  <li>✅ Auto-approves "Yes", "Run", "Continue" buttons</li>
                  <li>🔄 Syncs code between Codex and ChatGPT</li>
                  <li>💬 Auto-copies responses to clipboard</li>
                  <li>🖥️ Works with Desktop app and Browser</li>
                </ul>
              </div>
            </div>

            <div className="desktop-features">
              <h2>⚡ Available Actions</h2>
              <div className="features-grid">
                <div className="feature-item">📷 Screenshot</div>
                <div className="feature-item">⌨️ Type Text</div>
                <div className="feature-item">🖱️ Mouse Control</div>
                <div className="feature-item">📋 Clipboard</div>
                <div className="feature-item">📁 File Operations</div>
                <div className="feature-item">🌐 Open URLs</div>
                <div className="feature-item">🪟 Window Control</div>
                <div className="feature-item">⚡ Run Commands</div>
              </div>
            </div>

            <div className="desktop-setup">
              <h2>🔧 Setup Instructions</h2>
              <ol>
                <li>Download the Desktop Agent ZIP file</li>
                <li>Extract to a folder on your PC</li>
                <li>Edit <code>config.json</code> with your user credentials</li>
                <li>Run <code>python agent.py</code> or double-click the executable</li>
                <li>The agent will connect automatically to this dashboard</li>
              </ol>
            </div>
          </div>
        )}

        {/* Settings Tab */}
        {activeTab === 'settings' && (
          <div className="settings-page" data-testid="settings-page">
            <h1>⚙️ Settings</h1>
            <div className="settings-section">
              <h2>👤 Profile</h2>
              <div className="profile-info">
                <div className="avatar-large">{user?.name?.[0]?.toUpperCase() || 'U'}</div>
                <div>
                  <h3>{user?.name}</h3>
                  <p>{user?.email}</p>
                  <small>Member since {new Date().toLocaleDateString()}</small>
                </div>
              </div>
            </div>
            <div className="settings-section">
              <h2>🎨 Preferences</h2>
              <div className="preference-item">
                <span>Language</span>
                <select defaultValue="en">
                  <option value="en">English</option>
                  <option value="hi">Hindi</option>
                </select>
              </div>
              <div className="preference-item">
                <span>AI Personality</span>
                <select defaultValue="friendly">
                  <option value="friendly">Friendly</option>
                  <option value="professional">Professional</option>
                  <option value="casual">Casual</option>
                </select>
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
