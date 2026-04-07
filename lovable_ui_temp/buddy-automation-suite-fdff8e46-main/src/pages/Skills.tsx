import { motion } from "framer-motion";
import { Sparkles, Cloud, Newspaper, Calculator, Languages, StickyNote } from "lucide-react";
import { mockSkills } from "@/lib/mock-data";

const iconMap: Record<string, any> = {
  weather: Cloud,
  news: Newspaper,
  calculator: Calculator,
  translator: Languages,
  notes: StickyNote,
};

const gradientMap: Record<string, string> = {
  weather: "from-cyan-500 to-blue-400",
  news: "from-red-500 to-orange-400",
  calculator: "from-violet-500 to-purple-400",
  translator: "from-emerald-500 to-teal-400",
  notes: "from-amber-500 to-yellow-400",
};

const Skills = () => {
  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-strong rounded-2xl p-6 lg:p-8 relative overflow-hidden"
      >
        <div className="absolute inset-0 mesh-gradient" />
        <div className="relative z-10">
          <p className="text-xs text-accent font-mono mb-1.5">// skills</p>
          <h1 className="text-2xl lg:text-3xl font-bold">Skills</h1>
          <p className="text-muted-foreground mt-1 text-sm">Superpowers your assistant can use</p>
        </div>
      </motion.div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {mockSkills.map((skill, i) => {
          const Icon = iconMap[skill.id] || Sparkles;
          const gradient = gradientMap[skill.id] || "from-gray-500 to-gray-400";
          return (
            <motion.div
              key={skill.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 + i * 0.08 }}
              className="glass-card rounded-2xl p-5 relative overflow-hidden group cursor-pointer"
            >
              <div className="relative z-10">
                <div className={`w-12 h-12 rounded-2xl bg-gradient-to-br ${gradient} flex items-center justify-center mb-4 shadow-lg`}>
                  <Icon className="w-6 h-6 text-white" />
                </div>

                <h3 className="text-lg font-bold mb-1">{skill.name}</h3>
                <p className="text-xs text-muted-foreground mb-4">{skill.description}</p>

                <div className="flex flex-wrap gap-1.5 mb-3">
                  {skill.trigger_phrases.map((phrase) => (
                    <span
                      key={phrase}
                      className="text-[10px] font-mono bg-accent/5 text-accent/80 border border-accent/15 px-2 py-0.5 rounded-md"
                    >
                      "{phrase}"
                    </span>
                  ))}
                </div>

                <span className="text-[10px] font-mono bg-secondary/50 text-muted-foreground px-2 py-0.5 rounded-md border border-border/30">
                  {skill.type}
                </span>
              </div>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
};

export default Skills;
