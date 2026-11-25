import type { MapBounds, PropertySummary } from "@/lib/types";

export function filterByBounds(
  properties: PropertySummary[],
  bounds: MapBounds | null,
): PropertySummary[] {
  if (!bounds) return properties;
  return properties.filter(
    ({ lat, lon }) =>
      lat !== null &&
      lon !== null &&
      lat >= bounds.south &&
      lat <= bounds.north &&
      lon >= bounds.west &&
      lon <= bounds.east,
  );
}
