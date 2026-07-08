"use client";

import { useCallback, useEffect, useState } from "react";
import { ClipboardList } from "lucide-react";
import { Badge, Button, Card, PageHeader, urgencyTone } from "@/components/ui";
import { CATEGORIES, CLUSTER_STATUS } from "@/lib/constants";

interface SubmissionRow {
  id: string;
  tracking_id: string;
  summary: string;
  category: string;
  urgency: string;
  status: string;
  source: string;
  needs_review: boolean;
  review_reason: string | null;
  sensitive_flags: string[];
  location: string | null;
  cluster_id: string | null;
  created_at: string;
}

interface ClusterRow {
  id: string;
  title: string;
  category: string;
  submission_count: number;
  unique_citizen_count: number;
  priority_score: number;
  urgency: string;
  status: string;
  verification_status: string;
  locations: string[];
}

type Tab = "entry" | "submissions" | "review" | "clusters";

export default function StaffPage() {
  const [tab, setTab] = useState<Tab>("entry");

  return (
    <div className="space-y-4">
      <PageHeader
        icon={ClipboardList}
        eyebrow="Internal tool"
        title="Staff Console"
        subtitle="Enter offline complaints, review AI-extracted fields, and manage issue clusters and reports."
      />

      <div className="flex flex-wrap gap-2">
        {(
          [
            ["entry", "Manual Entry"],
            ["submissions", "Submissions"],
            ["review", "Review Queue"],
            ["clusters", "Clusters"],
          ] as [Tab, string][]
        ).map(([id, label]) => (
          <button
            key={id}
            onClick={() => setTab(id)}
            className={
              tab === id
                ? "rounded-lg bg-brand-600 px-3 py-1.5 text-sm font-medium text-white"
                : "rounded-lg border border-slate-200 bg-white px-3 py-1.5 text-sm text-slate-600 hover:bg-slate-50"
            }
          >
            {label}
          </button>
        ))}
      </div>

      {tab === "entry" && <ManualEntry />}
      {tab === "submissions" && <SubmissionsTable />}
      {tab === "review" && <ReviewQueue />}
      {tab === "clusters" && <ClustersTable />}
    </div>
  );
}

function ManualEntry() {
  const [text, setText] = useState("");
  const [language, setLanguage] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<Record<string, unknown> | null>(null);

  async function submit() {
    if (!text.trim()) return;
    setLoading(true);
    setResult(null);
    try {
      const res = await fetch("/api/submissions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          source: "staff_entry",
          original_text: text,
          language_hint: language || null,
        }),
      });
      setResult(await res.json());
    } finally {
      setLoading(false);
    }
  }

  const parsed = result?.parsed as
    | { category: string; summary: string; secondary_category: string; urgency: string }
    | undefined;

  return (
    <div className="grid gap-4 lg:grid-cols-2">
      <Card>
        <div className="mb-2 text-sm font-semibold text-slate-900">
          New complaint from call / WhatsApp / meeting note
        </div>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          rows={6}
          placeholder='e.g. "Caller from Ward 8 says drainage water has been overflowing near temple for 3 days."'
          className="w-full rounded-lg border border-slate-300 p-2 text-sm outline-none focus:border-brand-400"
        />
        <div className="mt-2 flex items-center gap-2">
          <select
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            className="rounded-md border border-slate-300 px-2 py-1 text-xs"
          >
            <option value="">Auto language</option>
            <option value="English">English</option>
            <option value="Telugu">Telugu</option>
            <option value="Hindi">Hindi</option>
          </select>
          <Button onClick={submit} disabled={loading}>
            {loading ? "Structuring..." : "Structure & Save"}
          </Button>
        </div>
      </Card>

      <Card>
        <div className="mb-2 text-sm font-semibold text-slate-900">
          AI-extracted result
        </div>
        {!result && (
          <p className="text-sm text-slate-400">
            The structured fields, tracking ID and suggested cluster will appear
            here.
          </p>
        )}
        {parsed && (
          <div className="space-y-2 text-sm">
            <Row label="Tracking ID" value={String(result?.tracking_id)} />
            <Row label="Category" value={parsed.category} />
            <Row label="Secondary" value={parsed.secondary_category} />
            <Row label="Urgency" value={parsed.urgency} />
            <Row label="Summary" value={parsed.summary} />
            <Row label="Cluster" value={String(result?.cluster_title)} />
            <Row
              label="Cluster action"
              value={String(result?.cluster_action)}
            />
            {Boolean(result?.needs_review) && (
              <Badge tone="amber">Flagged for review</Badge>
            )}
          </div>
        )}
      </Card>
    </div>
  );
}

function Row({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex gap-2">
      <span className="w-28 shrink-0 text-slate-500">{label}</span>
      <span className="text-slate-800">{value}</span>
    </div>
  );
}

