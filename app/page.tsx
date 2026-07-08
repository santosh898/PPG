import Link from "next/link";
import {
  BarChart3,
  CheckCircle2,
  ClipboardList,
  Globe,
  Languages,
  MapPinned,
  MessageCircleMore,
  Route,
  ShieldCheck,
  Sparkles,
} from "lucide-react";

const steps = [
  {
    icon: MessageCircleMore,
    title: "Describe it, your way",
    desc: "Citizens report an issue in a natural conversation, in English, Telugu or Hindi \u2014 no forms, no jargon.",
  },
  {
    icon: Sparkles,
    title: "AI organizes the evidence",
    desc: "Similar reports are clustered, ranked by urgency and reach, and mapped \u2014 turning scattered complaints into constituency-wide signal.",
  },
  {
    icon: BarChart3,
    title: "MPs plan with confidence",
    desc: "MPs and staff see evidence-backed priorities, ask questions in plain language, and act \u2014 while citizens get guidance to the right scheme or channel.",
  },
];

const citizenFeatures = [
  { icon: Languages, text: "Report conversationally in your own language" },
  { icon: ClipboardList, text: "Get an instant tracking ID to follow up" },
  { icon: Route, text: "Immediate guidance to relevant schemes and official channels" },
];

const officialFeatures = [
  { icon: BarChart3, text: "Ranked, evidence-backed development priorities" },
  { icon: Sparkles, text: "Ask questions in plain language, get cited answers" },
  { icon: MapPinned, text: "Hotspot maps and one-click weekly reports" },
  { icon: ClipboardList, text: "Staff console to verify, cluster and publish updates" },
];

