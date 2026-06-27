"use client";

import { motion } from "framer-motion";
import { PHILOSOPHY } from "@/lib/data";
import { Reveal, staggerContainer, staggerItem } from "../Reveal";

export function Philosophy() {
  return (
    <section id="philosophy" className="relative px-6 py-28 sm:px-10 sm:py-40">
      <div className="mx-auto max-w-6xl">
        <div className="mb-16 max-w-2xl">
          <Reveal>
            <p className="mb-6 text-xs uppercase tracking-[0.3em] text-accent">
              02 — Philosophy
            </p>
          </Reveal>
          <Reveal delay={0.05}>
            <h2 className="font-display text-[clamp(1.8rem,4.5vw,3.4rem)] font-semibold leading-tight">
              What I believe shapes
              <br />
              <span className="text-gradient-accent">everything I build.</span>
            </h2>
          </Reveal>
        </div>

        <motion.div
          variants={staggerContainer}
          initial="hidden"
          whileInView="show"
          viewport={{ once: true, margin: "-60px" }}
          className="grid gap-px overflow-hidden rounded-3xl border border-border bg-border sm:grid-cols-2 lg:grid-cols-3"
        >
          {PHILOSOPHY.map((p) => (
            <motion.article
              key={p.index}
              variants={staggerItem}
              className="group relative flex flex-col gap-3 bg-background p-8 transition-colors duration-500 hover:bg-background-elev sm:p-10"
            >
              <span className="font-display text-sm text-faint transition-colors group-hover:text-accent">
                {p.index}
              </span>
              <h3 className="font-display text-xl font-semibold sm:text-2xl">
                {p.title}
              </h3>
              <p className="text-sm leading-relaxed text-muted sm:text-base">
                {p.body}
              </p>
              <div className="mt-auto h-px w-0 bg-gradient-to-r from-accent to-accent-2 transition-all duration-500 group-hover:w-full" />
            </motion.article>
          ))}
        </motion.div>
      </div>
    </section>
  );
}
