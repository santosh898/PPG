"use client";

import Link from "next/link";
import dynamic from "next/dynamic";
import { useCallback, useEffect, useState } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import {
  AlertTriangle,
  ArrowUpRight,
  Flame,
  Inbox,
  LayoutDashboard,
  Layers,
  Lock,
  MapPin,
  Minus,
  ShieldAlert,
  TrendingDown,
  TrendingUp,
} from "lucide-react";
import { Badge, Button, Card, PageHeader, SectionTitle, Stat, urgencyTone } from "@/components/ui";
import { categoryMeta } from "@/lib/categoryMeta";
import { DEFAULT_CONSTITUENCY } from "@/lib/constants";
import type { HeatPoint } from "@/components/HeatMap";

const HeatMap = dynamic(() => import("@/components/HeatMap"), {
  ssr: false,
  loading: () => (
    <div className="grid h-[420px] place-items-center rounded-xl border border-slate-200 text-sm text-slate-400">
      Loading map...
    </div>
  ),
});

interface DashboardData {
  priorities: Array<{
    rank: number;
    cluster_id: string;
    title: string;
    category: string;
    location: string;
    submission_count: number;
    urgency: string;
    trend: string;
    priority_score: number;
    reason: string;
  }>;
  category_breakdown: { category: string; submissions: number }[];
  hotspots: { location: string; submissions: number }[];
  rising: { id: string; title: string; priority_score: number; submission_count: number }[];
  unverified_urgent: { id: string; title: string; urgency: string; priority_score: number }[];
  map_points: HeatPoint[];
}

function TrendTag({ trend }: { trend: string }) {
  if (trend === "increasing") {
    return (
      <span className="inline-flex items-center gap-1 text-xs font-medium text-red-600">
        <TrendingUp className="h-3.5 w-3.5" /> Increasing
      </span>
    );
  }
  if (trend === "decreasing") {
    return (
      <span className="inline-flex items-center gap-1 text-xs font-medium text-emerald-600">
        <TrendingDown className="h-3.5 w-3.5" /> Decreasing
      </span>
    );
  }
  return (
    <span className="inline-flex items-center gap-1 text-xs font-medium text-slate-400">
      <Minus className="h-3.5 w-3.5" /> Stable
    </span>
  );
}

function DashboardSkeleton() {
  return (
    <div className="animate-pulse space-y-6">
      <div className="h-16 rounded-xl bg-slate-100" />
      <div className="grid gap-3 sm:grid-cols-4">
        {Array.from({ length: 4 }).map((_, i) => (
          <div key={i} className="h-24 rounded-xl bg-slate-100" />
        ))}
      </div>
      <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-3">
        {Array.from({ length: 3 }).map((_, i) => (
          <div key={i} className="h-32 rounded-xl bg-slate-100" />
        ))}
      </div>
      <div className="h-[420px] rounded-xl bg-slate-100" />
    </div>
  );
}

