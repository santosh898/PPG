"use client";

import { useRef, useState } from "react";
import { Badge, Button, Card, urgencyTone } from "@/components/ui";
import { TrustBadges } from "@/components/TrustBadges";

interface Priority {
  rank: number;
  cluster_id: string;
  title: string;
  submission_count: number;
  urgency: string;
  trend: string;
  priority_score: number;
  location: string;
}

interface Scene {
  scene_type: string;
  [key: string]: unknown;
}

interface Turn {
  role: "user" | "assistant";
  content: string;
  confidence?: "high" | "medium" | "low";
  dataUsed?: string[];
  limitations?: string[];
  scenes?: Scene[];
}

const SUGGESTED = [
  "What are the top issues this week?",
  "Why is water shortage ranked first?",
  "What is happening in Ward 8?",
  "Show me the map of water issues",
  "Generate a report for tomorrow's review",
];

export default function MpChatPage() {
  const [turns, setTurns] = useState<Turn[]>([
    {
      role: "assistant",
      content:
        "Ask me about constituency priorities, specific areas, trends, or request a report. I answer from recorded issue data and show my confidence and sources.",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const endRef = useRef<HTMLDivElement>(null);

  async function ask(text: string) {
    if (!text.trim() || loading) return;
    setTurns((t) => [...t, { role: "user", content: text }]);
    setInput("");
    setLoading(true);
    try {
      const res = await fetch("/api/mp/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          conversation_id: conversationId,
          message: text,
          filters: { area_id: "CONST_001" },
        }),
      });
      const data = await res.json();
      setConversationId(data.conversation_id);
      setTurns((t) => [
        ...t,
        {
          role: "assistant",
          content: data.answer,
          confidence: data.confidence,
          dataUsed: data.data_used,
          limitations: data.limitations,
          scenes: data.scenes,
        },
      ]);
    } catch {
      setTurns((t) => [
        ...t,
        { role: "assistant", content: "Something went wrong. Please try again." },
      ]);
    } finally {
      setLoading(false);
      setTimeout(() => endRef.current?.scrollIntoView({ behavior: "smooth" }), 50);
    }
  }

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_300px]">
      <div className="space-y-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">
            MP Chat Intelligence
          </h1>
          <p className="text-sm text-slate-500">
            Evidence-backed answers over the constituency knowledge base.
          </p>
        </div>

        <div className="space-y-4">
          {turns.map((t, i) => (
            <div key={i}>
              {t.role === "user" ? (
                <div className="flex justify-end">
                  <div className="max-w-[80%] rounded-2xl rounded-br-sm bg-brand-600 px-3 py-2 text-sm text-white">
                    {t.content}
                  </div>
                </div>
              ) : (
                <Card>
                  <div className="whitespace-pre-wrap text-sm text-slate-800">
                    {t.content}
                  </div>
                  {t.scenes?.map((s, si) => (
                    <SceneCard key={si} scene={s} />
                  ))}
                  {(t.confidence || t.limitations) && (
                    <TrustBadges
                      confidence={t.confidence}
                      dataUsed={t.dataUsed}
                      limitations={t.limitations}
                    />
                  )}
                </Card>
              )}
            </div>
          ))}
          {loading && <div className="text-xs text-slate-400">Thinking...</div>}
          <div ref={endRef} />
        </div>

        <form
          onSubmit={(e) => {
            e.preventDefault();
            ask(input);
          }}
          className="flex gap-2"
        >
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about priorities, areas, trends, or reports..."
            className="flex-1 rounded-lg border border-slate-300 px-3 py-2 text-sm outline-none focus:border-brand-400"
          />
          <Button type="submit" disabled={loading}>
            Ask
          </Button>
        </form>
      </div>

      <div>
        <Card className="bg-slate-50">
          <div className="text-xs font-semibold text-slate-600">
            Suggested questions
          </div>
          <div className="mt-2 space-y-1">
            {SUGGESTED.map((q) => (
              <button
                key={q}
                onClick={() => ask(q)}
                className="block w-full rounded-md bg-white px-2 py-1.5 text-left text-xs text-slate-600 hover:bg-brand-50"
              >
                {q}
              </button>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
}

function SceneCard({ scene }: { scene: Scene }) {
  if (scene.scene_type === "priority_scene") {
    const priorities = (scene.priorities as Priority[]) || [];
    if (!priorities.length) return null;
    return (
      <div className="mt-3 space-y-2">
        {priorities.map((p) => (
          <div
            key={p.cluster_id}
            className="flex items-center justify-between rounded-lg border border-slate-100 bg-slate-50 px-3 py-2"
          >
            <div>
              <span className="text-sm font-medium text-slate-800">
                {p.rank}. {p.title}
              </span>
              <div className="text-xs text-slate-500">
                {p.submission_count} submissions · {p.location} · {p.trend}
              </div>
            </div>
            <div className="flex items-center gap-1">
              <Badge tone={urgencyTone(p.urgency)}>{p.urgency}</Badge>
              <Badge tone="purple">{p.priority_score}</Badge>
            </div>
          </div>
        ))}
      </div>
    );
  }

  if (scene.scene_type === "issue_scene") {
    const metrics = scene.metrics as {
      submissions: number;
      unique_citizens: number;
      photos: number;
      priority_score: number;
    };
    return (
      <div className="mt-3 rounded-lg border border-slate-100 bg-slate-50 p-3 text-xs text-slate-600">
        <div className="font-medium text-slate-800">{String(scene.title)}</div>
        <div className="mt-1 flex flex-wrap gap-2">
          <span>{metrics.submissions} submissions</span>
          <span>· {metrics.unique_citizens} unique citizens</span>
          <span>· {metrics.photos} photos</span>
          <span>· score {metrics.priority_score}</span>
        </div>
      </div>
    );
  }

  if (scene.scene_type === "report_scene") {
    const sections = (scene.sections as { heading: string; content: string }[]) || [];
    return (
      <div className="mt-3 rounded-lg border border-brand-100 bg-brand-50 p-3">
        <div className="text-sm font-semibold text-brand-800">
          {String(scene.title)}
        </div>
        <div className="mt-2 space-y-2">
          {sections.map((s, i) => (
            <div key={i}>
              <div className="text-xs font-semibold text-slate-700">
                {s.heading}
              </div>
              <div className="whitespace-pre-wrap text-xs text-slate-600">
                {s.content}
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (scene.scene_type === "map_scene") {
    const points = (scene.points as unknown[]) || [];
    return (
      <div className="mt-3 text-xs text-slate-500">
        Map scene ready with {points.length} hotspot points. See the MP Dashboard
        for the full heatmap.
      </div>
    );
  }

  return null;
}
