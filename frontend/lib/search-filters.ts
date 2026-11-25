import { DEFAULT_RADIUS_M, MAX_PRICE } from "@/lib/config";

// Keys match the API query parameters, so one object serves both the URL and the request.
export type SearchFilters = {
  q: string;
  type: string;
  uf: string;
  max_price: number;
  min_bedrooms: number;
  min_visual_score: number;
  poi_cat: string;
  poi_radius_m: number;
};

export const DEFAULT_FILTERS: SearchFilters = {
  q: "",
  type: "",
  uf: "",
  max_price: MAX_PRICE,
  min_bedrooms: 0,
  min_visual_score: 0,
  poi_cat: "",
  poi_radius_m: DEFAULT_RADIUS_M,
};

type ParamsReader = Pick<URLSearchParams, "get">;

function readNumber(params: ParamsReader, key: string, fallback: number) {
  const value = Number(params.get(key));
  return params.get(key) !== null && Number.isFinite(value) ? value : fallback;
}

export function parseFilters(params: ParamsReader): SearchFilters {
  return {
    q: params.get("q") ?? DEFAULT_FILTERS.q,
    type: params.get("type") ?? DEFAULT_FILTERS.type,
    uf: params.get("uf") ?? DEFAULT_FILTERS.uf,
    max_price: readNumber(params, "max_price", DEFAULT_FILTERS.max_price),
    min_bedrooms: readNumber(
      params,
      "min_bedrooms",
      DEFAULT_FILTERS.min_bedrooms,
    ),
    min_visual_score: readNumber(
      params,
      "min_visual_score",
      DEFAULT_FILTERS.min_visual_score,
    ),
    poi_cat: params.get("poi_cat") ?? DEFAULT_FILTERS.poi_cat,
    poi_radius_m: readNumber(
      params,
      "poi_radius_m",
      DEFAULT_FILTERS.poi_radius_m,
    ),
  };
}

export function toSearchParams(filters: SearchFilters): URLSearchParams {
  const params = new URLSearchParams();
  for (const key of Object.keys(filters) as (keyof SearchFilters)[]) {
    if (filters[key] !== DEFAULT_FILTERS[key]) {
      params.set(key, String(filters[key]));
    }
  }
  return params;
}

const REFINEMENT_KEYS = [
  "type",
  "uf",
  "max_price",
  "min_bedrooms",
  "min_visual_score",
  "poi_cat",
] as const;

export function countActiveFilters(filters: SearchFilters): number {
  return REFINEMENT_KEYS.filter((key) => filters[key] !== DEFAULT_FILTERS[key])
    .length;
}
