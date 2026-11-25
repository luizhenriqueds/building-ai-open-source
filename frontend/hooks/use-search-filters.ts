"use client";

import { usePathname, useRouter, useSearchParams } from "next/navigation";
import { useCallback, useMemo } from "react";
import {
  countActiveFilters,
  DEFAULT_FILTERS,
  parseFilters,
  toSearchParams,
  type SearchFilters,
} from "@/lib/search-filters";

export function useSearchFilters() {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const filters = useMemo(() => parseFilters(searchParams), [searchParams]);

  const update = useCallback(
    (patch: Partial<SearchFilters>) => {
      const query = toSearchParams({ ...filters, ...patch }).toString();
      const navigate = pathname === "/" ? router.replace : router.push;
      navigate(query ? `/?${query}` : "/", { scroll: false });
    },
    [filters, pathname, router],
  );

  const reset = useCallback(() => update({ ...DEFAULT_FILTERS }), [update]);

  return { filters, update, reset, activeCount: countActiveFilters(filters) };
}
