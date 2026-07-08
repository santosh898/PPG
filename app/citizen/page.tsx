"use client";

import { useRef, useState } from "react";
import { MessageCircleMore } from "lucide-react";
import { Badge, Button, Card, PageHeader } from "@/components/ui";

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

interface GuidanceItem {
  type: string;
  name: string;
  reason: string;
  url: string | null;
  confidence: number;
}

interface ApiResult {
  conversation_id: string;
  reply: string;
  submission?: {
    tracking_id: string;
    cluster_title: string;
    cluster_action: string;
    needs_review: boolean;
  };
  guidance?: GuidanceItem[];
  guidance_disclaimer?: string;
}

export default function CitizenPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      role: "assistant",
      content:
        "Namaste. Please describe your issue in your own language (English, Telugu or Hindi). For example: water, road, drainage, streetlight, pension, health or school problems.",
    },
  ]);
  const [input, setInput] = useState("");
  const [language, setLanguage] = useState<string>("");
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ApiResult | null>(null);
  const [location, setLocation] = useState<string>("");
  const endRef = useRef<HTMLDivElement>(null);

  async function send(text: string) {
    if (!text.trim() || loading) return;
    const userMsg: ChatMessage = { role: "user", content: text };
    setMessages((m) => [...m, userMsg]);
    setInput("");
    setLoading(true);
    try {
      const res = await fetch("/api/citizen/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          conversation_id: conversationId,
          message: text,
          language_hint: language || null,
        }),
      });
      const data: ApiResult = await res.json();
      setConversationId(data.conversation_id);
      setResult(data);
      setMessages((m) => [...m, { role: "assistant", content: data.reply }]);
    } catch {
      setMessages((m) => [
        ...m,
        { role: "assistant", content: "Sorry, something went wrong. Please try again." },
      ]);
    } finally {
      setLoading(false);
      setTimeout(() => endRef.current?.scrollIntoView({ behavior: "smooth" }), 50);
    }
  }

  function useLocation() {
    if (!navigator.geolocation) return;
    navigator.geolocation.getCurrentPosition((pos) => {
      const text = `My location coordinates are ${pos.coords.latitude.toFixed(
        4
      )}, ${pos.coords.longitude.toFixed(4)}`;
      send(text);
    });
  }

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_360px]">
      <div className="space-y-4">
        <PageHeader
          icon={MessageCircleMore}
          eyebrow="For citizens"
          title="Report an Issue"
          subtitle="Your issue will be recorded, grouped with similar local issues, and made visible to the MP office. We will also suggest next steps. This does not replace official grievance systems."
          tone="emerald"
        />

        <Card className="flex h-[520px] flex-col p-0">
          <div className="flex-1 space-y-3 overflow-y-auto p-4">
            {messages.map((m, i) => (
              <div
                key={i}
                className={
                  m.role === "user" ? "flex justify-end" : "flex justify-start"
                }
              >
                <div
                  className={
                    m.role === "user"
                      ? "max-w-[80%] whitespace-pre-wrap rounded-2xl rounded-br-sm bg-brand-600 px-3 py-2 text-sm text-white"
                      : "max-w-[85%] whitespace-pre-wrap rounded-2xl rounded-bl-sm bg-slate-100 px-3 py-2 text-sm text-slate-800"
                  }
                >
                  {m.content}
                </div>
              </div>
            ))}
            {loading && (
              <div className="text-xs text-slate-400">Agent is thinking...</div>
            )}
            <div ref={endRef} />
          </div>

          <div className="border-t border-slate-200 p-3">
            <div className="mb-2 flex flex-wrap items-center gap-2">
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
              <Button variant="outline" onClick={useLocation} className="text-xs">
                Share my location
              </Button>
              <input
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                placeholder="or type area / landmark"
                className="flex-1 rounded-md border border-slate-300 px-2 py-1 text-xs"
              />
              <Button
                variant="ghost"
                className="text-xs"
                onClick={() => location.trim() && send(location.trim())}
              >
                Send location
              </Button>
            </div>
            <form
              onSubmit={(e) => {
                e.preventDefault();
                send(input);
              }}
              className="flex gap-2"
            >
              <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Describe your issue..."
                className="flex-1 rounded-lg border border-slate-300 px-3 py-2 text-sm outline-none focus:border-brand-400"
              />
              <Button type="submit" disabled={loading}>
                Send
              </Button>
            </form>
          </div>
        </Card>
      </div>

      <div className="space-y-4">
        {result?.submission && (
          <Card className="border-brand-200 bg-brand-50">
            <div className="text-xs font-medium uppercase text-brand-700">
              Tracking ID
            </div>
            <div className="mt-1 text-2xl font-bold text-brand-800">
              {result.submission.tracking_id}
            </div>
            <p className="mt-2 text-sm text-slate-600">
              {result.submission.cluster_action === "attached_to_existing"
                ? `Added to existing cluster: ${result.submission.cluster_title}`
                : `Started a new cluster: ${result.submission.cluster_title}`}
            </p>
            {result.submission.needs_review && (
              <p className="mt-2 text-xs text-amber-700">
                Sent to MP office staff for review.
              </p>
            )}
          </Card>
        )}

        {result?.guidance && result.guidance.length > 0 && (
          <Card>
            <div className="mb-2 text-sm font-semibold text-slate-900">
              What you can do next
            </div>
            <div className="space-y-3">
              {result.guidance.map((g, i) => (
                <div key={i} className="rounded-lg border border-slate-100 p-2">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-slate-800">
                      {g.name}
                    </span>
                    <Badge tone="blue">{g.type.replace(/_/g, " ")}</Badge>
                  </div>
                  <p className="mt-1 text-xs text-slate-500">{g.reason}</p>
                  {g.url && (
                    <a
                      href={g.url}
                      target="_blank"
                      rel="noreferrer"
                      className="mt-1 inline-block text-xs font-medium text-brand-600"
                    >
                      Official link &rarr;
                    </a>
                  )}
                </div>
              ))}
            </div>
            {result.guidance_disclaimer && (
              <p className="mt-3 border-t border-slate-100 pt-2 text-xs text-slate-400">
                {result.guidance_disclaimer}
              </p>
            )}
          </Card>
        )}

        <Card className="bg-slate-50">
          <div className="text-xs font-semibold text-slate-600">
            Try these examples
          </div>
          <div className="mt-2 space-y-1">
            {[
              "Water has not come in our colony for five days near the old school",
              "Drainage water is overflowing near the temple in Ward 8",
              "My old age pension has not come for two months",
            ].map((ex) => (
              <button
                key={ex}
                onClick={() => send(ex)}
                className="block w-full rounded-md bg-white px-2 py-1.5 text-left text-xs text-slate-600 hover:bg-brand-50"
              >
                {ex}
              </button>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
}
