import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { Bot, Eye, EyeOff, Zap, ArrowRight, Sparkles, Cpu } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useAuth } from "@/lib/auth-context";
import { useToast } from "@/hooks/use-toast";
import buddyRobot from "@/assets/buddy-robot.png";
import { MorphingBlob } from "@/components/3DComponents";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [focusedField, setFocusedField] = useState<string | null>(null);
  const { login } = useAuth();
  const navigate = useNavigate();
  const { toast } = useToast();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !password) return;
    setIsLoading(true);
    try {
      await login(email, password);
      toast({ title: "Welcome back!", description: "Successfully logged in." });
      navigate("/dashboard");
    } catch {
      toast({ title: "Error", description: "Login failed.", variant: "destructive" });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen relative overflow-hidden bg-background">

      {/* Morphing Blobs */}
      <MorphingBlob className="w-96 h-96 top-[-10%] left-[-5%]" color="primary" />
      <MorphingBlob className="w-80 h-80 bottom-[-10%] right-[-5%]" color="accent" />
      <MorphingBlob className="w-64 h-64 top-[40%] right-[20%]" color="info" />

      {/* Grid overlay */}
      <div className="fixed inset-0 z-[1] opacity-[0.03]" style={{
        backgroundImage: "linear-gradient(hsl(160 84% 39%) 1px, transparent 1px), linear-gradient(90deg, hsl(160 84% 39%) 1px, transparent 1px)",
        backgroundSize: "60px 60px",
      }} />

      <div className="relative z-10 min-h-screen flex flex-col lg:flex-row">
        {/* Left - Robot (desktop) */}
        <div className="hidden lg:flex lg:w-1/2 items-center justify-center relative flex-col gap-6">
          <motion.img
            src={buddyRobot}
            alt="AI Buddy Robot"
            initial={{ opacity: 0, scale: 0.5, y: 40 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            transition={{ duration: 1, type: "spring", stiffness: 60 }}
            className="w-80 h-80 object-contain drop-shadow-[0_0_40px_hsl(160_84%_39%/0.4)] animate-float"
          />
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.8, duration: 0.8 }}
            className="glass rounded-2xl p-6 max-w-sm text-center"
          >
            <h1 className="text-3xl font-bold mb-2">
              <span className="text-gradient">Buddy</span>{" "}
              <span className="text-foreground">Automation</span>
            </h1>
            <p className="text-muted-foreground text-sm">
              Your AI assistant that controls emails, calendars, desktop & more.
            </p>
            <div className="flex items-center justify-center gap-6 mt-4 text-xs text-muted-foreground">
              <div className="flex items-center gap-1.5">
                <Cpu className="w-3.5 h-3.5 text-primary" />
                <span>5 AI Agents</span>
              </div>
              <div className="flex items-center gap-1.5">
                <Sparkles className="w-3.5 h-3.5 text-accent" />
                <span>5 Skills</span>
              </div>
              <div className="flex items-center gap-1.5">
                <Zap className="w-3.5 h-3.5 text-warning" />
                <span>6 Integrations</span>
              </div>
            </div>
          </motion.div>
        </div>

        {/* Mobile Robot (above form) */}
        <div className="lg:hidden w-full flex justify-center py-6">
          <motion.img
            src={buddyRobot}
            alt="AI Buddy Robot"
            initial={{ opacity: 0, scale: 0.5 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, type: "spring" }}
            className="w-40 h-40 object-contain drop-shadow-[0_0_30px_hsl(160_84%_39%/0.3)]"
          />
        </div>

        {/* Right - Login Form */}
        <div className="flex-1 flex items-center justify-center p-6 lg:p-12">
          <div className="w-full max-w-md">
            <motion.div
              initial={{ opacity: 0, scale: 0.9, rotateX: 10 }}
              animate={{ opacity: 1, scale: 1, rotateX: 0 }}
              transition={{ duration: 0.8, type: "spring", stiffness: 80 }}
              className="glass-strong rounded-2xl p-8 lg:p-10 relative overflow-hidden"
            >
              {/* Animated border glow */}
              <div className="absolute inset-0 rounded-2xl animated-border" />

              {/* Shimmer effect */}
              <div className="absolute inset-0 shimmer rounded-2xl" />

              <div className="relative z-10">
                {/* Mobile logo */}
                <div className="lg:hidden flex items-center gap-3 mb-8">
                  <motion.div
                    animate={{ rotateY: [0, 360] }}
                    transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
                    className="w-11 h-11 rounded-xl gradient-primary flex items-center justify-center glow-primary"
                  >
                    <Bot className="w-6 h-6 text-primary-foreground" />
                  </motion.div>
                  <span className="text-xl font-bold text-gradient">Buddy</span>
                </div>

                <motion.h2
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.3 }}
                  className="text-3xl font-bold mb-2"
                >
                  Welcome back
                </motion.h2>
                <motion.p
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.4 }}
                  className="text-muted-foreground mb-8"
                >
                  Sign in to your automation hub
                </motion.p>

                <form onSubmit={handleSubmit} className="space-y-5">
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.5 }}
                    className="space-y-2"
                  >
                    <Label htmlFor="email" className={focusedField === "email" ? "text-primary" : ""}>
                      Email
                    </Label>
                    <div className={`relative rounded-lg transition-all duration-300 ${focusedField === "email" ? "shadow-[0_0_20px_hsl(160_84%_39%/0.15)]" : ""}`}>
                      <Input
                        id="email"
                        type="email"
                        placeholder="you@example.com"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        onFocus={() => setFocusedField("email")}
                        onBlur={() => setFocusedField(null)}
                        className="h-12 bg-secondary/50 border-border/50 focus:border-primary transition-all duration-300"
                      />
                    </div>
                  </motion.div>

                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.6 }}
                    className="space-y-2"
                  >
                    <Label htmlFor="password" className={focusedField === "password" ? "text-primary" : ""}>
                      Password
                    </Label>
                    <div className={`relative rounded-lg transition-all duration-300 ${focusedField === "password" ? "shadow-[0_0_20px_hsl(160_84%_39%/0.15)]" : ""}`}>
                      <Input
                        id="password"
                        type={showPassword ? "text" : "password"}
                        placeholder="••••••••"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        onFocus={() => setFocusedField("password")}
                        onBlur={() => setFocusedField(null)}
                        className="h-12 bg-secondary/50 border-border/50 focus:border-primary pr-12 transition-all duration-300"
                      />
                      <button
                        type="button"
                        onClick={() => setShowPassword(!showPassword)}
                        className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
                      >
                        {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                      </button>
                    </div>
                  </motion.div>

                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.7 }}
                  >
                    <Button
                      type="submit"
                      disabled={isLoading}
                      className="w-full h-12 gradient-primary text-primary-foreground font-semibold text-base relative overflow-hidden group"
                    >
                      <motion.span
                        className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent"
                        animate={{ x: ["-100%", "100%"] }}
                        transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
                      />
                      <span className="relative z-10 flex items-center justify-center gap-2">
                        {isLoading ? (
                          <div className="w-5 h-5 border-2 border-primary-foreground border-t-transparent rounded-full animate-spin" />
                        ) : (
                          <>
                            Sign In
                            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                          </>
                        )}
                      </span>
                    </Button>
                  </motion.div>
                </form>

                <motion.p
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.9 }}
                  className="text-center text-muted-foreground mt-8"
                >
                  Don't have an account?{" "}
                  <Link to="/register" className="text-primary hover:underline font-medium">
                    Create one
                  </Link>
                </motion.p>
              </div>
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