export default function HomePage() {
  return (
    <div className="space-y-16 pb-8">
      {/* Hero */}
      <section className="pt-6 text-center">
        <div className="mx-auto inline-flex items-center gap-1.5 rounded-full bg-brand-50 px-3 py-1 text-xs font-semibold uppercase tracking-wide text-brand-700">
          <Sparkles className="h-3.5 w-3.5" />
          AI-powered constituency intelligence
        </div>
        <h1 className="mx-auto mt-4 max-w-3xl text-4xl font-bold tracking-tight text-slate-900 sm:text-5xl">
          From individual complaints to{" "}
          <span className="text-brand-600">constituency-wide priorities</span>
        </h1>
        <p className="mx-auto mt-4 max-w-2xl text-base text-slate-600 sm:text-lg">
          Citizens report issues through conversation. AI organizes, ranks and
          maps them into evidence-backed insights &mdash; so MPs can plan
          better, decide faster, and citizens get immediate guidance to the
          right government schemes and official channels.
        </p>
        <div className="mt-8 flex flex-wrap items-center justify-center gap-3">
          <Link
            href="/citizen"
            className="inline-flex items-center gap-2 rounded-lg bg-emerald-600 px-5 py-3 text-sm font-semibold text-white shadow-soft transition hover:bg-emerald-700"
          >
            <MessageCircleMore className="h-4 w-4" />
            Report an Issue
          </Link>
          <Link
            href="/mp/dashboard"
            className="inline-flex items-center gap-2 rounded-lg border border-slate-300 bg-white px-5 py-3 text-sm font-semibold text-slate-700 transition hover:border-brand-300 hover:text-brand-700"
          >
            <BarChart3 className="h-4 w-4" />
            View MP Dashboard
          </Link>
        </div>
        <p className="mt-4 text-xs text-slate-400">
          Does not replace official grievance systems &mdash; a listening,
          prioritization and guidance layer alongside them.
        </p>
      </section>

      {/* How it works */}
      <section>
        <div className="mb-6 text-center">
          <h2 className="text-xl font-bold text-slate-900">How it works</h2>
          <p className="mt-1 text-sm text-slate-500">
            One conversation, two outcomes: citizens get guidance, MPs get a plan.
          </p>
        </div>
        <div className="grid gap-4 md:grid-cols-3">
          {steps.map((s, i) => (
            <div
              key={s.title}
              className="relative rounded-2xl border border-slate-200 bg-white p-6 shadow-soft"
            >
              <span className="absolute -top-3 -left-1 grid h-7 w-7 place-items-center rounded-full bg-slate-900 text-xs font-bold text-white">
                {i + 1}
              </span>
              <span className="grid h-11 w-11 place-items-center rounded-xl bg-brand-100 text-brand-700">
                <s.icon className="h-5 w-5" />
              </span>
              <h3 className="mt-4 text-base font-semibold text-slate-900">
                {s.title}
              </h3>
              <p className="mt-1.5 text-sm text-slate-500">{s.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Persona split */}
      <section className="grid gap-5 lg:grid-cols-2">
        <div className="flex flex-col rounded-2xl border border-emerald-200 bg-emerald-50/60 p-6">
          <span className="inline-flex w-fit items-center gap-1.5 rounded-full bg-emerald-100 px-2.5 py-1 text-xs font-semibold uppercase tracking-wide text-emerald-700">
            For Citizens
          </span>
          <h3 className="mt-3 text-xl font-bold text-slate-900">
            Say it once. Get heard, get guided.
          </h3>
          <p className="mt-1 text-sm text-slate-600">
            No forms, no queues &mdash; just describe your issue and we take
            it from there.
          </p>
          <ul className="mt-4 flex-1 space-y-3">
            {citizenFeatures.map((f) => (
              <li key={f.text} className="flex items-start gap-2.5 text-sm text-slate-700">
                <f.icon className="mt-0.5 h-4 w-4 shrink-0 text-emerald-600" />
                {f.text}
              </li>
            ))}
          </ul>
          <Link
            href="/citizen"
            className="mt-5 inline-flex w-fit items-center gap-2 rounded-lg bg-emerald-600 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-emerald-700"
          >
            Start reporting &rarr;
          </Link>
        </div>

        <div className="flex flex-col rounded-2xl border border-brand-200 bg-brand-50/60 p-6">
          <span className="inline-flex w-fit items-center gap-1.5 rounded-full bg-brand-100 px-2.5 py-1 text-xs font-semibold uppercase tracking-wide text-brand-700">
            For MPs &amp; Staff
          </span>
          <h3 className="mt-3 text-xl font-bold text-slate-900">
            Move from reacting to planning.
          </h3>
          <p className="mt-1 text-sm text-slate-600">
            See what your constituency actually needs, backed by evidence,
            not anecdotes.
          </p>
          <ul className="mt-4 flex-1 space-y-3">
            {officialFeatures.map((f) => (
              <li key={f.text} className="flex items-start gap-2.5 text-sm text-slate-700">
                <f.icon className="mt-0.5 h-4 w-4 shrink-0 text-brand-600" />
                {f.text}
              </li>
            ))}
          </ul>
          <div className="mt-5 flex flex-wrap items-center gap-4">
            <Link
              href="/mp/dashboard"
              className="inline-flex items-center gap-2 rounded-lg bg-brand-600 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-brand-700"
            >
              Open dashboard &rarr;
            </Link>
            <Link
              href="/staff"
              className="text-sm font-medium text-brand-700 hover:underline"
            >
              Staff console
            </Link>
          </div>
        </div>
      </section>

      {/* Trust & transparency */}
      <section className="rounded-2xl border border-slate-200 bg-white p-6 sm:p-8">
        <div className="grid gap-6 sm:grid-cols-3">
          <div className="flex items-start gap-3">
            <span className="grid h-10 w-10 shrink-0 place-items-center rounded-xl bg-slate-100 text-slate-600">
              <ShieldCheck className="h-5 w-5" />
            </span>
            <div>
              <div className="text-sm font-semibold text-slate-900">
                A layer, not a replacement
              </div>
              <p className="mt-1 text-sm text-slate-500">
                People&apos;s Priorities does not replace official grievance
                systems. It listens, prioritizes and guides &mdash; alongside
                them.
              </p>
            </div>
          </div>
          <div className="flex items-start gap-3">
            <span className="grid h-10 w-10 shrink-0 place-items-center rounded-xl bg-slate-100 text-slate-600">
              <CheckCircle2 className="h-5 w-5" />
            </span>
            <div>
              <div className="text-sm font-semibold text-slate-900">
                Evidence-backed, not black-box
              </div>
              <p className="mt-1 text-sm text-slate-500">
                Every MP Chat answer shows its confidence and the underlying
                data sources it used.
              </p>
            </div>
          </div>
          <div className="flex items-start gap-3">
            <span className="grid h-10 w-10 shrink-0 place-items-center rounded-xl bg-slate-100 text-slate-600">
              <Globe className="h-5 w-5" />
            </span>
            <div>
              <div className="text-sm font-semibold text-slate-900">
                Publicly transparent
              </div>
              <p className="mt-1 text-sm text-slate-500">
                Anonymized issue clusters and status updates are visible to
                everyone &mdash;{" "}
                <Link href="/public/issues" className="font-medium text-brand-600 hover:underline">
                  see the public tracker
                </Link>
                .
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer strip */}
      <footer className="flex flex-wrap items-center justify-between gap-3 border-t border-slate-200 pt-6 text-xs text-slate-400">
        <span>People&apos;s Priorities &mdash; a listening, prioritization and guidance layer for constituencies.</span>
        <div className="flex gap-4">
          <Link href="/public/issues" className="hover:text-slate-600">
            Public Issues
          </Link>
          <Link href="/staff" className="hover:text-slate-600">
            Staff Console
          </Link>
        </div>
      </footer>
    </div>
  );
}
