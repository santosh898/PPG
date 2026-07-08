"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { LayoutDashboard, MessageCircleMore, MessageSquareText } from "lucide-react";
import { cn } from "@/lib/utils";

const officialLinks = [
  { href: "/mp/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { href: "/mp/chat", label: "MP Chat", icon: MessageSquareText },
];

const utilityLinks = [
  { href: "/staff", label: "Staff" },
  { href: "/public/issues", label: "Public Issues" },
];

export function SiteNav() {
  const pathname = usePathname();

  return (
    <header className="sticky top-0 z-30 border-b border-slate-200 bg-white/90 backdrop-blur">
      <div className="mx-auto flex w-full max-w-7xl items-center justify-between gap-3 px-4 py-2.5">
        <Link href="/" className="flex shrink-0 items-center gap-2">
          <span className="grid h-8 w-8 place-items-center rounded-lg bg-brand-600 text-sm font-bold text-white">
            PP
          </span>
          <span className="hidden text-sm font-semibold text-slate-900 sm:inline">
            People&apos;s Priorities
          </span>
        </Link>

        <nav className="flex items-center gap-1 rounded-lg bg-slate-100 p-1">
          {officialLinks.map((l) => {
            const active = pathname === l.href;
            const Icon = l.icon;
            return (
              <Link
                key={l.href}
                href={l.href}
                className={cn(
                  "flex items-center gap-1.5 rounded-md px-3 py-1.5 text-sm transition",
                  active
                    ? "bg-white font-medium text-brand-700 shadow-sm"
                    : "text-slate-500 hover:text-slate-800"
                )}
              >
                <Icon className="h-4 w-4" />
                <span className="hidden sm:inline">{l.label}</span>
              </Link>
            );
          })}
        </nav>

        <div className="flex items-center gap-4">
          <div className="hidden items-center gap-3 md:flex">
            {utilityLinks.map((l) => (
              <Link
                key={l.href}
                href={l.href}
                className={cn(
                  "text-xs transition",
                  pathname === l.href
                    ? "font-medium text-slate-700"
                    : "text-slate-400 hover:text-slate-600"
                )}
              >
                {l.label}
              </Link>
            ))}
          </div>
          <Link
            href="/citizen"
            className="flex items-center gap-1.5 rounded-lg bg-emerald-600 px-3.5 py-2 text-sm font-medium text-white transition hover:bg-emerald-700"
          >
            <MessageCircleMore className="h-4 w-4" />
            <span className="hidden sm:inline">Report an Issue</span>
          </Link>
        </div>
      </div>
    </header>
  );
}
