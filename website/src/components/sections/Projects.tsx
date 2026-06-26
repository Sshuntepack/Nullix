"use client";

import { useRef } from "react";
import { motion } from "framer-motion";
import { ArrowUpRight } from "lucide-react";
import { PROJECTS } from "@/lib/data";
import { Reveal, staggerContainer, staggerItem } from "../Reveal";

function ProjectCard({
  project,
}: {
  project: (typeof PROJECTS)[number];
}) {
  const ref = useRef<HTMLDivElement>(null);

  const onMove = (e: React.MouseEvent) => {
    const el = ref.current;
    if (!el) return;
    const rect = el.getBoundingClientRect();
    const px = (e.clientX - rect.left) / rect.width - 0.5;
    const py = (e.clientY - rect.top) / rect.height - 0.5;
    el.style.setProperty("--rx", `${py * -6}deg`);
    el.style.setProperty("--ry", `${px * 8}deg`);
  };
  const onLeave = () => {
    const el = ref.current;
    if (!el) return;
    el.style.setProperty("--rx", "0deg");
    el.style.setProperty("--ry", "0deg");
  };

  return (
    <motion.article variants={staggerItem} className="[perspective:1200px]">
      <div
        ref={ref}
        onMouseMove={onMove}
        onMouseLeave={onLeave}
        className="group relative h-full overflow-hidden rounded-3xl border border-border bg-background-elev/40 p-8 transition-[transform,border-color] duration-300 ease-out hover:border-border-strong sm:p-10"
        style={{
          transform:
            "rotateX(var(--rx,0)) rotateY(var(--ry,0))",
          transformStyle: "preserve-3d",
        }}
      >
        <div
          className="pointer-events-none absolute inset-0 opacity-0 transition-opacity duration-500 group-hover:opacity-100"
          style={{
            background:
              "linear-gradient(135deg, color-mix(in srgb, var(--accent) 14%, transparent), transparent 55%)",
          }}
        />
        <div className="relative flex h-full flex-col">
          <div className="flex items-start justify-between">
            <span className="inline-flex items-center gap-2 rounded-full border border-border px-3 py-1 text-[10px] uppercase tracking-[0.2em] text-muted">
              <span className="h-1.5 w-1.5 rounded-full bg-accent-3" />
              In development
            </span>
            <ArrowUpRight className="h-5 w-5 text-faint transition-all duration-300 group-hover:-translate-y-1 group-hover:translate-x-1 group-hover:text-accent" />
          </div>

          <h3 className="mt-8 font-display text-3xl font-bold sm:text-4xl">
            {project.name}
          </h3>
          <p className="mt-1 text-sm font-medium text-accent">
            {project.tagline}
          </p>
          <p className="mt-4 text-sm leading-relaxed text-muted">
            {project.description}
          </p>

          <div className="mt-auto flex flex-wrap gap-2 pt-8">
            {project.tags.map((t) => (
              <span
                key={t}
                className="rounded-full bg-foreground/[0.06] px-3 py-1 text-xs text-muted"
              >
                {t}
              </span>
            ))}
          </div>
        </div>
      </div>
    </motion.article>
  );
}

export function Projects() {
  return (
    <section id="projects" className="relative px-6 py-28 sm:px-10 sm:py-40">
      <div className="mx-auto max-w-6xl">
        <div className="mb-16 flex flex-wrap items-end justify-between gap-6">
          <div className="max-w-2xl">
            <Reveal>
              <p className="mb-6 text-xs uppercase tracking-[0.3em] text-accent">
                05 — Projects
              </p>
            </Reveal>
            <Reveal delay={0.05}>
              <h2 className="font-display text-[clamp(1.8rem,4.5vw,3.4rem)] font-semibold leading-tight">
                Building in the open.
                <span className="text-muted"> More soon.</span>
              </h2>
            </Reveal>
          </div>
          <Reveal delay={0.1}>
            <p className="max-w-xs text-sm text-muted">
              Early-stage work, shared as it takes shape. Each one is a step
              toward something larger.
            </p>
          </Reveal>
        </div>

        <motion.div
          variants={staggerContainer}
          initial="hidden"
          whileInView="show"
          viewport={{ once: true, margin: "-60px" }}
          className="grid gap-5 md:grid-cols-3"
        >
          {PROJECTS.map((p) => (
            <ProjectCard key={p.name} project={p} />
          ))}
        </motion.div>
      </div>
    </section>
  );
}
