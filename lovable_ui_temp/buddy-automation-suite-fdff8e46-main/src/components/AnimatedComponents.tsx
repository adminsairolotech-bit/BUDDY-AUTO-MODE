import { motion } from "framer-motion";
import { ReactNode } from "react";

interface AnimatedCardProps {
  children: ReactNode;
  className?: string;
  delay?: number;
  hover3D?: boolean;
}

export const AnimatedCard = ({ children, className = "", delay = 0, hover3D = true }: AnimatedCardProps) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 30, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{
        duration: 0.6,
        delay,
        type: "spring",
        stiffness: 100,
        damping: 15,
      }}
      whileHover={hover3D ? {
        scale: 1.02,
        rotateX: -2,
        rotateY: 2,
        transition: { duration: 0.3 },
      } : undefined}
      className={`glass-card rounded-2xl ${className}`}
      style={{ perspective: "1000px", transformStyle: "preserve-3d" }}
    >
      {children}
    </motion.div>
  );
};

export const AnimatedPage = ({ children, className = "" }: { children: ReactNode; className?: string }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
      className={className}
    >
      {children}
    </motion.div>
  );
};

export const StaggerContainer = ({ children, className = "" }: { children: ReactNode; className?: string }) => {
  return (
    <motion.div
      initial="hidden"
      animate="show"
      variants={{
        hidden: { opacity: 0 },
        show: {
          opacity: 1,
          transition: { staggerChildren: 0.1, delayChildren: 0.1 },
        },
      }}
      className={className}
    >
      {children}
    </motion.div>
  );
};

export const StaggerItem = ({ children, className = "" }: { children: ReactNode; className?: string }) => {
  return (
    <motion.div
      variants={{
        hidden: { opacity: 0, y: 20, scale: 0.95 },
        show: {
          opacity: 1,
          y: 0,
          scale: 1,
          transition: { type: "spring", stiffness: 100, damping: 12 },
        },
      }}
      className={className}
    >
      {children}
    </motion.div>
  );
};

export const GlowingBadge = ({ children, color = "primary" }: { children: ReactNode; color?: string }) => {
  const colorClasses: Record<string, string> = {
    primary: "bg-primary/10 text-primary border-primary/20 shadow-[0_0_15px_hsl(160_84%_39%/0.15)]",
    accent: "bg-accent/10 text-accent border-accent/20 shadow-[0_0_15px_hsl(270_60%_55%/0.15)]",
    info: "bg-info/10 text-info border-info/20 shadow-[0_0_15px_hsl(217_91%_60%/0.15)]",
    warning: "bg-warning/10 text-warning border-warning/20 shadow-[0_0_15px_hsl(38_92%_50%/0.15)]",
    success: "bg-success/10 text-success border-success/20 shadow-[0_0_15px_hsl(160_84%_39%/0.15)]",
    muted: "bg-muted text-muted-foreground border-border",
  };
  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-mono border ${colorClasses[color] || colorClasses.muted}`}>
      {children}
    </span>
  );
};

export const CountUpNumber = ({ value, duration = 1.5 }: { value: number; duration?: number }) => {
  return (
    <motion.span
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.3 }}
    >
      <motion.span
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
      >
        {value}
      </motion.span>
    </motion.span>
  );
};
