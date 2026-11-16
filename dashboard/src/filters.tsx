import { createContext, useContext, useState, type ReactNode } from "react";
import type { Filters } from "./api";

interface FiltersContextValue {
  filters: Filters;
  setFilters: (f: Filters) => void;
}

const FiltersContext = createContext<FiltersContextValue | null>(null);

export function FiltersProvider({ children }: { children: ReactNode }) {
  const [filters, setFilters] = useState<Filters>({});
  return <FiltersContext.Provider value={{ filters, setFilters }}>{children}</FiltersContext.Provider>;
}

export function useFilters(): FiltersContextValue {
  const ctx = useContext(FiltersContext);
  if (!ctx) throw new Error("useFilters must be used inside FiltersProvider");
  return ctx;
}