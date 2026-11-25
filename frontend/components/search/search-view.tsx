"use client";

import { useMemo, useState } from "react";
import { FiltersBar } from "@/components/search/filters-bar";
import { ResultsList } from "@/components/search/results-list";
import { ResultsMap } from "@/components/map/results-map";
import { useApiGet } from "@/hooks/use-api-get";
import { useSearchFilters } from "@/hooks/use-search-filters";
import { filterByBounds } from "@/lib/map-bounds";
import { toSearchParams } from "@/lib/search-filters";
import type { MapBounds, PropertySummary } from "@/lib/types";

export function SearchView() {
  const { filters, reset } = useSearchFilters();
  const { data, loading, error } = useApiGet<PropertySummary[]>(
    `/properties?${toSearchParams(filters)}`,
  );
  const [hoveredId, setHoveredId] = useState<string | null>(null);
  const [bounds, setBounds] = useState<MapBounds | null>(null);
  const inView = useMemo(
    () => (data ? filterByBounds(data, bounds) : undefined),
    [data, bounds],
  );

  return (
    <>
      <FiltersBar />
      <div className="min-h-0 flex-1 lg:grid lg:grid-cols-[0.9fr_1fr] lg:grid-rows-1">
        <ResultsList
          properties={inView}
          totalCount={data?.length ?? 0}
          loading={loading}
          error={error}
          onHover={setHoveredId}
          onReset={reset}
        />
        <ResultsMap
          properties={data ?? []}
          hoveredId={hoveredId}
          onBoundsChange={setBounds}
        />
      </div>
    </>
  );
}
