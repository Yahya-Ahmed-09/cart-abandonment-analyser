    import type { ReactNode } from "react";
import { MODEL_INFO as M } from "../modelInfo";
import { fmtNum } from "../format";
import { Card } from "../ui";

const BAR_COLORS: Record<string, string> = { High: "#B4233F", Medium: "#E8B04A", Low: "#5FA08B" };

function BandBars() {
  return (
    <div>
      {M.bands.map((b) => (
        <div key={b.key} className="grid grid-cols-[96px_1fr_56px] items-center gap-3 py-3 md:grid-cols-[130px_1fr_64px]">
          <div>
            <div className="text-[15px] font-bold">{b.label}</div>
            <div className="text-sm text-muted">{fmtNum(b.carts)} carts</div>
          </div>
          <div
            className="relative h-9 rounded-lg bg-ground"
            role="img"
            aria-label={`${b.label}: ${b.abandoned} percent were really abandoned`}
          >
            <div className="h-full rounded-lg" style={{ width: `${b.abandoned}%`, background: BAR_COLORS[b.key] }} />
            <div className="absolute -bottom-1 -top-1 w-0.5 bg-ink" style={{ left: `${M.baseRate}%` }} />
          </div>
          <div className="text-right text-xl font-bold">{b.abandoned}%</div>
        </div>
      ))}
      <p className="mt-2 text-sm text-muted">
        The dark line marks all carts together: {M.baseRate.toFixed(1)}% were abandoned.
      </p>
    </div>
  );
}

function Gauge({ value, baseline, baselineLabel }: { value: number; baseline?: number; baselineLabel?: string }) {
  return (
    <div>
      <div className="relative h-2.5 rounded-full bg-line">
        <div className="h-full rounded-full bg-plum" style={{ width: `${Math.min(100, value)}%` }} />
        {baseline !== undefined && (
          <div className="absolute -top-1 h-[18px] w-0.5 bg-ink" style={{ left: `${baseline}%` }} aria-hidden="true" />
        )}
      </div>
      {baseline !== undefined && baselineLabel && (
        <p className="mt-1.5 text-xs text-muted">
          {baselineLabel}: {baseline.toFixed(1)}
        </p>
      )}
    </div>
  );
}

interface Row {
  name: string;
  value: number;
  meaning: string;
  baseline?: number;
  baselineLabel?: string;
}

const ROWS: Row[] = [
  {
    name: "ROC-AUC",
    value: M.metrics.rocAuc,
    meaning: "How well the model ranks an abandoned cart above a purchased one. 50 is a coin flip, 100 is perfect.",
    baseline: M.baseline.rocAuc,
    baselineLabel: "Coin flip",
  },
  {
    name: "PR-AUC",
    value: M.metrics.prAuc,
    meaning: "Ranking quality when the goal is to find abandoned carts.",
    baseline: M.baseline.prAuc,
    baselineLabel: "Guessing",
  },
  {
    name: "Accuracy",
    value: M.metrics.accuracy,
    meaning: "Share of carts labeled correctly.",
    baseline: M.baseline.accuracy,
    baselineLabel: "Saying \"abandoned\" for every cart",
  },
  {
    name: "Precision",
    value: M.metrics.precision,
    meaning: "When the model says a cart will be abandoned, how often it is right.",
    baseline: M.baseline.precision,
    baselineLabel: "Saying \"abandoned\" for every cart",
  },
  {
    name: "Recall",
    value: M.metrics.recall,
    meaning: "Share of truly abandoned carts that the model catches.",
  },
  {
    name: "F1 score",
    value: M.metrics.f1,
    meaning: "A single score that balances precision and recall.",
    baseline: M.baseline.f1,
    baselineLabel: "Saying \"abandoned\" for every cart",
  },
];

function Fact({ term, children }: { term: string; children: ReactNode }) {
  return (
    <div className="border-b border-line py-3 last:border-b-0">
      <dt className="text-sm font-medium text-muted">{term}</dt>
      <dd className="mt-1 text-[15px] leading-relaxed">{children}</dd>
    </div>
  );
}

