import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { SiteNav } from "@/components/SiteNav";
import { cn } from "@/lib/utils";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });

export const metadata: Metadata = {
  title: "People's Priorities",
  description:
    "AI-powered constituency intelligence: citizens report issues through conversation, MPs get ranked, evidence-backed priorities.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={inter.variable}>
      <body className={cn(inter.className, "antialiased")}>
        <SiteNav />
        <main className="mx-auto w-full max-w-7xl px-4 py-6">{children}</main>
      </body>
    </html>
  );
}