export default function MpDashboardPage() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [reportBusy, setReportBusy] = useState(false);
  const [report, setReport] = useState<{
    title: string;
    sections: { heading: string; content: string }[];
  } | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    const res = await fetch("/api/mp/dashboard");
    setData(await res.json());
    setLoading(false);
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  async function generateReport() {
    setReportBusy(true);
    const res = await fetch("/api/mp/reports", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ report_type: "weekly_priority_report" }),
    });
    setReport(await res.json());
    setReportBusy(false);
  }

  if (loading || !data) {
    return (
      <div className="space-y-6">
        <PageHeader
          icon={LayoutDashboard}
          eyebrow="For officials"
          title="MP Dashboard"
          subtitle={`Constituency-wide priorities for ${DEFAULT_CONSTITUENCY.name}`}
        />
        <DashboardSkeleton />
      </div>
    );
  }

  const totalSubs = data.category_breakdown.reduce(
    (s, c) => s + c.submissions,
    0
  );

  return (
    <div className="space-y-6">
      <PageHeader
        icon={LayoutDashboard}
        eyebrow="For officials"
        title="MP Dashboard"
        subtitle={`Constituency-wide priorities for ${DEFAULT_CONSTITUENCY.name} \u00b7 updated this week`}
        action={
          <div className="flex flex-wrap items-center gap-2">
            <span className="inline-flex items-center gap-1.5 rounded-full border border-slate-200 bg-slate-50 px-3 py-1.5 text-xs font-medium text-slate-500">
              <Lock className="h-3.5 w-3.5" />
              {DEFAULT_CONSTITUENCY.name} only
            </span>
            <Button onClick={generateReport} disabled={reportBusy}>
              {reportBusy ? "Generating..." : "Generate weekly report"}
            </Button>
          </div>
        }
      />

      <div className="grid gap-3 sm:grid-cols-4">
        <Stat icon={Inbox} label="Total submissions" value={totalSubs} />
        <Stat
          icon={Layers}
          label="Active clusters"
          value={data.category_breakdown.length ? data.priorities.length + data.rising.length : 0}
        />
        <Stat
          icon={Flame}
          tone="amber"
          label="Top priority score"
          value={data.priorities[0]?.priority_score ?? "-"}
          hint={data.priorities[0]?.title}
        />
        <Stat
          icon={ShieldAlert}
          tone="red"
          label="Urgent & unverified"
          value={data.unverified_urgent.length}
          hint={data.unverified_urgent.length ? "Needs staff verification" : "All clear"}
        />
      </div>

      <div>
        <SectionTitle title="Top 5 priority issues" subtitle="Ranked by explainable priority score, weighted by reach, urgency and recency" />
        <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-3">
          {data.priorities.map((p) => {
            const meta = categoryMeta(p.category);
            const CatIcon = meta.icon;
            return (
              <Card key={p.cluster_id} className="flex flex-col">
                <div className="flex items-start justify-between gap-2">
                  <div className="flex items-start gap-2.5">
                    <span className="grid h-8 w-8 shrink-0 place-items-center rounded-full bg-slate-900 text-xs font-bold text-white">
                      {p.rank}
                    </span>
                    <span className="text-sm font-semibold leading-snug text-slate-900">
                      {p.title}
                    </span>
                  </div>
                  <Badge tone="purple" className="shrink-0">
                    {p.priority_score}
                  </Badge>
                </div>
                <div className="mt-2 flex flex-wrap items-center gap-1.5">
                  <span className={`inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-xs font-medium ${meta.chip}`}>
                    <CatIcon className="h-3 w-3" />
                    {p.category}
                  </span>
                  <Badge tone={urgencyTone(p.urgency)}>{p.urgency}</Badge>
                </div>
                <div className="mt-2 flex items-center justify-between text-xs text-slate-500">
                  <span className="flex items-center gap-1">
                    <MapPin className="h-3.5 w-3.5" />
                    {p.location}
                  </span>
                  <TrendTag trend={p.trend} />
                </div>
                <p className="mt-2 flex-1 text-xs text-slate-500">{p.reason}</p>
                <div className="mt-3 flex items-center justify-between border-t border-slate-100 pt-2 text-xs text-slate-400">
                  <span>{p.submission_count} submissions</span>
                  <Link
                    href={`/mp/chat?q=${encodeURIComponent(`Why is "${p.title}" ranked #${p.rank}?`)}`}
                    className="inline-flex items-center gap-1 font-medium text-brand-600 hover:underline"
                  >
                    Ask about this <ArrowUpRight className="h-3 w-3" />
                  </Link>
                </div>
              </Card>
            );
          })}
        </div>
      </div>

      <div>
        <SectionTitle title="Issue heatmap" subtitle="Concentration of submissions across the constituency" />
        <HeatMap points={data.map_points} />
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <Card>
          <SectionTitle title="Issue category breakdown" subtitle={`${totalSubs} submissions across ${data.category_breakdown.length} categories`} />
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={data.category_breakdown}>
              <CartesianGrid strokeDasharray="3 3" stroke="#eef2f7" />
              <XAxis dataKey="category" tick={{ fontSize: 11 }} />
              <YAxis tick={{ fontSize: 11 }} allowDecimals={false} />
              <Tooltip />
              <Bar dataKey="submissions" radius={[4, 4, 0, 0]}>
                {data.category_breakdown.map((c) => (
                  <Cell key={c.category} fill={categoryMeta(c.category).hex} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
          <div className="mt-2 flex flex-wrap gap-x-3 gap-y-1">
            {data.category_breakdown.map((c) => (
              <span key={c.category} className="flex items-center gap-1.5 text-xs text-slate-500">
                <span
                  className="h-2 w-2 rounded-full"
                  style={{ backgroundColor: categoryMeta(c.category).hex }}
                />
                {c.category}
              </span>
            ))}
          </div>
        </Card>

        <Card>
          <SectionTitle title="Location hotspots" subtitle="Top areas by submission volume" />
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={data.hotspots} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="#eef2f7" />
              <XAxis type="number" tick={{ fontSize: 11 }} allowDecimals={false} />
              <YAxis
                type="category"
                dataKey="location"
                width={100}
                tick={{ fontSize: 11 }}
              />
              <Tooltip />
              <Bar dataKey="submissions" fill="#164bdd" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Card>
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <Card>
          <SectionTitle title="Rising issues" subtitle="High-priority clusters gaining momentum" />
          <div className="space-y-1">
            {data.rising.map((r) => (
              <div
                key={r.id}
                className="flex items-center justify-between gap-2 rounded-lg px-2 py-2 text-sm hover:bg-slate-50"
              >
                <span className="flex items-center gap-2 text-slate-700">
                  <TrendingUp className="h-4 w-4 shrink-0 text-red-500" />
                  {r.title}
                </span>
                <Badge tone="amber">score {r.priority_score}</Badge>
              </div>
            ))}
            {!data.rising.length && (
              <p className="px-2 text-xs text-slate-400">Nothing trending up right now.</p>
            )}
          </div>
        </Card>
        <Card>
          <SectionTitle title="Unverified urgent issues" subtitle="Need staff verification first" />
          <div className="space-y-1">
            {data.unverified_urgent.map((r) => (
              <div
                key={r.id}
                className="flex items-center justify-between gap-2 rounded-lg px-2 py-2 text-sm hover:bg-slate-50"
              >
                <span className="flex items-center gap-2 text-slate-700">
                  <AlertTriangle className="h-4 w-4 shrink-0 text-red-500" />
                  {r.title}
                </span>
                <div className="flex gap-1">
                  <Badge tone={urgencyTone(r.urgency)}>{r.urgency}</Badge>
                  <Badge tone="red">unverified</Badge>
                </div>
              </div>
            ))}
            {!data.unverified_urgent.length && (
              <p className="px-2 text-xs text-slate-400">None right now.</p>
            )}
          </div>
        </Card>
      </div>

      {report && (
        <Card className="border-brand-200 bg-brand-50">
          <SectionTitle title={report.title} />
          <div className="space-y-3">
            {report.sections.map((s, i) => (
              <div key={i}>
                <div className="text-sm font-semibold text-slate-800">
                  {s.heading}
                </div>
                <div className="whitespace-pre-wrap text-sm text-slate-600">
                  {s.content}
                </div>
              </div>
            ))}
          </div>
          <p className="mt-3 text-xs text-slate-400">
            Population figures are public baseline estimates. Some clusters are
            AI-grouped and not yet staff-verified.
          </p>
        </Card>
      )}
    </div>
  );
}
