import { useState } from "react";
import { motion } from "framer-motion";
import { User, Globe, Bell, Mic, Save } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useAuth } from "@/lib/auth-context";
import { useToast } from "@/hooks/use-toast";

const SettingsPage = () => {
  const { user } = useAuth();
  const { toast } = useToast();
  const [prefs, setPrefs] = useState({
    language: user?.preferences?.language || "en",
    timezone: user?.preferences?.timezone || "Asia/Kolkata",
    notification_enabled: user?.preferences?.notification_enabled ?? true,
    voice_enabled: user?.preferences?.voice_enabled ?? true,
    personality: user?.preferences?.personality || "friendly",
  });

  const handleSave = () => {
    toast({ title: "Settings saved!", description: "Your preferences have been updated." });
  };

  const sections = [
    {
      icon: User,
      title: "Profile",
      gradient: "from-emerald-500 to-teal-400",
      content: (
        <div className="space-y-4">
          <div className="space-y-2">
            <Label className="text-xs">Name</Label>
            <Input value={user?.name || ""} disabled className="bg-secondary/30 border-border/30 h-11" />
          </div>
          <div className="space-y-2">
            <Label className="text-xs">Email</Label>
            <Input value={user?.email || ""} disabled className="bg-secondary/30 border-border/30 h-11" />
          </div>
        </div>
      ),
    },
    {
      icon: Globe,
      title: "Preferences",
      gradient: "from-blue-500 to-cyan-400",
      content: (
        <div className="space-y-4">
          {[
            { label: "Language", value: prefs.language, key: "language", options: [{ v: "en", l: "English" }, { v: "hi", l: "Hindi" }, { v: "es", l: "Spanish" }] },
            { label: "Timezone", value: prefs.timezone, key: "timezone", options: [{ v: "Asia/Kolkata", l: "Asia/Kolkata (IST)" }, { v: "America/New_York", l: "America/New_York (EST)" }, { v: "Europe/London", l: "Europe/London (GMT)" }] },
            { label: "AI Personality", value: prefs.personality, key: "personality", options: [{ v: "friendly", l: "Friendly" }, { v: "professional", l: "Professional" }, { v: "casual", l: "Casual" }, { v: "concise", l: "Concise" }] },
          ].map((field) => (
            <div key={field.key} className="space-y-2">
              <Label className="text-xs">{field.label}</Label>
              <Select value={field.value} onValueChange={(v) => setPrefs({ ...prefs, [field.key]: v })}>
                <SelectTrigger className="bg-secondary/30 border-border/30 h-11">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {field.options.map((opt) => (
                    <SelectItem key={opt.v} value={opt.v}>{opt.l}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          ))}
        </div>
      ),
    },
    {
      icon: Bell,
      title: "Notifications & Voice",
      gradient: "from-amber-500 to-yellow-400",
      content: (
        <div className="space-y-3">
          {[
            { icon: Bell, label: "Notifications", desc: "Get notified about agent activities", key: "notification_enabled", value: prefs.notification_enabled },
            { icon: Mic, label: "Voice", desc: "Enable voice interactions", key: "voice_enabled", value: prefs.voice_enabled },
          ].map((item) => (
            <div key={item.key} className="flex items-center justify-between p-3.5 rounded-xl bg-secondary/15 border border-border/20">
              <div className="flex items-center gap-3">
                <item.icon className="w-4 h-4 text-muted-foreground" />
                <div>
                  <p className="text-sm font-medium">{item.label}</p>
                  <p className="text-[11px] text-muted-foreground">{item.desc}</p>
                </div>
              </div>
              <Switch
                checked={item.value}
                onCheckedChange={(v) => setPrefs({ ...prefs, [item.key]: v })}
              />
            </div>
          ))}
        </div>
      ),
    },
  ];

  return (
    <div className="space-y-6 max-w-2xl">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-strong rounded-2xl p-6 lg:p-8 relative overflow-hidden"
      >
        <div className="absolute inset-0 mesh-gradient" />
        <div className="relative z-10">
          <p className="text-xs text-accent font-mono mb-1.5">// settings</p>
          <h1 className="text-2xl lg:text-3xl font-bold">Settings</h1>
          <p className="text-muted-foreground mt-1 text-sm">Customize your experience</p>
        </div>
      </motion.div>

      {sections.map((section, i) => (
        <motion.div
          key={section.title}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 + i * 0.1 }}
          className="glass-card rounded-2xl p-5 lg:p-6"
        >
          <div className="flex items-center gap-3 mb-5">
            <div className={`w-9 h-9 rounded-xl bg-gradient-to-br ${section.gradient} flex items-center justify-center`}>
              <section.icon className="w-4 h-4 text-white" />
            </div>
            <h3 className="text-sm font-semibold">{section.title}</h3>
          </div>
          {section.content}
        </motion.div>
      ))}

      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
      >
        <Button onClick={handleSave} className="gradient-primary text-primary-foreground gap-2">
          <Save className="w-4 h-4" /> Save Settings
        </Button>
      </motion.div>
    </div>
  );
};

export default SettingsPage;
