import { Badge } from "./ui";

/**
 * Section 24.3 - AI trust rules. Surfaces confidence, data used, verification
 * and limitations wherever the platform shows an AI-derived answer.
 */
export function TrustBadges({
  confidence,
  dataUsed,
  limitations,
}: {
  confidence?: "high" | "medium" | "low";
  dataUsed?: string[];
  limitations?: string[];
}) {
  const tone =
    confidence === "high" ? "green" : confidence === "medium" ? "amber" : "red";
  return (
    <div className="mt-3 space-y-2 border-t border-slate-100 pt-3 text-xs text-slate-500">
      <div className="flex flex-wrap items-center gap-2">
        {confidence && (
          <Badge tone={tone}>Confidence: {confidence}</Badge>
        )}
        {dataUsed && dataUsed.length > 0 && (
          <Badge tone="blue">Data used: {dataUsed.length} source(s)</Badge>
        )}
      </div>
      {limitations && limitations.length > 0 && (
        <ul className="list-inside list-disc space-y-0.5">
          {limitations.map((l, i) => (
            <li key={i}>{l}</li>
          ))}
        </ul>
      )}
    </div>
  );
}

export function VerificationBadge({ status }: { status: string }) {
  const map: Record<string, { tone: string; label: string }> = {
    staff_verified: { tone: "green", label: "Staff verified" },
    unverified: { tone: "amber", label: "Unverified (AI-grouped)" },
    disputed: { tone: "red", label: "Disputed" },
  };
  const v = map[status] || map.unverified;
  return <Badge tone={v.tone}>{v.label}</Badge>;
}
