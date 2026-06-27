"use client";

import { useEffect, useRef } from "react";
import { motion, useScroll, useTransform, useSpring } from "framer-motion";

export function Background() {
  const ref = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll();
  const y1 = useSpring(useTransform(scrollYProgress, [0, 1], [0, -180]), {
    stiffness: 60,
    damping: 30,
  });
  const y2 = useSpring(useTransform(scrollYProgress, [0, 1], [0, 220]), {
    stiffness: 60,
    damping: 30,
  });

  // Subtle pointer-reactive parallax for the hero orb.
  useEffect(() => {
    const reduce = window.matchMedia(
      "(prefers-reduced-motion: reduce)",
    ).matches;
    if (reduce || !ref.current) return;
    const el = ref.current;
    const onMove = (e: MouseEvent) => {
      const px = (e.clientX / window.innerWidth - 0.5) * 2;
      const py = (e.clientY / window.innerHeight - 0.5) * 2;
      el.style.setProperty("--mx", `${px * 24}px`);
      el.style.setProperty("--my", `${py * 24}px`);
    };
    window.addEventListener("mousemove", onMove);
    return () => window.removeEventListener("mousemove", onMove);
  }, []);

  return (
    <div
      ref={ref}
      aria-hidden="true"
      className="pointer-events-none fixed inset-0 -z-10 overflow-hidden"
    >
      {/* base wash */}
      <div className="absolute inset-0 bg-background" />

      {/* animated orbs */}
      <motion.div
        style={{ y: y1 }}
        className="absolute -top-40 left-[8%] h-[44rem] w-[44rem] rounded-full opacity-50 blur-[120px]"
      >
        <div
          className="h-full w-full rounded-full"
          style={{
            background:
              "radial-gradient(circle at 30% 30%, var(--accent), transparent 70%)",
            animation: "float-slow 18s ease-in-out infinite",
            transform: "translate(var(--mx,0), var(--my,0))",
          }}
        />
      </motion.div>

      <motion.div
        style={{ y: y2 }}
        className="absolute top-[30%] right-[2%] h-[40rem] w-[40rem] rounded-full opacity-40 blur-[130px]"
      >
        <div
          className="h-full w-full rounded-full"
          style={{
            background:
              "radial-gradient(circle at 60% 40%, var(--accent-2), transparent 70%)",
            animation: "float-slow 22s ease-in-out infinite reverse",
          }}
        />
      </motion.div>

      <div
        className="absolute bottom-[-10%] left-[35%] h-[36rem] w-[36rem] rounded-full opacity-25 blur-[140px]"
        style={{
          background:
            "radial-gradient(circle, var(--accent-3), transparent 70%)",
          animation: "float-slow 26s ease-in-out infinite",
        }}
      />

      {/* fine grid */}
      <div
        className="absolute inset-0 opacity-[0.04]"
        style={{
          backgroundImage:
            "linear-gradient(var(--foreground) 1px, transparent 1px), linear-gradient(90deg, var(--foreground) 1px, transparent 1px)",
          backgroundSize: "64px 64px",
          maskImage:
            "radial-gradient(ellipse at center, black 30%, transparent 75%)",
          WebkitMaskImage:
            "radial-gradient(ellipse at center, black 30%, transparent 75%)",
        }}
      />
    </div>
  );
}
