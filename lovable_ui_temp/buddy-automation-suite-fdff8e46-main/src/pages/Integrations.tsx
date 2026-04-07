import { motion } from "framer-motion";
import { Plug, CheckCircle, Circle, ExternalLink, Mail, Send, Calendar, BookOpen, GitBranch, Cpu } from "lucide-react";
import { Button } from "@/components/ui/button";
import { mockIntegrations } from "@/lib/mock-data";

const integrationIcons: Record<string, any> = {
  telegram: Send,
  gmail: Mail,
  calendar: Calendar,
  notion: BookOpen,
  github: GitBranch,
  gemini: Cpu,
};

const integrationGradients: Record<string, string> = {
  telegram: "from-blue-400 to-cyan-400",
  gmail: "from-red-500 to-orange-400",
  calendar: "from-blue-500 to-indigo-400",
  notion: "from-gray-200 to-gray-400",
  github: "from-gray-400 to-gray-600",
  gemini: "from-blue-500 to-violet-500",
};

const Integrations = () => {
  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-strong rounded-2xl p-6 lg:p-8 relative overflow-hidden"
      >
        <div className="absolute inset-0 mesh-gradient" />
        <div className="relative z-10">
          <p className="text-xs text-info font-mono mb-1.5">// integrations</p>
          <h1 className="text-2xl lg:text-3xl font-bold">Integrations</h1>
          <p className="text-muted-foreground mt-1 text-sm">Connect your ecosystem</p>
        </div>
      </motion.div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {mockIntegrations.map((integration, i) => {
          const connected = integration.status === "connected";
          const Icon = integrationIcons[integration.id] || Plug;
          const gradient = integrationGradients[integration.id] || "from-gray-500 to-gray-400";

          return (
            <motion.div
              key={integration.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 + i * 0.08 }}
              className="glass-card rounded-2xl p-5 relative overflow-hidden"
            >
              {connected && (
                <div className="absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r from-transparent via-primary to-transparent" />
              )}
              <div className="relative z-10">
                <div className="flex items-start justify-between mb-5">
                  <div className={`w-12 h-12 rounded-2xl bg-gradient-to-br ${gradient} flex items-center justify-center shadow-lg`}>
                    <Icon className="w-6 h-6 text-white" />
                  </div>
                  {connected ? (
                    <div className="flex items-center gap-1.5 text-success text-[10px] font-mono bg-success/10 px-2.5 py-1 rounded-full">
                      <CheckCircle className="w-3 h-3" />
                      Connected
                    </div>
                  ) : (
                    <div className="flex items-center gap-1.5 text-muted-foreground text-[10px] font-mono bg-muted px-2.5 py-1 rounded-full">
                      <Circle className="w-3 h-3" />
                      Offline
                    </div>
                  )}
                </div>

                <h3 className="text-lg font-bold mb-4">{integration.name}</h3>

                <Button
                  variant={connected ? "outline" : "default"}
                  size="sm"
                  className={`w-full ${
                    !connected ? "gradient-primary text-primary-foreground" : "glass border-border/40"
                  }`}
                >
                  <span className="flex items-center gap-2">
                    {connected ? "Manage" : "Connect"}
                    <ExternalLink className="w-3.5 h-3.5" />
                  </span>
                </Button>
              </div>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
};

export default Integrations;
