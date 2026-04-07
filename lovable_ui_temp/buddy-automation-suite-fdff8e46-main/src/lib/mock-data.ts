import { Agent, Skill, Integration, Schedule } from "./types";

export const mockAgents: Agent[] = [
  {
    id: "email_agent",
    name: "Email Agent",
    description: "Handles Gmail operations",
    capabilities: ["send", "read", "search", "draft", "unread_count"],
    status: "active",
  },
  {
    id: "telegram_agent",
    name: "Telegram Agent",
    description: "Handles Telegram messages",
    capabilities: ["send", "receive", "groups"],
    status: "active",
  },
  {
    id: "calendar_agent",
    name: "Calendar Agent",
    description: "Handles Google Calendar operations",
    capabilities: ["create", "view", "modify", "today_summary"],
    status: "active",
  },
  {
    id: "desktop_agent",
    name: "Desktop Agent",
    description: "Controls desktop computer via websocket bridge",
    capabilities: ["apps", "files", "browser", "keyboard", "mouse", "command"],
    status: "offline",
  },
  {
    id: "skill_agent",
    name: "Skill Agent",
    description: "Executes built-in and custom skills",
    capabilities: ["execute_skill"],
    status: "active",
  },
];

export const mockSkills: Skill[] = [
  { id: "weather", name: "Weather", description: "Get current weather and forecasts", trigger_phrases: ["weather", "temperature"], type: "builtin" },
  { id: "news", name: "News", description: "Fetch latest news headlines", trigger_phrases: ["news", "headlines"], type: "builtin" },
  { id: "calculator", name: "Calculator", description: "Perform calculations", trigger_phrases: ["calculate", "math"], type: "builtin" },
  { id: "translator", name: "Translator", description: "Translate text between languages", trigger_phrases: ["translate", "translation"], type: "builtin" },
  { id: "notes", name: "Notes", description: "Create and manage personal notes", trigger_phrases: ["note", "reminder"], type: "builtin" },
];

export const mockIntegrations: Integration[] = [
  { id: "telegram", name: "Telegram", status: "not_connected" },
  { id: "gmail", name: "Gmail", status: "connected" },
  { id: "calendar", name: "Calendar", status: "connected" },
  { id: "notion", name: "Notion", status: "not_connected" },
  { id: "github", name: "Github", status: "not_connected" },
  { id: "gemini", name: "Gemini", status: "connected" },
];

export const mockSchedules: Schedule[] = [
  { id: "1", name: "Morning Briefing", cron: "0 8 * * *", enabled: true, agent_id: "email_agent", action: "Send daily summary" },
  { id: "2", name: "Calendar Sync", cron: "*/30 * * * *", enabled: true, agent_id: "calendar_agent", action: "Sync events" },
  { id: "3", name: "News Digest", cron: "0 12 * * *", enabled: false, agent_id: "skill_agent", action: "Fetch news summary" },
];
