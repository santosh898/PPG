import {
  Droplets,
  GraduationCap,
  HandCoins,
  HeartPulse,
  Lightbulb,
  Trash2,
  Waves,
  Zap,
  CircleHelp,
  Construction,
  type LucideIcon,
} from "lucide-react";
import type { Category } from "./constants";

interface CategoryMeta {
  icon: LucideIcon;
  /** Tailwind classes for icon chip background + text */
  chip: string;
  /** Hex used in recharts bars, matched to the chip color */
  hex: string;
}

export const CATEGORY_META: Record<Category, CategoryMeta> = {
  Water: { icon: Droplets, chip: "bg-sky-100 text-sky-700", hex: "#0284c7" },
  Roads: { icon: Construction, chip: "bg-orange-100 text-orange-700", hex: "#ea580c" },
  Drainage: { icon: Waves, chip: "bg-cyan-100 text-cyan-700", hex: "#0891b2" },
  Streetlights: { icon: Lightbulb, chip: "bg-amber-100 text-amber-700", hex: "#d97706" },
  Pension: { icon: HandCoins, chip: "bg-violet-100 text-violet-700", hex: "#7c3aed" },
  Health: { icon: HeartPulse, chip: "bg-rose-100 text-rose-700", hex: "#e11d48" },
  Education: { icon: GraduationCap, chip: "bg-indigo-100 text-indigo-700", hex: "#4f46e5" },
  Sanitation: { icon: Trash2, chip: "bg-lime-100 text-lime-700", hex: "#65a30d" },
  Electricity: { icon: Zap, chip: "bg-yellow-100 text-yellow-700", hex: "#ca8a04" },
  Other: { icon: CircleHelp, chip: "bg-slate-100 text-slate-600", hex: "#64748b" },
};

export function categoryMeta(category: string): CategoryMeta {
  return CATEGORY_META[category as Category] ?? CATEGORY_META.Other;
}
