import type { LucideIcon } from "lucide-react";
import { cn } from "@/lib/utils";

export function PageHeader({
  icon: Icon,
  eyebrow,
  title,
  subtitle,
  action,
  tone = "brand",
}: {
  icon?: LucideIcon;
  eyebrow?: string;
  title: string;
  subtitle?: string;
  action?: React.ReactNode;
  tone?: "brand" | "emerald";
}) {
  const toneStyles =
    tone === "emerald"
      ? "bg-emerald-100 text-emerald-700"
      : "bg-brand-100 text-brand-700";
  return (
    <div className="flex flex-wrap items-start justify-between gap-3">
      <div className="flex items-start gap-3">
        {Icon && (
          <span
            className={cn(
              "mt-0.5 grid h-10 w-10 shrink-0 place-items-center rounded-xl",
              toneStyles
            )}
          >
            <Icon className="h-5 w-5" />
          </span>
        )}
        <div>
          {eyebrow && (
            <div className="text-xs font-semibold uppercase tracking-wide text-slate-400">
              {eyebrow}
            </div>
          )}
          <h1 className="text-2xl font-bold text-slate-900">{title}</h1>
          {subtitle && (
            <p className="mt-1 max-w-2xl text-sm text-slate-500">{subtitle}</p>
          )}
        </div>
      </div>
      {action && <div className="shrink-0">{action}</div>}
    </div>
  );
}

export function Card({
  className,
  children,
}: {
  className?: string;
  children: React.ReactNode;
}) {
  return (
    <div
      className={cn(
        "rounded-xl border border-slate-200 bg-white p-4 shadow-sm",
        className
      )}
    >
      {children}
    </div>
  );
}

export function SectionTitle({
  title,
  subtitle,
}: {
  title: string;
  subtitle?: string;
}) {
  return (
    <div className="mb-3">
      <h2 className="text-lg font-semibold text-slate-900">{title}</h2>
      {subtitle && <p className="text-sm text-slate-500">{subtitle}</p>}
    </div>
  );
}

const badgeTones: Record<string, string> = {
  gray: "bg-slate-100 text-slate-700",
  blue: "bg-brand-100 text-brand-800",
  green: "bg-emerald-100 text-emerald-800",
  amber: "bg-amber-100 text-amber-800",
  red: "bg-red-100 text-red-800",
  purple: "bg-purple-100 text-purple-800",
};

export function Badge({
  children,
  tone = "gray",
  className,
}: {
  children: React.ReactNode;
  tone?: keyof typeof badgeTones | string;
  className?: string;
}) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium",
        badgeTones[tone] || badgeTones.gray,
        className
      )}
    >
      {children}
    </span>
  );
}

export function urgencyTone(urgency: string): string {
  switch (urgency) {
    case "Critical":
      return "red";
    case "High":
      return "amber";
    case "Medium":
      return "blue";
    default:
      return "gray";
  }
}

export function Stat({
  label,
  value,
  hint,
  icon: Icon,
  tone = "brand",
}: {
  label: string;
  value: React.ReactNode;
  hint?: string;
  icon?: LucideIcon;
  tone?: "brand" | "emerald" | "amber" | "red";
}) {
  const toneStyles: Record<string, string> = {
    brand: "bg-brand-100 text-brand-700",
    emerald: "bg-emerald-100 text-emerald-700",
    amber: "bg-amber-100 text-amber-700",
    red: "bg-red-100 text-red-700",
  };
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-soft">
      <div className="flex items-center gap-2">
        {Icon && (
          <span
            className={cn(
              "grid h-8 w-8 shrink-0 place-items-center rounded-lg",
              toneStyles[tone]
            )}
          >
            <Icon className="h-4 w-4" />
          </span>
        )}
        <div className="text-xs uppercase tracking-wide text-slate-500">
          {label}
        </div>
      </div>
      <div className="mt-2 text-2xl font-semibold text-slate-900">{value}</div>
      {hint && <div className="mt-0.5 truncate text-xs text-slate-400">{hint}</div>}
    </div>
  );
}

export function Button({
  children,
  onClick,
  disabled,
  variant = "primary",
  type = "button",
  className,
}: {
  children: React.ReactNode;
  onClick?: () => void;
  disabled?: boolean;
  variant?: "primary" | "ghost" | "outline";
  type?: "button" | "submit";
  className?: string;
}) {
  const styles = {
    primary: "bg-brand-600 text-white hover:bg-brand-700 disabled:bg-slate-300",
    ghost: "text-slate-600 hover:bg-slate-100",
    outline: "border border-slate-300 text-slate-700 hover:bg-slate-50",
  };
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={cn(
        "inline-flex items-center justify-center rounded-lg px-3 py-2 text-sm font-medium transition disabled:cursor-not-allowed",
        styles[variant],
        className
      )}
    >
      {children}
    </button>
  );
}
