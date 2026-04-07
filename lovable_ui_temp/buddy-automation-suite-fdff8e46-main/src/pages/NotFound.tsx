import { Link } from "react-router-dom";
import { useLocation } from "react-router-dom";
import { useEffect } from "react";
import { motion } from "framer-motion";
import { Home } from "lucide-react";
import { Button } from "@/components/ui/button";
import buddyRobot from "@/assets/buddy-robot.png";

const NotFound = () => {
  const location = useLocation();

  useEffect(() => {
    console.error("404 Error: User attempted to access non-existent route:", location.pathname);
  }, [location.pathname]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-background mesh-gradient p-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center max-w-sm"
      >
        <motion.img
          src={buddyRobot}
          alt="Buddy"
          initial={{ scale: 0.5 }}
          animate={{ scale: 1 }}
          className="w-32 h-32 mx-auto mb-6 object-contain opacity-60"
        />
        <h1 className="text-6xl font-bold text-gradient mb-3">404</h1>
        <p className="text-muted-foreground mb-6">Yeh page nahi mila — shayad ghalat link hai.</p>
        <Link to="/">
          <Button className="gradient-primary text-primary-foreground gap-2">
            <Home className="w-4 h-4" /> Home jaayein
          </Button>
        </Link>
      </motion.div>
    </div>
  );
};

export default NotFound;
