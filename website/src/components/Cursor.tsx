"use client";

import { useEffect, useState } from "react";
import { motion, useMotionValue, useSpring } from "framer-motion";

export function Cursor() {
  const [enabled, setEnabled] = useState(false);
  const [hovering, setHovering] = useState(false);
  const [hidden, setHidden] = useState(true);

  const x = useMotionValue(-100);
  const y = useMotionValue(-100);
  const springConfig = { damping: 26, stiffness: 380, mass: 0.4 };
  const dotX = useSpring(x, { damping: 40, stiffness: 900, mass: 0.2 });
  const dotY = useSpring(y, { damping: 40, stiffness: 900, mass: 0.2 });
  const ringX = useSpring(x, springConfig);
  const ringY = useSpring(y, springConfig);

  useEffect(() => {
    const fine =
      window.matchMedia("(pointer: fine)").matches &&
      !window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (!fine) return;

    // eslint-disable-next-line react-hooks/set-state-in-effect -- client-only capability detection
    setEnabled(true);
    document.documentElement.classList.add("cursor-hidden");

    const move = (e: MouseEvent) => {
      x.set(e.clientX);
      y.set(e.clientY);
      setHidden(false);
      const target = e.target as HTMLElement;
      const interactive = target.closest(
        'a, button, [role="button"], input, textarea, [data-cursor="hover"]',
      );
      setHovering(Boolean(interactive));
    };
    const leave = () => setHidden(true);

    window.addEventListener("mousemove", move);
    document.addEventListener("mouseleave", leave);
    return () => {
      window.removeEventListener("mousemove", move);
      document.removeEventListener("mouseleave", leave);
      document.documentElement.classList.remove("cursor-hidden");
    };
  }, [x, y]);

  if (!enabled) return null;

  return (
    <div aria-hidden="true" className="pointer-events-none">
      <motion.div
        className="fixed left-0 top-0 z-[90] h-2 w-2 -translate-x-1/2 -translate-y-1/2 rounded-full bg-accent"
        style={{ x: dotX, y: dotY, opacity: hidden ? 0 : 1 }}
      />
      <motion.div
        className="fixed left-0 top-0 z-[90] -translate-x-1/2 -translate-y-1/2 rounded-full border border-foreground/40 backdrop-invert"
        style={{
          x: ringX,
          y: ringY,
          opacity: hidden ? 0 : 1,
          mixBlendMode: "difference",
        }}
        animate={{
          width: hovering ? 56 : 34,
          height: hovering ? 56 : 34,
          borderColor: hovering
            ? "rgba(255,255,255,0.9)"
            : "rgba(255,255,255,0.4)",
        }}
        transition={{ type: "spring", damping: 22, stiffness: 300 }}
      />
    </div>
  );
}
