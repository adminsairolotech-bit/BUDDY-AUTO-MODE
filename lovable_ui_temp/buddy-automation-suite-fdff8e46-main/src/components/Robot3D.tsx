import { useRef } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { Float, Environment, MeshTransmissionMaterial } from "@react-three/drei";
import * as THREE from "three";

const RobotHead = () => {
  const headRef = useRef<THREE.Group>(null);

  useFrame((state) => {
    if (headRef.current) {
      headRef.current.rotation.y = Math.sin(state.clock.elapsedTime * 0.5) * 0.3;
      headRef.current.rotation.x = Math.sin(state.clock.elapsedTime * 0.3) * 0.1;
    }
  });

  return (
    <group ref={headRef} position={[0, 1.6, 0]}>
      {/* Main head - rounded box */}
      <mesh>
        <boxGeometry args={[1.2, 1, 1]} />
        <meshStandardMaterial
          color="#1a1a2e"
          metalness={0.9}
          roughness={0.15}
        />
      </mesh>
      {/* Head top plate */}
      <mesh position={[0, 0.52, 0]}>
        <boxGeometry args={[1.0, 0.08, 0.8]} />
        <meshStandardMaterial color="#10b981" metalness={0.8} roughness={0.2} emissive="#10b981" emissiveIntensity={0.3} />
      </mesh>

      {/* Visor / Face plate */}
      <mesh position={[0, 0.05, 0.45]}>
        <boxGeometry args={[1.0, 0.55, 0.15]} />
        <meshStandardMaterial color="#0f172a" metalness={0.5} roughness={0.1} />
      </mesh>

      {/* Left Eye */}
      <mesh position={[-0.25, 0.1, 0.54]}>
        <sphereGeometry args={[0.12, 32, 32]} />
        <meshStandardMaterial
          color="#10b981"
          emissive="#10b981"
          emissiveIntensity={2}
          metalness={0.3}
          roughness={0.1}
        />
      </mesh>
      {/* Left Eye glow ring */}
      <mesh position={[-0.25, 0.1, 0.53]}>
        <torusGeometry args={[0.16, 0.02, 16, 32]} />
        <meshStandardMaterial color="#10b981" emissive="#10b981" emissiveIntensity={1} />
      </mesh>

      {/* Right Eye */}
      <mesh position={[0.25, 0.1, 0.54]}>
        <sphereGeometry args={[0.12, 32, 32]} />
        <meshStandardMaterial
          color="#10b981"
          emissive="#10b981"
          emissiveIntensity={2}
          metalness={0.3}
          roughness={0.1}
        />
      </mesh>
      {/* Right Eye glow ring */}
      <mesh position={[0.25, 0.1, 0.53]}>
        <torusGeometry args={[0.16, 0.02, 16, 32]} />
        <meshStandardMaterial color="#10b981" emissive="#10b981" emissiveIntensity={1} />
      </mesh>

      {/* Mouth / Speaker grille */}
      {[-0.2, -0.1, 0, 0.1, 0.2].map((x, i) => (
        <mesh key={i} position={[x, -0.2, 0.54]}>
          <boxGeometry args={[0.06, 0.04, 0.02]} />
          <meshStandardMaterial color="#10b981" emissive="#10b981" emissiveIntensity={0.5} />
        </mesh>
      ))}

      {/* Antenna */}
      <mesh position={[0, 0.7, 0]}>
        <cylinderGeometry args={[0.03, 0.03, 0.4, 8]} />
        <meshStandardMaterial color="#334155" metalness={0.9} roughness={0.2} />
      </mesh>
      {/* Antenna top */}
      <AntennaOrb />

      {/* Side panels */}
      <mesh position={[-0.65, 0, 0]}>
        <boxGeometry args={[0.1, 0.6, 0.6]} />
        <meshStandardMaterial color="#1e293b" metalness={0.9} roughness={0.15} />
      </mesh>
      <mesh position={[0.65, 0, 0]}>
        <boxGeometry args={[0.1, 0.6, 0.6]} />
        <meshStandardMaterial color="#1e293b" metalness={0.9} roughness={0.15} />
      </mesh>
    </group>
  );
};

