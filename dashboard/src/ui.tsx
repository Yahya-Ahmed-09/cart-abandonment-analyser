import type { ReactNode } from "react";
import type { ReasonRow, RiskBand } from "./api";
import { fmtMoney, fmtNum } from "./format";

// Shared class for pill-shaped inputs, selects and buttons
export const controlClass =
  "min-h-11 rounded-full border border-edge bg-white px-4 text-sm text-ink hover:border-plum disabled:cursor-not-allowed disabled:opacity-40";

export function Card({ title, children, right }: { title: string; children: ReactNode; right?: ReactNode }) {
  return (
    <section className="rounded-2xl bg-white p-6">
      <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
        <h2 className="text-xl font-bold tracking-tight text-ink">{title}</h2>
        {right}
      </div>
      {children}
    </section>
  );
}

export function RiskBadge({ band }: { band: RiskBand }) {
  const styles: Record<RiskBand, string> = {
    High: "bg-high text-white",
    Medium: "bg-mid text-ink",
    Low: "bg-low text-ink",
  };
  const label = band === "Low" ? "Lower risk" : `${band} risk`;
  return <span className={`inline-block rounded-full px-3 py-1 text-xs font-medium ${styles[band]}`}>{label}</span>;
}

export function ReasonItem({ reason, showTotals = false }: { reason: ReasonRow; showTotals?: boolean }) {
  return (
    <div className="grid gap-3 border-b border-line py-5 last:border-b-0 md:grid-cols-2 md:gap-10">
      <div>
        <div className="flex items-baseline justify-between gap-3">
          <h3 className="text-[17px] font-bold text-ink">{reason.title}</h3>
          <span className="text-sm font-medium text-muted">{reason.share_pct}%</span>
        </div>
        <div className="mt-2 h-1.5 rounded-full bg-line" aria-hidden="true">
          <div className="h-full rounded-full bg-plum" style={{ width: `${Math.min(100, reason.share_pct)}%` }} />
        </div>
        <p className="mt-3 text-[15px] leading-relaxed text-muted">{reason.explanation}</p>
        {showTotals && (
          <p className="mt-2 text-sm text-muted">
            {fmtNum(reason.carts)} carts, {fmtMoney(reason.cart_value)} cart value
          </p>
        )}
      </div>
      <p className="text-[15px] leading-relaxed text-ink">
        <span className="font-bold text-plum">Do this:</span> {reason.suggested_action}
      </p>
    </div>
  );
}

export function Loading() {
  return (
    <div className="space-y-4" role="status" aria-label="Loading">
      <div className="h-12 w-2/3 rounded-xl bg-white/70 motion-safe:animate-pulse" />
      <div className="h-20 rounded-2xl bg-white/70 motion-safe:animate-pulse" />
      <div className="h-64 rounded-2xl bg-white/70 motion-safe:animate-pulse" />
    </div>
  );
}

export function ErrorBox({ message }: { message: string }) {
  return (
    <div className="rounded-2xl bg-white p-6 text-ink" role="alert">
      <p className="font-bold text-high">Could not load data</p>
      <p className="mt-1 text-[15px] text-muted">{message}. Check that the API is running on port 8000, then reload the page.</p>
    </div>
  );
}

export function Disclaimer() {
  return (
    <p className="text-sm text-muted">
      Reasons are likely drivers estimated from past shopper behavior. They are not proven causes.
    </p>
  );
}