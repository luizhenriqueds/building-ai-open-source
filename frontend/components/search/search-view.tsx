"use client";

import { useState } from "react";
import { FiltersBar } from "@/components/search/filters-bar";
import { ResultsList } from "@/components/search/results-list";
import { ResultsMap } from "@/components/map/results-map";
import { useApiGet } from "@/hooks/use-api-get";
import { useSearchFilters } from "@/hooks/use-search-filters";
import { toSearchParams } from "@/lib/search-filters";
import type { PropertySummary } from "@/lib/types";

export function SearchView() {
  const { filters, reset } = useSearchFilters();
  const { data, loading, error } = useApiGet<PropertySummary[]>(
    `/properties?${toSearchParams(filters)}`,
  );
  const [hoveredId, setHoveredId] = useState<string | null>(null);

  return (
    <>
      <FiltersBar />
      <div className="min-h-0 flex-1 lg:grid lg:grid-cols-[0.9fr_1fr] lg:grid-rows-1">
        <ResultsList
          properties={data}
          loading={loading}
          error={error}
          onHover={setHoveredId}
          onReset={reset}
        />
        <ResultsMap properties={data ?? []} hoveredId={hoveredId} />
      </div>
    </>
  );
}
