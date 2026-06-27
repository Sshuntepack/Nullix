import { Preloader } from "@/components/Preloader";
import { Cursor } from "@/components/Cursor";
import { Background } from "@/components/Background";
import { Navbar } from "@/components/Navbar";
import { Hero } from "@/components/sections/Hero";
import { About } from "@/components/sections/About";
import { Philosophy } from "@/components/sections/Philosophy";
import { Focus } from "@/components/sections/Focus";
import { Vision } from "@/components/sections/Vision";
import { Projects } from "@/components/sections/Projects";
import { Timeline } from "@/components/sections/Timeline";
import { Contact } from "@/components/sections/Contact";

export default function Home() {
  return (
    <>
      <Preloader />
      <Cursor />
      <Background />
      <div className="grain" aria-hidden="true" />
      <Navbar />
      <main className="relative z-[2]">
        <Hero />
        <About />
        <Philosophy />
        <Focus />
        <Vision />
        <Projects />
        <Timeline />
        <Contact />
      </main>
    </>
  );
}
