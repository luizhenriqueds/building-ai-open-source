import { titleCase } from "@/lib/format";
import type { VisualDetails } from "@/lib/types";

const AGE_LABELS: Record<VisualDetails["age_class"], string> = {
  new: "New building",
  intermediate: "Mid-age building",
  old: "Old building",
  unknown: "Age unknown",
};

const PRECISION_LABELS: Record<string, string> = {
  street: "Street level",
  neighborhood: "Neighborhood level",
  city: "City level",
};

export function formatDistance(meters: number): string {
  return meters < 1000 ? `${meters} m` : `${(meters / 1000).toFixed(1)} km`;
}

export function formatArea(value: number): string {
  return `${value.toLocaleString("en-US", { maximumFractionDigits: 1 })} m²`;
}

export function formatDate(isoDate: string): string {
  return new Date(`${isoDate}T00:00:00`).toLocaleDateString("en-GB", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
}

export function formatAge(details: VisualDetails): string {
  const label = AGE_LABELS[details.age_class];
  const { age_years_low: low, age_years_high: high } = details;
  return low !== null && high !== null
    ? `${label}, ${low}–${high} years`
    : label;
}

export function formatPrecision(
  precision: string | null,
  confidence: number | null,
): string | null {
  if (!precision) return null;
  const label = PRECISION_LABELS[precision] ?? titleCase(precision);
  return confidence === null
    ? label
    : `${label} (${Math.round(confidence * 100)}% confidence)`;
}
