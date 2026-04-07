export interface User {
  id: string;
  email: string;
  name: string;
  email_verified: boolean;
  preferences: UserPreferences;
}

export interface UserPreferences {
  language: string;
  timezone: string;
  notification_enabled: boolean;
  voice_enabled: boolean;
  personality: string;
}

export interface Agent {
  id: string;
  name: string;
  description: string;
  capabilities: string[];
  status: "active" | "offline" | "error";
}

export interface Skill {
  id: string;
  name: string;
  description: string;
  trigger_phrases: string[];
  type: "builtin" | "custom";
}

export interface Integration {
  id: string;
  name: string;
  status: "connected" | "not_connected";
}

export interface Schedule {
  id: string;
  name: string;
  cron: string;
  enabled: boolean;
  agent_id: string;
  action: string;
}
