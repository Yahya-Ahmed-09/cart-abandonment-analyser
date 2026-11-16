import { useState } from "react";
import { keepPreviousData, useQuery } from "@tanstack/react-query";
import { api } from "../api";
import { useFilters } from "../filters";
import { fmtMoney, fmtNum } from "../format";
import { Card, controlClass, Disclaimer, ErrorBox, Loading, RiskBadge } from "../ui";

const PAGE_SIZE = 25;

export default function AtRisk() {
  const { filters } = useFilters();
  const [bands, setBands] = useState("High");
  const [sort, setSort] = useState("risk");
  const [page, setPage] = useState(0);

  const carts = useQuery({
    queryKey: ["at-risk", filters, bands, sort, page],
    queryFn: () => api.atRisk(filters, bands, sort, PAGE_SIZE, page * PAGE_SIZE),
    placeholderData: keepPreviousData,
  });

  if (carts.error) return <ErrorBox message={carts.error.message} />;
  if (!carts.data) return <Loading />;

  const { total, items } = carts.data;
  const lastPage = Math.max(0, Math.ceil(total / PAGE_SIZE) - 1);

  return (
    <div className="space-y-8">
      <Card
        title={`${fmtNum(total)} carts`}
        right={
          <div className="flex flex-wrap gap-2">
            <select
              aria-label="Risk level"
              value={bands}
              onChange={(e) => { setBands(e.target.value); setPage(0); }}
              className={controlClass}
            >
              <option value="High">High risk</option>
              <option value="High,Medium">High and medium risk</option>
              <option value="Medium">Medium risk</option>
            </select>
            <select
              aria-label="Sort order"
              value={sort}
              onChange={(e) => { setSort(e.target.value); setPage(0); }}
              className={controlClass}
            >
              <option value="risk">Highest risk first</option>
              <option value="value">Highest value first</option>
            </select>
          </div>
        }
      >
        <div className="overflow-x-auto">
          <table className="w-full text-left text-[15px]">
            <thead className="border-b border-line text-muted">
              <tr>
                <th className="py-3 pr-4 font-medium">Risk</th>
                <th className="py-3 pr-4 font-medium">Brand</th>
                <th className="py-3 pr-4 font-medium">Price</th>
                <th className="py-3 pr-4 font-medium">Likely reasons</th>
                <th className="py-3 pr-4 font-medium">Customer</th>
                <th className="py-3 font-medium">Added to cart</th>
              </tr>
            </thead>
            <tbody>
              {items.map((c) => (
                <tr key={c.row_id} className="border-b border-line align-top last:border-b-0">
                  <td className="py-3 pr-4"><RiskBadge band={c.risk_band} /></td>
                  <td className="py-3 pr-4">{c.brand === "unknown" ? "-" : c.brand}</td>
                  <td className="py-3 pr-4">{fmtMoney(c.price)}</td>
                  <td className="py-3 pr-4">
                    <div className="flex flex-wrap gap-1.5">
                      {c.reasons.map((r) => (
                        <span
                          key={r.code}
                          title={r.suggested_action}
                          className="rounded-full bg-ground px-2.5 py-1 text-xs text-ink"
                        >
                          {r.title}
                        </span>
                      ))}
                    </div>
                  </td>
                  <td className="py-3 pr-4">#{c.user_id}</td>
                  <td className="py-3 text-muted">{c.event_time}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="mt-5 flex items-center justify-between text-[15px]">
          <button disabled={page === 0} onClick={() => setPage(page - 1)} className={controlClass}>
            Previous
          </button>
          <span className="text-muted">Page {page + 1} of {lastPage + 1}</span>
          <button disabled={page >= lastPage} onClick={() => setPage(page + 1)} className={controlClass}>
            Next
          </button>
        </div>
      </Card>
      <Disclaimer />
    </div>
  );
}