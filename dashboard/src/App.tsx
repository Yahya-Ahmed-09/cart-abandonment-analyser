import { NavLink, Route, Routes, useLocation } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { api } from "./api";
import { useFilters } from "./filters";
import { controlClass } from "./ui";
import Overview from "./pages/Overview";
import Reasons from "./pages/Reasons";
import Brands from "./pages/Brands";
import AtRisk from "./pages/AtRisk";
import Model from "./pages/Model";

const NAV = [
  { to: "/", label: "Overview" },
  { to: "/reasons", label: "Reasons" },
  { to: "/brands", label: "Brands & categories" },
  { to: "/at-risk", label: "At-risk carts" },
  { to: "/model", label: "Model results" },
];

function FilterBar() {
  const { filters, setFilters } = useFilters();
  const info = useQuery({ queryKey: ["filters"], queryFn: api.filters });
  const range = info.data?.date_range;

  return (
    <div className="flex flex-wrap items-center gap-2">
      <label className={`${controlClass} flex items-center gap-2`}>
        <span className="text-muted">From</span>
        <input
          type="date"
          min={range?.min_date}
          max={range?.max_date}
          value={filters.date_from ?? ""}
          onChange={(e) => setFilters({ ...filters, date_from: e.target.value || undefined })}
          className="bg-transparent text-ink outline-none"
        />
      </label>
      <label className={`${controlClass} flex items-center gap-2`}>
        <span className="text-muted">To</span>
        <input
          type="date"
          min={range?.min_date}
          max={range?.max_date}
          value={filters.date_to ?? ""}
          onChange={(e) => setFilters({ ...filters, date_to: e.target.value || undefined })}
          className="bg-transparent text-ink outline-none"
        />
      </label>
      <select
        aria-label="Brand"
        value={filters.brand ?? ""}
        onChange={(e) => setFilters({ ...filters, brand: e.target.value || undefined })}
        className={controlClass}
      >
        <option value="">All brands</option>
        {info.data?.brands.map((b) => (
          <option key={b.brand} value={b.brand}>
            {b.brand} ({b.carts.toLocaleString("en-US")})
          </option>
        ))}
      </select>
      <button onClick={() => setFilters({})} className={controlClass}>
        Reset filters
      </button>
    </div>
  );
}

export default function App() {
  const { pathname } = useLocation();
  const current = NAV.find((n) => n.to === pathname) ?? NAV[0];

  return (
    <div className="flex min-h-screen flex-col bg-ground text-ink md:flex-row">
      <aside className="shrink-0 bg-ink px-4 py-5 text-[#F4F1F7] md:w-60 md:py-7">
        <div className="px-3 pb-4 text-lg font-bold tracking-tight md:pb-6">Cart Recovery</div>
        <nav className="flex gap-1 overflow-x-auto md:flex-col" aria-label="Main">
          {NAV.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === "/"}
              className={({ isActive }) =>
                `whitespace-nowrap rounded-lg px-3 py-2.5 text-[15px] ${
                  isActive ? "bg-plum font-medium text-white" : "text-[#CFC8DB] hover:bg-[#2E2942]"
                }`
              }
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
      </aside>

      <main className="min-w-0 flex-1 px-5 py-8 md:px-12 md:py-9">
        <div className="mx-auto max-w-[1128px]">
          <div className="mb-10 flex flex-wrap items-center justify-between gap-4">
            <h1 className="text-[15px] font-medium text-muted">{current.label}</h1>
            {pathname !== "/model" && <FilterBar />}
          </div>
          <Routes>
            <Route path="/" element={<Overview />} />
            <Route path="/reasons" element={<Reasons />} />
            <Route path="/brands" element={<Brands />} />
            <Route path="/at-risk" element={<AtRisk />} />
            <Route path="/model" element={<Model />} />
          </Routes>
        </div>
      </main>
    </div>
  );
}