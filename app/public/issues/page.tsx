"use client";

import { useCallback, useEffect, useState } from "react";
import { Badge, Card } from "@/components/ui";
import { CATEGORIES } from "@/lib/constants";

interface PublicIssue {
  id: string;
  title: string;
  category: string;
  area: string;
  status: string;
  report_count: number;
  public_updates: { note: string; created_at: string }[];
}

export default function PublicIssuesPage() {
  const [issues, setIssues] = useState<PublicIssue[]>([]);
  const [category, setCategory] = useState("");
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    setLoading(true);
    const qs = category ? `?category=${encodeURIComponent(category)}` : "";
    const res = await fetch(`/api/public/issues${qs}`);
    const data = await res.json();
    setIssues(data.issues || []);
    setLoading(false);
  }, [category]);

  useEffect(() => {
    load();
  }, [load]);

  return (
    <div className="space-y-4">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">
          Public Issue Tracker
        </h1>
        <p className="text-sm text-slate-500">
          Anonymized local issue clusters and public updates. No personal data,
          names, phone numbers, raw complaints or home locations are shown.
        </p>
      </div>

      <div className="flex flex-wrap items-center gap-2">
        <button
          onClick={() => setCategory("")}
          className={
            category === ""
              ? "rounded-full bg-brand-600 px-3 py-1 text-xs font-medium text-white"
              : "rounded-full border border-slate-200 bg-white px-3 py-1 text-xs text-slate-600"
          }
        >
          All
        </button>
        {CATEGORIES.filter((c) => c !== "Other").map((c) => (
          <button
            key={c}
            onClick={() => setCategory(c)}
            className={
              category === c
                ? "rounded-full bg-brand-600 px-3 py-1 text-xs font-medium text-white"
                : "rounded-full border border-slate-200 bg-white px-3 py-1 text-xs text-slate-600"
            }
          >
            {c}
          </button>
        ))}
      </div>

      {loading ? (
        <Card>Loading...</Card>
      ) : (
        <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-3">
          {issues.map((issue) => (
            <Card key={issue.id}>
              <div className="flex items-start justify-between gap-2">
                <span className="text-sm font-semibold text-slate-900">
                  {issue.title}
                </span>
                <Badge tone="blue">{issue.category}</Badge>
              </div>
              <div className="mt-1 text-xs text-slate-500">
                {issue.area || "Constituency"} · {issue.report_count} reports
              </div>
              <div className="mt-2">
                <Badge tone="gray">Status: {issue.status}</Badge>
              </div>
              {issue.public_updates.length > 0 && (
                <div className="mt-3 space-y-1 border-t border-slate-100 pt-2">
                  <div className="text-xs font-semibold text-slate-600">
                    Public updates
                  </div>
                  {issue.public_updates.map((u, i) => (
                    <p key={i} className="text-xs text-slate-500">
                      {u.note}
                    </p>
                  ))}
                </div>
              )}
            </Card>
          ))}
          {!issues.length && <Card>No public issues to show yet.</Card>}
        </div>
      )}
    </div>
  );
}
