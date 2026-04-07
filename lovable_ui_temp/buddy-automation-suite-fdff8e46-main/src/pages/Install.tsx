import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Download, Smartphone, Check, ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";
import buddyRobot from "@/assets/buddy-robot.png";

interface BeforeInstallPromptEvent extends Event {
  prompt: () => Promise<void>;
  userChoice: Promise<{ outcome: "accepted" | "dismissed" }>;
}

const Install = () => {
  const [deferredPrompt, setDeferredPrompt] = useState<BeforeInstallPromptEvent | null>(null);
  const [isInstalled, setIsInstalled] = useState(false);

  useEffect(() => {
    const handler = (e: Event) => {
      e.preventDefault();
      setDeferredPrompt(e as BeforeInstallPromptEvent);
    };
    window.addEventListener("beforeinstallprompt", handler);

    if (window.matchMedia("(display-mode: standalone)").matches) {
      setIsInstalled(true);
    }

    return () => window.removeEventListener("beforeinstallprompt", handler);
  }, []);

  const handleInstall = async () => {
    if (!deferredPrompt) return;
    await deferredPrompt.prompt();
    const { outcome } = await deferredPrompt.userChoice;
    if (outcome === "accepted") setIsInstalled(true);
    setDeferredPrompt(null);
  };

  return (
    <div className="min-h-screen bg-background flex flex-col items-center justify-center p-6 relative overflow-hidden">
      <div className="fixed inset-0 z-0 opacity-[0.03]" style={{
        backgroundImage: "linear-gradient(hsl(160 84% 39%) 1px, transparent 1px), linear-gradient(90deg, hsl(160 84% 39%) 1px, transparent 1px)",
        backgroundSize: "60px 60px",
      }} />

      <div className="relative z-10 max-w-md w-full text-center space-y-8">
        <motion.img
          src={buddyRobot}
          alt="AI Buddy"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, type: "spring" }}
          className="w-48 h-48 mx-auto object-contain drop-shadow-[0_0_30px_hsl(160_84%_39%/0.3)]"
        />

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="space-y-3"
        >
          <h1 className="text-3xl font-bold">
            <span className="text-gradient">Buddy</span> Install karein
          </h1>
          <p className="text-muted-foreground">
            Apne phone pe install karke real app jaisa experience paayein — offline bhi chalega!
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="space-y-4"
        >
          {isInstalled ? (
            <div className="glass rounded-2xl p-6 space-y-3">
              <Check className="w-12 h-12 text-primary mx-auto" />
              <p className="text-primary font-semibold text-lg">App installed hai! 🎉</p>
              <p className="text-muted-foreground text-sm">Home screen se kholein.</p>
            </div>
          ) : deferredPrompt ? (
            <Button
              onClick={handleInstall}
              size="lg"
              className="w-full h-14 gradient-primary text-primary-foreground font-semibold text-lg gap-3"
            >
              <Download className="w-6 h-6" />
              Install App
            </Button>
          ) : (
            <div className="glass rounded-2xl p-6 space-y-4">
              <Smartphone className="w-10 h-10 text-primary mx-auto" />
              <div className="space-y-2 text-sm text-muted-foreground">
                <p className="font-semibold text-foreground">Manual install:</p>
                <p><strong>iPhone:</strong> Safari → Share → "Add to Home Screen"</p>
                <p><strong>Android:</strong> Chrome menu → "Install app" ya "Add to Home Screen"</p>
              </div>
            </div>
          )}
        </motion.div>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.7 }}
        >
          <Link to="/login" className="inline-flex items-center gap-2 text-primary hover:underline text-sm">
            <ArrowLeft className="w-4 h-4" />
            Login pe jaayein
          </Link>
        </motion.div>
      </div>
    </div>
  );
};

export default Install;
