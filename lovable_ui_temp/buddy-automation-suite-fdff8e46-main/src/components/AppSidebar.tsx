import { Link, useLocation } from "react-router-dom";
import { motion } from "framer-motion";
import { Bot, LayoutDashboard, Cpu, Sparkles, Plug, Clock, Settings, LogOut } from "lucide-react";
import { cn } from "@/lib/utils";
import { useAuth } from "@/lib/auth-context";
import buddyRobot from "@/assets/buddy-robot.png";

const navItems = [
  { icon: LayoutDashboard, label: "Dashboard", path: "/dashboard" },
  { icon: Cpu, label: "Agents", path: "/agents" },
  { icon: Sparkles, label: "Skills", path: "/skills" },
  { icon: Plug, label: "Integrations", path: "/integrations" },
  { icon: Clock, label: "Schedules", path: "/schedules" },
  { icon: Settings, label: "Settings", path: "/settings" },
];

const AppSidebar = ({ onNavigate }: { onNavigate?: () => void }) => {
  const location = useLocation();
  const { user, logout } = useAuth();

  return (
    <aside className="fixed left-0 top-0 h-screen w-64 glass-sidebar flex flex-col z-30 safe-top safe-bottom">
      {/* Logo */}
      <div className="p-5 flex items-center gap-3">
        <img src={buddyRobot} alt="Buddy" className="w-10 h-10 object-contain" />
        <div>
          <h1 className="font-bold text-sm text-gradient">Buddy</h1>
          <p className="text-[10px] text-muted-foreground tracking-wider uppercase">Automation</p>
        </div>
      </div>

      {/* Nav */}
      <nav className="flex-1 px-3 py-2 space-y-0.5">
        {navItems.map((item, i) => {
          const isActive = location.pathname === item.path;
          return (
            <motion.div
              key={item.path}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.05 + i * 0.04 }}
            >
              <Link
                to={item.path}
                onClick={onNavigate}
                className={cn(
                  "flex items-center gap-3 px-4 py-2.5 rounded-xl text-sm font-medium transition-all duration-300 relative overflow-hidden",
                  isActive
                    ? "text-primary"
                    : "text-muted-foreground hover:text-foreground hover:bg-secondary/30"
                )}
              >
                {isActive && (
                  <motion.div
                    layoutId="sidebar-active"
                    className="absolute inset-0 bg-primary/8 border border-primary/15 rounded-xl"
                    transition={{ type: "spring", stiffness: 200, damping: 25 }}
                  />
                )}
                {isActive && (
                  <motion.div
                    layoutId="sidebar-glow"
                    className="absolute left-0 top-1/2 -translate-y-1/2 w-[3px] h-5 gradient-primary rounded-r-full"
                    transition={{ type: "spring", stiffness: 200, damping: 25 }}
                  />
                )}
                <item.icon className={cn("w-[18px] h-[18px] relative z-10", isActive && "text-primary")} />
                <span className="relative z-10">{item.label}</span>
              </Link>
            </motion.div>
          );
        })}
      </nav>

      {/* User */}
      <div className="p-3 border-t border-border/20">
        <div className="flex items-center gap-3 px-3 py-2">
          <div className="w-8 h-8 rounded-full gradient-accent flex items-center justify-center text-xs font-bold text-accent-foreground">
            {user?.name?.charAt(0)?.toUpperCase() || "U"}
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium truncate">{user?.name || "User"}</p>
            <p className="text-[11px] text-muted-foreground truncate">{user?.email || ""}</p>
          </div>
          <button
            onClick={() => { logout(); onNavigate?.(); }}
            className="text-muted-foreground hover:text-destructive transition-colors p-1.5 rounded-lg hover:bg-destructive/10"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>
    </aside>
  );
};

export default AppSidebar;
