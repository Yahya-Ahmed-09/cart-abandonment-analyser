import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { api } from "../api";
import { useFilters } from "../filters";
import { controlClass, Disclaimer, ErrorBox, Loading, ReasonItem } from "../ui";

export default function Reasons() {
  const { filters } = useFilters();
  const [bands, setBands] = useState("High,Medium");
  const reasons = useQuery({
    queryKey: ["reasons", filters, bands],
    queryFn: () => api.reasons(filters, bands),
  });

  if (reasons.error) return <ErrorBox message={reasons.error.message} />;
  if (!reasons.data) return <Loading />;

  return (
    <div className="space-y-8">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Why carts are likely to be abandoned</h2>
          <p className="mt-2 text-[15px] text-muted">Share of at-risk carts by main reason, most common first.</p>
        </div>
        <select
          aria-label="Risk level"
          value={bands}
          onChange={(e) => setBands(e.target.value)}
          className={controlClass}
        >
          <option value="High">High-risk carts only</option>
          <option value="High,Medium">High and medium risk</option>
        </select>
      </div>

      <div className="rounded-2xl bg-white px-6">
        {reasons.data.map((r) => (
          <ReasonItem key={r.code} reason={r} showTotals />
        ))}
        {reasons.data.length === 0 && <p className="py-6 text-muted">No reasons to show for this selection.</p>}
      </div>

      <Disclaimer />
    </div>
  );
}