const AntennaOrb = () => {
  const orbRef = useRef<THREE.Mesh>(null);

  useFrame((state) => {
    if (orbRef.current) {
      orbRef.current.position.y = 0.95 + Math.sin(state.clock.elapsedTime * 2) * 0.05;
      const intensity = 1 + Math.sin(state.clock.elapsedTime * 3) * 0.5;
      (orbRef.current.material as THREE.MeshStandardMaterial).emissiveIntensity = intensity;
    }
  });

  return (
    <mesh ref={orbRef} position={[0, 0.95, 0]}>
      <sphereGeometry args={[0.08, 16, 16]} />
      <meshStandardMaterial
        color="#10b981"
        emissive="#10b981"
        emissiveIntensity={1.5}
        metalness={0.3}
        roughness={0.1}
      />
    </mesh>
  );
};

const RobotBody = () => {
  return (
    <group position={[0, 0.3, 0]}>
      {/* Neck */}
      <mesh position={[0, 0.95, 0]}>
        <cylinderGeometry args={[0.15, 0.2, 0.3, 8]} />
        <meshStandardMaterial color="#334155" metalness={0.9} roughness={0.2} />
      </mesh>

      {/* Chest */}
      <mesh position={[0, 0.3, 0]}>
        <boxGeometry args={[1.4, 1.0, 0.8]} />
        <meshStandardMaterial color="#1a1a2e" metalness={0.85} roughness={0.15} />
      </mesh>

      {/* Chest plate / Arc reactor */}
      <mesh position={[0, 0.4, 0.42]}>
        <cylinderGeometry args={[0.2, 0.2, 0.05, 32]} />
        <meshStandardMaterial
          color="#10b981"
          emissive="#10b981"
          emissiveIntensity={1.5}
          metalness={0.5}
          roughness={0.1}
        />
      </mesh>
      <mesh position={[0, 0.4, 0.41]}>
        <torusGeometry args={[0.25, 0.03, 16, 32]} />
        <meshStandardMaterial color="#10b981" emissive="#10b981" emissiveIntensity={0.8} />
      </mesh>
      <mesh position={[0, 0.4, 0.40]}>
        <torusGeometry args={[0.32, 0.02, 16, 32]} />
        <meshStandardMaterial color="#0ea5e9" emissive="#0ea5e9" emissiveIntensity={0.4} />
      </mesh>

      {/* Chest detail lines */}
      {[-0.15, 0, 0.15].map((y, i) => (
        <mesh key={i} position={[0, 0.1 + y, 0.42]}>
          <boxGeometry args={[0.8, 0.02, 0.02]} />
          <meshStandardMaterial color="#10b981" emissive="#10b981" emissiveIntensity={0.3} />
        </mesh>
      ))}

      {/* Shoulder joints */}
      <mesh position={[-0.8, 0.65, 0]}>
        <sphereGeometry args={[0.18, 16, 16]} />
        <meshStandardMaterial color="#334155" metalness={0.9} roughness={0.15} />
      </mesh>
      <mesh position={[0.8, 0.65, 0]}>
        <sphereGeometry args={[0.18, 16, 16]} />
        <meshStandardMaterial color="#334155" metalness={0.9} roughness={0.15} />
      </mesh>

      {/* Waist */}
      <mesh position={[0, -0.3, 0]}>
        <boxGeometry args={[1.0, 0.3, 0.6]} />
        <meshStandardMaterial color="#1e293b" metalness={0.9} roughness={0.15} />
      </mesh>
    </group>
  );
};

const RobotArm = ({ side }: { side: "left" | "right" }) => {
  const armRef = useRef<THREE.Group>(null);
  const x = side === "left" ? -1 : 1;

  useFrame((state) => {
    if (armRef.current) {
      armRef.current.rotation.x = Math.sin(state.clock.elapsedTime * 0.8 + (side === "left" ? 0 : Math.PI)) * 0.15;
      armRef.current.rotation.z = side === "left" ? 0.1 : -0.1;
    }
  });

  return (
    <group ref={armRef} position={[x * 0.95, 0.8, 0]}>
      {/* Upper arm */}
      <mesh position={[0, -0.25, 0]}>
        <boxGeometry args={[0.25, 0.5, 0.25]} />
        <meshStandardMaterial color="#1e293b" metalness={0.9} roughness={0.15} />
      </mesh>
      {/* Elbow joint */}
      <mesh position={[0, -0.55, 0]}>
        <sphereGeometry args={[0.14, 16, 16]} />
        <meshStandardMaterial color="#334155" metalness={0.9} roughness={0.15} />
      </mesh>
      {/* Forearm */}
      <mesh position={[0, -0.85, 0]}>
        <boxGeometry args={[0.2, 0.45, 0.2]} />
        <meshStandardMaterial color="#1a1a2e" metalness={0.9} roughness={0.15} />
      </mesh>
      {/* Hand */}
      <mesh position={[0, -1.15, 0]}>
        <boxGeometry args={[0.22, 0.15, 0.15]} />
        <meshStandardMaterial color="#334155" metalness={0.9} roughness={0.2} />
      </mesh>
      {/* Arm accent light */}
      <mesh position={[0, -0.4, 0.14]}>
        <boxGeometry args={[0.04, 0.3, 0.02]} />
        <meshStandardMaterial color="#8b5cf6" emissive="#8b5cf6" emissiveIntensity={0.8} />
      </mesh>
    </group>
  );
};

