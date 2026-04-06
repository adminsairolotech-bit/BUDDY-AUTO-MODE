# 🤖 BUDDY AI - Complete UI Specification for Lovable

## 📋 Document Overview
**App Name:** BUDDY AI - Personal Assistant  
**Backend URL:** `https://buddy-automation.preview.emergentagent.com`  
**Design Style:** 3D Glassmorphism, Futuristic, Dark Theme  
**Target:** Premium AI Assistant Experience

---

# 🎨 DESIGN SYSTEM

## Color Palette

### Primary Colors
```
Background Dark:     #0a0a0f (Deep Space Black)
Background Card:     #12121a (Card Dark)
Primary Accent:      #6366f1 (Electric Indigo)
Secondary Accent:    #8b5cf6 (Vivid Purple)
Tertiary Accent:     #06b6d4 (Cyber Cyan)
Success:             #10b981 (Neon Green)
Warning:             #f59e0b (Amber Glow)
Error:               #ef4444 (Red Alert)
```

### Gradient Combinations
```
Hero Gradient:       linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #06b6d4 100%)
Card Gradient:       linear-gradient(145deg, rgba(99,102,241,0.1) 0%, rgba(139,92,246,0.05) 100%)
Glow Effect:         0 0 40px rgba(99,102,241,0.3), 0 0 80px rgba(139,92,246,0.2)
Button Hover:        linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%)
```

### Text Colors
```
Primary Text:        #ffffff (Pure White)
Secondary Text:      #a1a1aa (Muted Gray)
Accent Text:         #6366f1 (Indigo)
Link Text:           #06b6d4 (Cyan)
```

## Typography

### Font Family
```
Primary:    'Space Grotesk', sans-serif (Headlines)
Secondary:  'Inter', sans-serif (Body)
Monospace:  'JetBrains Mono', monospace (Code/Commands)
```

### Font Sizes
```
Hero Title:      64px / 4rem (font-weight: 700)
Page Title:      48px / 3rem (font-weight: 600)
Section Title:   32px / 2rem (font-weight: 600)
Card Title:      24px / 1.5rem (font-weight: 500)
Body Large:      18px / 1.125rem (font-weight: 400)
Body:            16px / 1rem (font-weight: 400)
Caption:         14px / 0.875rem (font-weight: 400)
Small:           12px / 0.75rem (font-weight: 400)
```

## 3D Effects & Glassmorphism

### Card Style
```css
.glass-card {
  background: rgba(18, 18, 26, 0.7);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 24px;
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.4),
    0 0 0 1px rgba(255, 255, 255, 0.05),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  transform: perspective(1000px) rotateX(2deg);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.glass-card:hover {
  transform: perspective(1000px) rotateX(0deg) translateY(-8px);
  box-shadow: 
    0 20px 60px rgba(99, 102, 241, 0.3),
    0 0 0 1px rgba(99, 102, 241, 0.3);
}
```

### 3D Button Style
```css
.btn-3d {
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  border: none;
  border-radius: 16px;
  padding: 16px 32px;
  color: white;
  font-weight: 600;
  box-shadow: 
    0 4px 0 #4f46e5,
    0 8px 20px rgba(99, 102, 241, 0.4);
  transform: translateY(0);
  transition: all 0.2s ease;
}

.btn-3d:hover {
  transform: translateY(-2px);
  box-shadow: 
    0 6px 0 #4f46e5,
    0 12px 30px rgba(99, 102, 241, 0.5);
}

.btn-3d:active {
  transform: translateY(2px);
  box-shadow: 
    0 2px 0 #4f46e5,
    0 4px 10px rgba(99, 102, 241, 0.3);
}
```

### Floating Animation
```css
@keyframes float {
  0%, 100% { transform: translateY(0px) rotateX(2deg); }
  50% { transform: translateY(-10px) rotateX(-2deg); }
}

.floating-element {
  animation: float 6s ease-in-out infinite;
}
```

