export interface Filters {
  date_from?: string;
  date_to?: string;
  brand?: string;
}

export interface ReasonInfo {
  code: string;
  title: string;
  explanation: string;
  suggested_action: string;
}

export interface Kpis {
  total_carts: number;
  abandonment_rate: number;
  total_cart_value: number;
  abandoned_value: number;
  high_risk_carts: number;
  medium_risk_carts: number;
  high_risk_value: number;
}

export interface ReasonRow extends ReasonInfo {
  carts: number;
  cart_value: number;
  share_pct: number;
}

export interface BreakdownRow {
  name: string | number;
  carts: number;
  abandonment_rate: number;
  high_risk_carts: number;
  revenue_at_risk: number;
  top_reason: ReasonInfo | null;
}

export type RiskBand = "High" | "Medium" | "Low";

export interface CartItem {
  row_id: number;
  user_id: number;
  product_id: number;
  category_id: number;
  brand: string;
  price: number;
  event_time: string;
  risk_band: RiskBand;
  risk_score: number;
  reasons: ReasonInfo[];
}

export interface AtRiskResponse {
  total: number;
  items: CartItem[];
}

export interface TrendRow {
  date: string;
  carts: number;
  abandonment_rate: number;
  high_risk_carts: number;
  revenue_at_risk: number;
}

export interface FiltersInfo {
  date_range: { min_date: string; max_date: string };
  brands: { brand: string; carts: number }[];
}

type Params = Record<string, string | number | undefined>;

async function get<T>(path: string, params: Params = {}): Promise<T> {
  const search = new URLSearchParams();
  for (const [key, value] of Object.entries(params)) {
    if (value !== undefined && value !== "") search.set(key, String(value));
  }
  const qs = search.toString();
  const res = await fetch(`/api${path}${qs ? `?${qs}` : ""}`);
  if (!res.ok) throw new Error(`API error ${res.status} on ${path}`);
  return (await res.json()) as T;
}

export const api = {
  filters: () => get<FiltersInfo>("/filters"),
  kpis: (f: Filters) => get<Kpis>("/kpis", { ...f }),
  trends: (f: Filters) => get<TrendRow[]>("/trends", { ...f }),
  reasons: (f: Filters, bands: string) => get<ReasonRow[]>("/reasons", { ...f, bands }),
  brands: (f: Filters) =>
    get<BreakdownRow[]>("/brands", { date_from: f.date_from, date_to: f.date_to, limit: 100 }),
  categories: (f: Filters) => get<BreakdownRow[]>("/categories", { ...f, limit: 100 }),
  atRisk: (f: Filters, bands: string, sort: string, limit: number, offset: number) =>
    get<AtRiskResponse>("/carts/at-risk", { ...f, bands, sort, limit, offset }),
};