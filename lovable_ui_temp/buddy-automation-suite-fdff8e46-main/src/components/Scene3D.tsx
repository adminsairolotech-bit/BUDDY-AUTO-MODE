import { useRef, useMemo } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { Float, MeshDistortMaterial, MeshWobbleMaterial, Sphere } from "@react-three/drei";
import * as THREE from "three";

const FloatingOrb = ({ position, color, speed = 1, distort = 0.3, size = 1 }: {
  position: [number, number, number];
  color: string;
  speed?: number;
  distort?: number;
  size?: number;
}) => {
  const meshRef = useRef<THREE.Mesh>(null);

  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.position.y = position[1] + Math.sin(state.clock.elapsedTime * speed * 0.5) * 0.5;
      meshRef.current.rotation.x = state.clock.elapsedTime * 0.1 * speed;
      meshRef.current.rotation.z = state.clock.elapsedTime * 0.05 * speed;
    }
  });

  return (
    <Float speed={speed * 2} rotationIntensity={0.5} floatIntensity={1}>
      <mesh ref={meshRef} position={position}>
        <sphereGeometry args={[size, 64, 64]} />
        <MeshDistortMaterial
          color={color}
          transparent
          opacity={0.6}
          distort={distort}
          speed={speed * 2}
          roughness={0.2}
          metalness={0.8}
        />
      </mesh>
    </Float>
  );
};

const Particles = ({ count = 200 }: { count?: number }) => {
  const points = useRef<THREE.Points>(null);

  const particlesPosition = useMemo(() => {
    const positions = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      positions[i * 3] = (Math.random() - 0.5) * 20;
      positions[i * 3 + 1] = (Math.random() - 0.5) * 20;
      positions[i * 3 + 2] = (Math.random() - 0.5) * 20;
    }
    return positions;
  }, [count]);

  useFrame((state) => {
    if (points.current) {
      points.current.rotation.y = state.clock.elapsedTime * 0.02;
      points.current.rotation.x = state.clock.elapsedTime * 0.01;
    }
  });

  return (
    <points ref={points}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          args={[particlesPosition, 3]}
        />
      </bufferGeometry>
      <pointsMaterial
        size={0.03}
        color="#10b981"
        transparent
        opacity={0.6}
        sizeAttenuation
      />
    </points>
  );
};

const WobbleSphere = ({ position, color, size = 0.5 }: {
  position: [number, number, number];
  color: string;
  size?: number;
}) => {
  return (
    <Float speed={1.5} rotationIntensity={1} floatIntensity={2}>
      <mesh position={position}>
        <sphereGeometry args={[size, 32, 32]} />
        <MeshWobbleMaterial
          color={color}
          transparent
          opacity={0.3}
          factor={0.6}
          speed={2}
          wireframe
        />
      </mesh>
    </Float>
  );
};

export const Scene3DLogin = () => {
  return (
    <Canvas
      camera={{ position: [0, 0, 6], fov: 60 }}
      style={{ position: "absolute", inset: 0 }}
      gl={{ antialias: true, alpha: true }}
    >
      <ambientLight intensity={0.3} />
      <directionalLight position={[5, 5, 5]} intensity={0.5} color="#10b981" />
      <pointLight position={[-5, -5, 5]} intensity={0.3} color="#8b5cf6" />
      <pointLight position={[5, -5, -5]} intensity={0.2} color="#3b82f6" />

      <FloatingOrb position={[-3, 1, -2]} color="#10b981" speed={0.8} distort={0.4} size={1.2} />
      <FloatingOrb position={[3, -1, -3]} color="#8b5cf6" speed={0.6} distort={0.3} size={0.9} />
      <FloatingOrb position={[0, 2, -4]} color="#3b82f6" speed={1} distort={0.5} size={0.7} />
      <FloatingOrb position={[-2, -2, -1]} color="#10b981" speed={0.4} distort={0.2} size={0.5} />
      <FloatingOrb position={[2, 1.5, -2]} color="#f59e0b" speed={0.7} distort={0.3} size={0.4} />

      <WobbleSphere position={[4, 2, -5]} color="#10b981" size={1.5} />
      <WobbleSphere position={[-4, -2, -4]} color="#8b5cf6" size={1} />

      <Particles count={300} />
    </Canvas>
  );
};

export const Scene3DDashboard = () => {
  return (
    <Canvas
      camera={{ position: [0, 0, 5], fov: 50 }}
      style={{ position: "absolute", inset: 0, pointerEvents: "none" }}
      gl={{ antialias: true, alpha: true }}
    >
      <ambientLight intensity={0.2} />
      <pointLight position={[5, 5, 5]} intensity={0.4} color="#10b981" />
      <pointLight position={[-5, -5, 5]} intensity={0.2} color="#8b5cf6" />

      <FloatingOrb position={[5, 3, -6]} color="#10b981" speed={0.3} distort={0.2} size={0.8} />
      <FloatingOrb position={[-5, -2, -5]} color="#8b5cf6" speed={0.5} distort={0.3} size={0.6} />
      <FloatingOrb position={[3, -3, -7]} color="#3b82f6" speed={0.4} distort={0.2} size={0.5} />

      <Particles count={100} />
    </Canvas>
  );
};