### Glow Pulse Animation
```css
@keyframes glow-pulse {
  0%, 100% { box-shadow: 0 0 20px rgba(99, 102, 241, 0.3); }
  50% { box-shadow: 0 0 40px rgba(99, 102, 241, 0.6); }
}
```

---

# 📱 SCREENS & COMPONENTS

## 1. SPLASH / LOADING SCREEN

### Design
- Full screen dark background (#0a0a0f)
- Centered 3D animated logo (floating effect)
- Particle background effect
- Loading progress bar with glow
- "Initializing BUDDY AI..." text

### Elements
```
┌─────────────────────────────────────────┐
│                                         │
│                                         │
│            ╭───────────────╮            │
│            │   🤖 LOGO     │  (3D Float)│
│            │   BUDDY AI    │            │
│            ╰───────────────╯            │
│                                         │
│         ████████░░░░░░░░░░ 45%          │
│         Initializing AI Engine...       │
│                                         │
│                                         │
└─────────────────────────────────────────┘
```

---

## 2. AUTH SCREENS

### 2.1 Login Screen

#### Layout
```
┌─────────────────────────────────────────┐
│  ← Back                                 │
│                                         │
│            ╭─────────────╮              │
│            │  🤖 BUDDY   │ (3D Glow)    │
│            ╰─────────────╯              │
│                                         │
│         Welcome Back, Human             │
│         Your AI assistant awaits        │
│                                         │
│  ┌─────────────────────────────────┐    │
│  │ 📧 Email                        │    │
│  └─────────────────────────────────┘    │
│                                         │
│  ┌─────────────────────────────────┐    │
│  │ 🔒 Password                     │    │
│  └─────────────────────────────────┘    │
│                                         │
│  ┌─────────────────────────────────┐    │
│  │         🚀 LOGIN                │    │
│  └─────────────────────────────────┘    │
│                                         │
│         Don't have account?             │
│         → Create Account                │
│                                         │
└─────────────────────────────────────────┘
```

#### API Integration
```javascript
// Login API
POST /api/auth/login
Body: { "email": "user@email.com", "password": "Password@123!" }
Response: { "success": true, "token": "jwt...", "refresh_token": "...", "user": {...} }

// Store tokens in localStorage
localStorage.setItem('token', response.token);
localStorage.setItem('refresh_token', response.refresh_token);
```

### 2.2 Register Screen

#### Layout
```
┌─────────────────────────────────────────┐
│  ← Back                                 │
│                                         │
│            ╭─────────────╮              │
│            │  🤖 BUDDY   │              │
│            ╰─────────────╯              │
│                                         │
│         Create Your Account             │
│         Join the AI revolution          │
│                                         │
│  ┌─────────────────────────────────┐    │
│  │ 👤 Full Name                    │    │
│  └─────────────────────────────────┘    │
│                                         │
│  ┌─────────────────────────────────┐    │
│  │ 📧 Email                        │    │
│  └─────────────────────────────────┘    │
│                                         │
│  ┌─────────────────────────────────┐    │
│  │ 🔒 Password (min 12 chars)      │    │
│  └─────────────────────────────────┘    │
│  ✓ Uppercase ✓ Lowercase               │
│  ✓ Number   ✓ Special char             │
│                                         │
│  ┌─────────────────────────────────┐    │
│  │       ✨ CREATE ACCOUNT         │    │
│  └─────────────────────────────────┘    │
│                                         │
│         Already have account?           │
│         → Login                         │
│                                         │
└─────────────────────────────────────────┘
```

#### API Integration
```javascript
// Register API
POST /api/auth/register
Body: { "email": "...", "password": "...", "name": "..." }
// Password must have: 12+ chars, uppercase, lowercase, number, special char
```

---

## 3. MAIN DASHBOARD

### Layout
```
┌─────────────────────────────────────────────────────────────────┐
│  ┌─────┐                                              👤 User   │
│  │BUDDY│  Dashboard    Skills    Integrations    Settings       │
│  └─────┘                                                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ╭─────────────────────────────────────────────────────────╮   │
│   │                                                         │   │
│   │     👋 Hello, {User Name}!                             │   │
│   │                                                         │   │
│   │     "How can I assist you today?"                       │   │
│   │                                                         │   │
│   │  ┌─────────────────────────────────────────────────┐    │   │
│   │  │ 💬 Type your command or ask anything...    🎤 📎│    │   │
│   │  └─────────────────────────────────────────────────┘    │   │
│   │                                                         │   │
│   ╰─────────────────────────────────────────────────────────╯   │
│                                                                 │
│   ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│   │ 🌤️ Weather      │  │ 📰 News         │  │ 🧮 Calculator   │ │
│   │ Quick Access    │  │ Latest Updates  │  │ Quick Math      │ │
│   │ ─────────────── │  │ ─────────────── │  │ ─────────────── │ │
│   │ Click to ask    │  │ Click to ask    │  │ Click to use    │ │
│   └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│                                                                 │
│   ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│   │ 🌐 Translator   │  │ 📝 Notes        │  │ 🖥️ Desktop      │ │
│   │ Any Language    │  │ Quick Notes     │  │ Remote Control  │ │
│   │ ─────────────── │  │ ─────────────── │  │ ─────────────── │ │
│   │ Click to use    │  │ Click to open   │  │ Connect Agent   │ │
│   └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│                                                                 │
│   ╭─────────────────────────────────────────────────────────╮   │
│   │  📊 Recent Activity                                     │   │
│   │  ─────────────────────────────────────────────────────  │   │
│   │  • "What's the weather?" - 2 min ago                    │   │
│   │  • "Translate hello to Hindi" - 5 min ago               │   │
│   │  • "Calculate 25 * 4" - 10 min ago                      │   │
│   ╰─────────────────────────────────────────────────────────╯   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### API Integration
```javascript
// Get User Profile
GET /api/auth/me
Headers: { "Authorization": "Bearer {token}" }

// Send Command
POST /api/command
Headers: { "Authorization": "Bearer {token}" }
Body: { "command": "What's the weather?", "type": "text" }
Response: { "success": true, "response": { "text": "...", "action_taken": {...} } }

// Get Skills
GET /api/skills
Headers: { "Authorization": "Bearer {token}" }
```

---

## 4. CHAT / COMMAND INTERFACE

### Full Chat Screen Layout
```
┌─────────────────────────────────────────────────────────────────┐
│  ← Dashboard              💬 BUDDY Chat              ⚙️ ⋮      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                     ╭───────────────────────╮                   │
│                     │ Today, 2:30 PM        │                   │
│                     ╰───────────────────────╯                   │
│                                                                 │
│   ╭─────────────────────────────────────────────────────╮       │
│   │ 🤖 BUDDY                                            │       │
│   │                                                     │       │
│   │ Hello! I'm your AI assistant. I can help you with: │       │
│   │ • Weather updates                                   │       │
│   │ • News briefings                                    │       │
│   │ • Calculations                                      │       │
│   │ • Translations                                      │       │
│   │ • Desktop automation                                │       │
│   │                                                     │       │
│   │ What would you like to do?                          │       │
│   ╰─────────────────────────────────────────────────────╯       │
│                                                                 │
│       ╭─────────────────────────────────────────────────╮       │
│       │                                            👤 You│       │
│       │                                                 │       │
│       │ What's the weather in Mumbai?                   │       │
│       ╰─────────────────────────────────────────────────╯       │
│                                                                 │
│   ╭─────────────────────────────────────────────────────╮       │
│   │ 🤖 BUDDY                                   🌤️ Weather│       │
│   │                                                     │       │
│   │ Here's the weather for Mumbai:                      │       │
│   │ ┌─────────────────────────────────────────┐         │       │
│   │ │  🌡️ 32°C  │  💧 65%  │  💨 12 km/h     │         │       │
│   │ │  Sunny    │  Humidity │  Wind          │         │       │
│   │ └─────────────────────────────────────────┘         │       │
│   ╰─────────────────────────────────────────────────────╯       │
│                                                                 │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ 💬 Type your message...                         🎤  📎  ➤ │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│    💡 Suggestions:                                              │
│    ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐         │
│    │ Weather  │ │ News     │ │ Calculate│ │ Translate│         │
│    └──────────┘ └──────────┘ └──────────┘ └──────────┘         │
└─────────────────────────────────────────────────────────────────┘
```

### Message Bubble Components

#### User Message (Right Aligned)
```css
.user-message {
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  border-radius: 20px 20px 4px 20px;
  padding: 16px 20px;
  max-width: 70%;
  margin-left: auto;
  color: white;
  box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
}
```

#### Bot Message (Left Aligned)
```css
.bot-message {
  background: rgba(18, 18, 26, 0.8);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 20px 20px 20px 4px;
  padding: 16px 20px;
  max-width: 70%;
  color: white;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}
```

---

## 5. SKILLS PAGE

### Layout
```
┌─────────────────────────────────────────────────────────────────┐
│  ← Back                    ⚡ Skills                    + Add   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   🔍 Search skills...                                           │
│                                                                 │
│   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                 │
│   Built-in Skills                                               │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  🌤️                                                     │   │
│   │  Weather                                      ✓ Active  │   │
│   │  Get weather updates for any location                   │   │
│   │  ─────────────────────────────────────────────────────  │   │
│   │  Triggers: "weather", "temperature", "forecast"         │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  📰                                                     │   │
│   │  News                                         ✓ Active  │   │
│   │  Get latest news and updates                            │   │
│   │  ─────────────────────────────────────────────────────  │   │
│   │  Triggers: "news", "headlines", "updates"               │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  🧮                                                     │   │
│   │  Calculator                                   ✓ Active  │   │
│   │  Perform mathematical calculations                      │   │
│   │  ─────────────────────────────────────────────────────  │   │
│   │  Triggers: "calculate", "math", "compute"               │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  🌐                                                     │   │
│   │  Translator                                   ✓ Active  │   │
│   │  Translate text between languages                       │   │
│   │  ─────────────────────────────────────────────────────  │   │
│   │  Triggers: "translate", "convert language"              │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  📝                                                     │   │
│   │  Notes                                        ✓ Active  │   │
│   │  Create and manage quick notes                          │   │
│   │  ─────────────────────────────────────────────────────  │   │
│   │  Triggers: "note", "remember", "save"                   │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### API
```javascript
// Get Skills
GET /api/skills
Headers: { "Authorization": "Bearer {token}" }
Response: {
  "success": true,
  "skills": [
    { "id": "weather", "name": "Weather", "description": "...", "trigger_phrases": [...] },
    ...
  ]
}
```

---

## 6. INTEGRATIONS PAGE

### Layout
```
┌─────────────────────────────────────────────────────────────────┐
│  ← Back                 🔗 Integrations                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Connect your favorite services                                │
│                                                                 │
│   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  📱 Telegram                                            │   │
│   │  ─────────────────────────────────────────────────────  │   │
│   │  Send & receive messages via Telegram                   │   │
│   │                                                         │   │
│   │  Status: ⚪ Not Connected         [ 🔗 Connect ]        │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  📧 Gmail                                               │   │
│   │  ─────────────────────────────────────────────────────  │   │
│   │  Read and send emails                                   │   │
│   │                                                         │   │
│   │  Status: ⚪ Not Connected         [ 🔗 Connect ]        │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  📅 Calendar                                            │   │
│   │  ─────────────────────────────────────────────────────  │   │
│   │  Manage your schedule and events                        │   │
│   │                                                         │   │
│   │  Status: ⚪ Not Connected         [ 🔗 Connect ]        │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  📓 Notion                                              │   │
│   │  ─────────────────────────────────────────────────────  │   │
│   │  Access your Notion workspace                           │   │
│   │                                                         │   │
│   │  Status: ⚪ Not Connected         [ 🔗 Connect ]        │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  🐙 GitHub                                              │   │
│   │  ─────────────────────────────────────────────────────  │   │
│   │  Manage repositories and code                           │   │
│   │                                                         │   │
│   │  Status: ⚪ Not Connected         [ 🔗 Connect ]        │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  🤖 Gemini AI                                           │   │
│   │  ─────────────────────────────────────────────────────  │   │
│   │  Enhanced AI responses powered by Gemini                │   │
│   │                                                         │   │
│   │  Status: ⚪ Not Connected         [ 🔗 Connect ]        │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### API
```javascript
// Get Integrations
GET /api/integrations
Headers: { "Authorization": "Bearer {token}" }

// Connect Integration
POST /api/integrations/{integration_id}/connect
Headers: { "Authorization": "Bearer {token}" }
Body: { "bot_token": "...", "config": {...} }
```

---

## 7. DESKTOP AGENT PAGE

### Layout
```
┌─────────────────────────────────────────────────────────────────┐
│  ← Back                 🖥️ Desktop Agent                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ╭─────────────────────────────────────────────────────────╮   │
│   │                                                         │   │
│   │              ┌─────────────────────┐                    │   │
│   │              │                     │                    │   │
│   │              │    🖥️ Desktop       │                    │   │
│   │              │                     │                    │   │
│   │              │    ⚪ Offline       │                    │   │
│   │              │                     │                    │   │
│   │              └─────────────────────┘                    │   │
│   │                                                         │   │
│   │   Status: Not Connected                                 │   │
│   │                                                         │   │
│   ╰─────────────────────────────────────────────────────────╯   │
│                                                                 │
│   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                 │
│   📥 Download Desktop Agent                                     │
│                                                                 │
│   To control your computer remotely, download and install       │
│   the BUDDY Desktop Agent on your Windows PC.                   │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                                                         │   │
│   │         💻 Download for Windows (.exe)                  │   │
│   │                                                         │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                 │
│   ⚡ Available Actions (when connected)                         │
│                                                                 │
│   ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐   │
│   │ 📷        │ │ ⌨️         │ │ 🖱️         │ │ 📋        │   │
│   │ Screenshot│ │ Type Text  │ │ Mouse      │ │ Clipboard  │   │
│   └────────────┘ └────────────┘ └────────────┘ └────────────┘   │
│                                                                 │
│   ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐   │
│   │ 📁        │ │ 🌐         │ │ 🪟         │ │ ⚡        │   │
│   │ Files     │ │ Browser    │ │ Windows    │ │ Run Cmd   │   │
│   └────────────┘ └────────────┘ └────────────┘ └────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### API
```javascript
// Get Desktop Status
GET /api/desktop/status
Headers: { "Authorization": "Bearer {token}" }
Response: { "success": true, "status": "offline", "agent_info": null }

// Send Desktop Command
POST /api/desktop/command
Headers: { "Authorization": "Bearer {token}" }
Body: { "action": "screenshot", "params": {} }
```

---

## 8. SCHEDULES PAGE

### Layout
```
┌─────────────────────────────────────────────────────────────────┐
│  ← Back                  ⏰ Schedules                  + New    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Automate your daily tasks                                     │
│                                                                 │
│   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  ☀️ Morning Briefing                         🟢 Active  │   │
│   │  ─────────────────────────────────────────────────────  │   │
│   │  ⏰ Every day at 9:00 AM                                │   │
│   │                                                         │   │
│   │  Actions:                                               │   │
│   │  • Get weather update                                   │   │
│   │  • Read top news headlines                              │   │
│   │  • Check calendar events                                │   │
│   │                                                         │   │
│   │  [ ✏️ Edit ]  [ 🗑️ Delete ]  [ ⏸️ Pause ]              │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  🌙 Evening Summary                          🟢 Active  │   │
│   │  ─────────────────────────────────────────────────────  │   │
│   │  ⏰ Every day at 8:00 PM                                │   │
│   │                                                         │   │
│   │  Actions:                                               │   │
│   │  • Summarize today's activities                         │   │
│   │  • Tomorrow's calendar preview                          │   │
│   │                                                         │   │
│   │  [ ✏️ Edit ]  [ 🗑️ Delete ]  [ ⏸️ Pause ]              │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│   ╭─────────────────────────────────────────────────────────╮   │
│   │                                                         │   │
│   │     No more schedules. Create one to automate tasks!    │   │
│   │                                                         │   │
│   │              [ + Create Schedule ]                      │   │
│   │                                                         │   │
│   ╰─────────────────────────────────────────────────────────╯   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### API
```javascript
// List Schedules
GET /api/schedules
Headers: { "Authorization": "Bearer {token}" }

// Create Schedule
POST /api/schedules
Headers: { "Authorization": "Bearer {token}" }
Body: {
  "name": "Morning Briefing",
  "cron": "0 9 * * *",
  "description": "Daily morning update",
  "actions": [
    { "type": "skill", "skill_id": "weather" },
    { "type": "skill", "skill_id": "news" }
  ]
}

// Update Schedule
PUT /api/schedules/{schedule_id}
Headers: { "Authorization": "Bearer {token}" }

// Delete Schedule
DELETE /api/schedules/{schedule_id}
Headers: { "Authorization": "Bearer {token}" }
```

---

## 9. SETTINGS PAGE

### Layout
```
┌─────────────────────────────────────────────────────────────────┐
│  ← Back                   ⚙️ Settings                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   👤 Profile                                                    │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                                                         │   │
│   │    ╭────────╮  John Doe                                 │   │
│   │    │  👤    │  john@example.com                         │   │
│   │    ╰────────╯  Member since Jan 2024                    │   │
│   │                                                         │   │
│   │    [ ✏️ Edit Profile ]                                  │   │
│   │                                                         │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                 │
│   🎨 Preferences                                                │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                                                         │   │
│   │  Language           [ English          ▼ ]              │   │
│   │                                                         │   │
│   │  Timezone           [ Asia/Kolkata     ▼ ]              │   │
│   │                                                         │   │
│   │  Personality        [ Friendly         ▼ ]              │   │
│   │                                                         │   │
│   │  Notifications      [ 🟢 Enabled        ]               │   │
│   │                                                         │   │
│   │  Voice Mode         [ 🟢 Enabled        ]               │   │
│   │                                                         │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                 │
│   🔐 Security                                                   │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                                                         │   │
│   │  [ 🔑 Change Password ]                                 │   │
│   │                                                         │   │
│   │  [ 🚪 Logout from all devices ]                         │   │
│   │                                                         │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                 │
│   🗑️ Danger Zone                                                │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                                                         │   │
│   │  [ 📥 Export My Data ]                                  │   │
│   │                                                         │   │
│   │  [ ❌ Delete All Memory ]                               │   │
│   │                                                         │   │
│   │  [ ☠️ Delete Account (Forget Me) ]                      │   │
│   │                                                         │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                                                 │
│               [ 🚪 Logout ]                                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### API
```javascript
// Logout
POST /api/auth/logout
Headers: { "Authorization": "Bearer {token}" }

// Export Data
POST /api/privacy/export
Headers: { "Authorization": "Bearer {token}" }

// Delete All Memory
DELETE /api/memory/all
Headers: { "Authorization": "Bearer {token}" }

// Forget Me (Delete Account)
POST /api/privacy/forget-me
Headers: { "Authorization": "Bearer {token}" }
```

---

# 🔗 COMPLETE API REFERENCE

## Base URL
```
https://buddy-automation.preview.emergentagent.com
```

## Authentication
All protected endpoints require:
```
Headers: { "Authorization": "Bearer {token}" }
```

## Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login user |
| GET | `/api/auth/me` | Get current user |
| POST | `/api/auth/refresh` | Refresh token |
| POST | `/api/auth/logout` | Logout user |
| POST | `/api/command` | Send AI command |
| GET | `/api/skills` | List all skills |
| GET | `/api/schedules` | List schedules |
| POST | `/api/schedules` | Create schedule |
| PUT | `/api/schedules/{id}` | Update schedule |
| DELETE | `/api/schedules/{id}` | Delete schedule |
| GET | `/api/integrations` | List integrations |
| POST | `/api/integrations/{id}/connect` | Connect integration |
| DELETE | `/api/integrations/{id}` | Disconnect |
| GET | `/api/desktop/status` | Desktop agent status |
| POST | `/api/desktop/command` | Send desktop command |
| GET | `/api/memory/{key}` | Get memory item |
| POST | `/api/memory` | Store memory |
| DELETE | `/api/memory/all` | Delete all memory |
| POST | `/api/privacy/export` | Export user data |
| POST | `/api/privacy/forget-me` | Delete account |
| GET | `/api/agents` | List available agents |
| GET | `/api/health` | Health check |

---

# 📦 COMPONENT LIBRARY

## Reusable Components Needed

### 1. GlassCard
```jsx
<GlassCard>
  <CardHeader>
    <CardTitle>Title</CardTitle>
  </CardHeader>
  <CardContent>
    Content here
  </CardContent>
</GlassCard>
```

### 2. Button3D
```jsx
<Button3D variant="primary" onClick={}>
  Click Me
</Button3D>
```

### 3. InputField
```jsx
<InputField
  icon={<MailIcon />}
  placeholder="Email"
  type="email"
  value={email}
  onChange={setEmail}
/>
```

### 4. ChatBubble
```jsx
<ChatBubble type="user" message="Hello!" />
<ChatBubble type="bot" message="Hi there!" />
```

### 5. SkillCard
```jsx
<SkillCard
  icon="🌤️"
  name="Weather"
  description="Get weather updates"
  triggers={["weather", "temperature"]}
  active={true}
/>
```

### 6. IntegrationCard
```jsx
<IntegrationCard
  icon="📱"
  name="Telegram"
  description="Send messages"
  status="not_connected"
  onConnect={() => {}}
/>
```

### 7. ScheduleCard
```jsx
<ScheduleCard
  name="Morning Briefing"
  cron="0 9 * * *"
  actions={[...]}
  active={true}
  onEdit={() => {}}
  onDelete={() => {}}
/>
```

### 8. NavBar
```jsx
<NavBar
  user={currentUser}
  activeTab="dashboard"
  onLogout={() => {}}
/>
```

### 9. Loading Spinner
```jsx
<LoadingSpinner size="lg" text="Loading..." />
```

### 10. Toast Notification
```jsx
<Toast type="success" message="Action completed!" />
<Toast type="error" message="Something went wrong!" />
```

---

# 🎬 ANIMATIONS

## Page Transitions
```css
.page-enter {
  opacity: 0;
  transform: translateX(20px);
}
.page-enter-active {
  opacity: 1;
  transform: translateX(0);
  transition: all 0.3s ease-out;
}
```

## Card Hover
```css
.card {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}
.card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 0 20px 40px rgba(99, 102, 241, 0.2);
}
```

## Button Press
```css
.btn:active {
  transform: scale(0.95);
}
```

## Typing Indicator
```css
@keyframes typing {
  0%, 60%, 100% { transform: translateY(0); }
  30% { transform: translateY(-10px); }
}
.typing-dot {
  animation: typing 1.4s infinite;
}
.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }
```

---

# ✅ IMPLEMENTATION CHECKLIST

## Phase 1: Core
- [ ] Splash Screen
- [ ] Login Screen
- [ ] Register Screen
- [ ] Dashboard
- [ ] Chat Interface

## Phase 2: Features
- [ ] Skills Page
- [ ] Integrations Page
- [ ] Schedules Page
- [ ] Desktop Agent Page

## Phase 3: Settings
- [ ] Settings Page
- [ ] Profile Edit
- [ ] Privacy Controls

## Phase 4: Polish
- [ ] Loading States
- [ ] Error Handling
- [ ] Animations
- [ ] Responsive Design

---

**Document Version:** 1.0  
**Created For:** Lovable.dev  
**Backend Ready:** ✅ Yes  
**Last Updated:** April 2026
