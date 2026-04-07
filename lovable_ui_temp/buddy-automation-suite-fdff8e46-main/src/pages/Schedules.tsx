import { motion } from "framer-motion";
import { Clock, Play, Pause, Plus, Zap } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";
import { mockSchedules, mockAgents } from "@/lib/mock-data";

const Schedules = () => {
  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-strong rounded-2xl p-6 lg:p-8 relative overflow-hidden"
      >
        <div className="absolute inset-0 mesh-gradient" />
        <div className="relative z-10 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div>
            <p className="text-xs text-warning font-mono mb-1.5">// schedules</p>
            <h1 className="text-2xl lg:text-3xl font-bold">Schedules</h1>
            <p className="text-muted-foreground mt-1 text-sm">Automate on autopilot</p>
          </div>
          <Button className="gradient-primary text-primary-foreground gap-2">
            <Plus className="w-4 h-4" /> New Schedule
          </Button>
        </div>
      </motion.div>

      <div className="space-y-3">
        {mockSchedules.map((schedule, i) => {
          const agent = mockAgents.find((a) => a.id === schedule.agent_id);
          return (
            <motion.div
              key={schedule.id}
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 + i * 0.08 }}
              className="glass-card rounded-2xl p-4 lg:p-5 relative overflow-hidden"
            >
              {schedule.enabled && (
                <div className="absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r from-transparent via-primary to-transparent" />
              )}
              <div className="relative z-10 flex items-center justify-between gap-4">
                <div className="flex items-center gap-4 min-w-0 flex-1">
                  <div className={`w-10 h-10 rounded-xl flex-shrink-0 flex items-center justify-center ${
                    schedule.enabled
                      ? "bg-gradient-to-br from-emerald-500 to-teal-400 shadow-lg shadow-emerald-500/20"
                      : "bg-secondary"
                  }`}>
                    {schedule.enabled ? (
                      <Play className="w-4 h-4 text-white" />
                    ) : (
                      <Pause className="w-4 h-4 text-muted-foreground" />
                    )}
                  </div>
                  <div className="min-w-0">
                    <h3 className="font-semibold text-sm truncate">{schedule.name}</h3>
                    <p className="text-xs text-muted-foreground truncate">{schedule.action}</p>
                    <div className="flex items-center gap-2 mt-1.5 flex-wrap">
                      <span className="text-[10px] font-mono text-primary bg-primary/10 px-2 py-0.5 rounded-md">
                        <Clock className="w-2.5 h-2.5 inline mr-1" />
                        {schedule.cron}
                      </span>
                      {agent && (
                        <span className="text-[10px] text-muted-foreground flex items-center gap-1">
                          <Zap className="w-2.5 h-2.5" /> {agent.name}
                        </span>
                      )}
                    </div>
                  </div>
                </div>
                <Switch checked={schedule.enabled} />
              </div>
            </motion.div>
          );
        })}

        {mockSchedules.length === 0 && (
          <div className="glass-card rounded-2xl p-12 text-center border-dashed">
            <Clock className="w-12 h-12 text-muted-foreground mx-auto mb-3 opacity-40" />
            <h3 className="text-lg font-medium mb-1">No schedules yet</h3>
            <p className="text-muted-foreground text-xs">Create your first automated schedule</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Schedules;
