"use client";

import { useRef } from "react";
import { motion, useScroll, useTransform } from "framer-motion";
import { Reveal } from "../Reveal";

const PILLARS = [
  "Build technology companies",
  "Create games inspired by African stories",
  "Solve real-world problems",
  "Inspire future generations of creators",
];

export function Vision() {
  const ref = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start end", "end start"],
  });
  const y = useTransform(scrollYProgress, [0, 1], [60, -60]);

  return (
    <section
      id="vision"
      ref={ref}
      className="relative overflow-hidden px-6 py-28 sm:px-10 sm:py-44"
    >
      <motion.div
        style={{ y }}
        className="pointer-events-none absolute left-1/2 top-1/2 -z-[1] h-[30rem] w-[30rem] -translate-x-1/2 -translate-y-1/2 rounded-full opacity-30 blur-[120px]"
      >
        <div
          className="h-full w-full rounded-full"
          style={{
            background:
              "radial-gradient(circle, var(--accent-2), transparent 70%)",
          }}
        />
      </motion.div>

      <div className="mx-auto max-w-4xl text-center">
        <Reveal>
          <p className="mb-8 text-xs uppercase tracking-[0.3em] text-accent">
            04 — Vision
          </p>
        </Reveal>
        <Reveal delay={0.05}>
          <h2 className="font-display text-[clamp(2rem,5.5vw,4.2rem)] font-bold leading-[1.08]">
            The long game is to{" "}
            <span className="text-gradient animate-gradient">
              build, create, and inspire
            </span>{" "}
            on a global scale.
          </h2>
        </Reveal>
        <Reveal delay={0.12}>
          <p className="mx-auto mt-8 max-w-2xl text-lg leading-relaxed text-muted sm:text-xl">
            My mission is to build technology companies, create games rooted in
            African stories, solve problems that genuinely matter, and inspire
            the next generation of creators to believe their ideas are worth
            building.
          </p>
        </Reveal>

        <div className="mx-auto mt-14 grid max-w-3xl gap-3 sm:grid-cols-2">
          {PILLARS.map((p, i) => (
            <Reveal key={p} delay={0.1 + i * 0.08}>
              <div className="flex items-center gap-3 rounded-2xl border border-border bg-background-elev/40 px-5 py-4 text-left text-sm font-medium sm:text-base">
                <span className="font-display text-accent">0{i + 1}</span>
                {p}
              </div>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  );
}
