import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { Bot, Eye, EyeOff, ArrowRight, Shield } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useAuth } from "@/lib/auth-context";
import { useToast } from "@/hooks/use-toast";
import buddyRobot from "@/assets/buddy-robot.png";
import { MorphingBlob } from "@/components/3DComponents";

const Register = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();
  const { toast } = useToast();

  const passwordChecks = [
    { label: "12+ chars", met: password.length >= 12 },
    { label: "Uppercase", met: /[A-Z]/.test(password) },
    { label: "Special (!@#)", met: /[!@#$%^&*]/.test(password) },
  ];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name || !email || !password) return;
    if (passwordChecks.some((c) => !c.met)) return;
    setIsLoading(true);
    try {
      await register(name, email, password);
      toast({ title: "Account created!", description: "Welcome to Buddy Automation." });
      navigate("/dashboard");
    } catch {
      toast({ title: "Error", description: "Registration failed.", variant: "destructive" });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen relative overflow-hidden bg-background">
      <MorphingBlob className="w-96 h-96 top-[10%] right-[-10%]" color="accent" />
      <MorphingBlob className="w-80 h-80 bottom-[10%] left-[-5%]" color="primary" />

      <div className="fixed inset-0 z-[1] opacity-[0.03]" style={{
        backgroundImage: "linear-gradient(hsl(160 84% 39%) 1px, transparent 1px), linear-gradient(90deg, hsl(160 84% 39%) 1px, transparent 1px)",
        backgroundSize: "60px 60px",
      }} />

      <div className="relative z-10 min-h-screen flex flex-col lg:flex-row">
        {/* Left - Robot (desktop) */}
        <div className="hidden lg:flex lg:w-1/2 items-center justify-center">
          <motion.img
            src={buddyRobot}
            alt="AI Buddy Robot"
            initial={{ opacity: 0, scale: 0.5, y: 40 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            transition={{ duration: 1, type: "spring", stiffness: 60 }}
            className="w-80 h-80 object-contain drop-shadow-[0_0_40px_hsl(160_84%_39%/0.4)] animate-float"
          />
        </div>

        {/* Mobile Robot */}
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

        {/* Right - Register Form */}
        <div className="flex-1 flex items-center justify-center p-6 lg:p-12">
          <div className="w-full max-w-md">
          <motion.div
            initial={{ opacity: 0, scale: 0.9, rotateX: 10 }}
            animate={{ opacity: 1, scale: 1, rotateX: 0 }}
            transition={{ duration: 0.8, type: "spring", stiffness: 80 }}
            className="glass-strong rounded-2xl p-8 lg:p-10 relative overflow-hidden"
          >
            <div className="absolute inset-0 rounded-2xl animated-border" />
            <div className="absolute inset-0 shimmer rounded-2xl" />

            <div className="relative z-10">
              <Link to="/login" className="flex items-center gap-3 mb-8">
                <motion.div
                  animate={{ rotateY: [0, 360] }}
                  transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
                  className="w-11 h-11 rounded-xl gradient-primary flex items-center justify-center glow-primary"
                >
                  <Bot className="w-6 h-6 text-primary-foreground" />
                </motion.div>
                <span className="text-xl font-bold text-gradient">Buddy Automation</span>
              </Link>

              <motion.h2
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.2 }}
                className="text-3xl font-bold mb-2"
              >
                Create account
              </motion.h2>
              <motion.p
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.3 }}
                className="text-muted-foreground mb-8"
              >
                Start automating your daily tasks
              </motion.p>

              <form onSubmit={handleSubmit} className="space-y-5">
                {[
                  { id: "name", label: "Full Name", type: "text", placeholder: "John Doe", value: name, onChange: setName, delay: 0.4 },
                  { id: "email", label: "Email", type: "email", placeholder: "you@example.com", value: email, onChange: setEmail, delay: 0.5 },
                ].map((field) => (
                  <motion.div
                    key={field.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: field.delay }}
                    className="space-y-2"
                  >
                    <Label htmlFor={field.id}>{field.label}</Label>
                    <Input
                      id={field.id}
                      type={field.type}
                      placeholder={field.placeholder}
                      value={field.value}
                      onChange={(e) => field.onChange(e.target.value)}
                      className="h-12 bg-secondary/50 border-border/50 focus:border-primary"
                    />
                  </motion.div>
                ))}

                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.6 }}
                  className="space-y-2"
                >
                  <Label htmlFor="password">Password</Label>
                  <div className="relative">
                    <Input
                      id="password"
                      type={showPassword ? "text" : "password"}
                      placeholder="••••••••"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      className="h-12 bg-secondary/50 border-border/50 focus:border-primary pr-12"
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                    >
                      {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                    </button>
                  </div>
                  {password && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: "auto" }}
                      className="flex gap-3 mt-2"
                    >
                      {passwordChecks.map((check) => (
                        <motion.div
                          key={check.label}
                          initial={{ scale: 0.8 }}
                          animate={{ scale: 1 }}
                          className="flex items-center gap-1.5 text-xs"
                        >
                          <Shield className={`w-3 h-3 transition-colors ${check.met ? "text-success" : "text-muted-foreground"}`} />
                          <span className={check.met ? "text-success" : "text-muted-foreground"}>{check.label}</span>
                        </motion.div>
                      ))}
                    </motion.div>
                  )}
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
                        <>Create Account <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" /></>
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
                Already have an account?{" "}
                <Link to="/login" className="text-primary hover:underline font-medium">Sign in</Link>
              </motion.p>
            </div>
          </motion.div>
        </div>
        </div>
      </div>
    </div>
  );
};

export default Register;
