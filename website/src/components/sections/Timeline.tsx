"use client";

import { useRef } from "react";
import { motion, useScroll, useTransform } from "framer-motion";
import { TIMELINE } from "@/lib/data";
import { Reveal } from "../Reveal";

const STATUS_LABEL: Record<(typeof TIMELINE)[number]["status"], string> = {
  now: "Now",
  next: "Next",
  future: "Future",
};

export function Timeline() {
  const ref = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start center", "end center"],
  });
  const lineScale = useTransform(scrollYProgress, [0, 1], [0, 1]);

  return (
    <section id="journey" className="relative px-6 py-28 sm:px-10 sm:py-40">
      <div className="mx-auto max-w-4xl">
        <div className="mb-16 max-w-2xl">
          <Reveal>
            <p className="mb-6 text-xs uppercase tracking-[0.3em] text-accent">
              06 — The Journey
            </p>
          </Reveal>
          <Reveal delay={0.05}>
            <h2 className="font-display text-[clamp(1.8rem,4.5vw,3.4rem)] font-semibold leading-tight">
              From where I am
              <span className="text-muted"> to where I&apos;m going.</span>
            </h2>
          </Reveal>
        </div>

        <div ref={ref} className="relative pl-10 sm:pl-16">
          {/* track */}
          <div className="absolute left-[7px] top-2 h-[calc(100%-1rem)] w-px bg-border sm:left-[15px]" />
          {/* progress */}
          <motion.div
            style={{ scaleY: lineScale }}
            className="absolute left-[7px] top-2 h-[calc(100%-1rem)] w-px origin-top bg-gradient-to-b from-accent via-accent-2 to-accent-3 sm:left-[15px]"
          />

          <div className="space-y-12">
            {TIMELINE.map((t, i) => (
              <Reveal key={t.phase} delay={i * 0.05}>
                <div className="relative">
                  <span className="absolute -left-10 top-1 grid h-4 w-4 place-items-center sm:-left-16">
                    <span className="h-4 w-4 rounded-full border-2 border-accent bg-background" />
                    <span className="absolute h-1.5 w-1.5 rounded-full bg-accent" />
                  </span>
                  <div className="flex flex-wrap items-center gap-3">
                    <h3 className="font-display text-2xl font-semibold sm:text-3xl">
                      {t.phase}
                    </h3>
                    <span
                      className={`rounded-full px-2.5 py-0.5 text-[10px] uppercase tracking-[0.15em] ${
                        t.status === "now"
                          ? "bg-accent/15 text-accent"
                          : t.status === "next"
                            ? "bg-accent-2/15 text-accent-2"
                            : "bg-foreground/[0.06] text-faint"
                      }`}
                    >
                      {STATUS_LABEL[t.status]}
                    </span>
                  </div>
                  <p className="mt-1 text-sm font-medium text-foreground/80">
                    {t.title}
                  </p>
                  <p className="mt-2 max-w-lg text-sm leading-relaxed text-muted">
                    {t.description}
                  </p>
                </div>
              </Reveal>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
