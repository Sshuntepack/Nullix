import type { Metadata, Viewport } from "next";
import { Sora, Inter } from "next/font/google";
import "./globals.css";
import { ThemeProvider } from "@/components/ThemeProvider";

const display = Sora({
  variable: "--font-display",
  subsets: ["latin"],
  weight: ["400", "500", "600", "700", "800"],
  display: "swap",
});

const sans = Inter({
  variable: "--font-sans",
  subsets: ["latin"],
  display: "swap",
});

const SITE_URL = "https://donell.dev";

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: {
    default: "Donell — Building the future through software, AI & games",
    template: "%s · Donell",
  },
  description:
    "Donell is a student, software engineer, game developer, and founder building meaningful technology — companies, games inspired by African stories, and tools that solve real problems.",
  keywords: [
    "Donell",
    "software engineer",
    "game developer",
    "founder",
    "artificial intelligence",
    "startup",
    "creative technology",
  ],
  authors: [{ name: "Donell", url: SITE_URL }],
  creator: "Donell",
  openGraph: {
    type: "website",
    url: SITE_URL,
    title: "Donell — Building the future through software, AI & games",
    description:
      "Student • Software Engineer • Game Developer • Founder. Building meaningful technology and following a long-term vision.",
    siteName: "Donell",
  },
  twitter: {
    card: "summary_large_image",
    title: "Donell — Building the future through software, AI & games",
    description:
      "Student • Software Engineer • Game Developer • Founder. Building meaningful technology and following a long-term vision.",
  },
  robots: { index: true, follow: true },
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  themeColor: [
    { media: "(prefers-color-scheme: dark)", color: "#050507" },
    { media: "(prefers-color-scheme: light)", color: "#f7f7f5" },
  ],
};

// Set theme before paint to avoid flash.
const themeScript = `
(function() {
  try {
    var stored = localStorage.getItem('theme');
    var theme = stored || 'dark';
    document.documentElement.classList.toggle('dark', theme === 'dark');
    document.documentElement.style.colorScheme = theme;
  } catch (e) {
    document.documentElement.classList.add('dark');
  }
})();
`;

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <script dangerouslySetInnerHTML={{ __html: themeScript }} />
      </head>
      <body className={`${display.variable} ${sans.variable} antialiased`}>
        <ThemeProvider>{children}</ThemeProvider>
      </body>
    </html>
  );
}