const HolographicRing = () => {
  const ringRef = useRef<THREE.Mesh>(null);

  useFrame((state) => {
    if (ringRef.current) {
      ringRef.current.rotation.y = state.clock.elapsedTime * 0.5;
      ringRef.current.rotation.x = Math.sin(state.clock.elapsedTime * 0.3) * 0.2;
    }
  });

  return (
    <mesh ref={ringRef} position={[0, 0.6, 0]}>
      <torusGeometry args={[2, 0.02, 16, 64]} />
      <meshStandardMaterial
        color="#10b981"
        emissive="#10b981"
        emissiveIntensity={0.5}
        transparent
        opacity={0.4}
      />
    </mesh>
  );
};

const HolographicRing2 = () => {
  const ringRef = useRef<THREE.Mesh>(null);

  useFrame((state) => {
    if (ringRef.current) {
      ringRef.current.rotation.y = -state.clock.elapsedTime * 0.3;
      ringRef.current.rotation.z = Math.sin(state.clock.elapsedTime * 0.2) * 0.3 + 0.5;
    }
  });

  return (
    <mesh ref={ringRef} position={[0, 0.6, 0]}>
      <torusGeometry args={[2.3, 0.015, 16, 64]} />
      <meshStandardMaterial
        color="#8b5cf6"
        emissive="#8b5cf6"
        emissiveIntensity={0.4}
        transparent
        opacity={0.3}
      />
    </mesh>
  );
};

const FloatingParticles = () => {
  const particlesRef = useRef<THREE.Points>(null);

  const positions = new Float32Array(150 * 3);
  for (let i = 0; i < 150; i++) {
    positions[i * 3] = (Math.random() - 0.5) * 8;
    positions[i * 3 + 1] = (Math.random() - 0.5) * 8;
    positions[i * 3 + 2] = (Math.random() - 0.5) * 8;
  }

  useFrame((state) => {
    if (particlesRef.current) {
      particlesRef.current.rotation.y = state.clock.elapsedTime * 0.03;
    }
  });

  return (
    <points ref={particlesRef}>
      <bufferGeometry>
        <bufferAttribute attach="attributes-position" args={[positions, 3]} />
      </bufferGeometry>
      <pointsMaterial size={0.04} color="#10b981" transparent opacity={0.6} sizeAttenuation />
    </points>
  );
};

const FullRobot = () => {
  const robotRef = useRef<THREE.Group>(null);

  useFrame((state) => {
    if (robotRef.current) {
      robotRef.current.position.y = Math.sin(state.clock.elapsedTime * 0.6) * 0.15;
      robotRef.current.rotation.y = Math.sin(state.clock.elapsedTime * 0.3) * 0.15;
    }
  });

  return (
    <Float speed={1} rotationIntensity={0.2} floatIntensity={0.3}>
      <group ref={robotRef} scale={0.85}>
        <RobotHead />
        <RobotBody />
        <RobotArm side="left" />
        <RobotArm side="right" />
        <HolographicRing />
        <HolographicRing2 />
      </group>
    </Float>
  );
};

export const RealisticRobotScene = () => {
  return (
    <Canvas
      camera={{ position: [0, 1.5, 5.5], fov: 45 }}
      style={{ position: "absolute", inset: 0 }}
      gl={{ antialias: true, alpha: true }}
    >
      {/* Lighting */}
      <ambientLight intensity={0.2} />
      <directionalLight position={[5, 8, 5]} intensity={0.6} color="#ffffff" />
      <pointLight position={[-3, 3, 3]} intensity={0.8} color="#10b981" distance={10} />
      <pointLight position={[3, 2, -2]} intensity={0.4} color="#8b5cf6" distance={8} />
      <pointLight position={[0, -2, 3]} intensity={0.3} color="#0ea5e9" distance={6} />
      <spotLight position={[0, 6, 0]} angle={0.4} penumbra={0.5} intensity={0.5} color="#10b981" />

      <FullRobot />
      <FloatingParticles />
    </Canvas>
  );
};
