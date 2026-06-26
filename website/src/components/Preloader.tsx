"use client";

import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

export function Preloader() {
  const [done, setDone] = useState(false);
  const [count, setCount] = useState(0);

  useEffect(() => {
    // Respect reduced motion — skip the long intro.
    const reduce = window.matchMedia(
      "(prefers-reduced-motion: reduce)",
    ).matches;
    if (reduce) {
      // eslint-disable-next-line react-hooks/set-state-in-effect -- skip intro when reduced motion is preferred
      setDone(true);
      document.body.style.overflow = "";
      return;
    }

    document.body.style.overflow = "hidden";
    const duration = 1500;
    const start = performance.now();
    let raf = 0;

    const tick = (now: number) => {
      const progress = Math.min((now - start) / duration, 1);
      // easeOutExpo
      const eased = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
      setCount(Math.round(eased * 100));
      if (progress < 1) {
        raf = requestAnimationFrame(tick);
      } else {
        setTimeout(() => {
          setDone(true);
          document.body.style.overflow = "";
        }, 350);
      }
    };
    raf = requestAnimationFrame(tick);
    return () => {
      cancelAnimationFrame(raf);
      document.body.style.overflow = "";
    };
  }, []);

  return (
    <AnimatePresence>
      {!done && (
        <motion.div
          className="fixed inset-0 z-[100] flex flex-col items-center justify-center bg-background"
          exit={{
            clipPath: "inset(0 0 100% 0)",
            transition: { duration: 0.9, ease: [0.76, 0, 0.24, 1] },
          }}
          aria-hidden="true"
        >
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
            className="flex flex-col items-center gap-6"
          >
            <span className="font-display text-5xl sm:text-7xl text-gradient-accent">
              D
            </span>
            <div className="h-px w-40 overflow-hidden bg-border">
              <motion.div
                className="h-full w-full origin-left bg-foreground"
                style={{ scaleX: count / 100 }}
              />
            </div>
          </motion.div>
          <span className="absolute bottom-10 right-8 font-display text-6xl sm:text-8xl tabular-nums text-foreground/90">
            {count}
            <span className="text-accent">%</span>
          </span>
          <span className="absolute bottom-12 left-8 text-xs uppercase tracking-[0.3em] text-muted">
            Donell
          </span>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
