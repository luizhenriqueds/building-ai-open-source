"use client";

import { FilterSelect } from "@/components/search/filter-select";
import { FilterSlider } from "@/components/search/filter-slider";
import { Button } from "@/components/ui/button";
import { useApiGet } from "@/hooks/use-api-get";
import { useSearchFilters } from "@/hooks/use-search-filters";
import {
  MAX_PRICE,
  MAX_VISUAL_SCORE_FILTER,
  PRICE_STEP,
  VISUAL_SCORE_STEP,
} from "@/lib/config";
import {
  BEDROOM_OPTIONS,
  buildCategoryOptions,
  buildStateOptions,
  buildTypeOptions,
  RADIUS_OPTIONS,
} from "@/lib/filter-options";
import { formatMaxPrice, formatMinScore } from "@/lib/format";
import { DEFAULT_FILTERS } from "@/lib/search-filters";
import type { FilterOptions } from "@/lib/types";

export function FiltersBar() {
  const { filters, update, reset, activeCount } = useSearchFilters();
  const { data: options } = useApiGet<FilterOptions>("/filters");
  const isDefault = (key: keyof typeof DEFAULT_FILTERS) =>
    filters[key] === DEFAULT_FILTERS[key];

  return (
    <form
      aria-label="Filters"
      onSubmit={(event) => event.preventDefault()}
      className="flex shrink-0 flex-wrap items-end gap-x-4 gap-y-3 border-b border-border bg-secondary px-5 py-3"
    >
      <FilterSelect
        label="Type"
        value={filters.type}
        options={buildTypeOptions(options?.types ?? [])}
        onChange={(type) => update({ type })}
        active={!isDefault("type")}
      />
      <FilterSelect
        label="State"
        value={filters.uf}
        options={buildStateOptions(options?.ufs ?? [])}
        onChange={(uf) => update({ uf })}
        active={!isDefault("uf")}
      />
      <FilterSlider
        label="Max price"
        value={filters.max_price}
        min={PRICE_STEP}
        max={MAX_PRICE}
        step={PRICE_STEP}
        readout={formatMaxPrice}
        onCommit={(max_price) => update({ max_price })}
        active={!isDefault("max_price")}
      />
      <FilterSelect
        label="Bedrooms"
        value={String(filters.min_bedrooms)}
        options={BEDROOM_OPTIONS}
        onChange={(count) => update({ min_bedrooms: Number(count) })}
        active={!isDefault("min_bedrooms")}
      />
      <FilterSlider
        label="Min visual score"
        value={filters.min_visual_score}
        min={0}
        max={MAX_VISUAL_SCORE_FILTER}
        step={VISUAL_SCORE_STEP}
        readout={formatMinScore}
        onCommit={(min_visual_score) => update({ min_visual_score })}
        active={!isDefault("min_visual_score")}
      />
      <FilterSelect
        label="Near"
        value={filters.poi_cat}
        options={buildCategoryOptions(options?.poi_categories ?? [])}
        onChange={(poi_cat) => update({ poi_cat })}
        active={!isDefault("poi_cat")}
      />
      <FilterSelect
        label="Within"
        value={String(filters.poi_radius_m)}
        options={RADIUS_OPTIONS}
        onChange={(radius) => update({ poi_radius_m: Number(radius) })}
        active={false}
        disabled={!filters.poi_cat}
      />
      {(activeCount > 0 || filters.q) && (
        <Button type="button" variant="link" onClick={reset} className="h-10">
          Clear filters
        </Button>
      )}
    </form>
  );
}
