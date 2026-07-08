import Link from "next/link";

const links = [
  { href: "/citizen", label: "Citizen Chat" },
  { href: "/staff", label: "Staff Console" },
  { href: "/mp/chat", label: "MP Chat" },
  { href: "/mp/dashboard", label: "MP Dashboard" },
  { href: "/public/issues", label: "Public Issues" },
];

export function SiteNav() {
  return (
    <header className="sticky top-0 z-30 border-b border-slate-200 bg-white/90 backdrop-blur">
      <div className="mx-auto flex w-full max-w-7xl items-center gap-6 px-4 py-3">
        <Link href="/" className="flex items-center gap-2">
          <span className="grid h-8 w-8 place-items-center rounded-lg bg-brand-600 text-sm font-bold text-white">
            PP
          </span>
          <span className="text-sm font-semibold text-slate-900">
            People&apos;s Priorities
          </span>
        </Link>
        <nav className="flex flex-wrap items-center gap-1 text-sm">
          {links.map((l) => (
            <Link
              key={l.href}
              href={l.href}
              className="rounded-md px-3 py-1.5 text-slate-600 transition hover:bg-slate-100 hover:text-slate-900"
            >
              {l.label}
            </Link>
          ))}
        </nav>
      </div>
    </header>
  );
}
