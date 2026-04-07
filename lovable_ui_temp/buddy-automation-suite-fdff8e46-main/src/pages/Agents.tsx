import { motion } from "framer-motion";
import { Wifi, WifiOff, ArrowUpRight } from "lucide-react";
import { mockAgents } from "@/lib/mock-data";

const agentIcons: Record<string, string> = {
  email_agent: "📧",
  telegram_agent: "✈️",
  calendar_agent: "📅",
  desktop_agent: "🖥️",
  skill_agent: "⚡",
};

const Agents = () => {
  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-strong rounded-2xl p-6 lg:p-8 relative overflow-hidden"
      >
        <div className="absolute inset-0 mesh-gradient" />
        <div className="relative z-10">
          <p className="text-xs text-primary font-mono mb-1.5">// agents</p>
          <h1 className="text-2xl lg:text-3xl font-bold">AI Agents</h1>
          <p className="text-muted-foreground mt-1 text-sm">Your intelligent automation workforce</p>
        </div>
      </motion.div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {mockAgents.map((agent, i) => (
          <motion.div
            key={agent.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 + i * 0.08 }}
            className="glass-card rounded-2xl p-5 relative overflow-hidden group cursor-pointer"
          >
            <div className="relative z-10">
              <div className="flex items-start justify-between mb-4">
                <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-primary/20 to-accent/10 flex items-center justify-center text-2xl border border-primary/10">
                  {agentIcons[agent.id] || "🤖"}
                </div>
                <div className="flex items-center gap-2">
                  {agent.status === "active" ? (
                    <Wifi className="w-3.5 h-3.5 text-success" />
                  ) : (
                    <WifiOff className="w-3.5 h-3.5 text-muted-foreground" />
                  )}
                  <span className={`text-[10px] font-mono px-2 py-0.5 rounded-md ${
                    agent.status === "active" ? "bg-success/10 text-success" : "bg-muted text-muted-foreground"
                  }`}>
                    {agent.status}
                  </span>
                </div>
              </div>

              <h3 className="text-lg font-bold mb-1">{agent.name}</h3>
              <p className="text-xs text-muted-foreground mb-4">{agent.description}</p>

              <div className="flex flex-wrap gap-1.5">
                {agent.capabilities.map((cap) => (
                  <span
                    key={cap}
                    className="text-[10px] font-mono bg-primary/5 text-primary/80 border border-primary/10 px-2 py-0.5 rounded-md"
                  >
                    {cap}
                  </span>
                ))}
              </div>

              <ArrowUpRight className="absolute top-4 right-4 w-4 h-4 text-primary opacity-0 group-hover:opacity-100 transition-opacity" />
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default Agents;
