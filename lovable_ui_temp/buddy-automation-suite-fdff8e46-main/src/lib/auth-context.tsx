import React, { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { User } from "./types";

interface AuthContextType {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (name: string, email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType>({} as AuthContextType);

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(localStorage.getItem("buddy_token"));
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (token) {
      // Simulate fetching user - UI only, no real API calls
      const savedUser = localStorage.getItem("buddy_user");
      if (savedUser) {
        setUser(JSON.parse(savedUser));
      }
    }
    setIsLoading(false);
  }, [token]);

  const login = async (email: string, password: string) => {
    // UI only - mock login
    const mockUser: User = {
      id: "1",
      email,
      name: email.split("@")[0],
      email_verified: true,
      preferences: {
        language: "en",
        timezone: "Asia/Kolkata",
        notification_enabled: true,
        voice_enabled: true,
        personality: "friendly",
      },
    };
    const mockToken = "mock-token-" + Date.now();
    localStorage.setItem("buddy_token", mockToken);
    localStorage.setItem("buddy_user", JSON.stringify(mockUser));
    setToken(mockToken);
    setUser(mockUser);
  };

  const register = async (name: string, email: string, password: string) => {
    const mockUser: User = {
      id: "1",
      email,
      name,
      email_verified: false,
      preferences: {
        language: "en",
        timezone: "Asia/Kolkata",
        notification_enabled: true,
        voice_enabled: true,
        personality: "friendly",
      },
    };
    const mockToken = "mock-token-" + Date.now();
    localStorage.setItem("buddy_token", mockToken);
    localStorage.setItem("buddy_user", JSON.stringify(mockUser));
    setToken(mockToken);
    setUser(mockUser);
  };

  const logout = () => {
    localStorage.removeItem("buddy_token");
    localStorage.removeItem("buddy_user");
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, isLoading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
