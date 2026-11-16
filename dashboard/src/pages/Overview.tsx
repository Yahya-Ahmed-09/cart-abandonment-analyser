import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import { CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { api, type Kpis } from "../api";
import { useFilters } from "../filters";
import { fmtMoney, fmtNum, fmtPct } from "../format";
import { MODEL_INFO } from "../modelInfo";
import { Card, Disclaimer, ErrorBox, Loading, ReasonItem } from "../ui";

function RiskRibbon({ k }: { k: Kpis }) {
  const lower = Math.max(0, k.total_carts - k.high_risk_carts - k.medium_risk_carts);
  const segments = [
    { label: "High risk", count: k.high_risk_carts, className: "bg-high text-white" },
    { label: "Medium risk", count: k.medium_risk_carts, className: "bg-mid text-ink" },
    { label: "Lower risk", count: lower, className: "bg-low text-ink" },
  ];
  const summary = segments.map((s) => `${s.label} ${fmtNum(s.count)}`).join(", ");

  return (
    <div>
      <div className="flex h-[72px] gap-[3px] overflow-hidden rounded-2xl" role="img" aria-label={`Carts by risk: ${summary}`}>
        {segments.map((s) => (
          <div
            key={s.label}
            style={{ flexGrow: s.count, flexBasis: 0 }}
            className={`flex min-w-0 flex-col justify-center overflow-hidden px-4 ${s.className}`}
          >
            <span className="truncate text-base font-bold">{s.label}</span>
            <span className="truncate text-sm">{fmtNum(s.count)} carts</span>
          </div>
        ))}
      </div>
      <div className="mt-2 flex gap-[3px] text-sm text-muted">
        {segments.map((s) => (
          <div key={s.label} style={{ flexGrow: s.count, flexBasis: 0 }} className="min-w-0 truncate">
            {fmtPct(k.total_carts ? s.count / k.total_carts : 0)} of carts
          </div>
        ))}
      </div>
    </div>
  );
}

export default function Overview() {
  const { filters } = useFilters();
  const kpis = useQuery({ queryKey: ["kpis", filters], queryFn: () => api.kpis(filters) });
  const trends = useQuery({ queryKey: ["trends", filters], queryFn: () => api.trends(filters) });
  const reasons = useQuery({
    queryKey: ["reasons", filters, "High"],
    queryFn: () => api.reasons(filters, "High"),
  });

  const err = kpis.error ?? trends.error ?? reasons.error;
  if (err) return <ErrorBox message={err.message} />;
  if (!kpis.data || !trends.data || !reasons.data) return <Loading />;

  const k = kpis.data;

  return (
    <div className="space-y-12">
      <section>
        <h2 className="max-w-3xl text-4xl font-bold leading-[1.1] tracking-tight md:text-[44px]">
          {k.high_risk_carts > 0
            ? `${fmtNum(k.high_risk_carts)} carts are likely to be lost.`
            : "No high-risk carts for this selection."}
        </h2>
        <p className="mt-3 max-w-2xl text-[17px] leading-relaxed text-muted">
          Of {fmtNum(k.total_carts)} carts, {fmtPct(k.abandonment_rate)} were not bought within 7 days.
          About {fmtMoney(k.high_risk_value)} of cart value sits in high-risk carts.
        </p>
        <div className="mt-10">
          <RiskRibbon k={k} />
          <p className="mt-4 max-w-2xl text-[15px] leading-relaxed text-muted">
            In testing, {MODEL_INFO.bands[0].abandoned}% of carts the model called high risk were really abandoned,
            against {MODEL_INFO.bands[2].abandoned}% of lower-risk carts.{" "}
            <Link to="/model" className="font-medium text-plum underline">
              See model results
            </Link>
          </p>
        </div>
      </section>

      <section>
        <h2 className="text-2xl font-bold tracking-tight">Why high-risk carts get abandoned</h2>
        <p className="mb-5 mt-1 text-[15px] text-muted">Most common first.</p>
        <div className="rounded-2xl bg-white px-6">
          {reasons.data.slice(0, 5).map((r) => (
            <ReasonItem key={r.code} reason={r} />
          ))}
          {reasons.data.length === 0 && <p className="py-6 text-muted">No reasons to show for this selection.</p>}
        </div>
      </section>

      <Card title="Abandonment rate by day">
        <div className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={trends.data} margin={{ top: 8, right: 8, bottom: 0, left: 0 }}>
              <CartesianGrid stroke="#E4E0EC" vertical={false} />
              <XAxis dataKey="date" tick={{ fontSize: 12, fill: "#4A4560" }} tickLine={false} axisLine={{ stroke: "#E4E0EC" }} />
              <YAxis
                tickFormatter={(v) => `${Math.round(Number(v) * 100)}%`}
                domain={["auto", "auto"]}
                tick={{ fontSize: 12, fill: "#4A4560" }}
                tickLine={false}
                axisLine={false}
              />
              <Tooltip formatter={(value) => fmtPct(Number(value))} />
              <Line type="monotone" dataKey="abandonment_rate" name="Abandonment rate" stroke="#7A2E65" strokeWidth={2.5} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </Card>

      <Disclaimer />
    </div>
  );
}