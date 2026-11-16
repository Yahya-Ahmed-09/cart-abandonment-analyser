import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { api } from "../api";
import { useFilters } from "../filters";
import { fmtMoney, fmtNum, fmtPct } from "../format";
import { Card, Disclaimer, ErrorBox, Loading } from "../ui";

type Dimension = "brands" | "categories";

export default function Brands() {
  const { filters } = useFilters();
  const [dim, setDim] = useState<Dimension>("brands");
  const rows = useQuery({
    queryKey: ["breakdown", dim, filters],
    queryFn: () => (dim === "brands" ? api.brands(filters) : api.categories(filters)),
  });

  const tab = (value: Dimension, label: string) => (
    <button
      onClick={() => setDim(value)}
      aria-pressed={dim === value}
      className={`min-h-11 rounded-full px-4 text-sm font-medium ${
        dim === value ? "bg-ink text-white" : "border border-edge bg-white text-ink hover:border-plum"
      }`}
    >
      {label}
    </button>
  );

  return (
    <div className="space-y-8">
      <Card
        title={dim === "brands" ? "Revenue at risk by brand" : "Revenue at risk by category"}
        right={
          <div className="flex gap-2">
            {tab("brands", "Brands")}
            {tab("categories", "Categories")}
          </div>
        }
      >
        {rows.error ? (
          <ErrorBox message={rows.error.message} />
        ) : !rows.data ? (
          <Loading />
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-[15px]">
              <thead className="border-b border-line text-muted">
                <tr>
                  <th className="py-3 pr-4 font-medium">{dim === "brands" ? "Brand" : "Category"}</th>
                  <th className="py-3 pr-4 font-medium">Carts</th>
                  <th className="py-3 pr-4 font-medium">Abandonment rate</th>
                  <th className="py-3 pr-4 font-medium">High-risk carts</th>
                  <th className="py-3 pr-4 font-medium">Revenue at risk</th>
                  <th className="py-3 font-medium">Main likely reason</th>
                </tr>
              </thead>
              <tbody>
                {rows.data.map((r) => (
                  <tr key={String(r.name)} className="border-b border-line last:border-b-0">
                    <td className="py-3 pr-4 font-bold">{dim === "brands" ? r.name : `Category #${r.name}`}</td>
                    <td className="py-3 pr-4">{fmtNum(r.carts)}</td>
                    <td className="py-3 pr-4">{fmtPct(r.abandonment_rate)}</td>
                    <td className="py-3 pr-4">{fmtNum(r.high_risk_carts)}</td>
                    <td className="py-3 pr-4">{fmtMoney(r.revenue_at_risk)}</td>
                    <td className="py-3">{r.top_reason?.title ?? "-"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>
      <Disclaimer />
    </div>
  );
}