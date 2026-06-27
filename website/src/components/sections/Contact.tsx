"use client";

import { Github, Mail, Instagram, ArrowUpRight } from "@/components/icons";
import { CONTACT } from "@/lib/data";
import { Reveal } from "../Reveal";

const LINKS = [
  {
    label: "GitHub",
    value: "Sshuntepack",
    href: CONTACT.github,
    Icon: Github,
  },
  {
    label: "Email",
    value: CONTACT.email,
    href: `mailto:${CONTACT.email}`,
    Icon: Mail,
  },
  {
    label: "Instagram",
    value: "@l.ost_h.eir",
    href: CONTACT.instagram,
    Icon: Instagram,
  },
];

export function Contact() {
  return (
    <section id="contact" className="relative px-6 py-28 sm:px-10 sm:py-44">
      <div className="mx-auto max-w-4xl text-center">
        <Reveal>
          <p className="mb-8 text-xs uppercase tracking-[0.3em] text-accent">
            07 — Contact
          </p>
        </Reveal>
        <Reveal delay={0.05}>
          <h2 className="font-display text-[clamp(2.2rem,6vw,4.5rem)] font-bold leading-[1.05]">
            Let&apos;s build
            <br />
            <span className="text-gradient animate-gradient">
              something that lasts.
            </span>
          </h2>
        </Reveal>
        <Reveal delay={0.12}>
          <p className="mx-auto mt-7 max-w-xl text-lg text-muted">
            The journey is just beginning. If you want to follow along, collaborate,
            or just say hello — I&apos;d love to hear from you.
          </p>
        </Reveal>

        <div className="mx-auto mt-14 grid max-w-2xl gap-4 sm:grid-cols-3">
          {LINKS.map(({ label, value, href, Icon }, i) => (
            <Reveal key={label} delay={0.1 + i * 0.08}>
              <a
                href={href}
                target={href.startsWith("mailto:") ? undefined : "_blank"}
                rel="noopener noreferrer"
                className="group relative flex h-full flex-col items-center gap-3 overflow-hidden rounded-3xl border border-border bg-background-elev/40 p-7 transition-colors duration-300 hover:border-border-strong"
              >
                <ArrowUpRight className="absolute right-4 top-4 h-4 w-4 text-faint opacity-0 transition-all duration-300 group-hover:-translate-y-0.5 group-hover:translate-x-0.5 group-hover:text-accent group-hover:opacity-100" />
                <span className="grid h-12 w-12 place-items-center rounded-xl border border-border bg-background transition-transform duration-300 group-hover:scale-110 group-hover:border-accent/50">
                  <Icon className="h-5 w-5 text-accent" />
                </span>
                <span className="text-xs uppercase tracking-[0.2em] text-faint">
                  {label}
                </span>
                <span className="text-sm font-medium">{value}</span>
              </a>
            </Reveal>
          ))}
        </div>
      </div>

      <footer className="mx-auto mt-28 flex max-w-6xl flex-col items-center justify-between gap-4 border-t border-border pt-8 text-sm text-faint sm:flex-row">
        <span className="font-display text-base text-foreground">Donell</span>
        <span>© {new Date().getFullYear()} — Building the future, one step at a time.</span>
      </footer>
    </section>
  );
}
