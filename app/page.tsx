import Link from "next/link";

const surfaces = [
  {
    href: "/citizen",
    title: "Citizen Chat",
    desc: "Report a local issue conversationally in your own language and get immediate guidance plus a tracking ID.",
  },
  {
    href: "/staff",
    title: "Staff Console",
    desc: "Enter offline complaints, review AI-extracted fields, manage clusters, update status and generate reports.",
  },
  {
    href: "/mp/chat",
    title: "MP Chat Intelligence",
    desc: "Ask natural questions over the constituency knowledge base and get evidence-backed answers.",
  },
  {
    href: "/mp/dashboard",
    title: "MP Dashboard",
    desc: "Visual overview: top priorities, hotspots, category breakdown, rising issues and reports.",
  },
  {
    href: "/public/issues",
    title: "Public Issues",
    desc: "Anonymized issue clusters and public status updates. No personal data.",
  },
];

export default function HomePage() {
  return (
    <div className="space-y-8">
      <section className="rounded-2xl bg-gradient-to-br from-brand-700 to-brand-500 p-8 text-white">
        <h1 className="text-3xl font-bold">People&apos;s Priorities</h1>
        <p className="mt-2 max-w-2xl text-brand-50">
          A conversational constituency intelligence platform that turns
          scattered citizen complaints into ranked, evidence-backed development
          priorities, while guiding citizens to relevant schemes, services and
          complaint channels.
        </p>
        <p className="mt-4 max-w-2xl text-sm text-brand-100">
          This platform does not replace official grievance systems. It acts as
          a listening, prioritization, guidance and planning layer.
        </p>
      </section>

      <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {surfaces.map((s) => (
          <Link
            key={s.href}
            href={s.href}
            className="rounded-xl border border-slate-200 bg-white p-5 transition hover:border-brand-300 hover:shadow-sm"
          >
            <h2 className="text-lg font-semibold text-slate-900">{s.title}</h2>
            <p className="mt-2 text-sm text-slate-600">{s.desc}</p>
            <span className="mt-4 inline-block text-sm font-medium text-brand-600">
              Open &rarr;
            </span>
          </Link>
        ))}
      </section>
    </div>
  );
}
