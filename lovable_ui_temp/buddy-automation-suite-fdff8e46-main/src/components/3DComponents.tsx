import { useState, useRef, ReactNode, MouseEvent } from "react";
import { motion, useMotionValue, useSpring, useTransform } from "framer-motion";

interface Tilt3DCardProps {
  children: ReactNode;
  className?: string;
  intensity?: number;
  glare?: boolean;
  perspective?: number;
}

export const Tilt3DCard = ({
  children,
  className = "",
  intensity = 15,
  glare = true,
  perspective = 800,
}: Tilt3DCardProps) => {
  const ref = useRef<HTMLDivElement>(null);
  const [isHovered, setIsHovered] = useState(false);

  const x = useMotionValue(0);
  const y = useMotionValue(0);
  const glareX = useMotionValue(50);
  const glareY = useMotionValue(50);

  const rotateX = useSpring(useTransform(y, [-0.5, 0.5], [intensity, -intensity]), { stiffness: 200, damping: 20 });
  const rotateY = useSpring(useTransform(x, [-0.5, 0.5], [-intensity, intensity]), { stiffness: 200, damping: 20 });

  const handleMouseMove = (e: MouseEvent) => {
    if (!ref.current) return;
    const rect = ref.current.getBoundingClientRect();
    const px = (e.clientX - rect.left) / rect.width - 0.5;
    const py = (e.clientY - rect.top) / rect.height - 0.5;
    x.set(px);
    y.set(py);
    glareX.set((px + 0.5) * 100);
    glareY.set((py + 0.5) * 100);
  };

  const handleMouseLeave = () => {
    setIsHovered(false);
    x.set(0);
    y.set(0);
  };

  return (
    <motion.div
      ref={ref}
      onMouseMove={handleMouseMove}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={handleMouseLeave}
      style={{
        perspective,
        transformStyle: "preserve-3d",
      }}
      className={className}
    >
      <motion.div
        style={{
          rotateX,
          rotateY,
          transformStyle: "preserve-3d",
        }}
        className="relative w-full h-full"
      >
        {children}
        {glare && isHovered && (
          <motion.div
            className="absolute inset-0 rounded-2xl pointer-events-none z-10"
            style={{
              background: `radial-gradient(circle at ${glareX.get()}% ${glareY.get()}%, hsl(160 84% 39% / 0.12) 0%, transparent 60%)`,
            }}
          />
        )}
      </motion.div>
    </motion.div>
  );
};

interface FlipCardProps {
  front: ReactNode;
  back: ReactNode;
  className?: string;
}

export const FlipCard = ({ front, back, className = "" }: FlipCardProps) => {
  const [isFlipped, setIsFlipped] = useState(false);

  return (
    <div
      className={`cursor-pointer ${className}`}
      style={{ perspective: "1000px" }}
      onClick={() => setIsFlipped(!isFlipped)}
    >
      <motion.div
        animate={{ rotateY: isFlipped ? 180 : 0 }}
        transition={{ duration: 0.6, type: "spring", stiffness: 100, damping: 15 }}
        style={{ transformStyle: "preserve-3d" }}
        className="relative w-full h-full"
      >
        <div className="absolute inset-0" style={{ backfaceVisibility: "hidden" }}>
          {front}
        </div>
        <div
          className="absolute inset-0"
          style={{ backfaceVisibility: "hidden", transform: "rotateY(180deg)" }}
        >
          {back}
        </div>
      </motion.div>
    </div>
  );
};

interface Parallax3DLayerProps {
  children: ReactNode;
  depth?: number;
  className?: string;
}

export const Parallax3DLayer = ({ children, depth = 0, className = "" }: Parallax3DLayerProps) => {
  return (
    <motion.div
      initial={{ opacity: 0, z: -100 }}
      animate={{ opacity: 1, z: 0 }}
      transition={{ duration: 0.8, delay: depth * 0.15 }}
      style={{
        transform: `translateZ(${depth * 20}px)`,
        transformStyle: "preserve-3d",
      }}
      className={className}
    >
      {children}
    </motion.div>
  );
};

export const FloatingElement = ({ children, className = "", delay = 0, yRange = 15 }: {
  children: ReactNode;
  className?: string;
  delay?: number;
  yRange?: number;
}) => {
  return (
    <motion.div
      animate={{
        y: [-yRange, yRange, -yRange],
        rotateZ: [-1, 1, -1],
      }}
      transition={{
        duration: 6,
        repeat: Infinity,
        ease: "easeInOut",
        delay,
      }}
      className={className}
    >
      {children}
    </motion.div>
  );
};

export const MorphingBlob = ({ className = "", color = "primary" }: { className?: string; color?: string }) => {
  const colors: Record<string, string> = {
    primary: "hsl(160 84% 39% / 0.15)",
    accent: "hsl(270 60% 55% / 0.12)",
    info: "hsl(217 91% 60% / 0.1)",
  };

  return (
    <motion.div
      className={`absolute rounded-full blur-3xl ${className}`}
      style={{ background: colors[color] || colors.primary }}
      animate={{
        scale: [1, 1.2, 0.9, 1.1, 1],
        x: [0, 30, -20, 10, 0],
        y: [0, -20, 10, -30, 0],
        borderRadius: ["40% 60% 70% 30%", "60% 40% 30% 70%", "50% 50% 60% 40%", "40% 60% 70% 30%"],
      }}
      transition={{
        duration: 12,
        repeat: Infinity,
        ease: "easeInOut",
      }}
    />
  );
};
