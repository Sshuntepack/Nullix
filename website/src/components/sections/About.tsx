"use client";

import { motion } from "framer-motion";
import { Reveal } from "../Reveal";

export function About() {
  return (
    <section id="about" className="relative px-6 py-28 sm:px-10 sm:py-40">
      <div className="mx-auto max-w-5xl">
        <Reveal>
          <p className="mb-6 text-xs uppercase tracking-[0.3em] text-accent">
            01 — About
          </p>
        </Reveal>

        <div className="space-y-8">
          <Reveal delay={0.05}>
            <h2 className="font-display text-[clamp(1.8rem,4.5vw,3.4rem)] font-semibold leading-tight">
              This isn&apos;t a list of achievements.
              <br />
              <span className="text-muted">It&apos;s a statement of intent.</span>
            </h2>
          </Reveal>

          <div className="grid gap-8 pt-4 text-lg leading-relaxed text-muted md:grid-cols-2 md:text-xl">
            <Reveal delay={0.1}>
              <p>
                I&apos;m at the beginning of my journey — a student learning the
                craft, a builder shipping early experiments, and someone
                obsessed with the gap between where I am and where I&apos;m
                going.
              </p>
            </Reveal>
            <Reveal delay={0.18}>
              <p>
                What drives me isn&apos;t a résumé. It&apos;s ambition: a
                commitment to become a world-class engineer, entrepreneur, and
                creator — and to build technology that genuinely matters along
                the way.
              </p>
            </Reveal>
          </div>

          <Reveal delay={0.2}>
            <motion.blockquote className="mt-8 border-l-2 border-accent pl-6 font-display text-2xl font-medium leading-snug sm:text-3xl">
              &ldquo;I&apos;d rather be early and relentless than late and
              comfortable.&rdquo;
            </motion.blockquote>
          </Reveal>
        </div>
      </div>
    </section>
  );
}