export default function Model() {
  const gap = M.fit.train - M.fit.validation;
  const high = M.bands[0];
  const low = M.bands[2];

  return (
    <div className="space-y-12">
      <section>
        <h2 className="max-w-3xl text-4xl font-bold leading-[1.1] tracking-tight md:text-[44px]">
          The model tells risky carts from safe ones.
        </h2>
        <p className="mt-3 max-w-2xl text-[17px] leading-relaxed text-muted">
          Checked on {fmtNum(M.testCarts)} carts it had never seen. Carts it called high risk were abandoned{" "}
          {high.abandoned}% of the time, against {low.abandoned}% for lower-risk carts.
        </p>
      </section>

      <Card title="Does a risk level mean something?">
        <p className="mb-4 text-[15px] text-muted">Share of carts that were really abandoned, by the risk level the model gave.</p>
        <BandBars />
      </Card>

      <section>
        <h2 className="text-2xl font-bold tracking-tight">Scorecard</h2>
        <p className="mb-5 mt-1 text-[15px] text-muted">
          Each bar runs from 0 to 100. The dark tick shows the score of a model that always says &quot;abandoned&quot;.
        </p>
        <div className="rounded-2xl bg-white px-6">
          {ROWS.map((r) => (
            <div key={r.name} className="grid gap-3 border-b border-line py-5 last:border-b-0 md:grid-cols-[1fr_1fr] md:items-center md:gap-10">
              <div>
                <div className="flex items-baseline justify-between gap-3 md:justify-start md:gap-4">
                  <h3 className="text-[17px] font-bold">{r.name}</h3>
                  <span className="text-2xl font-bold text-plum">{r.value.toFixed(1)}</span>
                </div>
                <p className="mt-1 text-[15px] leading-relaxed text-muted">{r.meaning}</p>
              </div>
              <Gauge value={r.value} baseline={r.baseline} baselineLabel={r.baselineLabel} />
            </div>
          ))}
        </div>
        <div className="mt-4 rounded-2xl bg-white p-6">
          <p className="font-bold">How to read this</p>
          <p className="mt-1 max-w-3xl text-[15px] leading-relaxed text-muted">
            About {M.baseRate.toFixed(0)}% of carts are abandoned, so accuracy is only about{" "}
            {(M.metrics.accuracy - M.baseline.accuracy).toFixed(1)} points above always guessing &quot;abandoned&quot;. The
            model&apos;s real value is ranking: use the risk levels to decide which carts to act on first.
          </p>
        </div>
      </section>

      <Card title="Is it memorizing or learning?">
        <div className="grid grid-cols-3 gap-4">
          {[
            ["Training data", M.fit.train],
            ["Validation data", M.fit.validation],
            ["Test data", M.fit.test],
          ].map(([label, v]) => (
            <div key={String(label)}>
              <div className="text-3xl font-bold">{(v as number).toFixed(1)}</div>
              <div className="mt-1 text-sm text-muted">{label}</div>
            </div>
          ))}
        </div>
        <p className="mt-4 max-w-3xl text-[15px] leading-relaxed text-muted">
          ROC-AUC on each part of the data. The gap between training and validation is {gap.toFixed(1)} points. A small
          gap means the model learned general patterns instead of memorizing shoppers.
        </p>
      </Card>

      <div className="grid gap-4 lg:grid-cols-2">
        <Card title="How it works">
          <dl>
            <Fact term="Question it answers">Will this shopper buy the same product within 7 days of adding it to the cart?</Fact>
            <Fact term="Model">{M.algorithm}.</Fact>
            <Fact term="What it looks at">
              {M.featureCount} signals: the shopper&apos;s history with this product, how often the product sells, the
              shopper&apos;s buying history, behavior in the current visit, price, and timing.
            </Fact>
            <Fact term="Fair testing">No shopper appears in both the training data and the test data.</Fact>
          </dl>
        </Card>
        <Card title="Where to be careful">
          <dl>
            <Fact term="Risk levels are estimates">Use them to rank carts, not as a promise about one shopper.</Fact>
            <Fact term="Reasons are not proof">They show likely drivers based on past behavior, not confirmed causes.</Fact>
            <Fact term="Time-based signals">
              Some timing signals come from one season of data and may weaken in a new period. The model should be
              retrained on fresh data regularly.
            </Fact>
          </dl>
        </Card>
      </div>
    </div>
  );
}