"use client";

import { motion } from "framer-motion";
import { ArrowDown, ArrowUpRight } from "lucide-react";

const EASE = [0.22, 1, 0.36, 1] as const;

const container = {
  hidden: {},
  show: { transition: { staggerChildren: 0.09, delayChildren: 0.1 } },
};
const item = {
  hidden: { opacity: 0, y: 30 },
  show: { opacity: 1, y: 0, transition: { duration: 0.9, ease: EASE } },
};

export function Hero() {
  return (
    <section
      id="top"
      className="relative flex min-h-[100svh] items-center px-6 pt-32 pb-20 sm:px-10"
    >
      <div className="mx-auto grid w-full max-w-6xl gap-12 lg:grid-cols-[1.4fr_1fr] lg:items-center">
        <motion.div variants={container} initial="hidden" animate="show">
          <motion.div
            variants={item}
            className="mb-7 inline-flex items-center gap-2 rounded-full border border-border px-4 py-1.5 text-xs uppercase tracking-[0.2em] text-muted"
          >
            <span className="relative flex h-2 w-2">
              <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-accent opacity-75" />
              <span className="relative inline-flex h-2 w-2 rounded-full bg-accent" />
            </span>
            Student • Engineer • Game Dev • Founder
          </motion.div>

          <h1 className="font-display text-[clamp(2.6rem,7vw,5.5rem)] font-bold leading-[1.02]">
            <motion.span variants={item} className="block">
              Building the future
            </motion.span>
            <motion.span variants={item} className="block text-gradient animate-gradient">
              through software, AI &
            </motion.span>
            <motion.span variants={item} className="block">
              interactive experiences.
            </motion.span>
          </h1>

          <motion.p
            variants={item}
            className="mt-8 max-w-xl text-lg leading-relaxed text-muted sm:text-xl"
          >
            I&apos;m Donell — at the very beginning of a long journey, committed
            to becoming a world-class engineer, entrepreneur, and creator. This
            is where that story starts.
          </motion.p>

          <motion.div variants={item} className="mt-10 flex flex-wrap gap-4">
            <a
              href="#about"
              className="group inline-flex items-center gap-2 rounded-full bg-foreground px-7 py-3.5 text-sm font-medium text-background transition-transform hover:scale-[1.04]"
            >
              Explore
              <ArrowDown className="h-4 w-4 transition-transform group-hover:translate-y-0.5" />
            </a>
            <a
              href="#contact"
              className="group inline-flex items-center gap-2 rounded-full border border-border-strong px-7 py-3.5 text-sm font-medium transition-colors hover:bg-foreground/5"
            >
              Contact
              <ArrowUpRight className="h-4 w-4 transition-transform group-hover:translate-x-0.5 group-hover:-translate-y-0.5" />
            </a>
          </motion.div>
        </motion.div>

        {/* Portrait placeholder */}
        <motion.div
          initial={{ opacity: 0, scale: 0.92 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 1.1, delay: 0.3, ease: EASE }}
          className="relative mx-auto aspect-[3/4] w-full max-w-sm"
        >
          <div className="absolute -inset-4 rounded-[2rem] bg-gradient-to-br from-accent/30 via-accent-2/20 to-transparent blur-2xl" />
          <div className="glass relative h-full w-full overflow-hidden rounded-[2rem]">
            <div
              className="absolute inset-0 opacity-60"
              style={{
                background:
                  "conic-gradient(from 180deg at 50% 50%, var(--accent) 0deg, transparent 120deg, var(--accent-2) 240deg, transparent 360deg)",
                animation: "spin-slow 24s linear infinite",
              }}
            />
            <div className="absolute inset-[3px] rounded-[1.9rem] bg-background-elev/80 backdrop-blur-2xl" />
            <div className="relative flex h-full flex-col items-center justify-center gap-4 p-8 text-center">
              <span className="font-display text-7xl text-gradient-accent">
                D
              </span>
              <p className="text-sm uppercase tracking-[0.3em] text-faint">
                Portrait
              </p>
              <p className="max-w-[14rem] text-xs text-muted">
                A placeholder for now — the face behind the vision arrives soon.
              </p>
            </div>
          </div>
        </motion.div>
      </div>

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.4, duration: 1 }}
        className="absolute bottom-8 left-1/2 hidden -translate-x-1/2 flex-col items-center gap-2 text-faint sm:flex"
      >
        <span className="text-[10px] uppercase tracking-[0.3em]">Scroll</span>
        <motion.span
          animate={{ y: [0, 8, 0] }}
          transition={{ duration: 1.8, repeat: Infinity, ease: "easeInOut" }}
          className="h-8 w-px bg-gradient-to-b from-foreground/50 to-transparent"
        />
      </motion.div>
    </section>
  );
}
