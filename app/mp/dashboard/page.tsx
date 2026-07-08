"use client";

import dynamic from "next/dynamic";
import { useCallback, useEffect, useState } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { Badge, Button, Card, SectionTitle, Stat, urgencyTone } from "@/components/ui";
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

  if (loading || !data) return <Card>Loading dashboard...</Card>;

  const totalSubs = data.category_breakdown.reduce(
    (s, c) => s + c.submissions,
    0
  );

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">MP Dashboard</h1>
          <p className="text-sm text-slate-500">
            Constituency: Visakhapatnam · this week
          </p>
        </div>
        <Button onClick={generateReport} disabled={reportBusy}>
          {reportBusy ? "Generating..." : "Generate weekly report"}
        </Button>
      </div>

      <div className="grid gap-3 sm:grid-cols-4">
        <Stat label="Total submissions" value={totalSubs} />
        <Stat label="Active clusters" value={data.category_breakdown.length ? data.priorities.length + data.rising.length : 0} />
        <Stat label="Top priority" value={data.priorities[0]?.priority_score ?? "-"} hint={data.priorities[0]?.title} />
        <Stat label="Urgent & unverified" value={data.unverified_urgent.length} />
      </div>

      <div>
        <SectionTitle title="Top 5 priority issues" subtitle="Ranked by explainable priority score" />
        <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-3">
          {data.priorities.map((p) => (
            <Card key={p.cluster_id}>
              <div className="flex items-center justify-between">
                <span className="text-sm font-semibold text-slate-900">
                  #{p.rank} {p.title}
                </span>
                <Badge tone="purple">{p.priority_score}</Badge>
              </div>
              <div className="mt-1 flex flex-wrap items-center gap-1">
                <Badge tone="blue">{p.category}</Badge>
                <Badge tone={urgencyTone(p.urgency)}>{p.urgency}</Badge>
                <Badge tone="gray">{p.trend}</Badge>
              </div>
              <div className="mt-2 text-xs text-slate-500">
                {p.submission_count} submissions · {p.location}
              </div>
              <p className="mt-2 text-xs text-slate-500">{p.reason}</p>
            </Card>
          ))}
        </div>
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <Card>
          <SectionTitle title="Issue category breakdown" />
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={data.category_breakdown}>
              <CartesianGrid strokeDasharray="3 3" stroke="#eef2f7" />
              <XAxis dataKey="category" tick={{ fontSize: 11 }} />
              <YAxis tick={{ fontSize: 11 }} />
              <Tooltip />
              <Bar dataKey="submissions" fill="#3380fc" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Card>

        <Card>
          <SectionTitle title="Location hotspots" />
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={data.hotspots} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="#eef2f7" />
              <XAxis type="number" tick={{ fontSize: 11 }} />
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

      <div>
        <SectionTitle title="Issue heatmap" subtitle="Concentration of submissions across the constituency" />
        <HeatMap points={data.map_points} />
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <Card>
          <SectionTitle title="Rising issues" />
          <div className="space-y-2">
            {data.rising.map((r) => (
              <div
                key={r.id}
                className="flex items-center justify-between text-sm"
              >
                <span className="text-slate-700">{r.title}</span>
                <Badge tone="amber">score {r.priority_score}</Badge>
              </div>
            ))}
          </div>
        </Card>
        <Card>
          <SectionTitle title="Unverified urgent issues" subtitle="Need staff verification first" />
          <div className="space-y-2">
            {data.unverified_urgent.map((r) => (
              <div
                key={r.id}
                className="flex items-center justify-between text-sm"
              >
                <span className="text-slate-700">{r.title}</span>
                <div className="flex gap-1">
                  <Badge tone={urgencyTone(r.urgency)}>{r.urgency}</Badge>
                  <Badge tone="red">unverified</Badge>
                </div>
              </div>
            ))}
            {!data.unverified_urgent.length && (
              <p className="text-xs text-slate-400">None right now.</p>
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
