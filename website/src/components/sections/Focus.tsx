"use client";

import { useRef } from "react";
import { motion } from "framer-motion";
import { FOCUS_AREAS } from "@/lib/data";
import { Reveal, staggerContainer, staggerItem } from "../Reveal";

function FocusCard({
  title,
  description,
  Icon,
}: {
  title: string;
  description: string;
  Icon: (typeof FOCUS_AREAS)[number]["icon"];
}) {
  const ref = useRef<HTMLDivElement>(null);

  const onMove = (e: React.MouseEvent) => {
    const el = ref.current;
    if (!el) return;
    const rect = el.getBoundingClientRect();
    el.style.setProperty("--px", `${e.clientX - rect.left}px`);
    el.style.setProperty("--py", `${e.clientY - rect.top}px`);
  };

  return (
    <motion.div
      variants={staggerItem}
      ref={ref}
      onMouseMove={onMove}
      className="group relative overflow-hidden rounded-3xl border border-border bg-background-elev/40 p-8 transition-colors duration-500 hover:border-border-strong"
    >
      {/* spotlight */}
      <div
        className="pointer-events-none absolute inset-0 opacity-0 transition-opacity duration-500 group-hover:opacity-100"
        style={{
          background:
            "radial-gradient(380px circle at var(--px) var(--py), color-mix(in srgb, var(--accent) 18%, transparent), transparent 70%)",
        }}
      />
      <div className="relative">
        <div className="mb-6 grid h-12 w-12 place-items-center rounded-xl border border-border bg-background transition-transform duration-500 group-hover:scale-110 group-hover:border-accent/50">
          <Icon className="h-5 w-5 text-accent" />
        </div>
        <h3 className="font-display text-xl font-semibold">{title}</h3>
        <p className="mt-3 text-sm leading-relaxed text-muted">{description}</p>
      </div>
    </motion.div>
  );
}

export function Focus() {
  return (
    <section id="focus" className="relative px-6 py-28 sm:px-10 sm:py-40">
      <div className="mx-auto max-w-6xl">
        <div className="mb-16 max-w-2xl">
          <Reveal>
            <p className="mb-6 text-xs uppercase tracking-[0.3em] text-accent">
              03 — Current Focus
            </p>
          </Reveal>
          <Reveal delay={0.05}>
            <h2 className="font-display text-[clamp(1.8rem,4.5vw,3.4rem)] font-semibold leading-tight">
              Where my energy lives
              <span className="text-muted"> right now.</span>
            </h2>
          </Reveal>
        </div>

        <motion.div
          variants={staggerContainer}
          initial="hidden"
          whileInView="show"
          viewport={{ once: true, margin: "-60px" }}
          className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3"
        >
          {FOCUS_AREAS.map((f) => (
            <FocusCard
              key={f.title}
              title={f.title}
              description={f.description}
              Icon={f.icon}
            />
          ))}
        </motion.div>
      </div>
    </section>
  );
}
