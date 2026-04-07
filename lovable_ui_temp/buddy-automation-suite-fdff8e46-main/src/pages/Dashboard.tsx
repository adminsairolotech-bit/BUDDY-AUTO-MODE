import { motion } from "framer-motion";
import { Cpu, Sparkles, Plug, Clock, Activity, TrendingUp, CheckCircle, ArrowUpRight } from "lucide-react";
import { useAuth } from "@/lib/auth-context";
import { mockAgents, mockSkills, mockIntegrations, mockSchedules } from "@/lib/mock-data";

const Dashboard = () => {
  const { user } = useAuth();
  const activeAgents = mockAgents.filter((a) => a.status === "active").length;
  const connectedIntegrations = mockIntegrations.filter((i) => i.status === "connected").length;
  const enabledSchedules = mockSchedules.filter((s) => s.enabled).length;

  const stats = [
    { label: "Active Agents", value: activeAgents, total: mockAgents.length, icon: Cpu, gradient: "from-emerald-500 to-teal-400" },
    { label: "Skills", value: mockSkills.length, total: mockSkills.length, icon: Sparkles, gradient: "from-violet-500 to-purple-400" },
    { label: "Integrations", value: connectedIntegrations, total: mockIntegrations.length, icon: Plug, gradient: "from-blue-500 to-cyan-400" },
    { label: "Schedules", value: enabledSchedules, total: mockSchedules.length, icon: Clock, gradient: "from-amber-500 to-yellow-400" },
  ];

  const greeting = new Date().getHours() < 12 ? "Good morning" : new Date().getHours() < 17 ? "Good afternoon" : "Good evening";

  return (
    <div className="space-y-6">
      {/* Hero */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-strong rounded-2xl p-6 lg:p-8 relative overflow-hidden"
      >
        <div className="absolute inset-0 mesh-gradient" />
        <div className="relative z-10">
          <p className="text-xs text-primary font-mono mb-1.5">// dashboard</p>
          <h1 className="text-2xl lg:text-3xl font-bold">
            {greeting}, <span className="text-gradient">{user?.name}</span>
          </h1>
          <p className="text-muted-foreground mt-1 text-sm">Your automation empire at a glance</p>
        </div>
      </motion.div>

      {/* Stats */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 lg:gap-4">
        {stats.map((stat, i) => (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 + i * 0.08 }}
            className="glass-card rounded-2xl p-4 lg:p-5"
          >
            <div className="flex items-center justify-between mb-3">
              <div className={`w-10 h-10 rounded-xl bg-gradient-to-br ${stat.gradient} flex items-center justify-center`}>
                <stat.icon className="w-5 h-5 text-white" />
              </div>
              <span className="text-[10px] text-muted-foreground font-mono bg-secondary/50 px-1.5 py-0.5 rounded-md">
                {stat.value}/{stat.total}
              </span>
            </div>
            <p className="text-2xl lg:text-3xl font-bold">{stat.value}</p>
            <p className="text-xs text-muted-foreground mt-0.5">{stat.label}</p>
          </motion.div>
        ))}
      </div>

      {/* Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 lg:gap-6">
        {/* Agents */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="glass-card rounded-2xl p-5 lg:p-6"
        >
          <div className="flex items-center gap-2 mb-4">
            <Activity className="w-4 h-4 text-primary" />
            <h3 className="text-sm font-semibold">Agent Status</h3>
            <span className="text-[10px] font-mono text-primary bg-primary/10 px-2 py-0.5 rounded-full ml-auto">LIVE</span>
          </div>
          <div className="space-y-2">
            {mockAgents.map((agent, i) => (
              <motion.div
                key={agent.id}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.5 + i * 0.06 }}
                className="flex items-center justify-between p-3 rounded-xl bg-secondary/20 hover:bg-secondary/30 transition-all group cursor-pointer"
              >
                <div className="flex items-center gap-3">
                  <div className="relative">
                    <div className={`w-2.5 h-2.5 rounded-full ${agent.status === "active" ? "bg-success" : "bg-muted-foreground/50"}`} />
                    {agent.status === "active" && (
                      <div className="absolute inset-0 w-2.5 h-2.5 rounded-full bg-success animate-ping opacity-40" />
                    )}
                  </div>
                  <div>
                    <p className="text-sm font-medium">{agent.name}</p>
                    <p className="text-[11px] text-muted-foreground">{agent.description}</p>
                  </div>
                </div>
                <ArrowUpRight className="w-3.5 h-3.5 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity" />
              </motion.div>
            ))}
          </div>
        </motion.div>

        <div className="space-y-4 lg:space-y-6">
          {/* Integrations */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className="glass-card rounded-2xl p-5 lg:p-6"
          >
            <div className="flex items-center gap-2 mb-4">
              <Plug className="w-4 h-4 text-info" />
              <h3 className="text-sm font-semibold">Integrations</h3>
            </div>
            <div className="grid grid-cols-3 gap-2">
              {mockIntegrations.map((integration) => (
                <div
                  key={integration.id}
                  className={`p-3 rounded-xl text-center border transition-all cursor-pointer ${
                    integration.status === "connected"
                      ? "bg-primary/5 border-primary/15 hover:border-primary/30"
                      : "bg-secondary/15 border-border/30 hover:border-muted-foreground/30"
                  }`}
                >
                  <p className="text-xs font-medium">{integration.name}</p>
                  <div className="flex items-center justify-center gap-1 mt-1">
                    {integration.status === "connected" ? (
                      <CheckCircle className="w-3 h-3 text-success" />
                    ) : (
                      <div className="w-3 h-3 rounded-full border border-muted-foreground/40" />
                    )}
                    <span className="text-[10px] text-muted-foreground">
                      {integration.status === "connected" ? "On" : "Off"}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Activity */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
            className="glass-card rounded-2xl p-5 lg:p-6"
          >
            <div className="flex items-center gap-2 mb-4">
              <TrendingUp className="w-4 h-4 text-warning" />
              <h3 className="text-sm font-semibold">Today's Activity</h3>
            </div>
            <div className="space-y-3">
              {[
                { label: "Emails processed", value: 24, max: 50, color: "bg-gradient-to-r from-emerald-500 to-teal-400" },
                { label: "Tasks completed", value: 8, max: 15, color: "bg-gradient-to-r from-violet-500 to-purple-400" },
                { label: "Automations triggered", value: 12, max: 20, color: "bg-gradient-to-r from-blue-500 to-cyan-400" },
              ].map((stat, i) => (
                <div key={stat.label} className="space-y-1.5">
                  <div className="flex justify-between items-center">
                    <span className="text-xs">{stat.label}</span>
                    <span className="text-xs font-bold font-mono">{stat.value}</span>
                  </div>
                  <div className="h-1.5 rounded-full bg-secondary/50 overflow-hidden">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${(stat.value / stat.max) * 100}%` }}
                      transition={{ delay: 0.8 + i * 0.1, duration: 0.8, ease: "easeOut" }}
                      className={`h-full rounded-full ${stat.color}`}
                    />
                  </div>
                </div>
              ))}
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