function SubmissionsTable() {
  const [rows, setRows] = useState<SubmissionRow[]>([]);
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    setLoading(true);
    const res = await fetch("/api/submissions");
    const data = await res.json();
    setRows(data.submissions || []);
    setLoading(false);
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  if (loading) return <Card>Loading submissions...</Card>;

  return (
    <Card className="overflow-x-auto p-0">
      <table className="w-full text-sm">
        <thead className="bg-slate-50 text-left text-xs uppercase text-slate-500">
          <tr>
            <th className="px-3 py-2">Tracking</th>
            <th className="px-3 py-2">Summary</th>
            <th className="px-3 py-2">Category</th>
            <th className="px-3 py-2">Urgency</th>
            <th className="px-3 py-2">Location</th>
            <th className="px-3 py-2">Status</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r) => (
            <tr key={r.id} className="border-t border-slate-100">
              <td className="px-3 py-2 font-mono text-xs">{r.tracking_id}</td>
              <td className="max-w-xs truncate px-3 py-2">{r.summary}</td>
              <td className="px-3 py-2">
                <Badge tone="blue">{r.category}</Badge>
              </td>
              <td className="px-3 py-2">
                <Badge tone={urgencyTone(r.urgency)}>{r.urgency}</Badge>
              </td>
              <td className="px-3 py-2">{r.location || "-"}</td>
              <td className="px-3 py-2">
                {r.needs_review ? (
                  <Badge tone="amber">review</Badge>
                ) : (
                  <span className="text-xs text-slate-500">{r.status}</span>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className="p-2 text-xs text-slate-400">{rows.length} submissions</div>
    </Card>
  );
}

function ReviewQueue() {
  const [items, setItems] = useState<
    Array<{
      id: string;
      tracking_id: string;
      summary: string;
      category: string;
      urgency: string;
      reason: string;
      sensitive_flags: string[];
      location: string | null;
    }>
  >([]);
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    setLoading(true);
    const res = await fetch("/api/staff/review-queue");
    const data = await res.json();
    setItems(data.items || []);
    setLoading(false);
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  async function clearReview(id: string, category: string, location: string | null) {
    await fetch(`/api/staff/submissions/${id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ clear_review: true, category, location_text: location }),
    });
    load();
  }

  if (loading) return <Card>Loading review queue...</Card>;
  if (!items.length)
    return <Card>No submissions currently need review.</Card>;

  return (
    <div className="space-y-3">
      {items.map((it) => (
        <Card key={it.id}>
          <div className="flex items-start justify-between gap-4">
            <div>
              <div className="flex items-center gap-2">
                <span className="font-mono text-xs text-slate-500">
                  {it.tracking_id}
                </span>
                <Badge tone="blue">{it.category}</Badge>
                <Badge tone={urgencyTone(it.urgency)}>{it.urgency}</Badge>
                <Badge tone="red">{it.reason.replace(/_/g, " ")}</Badge>
              </div>
              <p className="mt-1 text-sm text-slate-800">{it.summary}</p>
              {it.sensitive_flags.length > 0 && (
                <p className="mt-1 text-xs text-red-600">
                  Sensitive: {it.sensitive_flags.join(", ")}
                </p>
              )}
            </div>
            <Button
              variant="outline"
              onClick={() => clearReview(it.id, it.category, it.location)}
            >
              Approve
            </Button>
          </div>
        </Card>
      ))}
    </div>
  );
}

function ClustersTable() {
  const [rows, setRows] = useState<ClusterRow[]>([]);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState<string | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    const res = await fetch("/api/staff/clusters");
    const data = await res.json();
    setRows(data.clusters || []);
    setLoading(false);
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  async function setStatus(id: string, status: string) {
    setBusy(id);
    await fetch(`/api/staff/clusters/${id}/status`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status, note: `Status set to ${status} by staff.` }),
    });
    await load();
    setBusy(null);
  }

  async function publish(id: string) {
    const message = window.prompt(
      "Public update message (anonymized, no personal data):",
      "This issue has been forwarded to the relevant department for review."
    );
    if (!message) return;
    setBusy(id);
    await fetch(`/api/staff/clusters/${id}/publish`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });
    setBusy(null);
    alert("Public update published.");
  }

  if (loading) return <Card>Loading clusters...</Card>;

  return (
    <div className="space-y-3">
      {rows.map((c) => (
        <Card key={c.id}>
          <div className="flex flex-wrap items-start justify-between gap-3">
            <div>
              <div className="flex items-center gap-2">
                <span className="font-semibold text-slate-900">{c.title}</span>
                <Badge tone="blue">{c.category}</Badge>
                <Badge tone={urgencyTone(c.urgency)}>{c.urgency}</Badge>
                <Badge tone="purple">score {c.priority_score}</Badge>
              </div>
              <p className="mt-1 text-xs text-slate-500">
                {c.submission_count} submissions · {c.unique_citizen_count} unique
                citizens · {c.locations.join(", ") || "no location"} ·{" "}
                {c.verification_status.replace(/_/g, " ")} · status: {c.status}
              </p>
            </div>
            <div className="flex flex-wrap gap-1">
              <select
                defaultValue={c.status}
                disabled={busy === c.id}
                onChange={(e) => setStatus(c.id, e.target.value)}
                className="rounded-md border border-slate-300 px-2 py-1 text-xs"
              >
                {CLUSTER_STATUS.map((s) => (
                  <option key={s} value={s}>
                    {s}
                  </option>
                ))}
              </select>
              <Button
                variant="outline"
                className="text-xs"
                onClick={() => publish(c.id)}
              >
                Publish update
              </Button>
            </div>
          </div>
        </Card>
      ))}
      <p className="text-xs text-slate-400">
        Categories tracked: {CATEGORIES.join(", ")}
      </p>
    </div>
  );
}
