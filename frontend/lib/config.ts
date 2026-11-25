export const API_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export const MAX_PRICE = 1_000_000;
export const PRICE_STEP = 25_000;
export const MAX_VISUAL_SCORE_FILTER = 90;
export const VISUAL_SCORE_STEP = 10;
export const BEDROOM_STEPS = [1, 2, 3, 4];
export const RADIUS_OPTIONS_M = [1000, 2000, 5000];
export const DEFAULT_RADIUS_M = 2000;

// The CAIXA data is Portuguese; the interface is English.
export const TYPE_LABELS: Record<string, string> = {
  Casa: "House",
  Apartamento: "Apartment",
};
