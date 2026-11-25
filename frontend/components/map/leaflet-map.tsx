"use client";

import "leaflet/dist/leaflet.css";
import "leaflet.markercluster/dist/MarkerCluster.css";
import { useRef } from "react";
import { useLeafletMap } from "@/components/map/use-leaflet-map";
import { useMapBounds } from "@/components/map/use-map-bounds";
import { usePropertyMarkers } from "@/components/map/use-property-markers";
import type { MapBounds, PropertySummary } from "@/lib/types";

export type LeafletMapProps = {
  properties: PropertySummary[];
  hoveredId: string | null;
  onBoundsChange?: (bounds: MapBounds) => void;
};

export default function LeafletMap({
  properties,
  hoveredId,
  onBoundsChange,
}: LeafletMapProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const view = useLeafletMap(containerRef);
  usePropertyMarkers(view, properties, hoveredId);
  useMapBounds(view, onBoundsChange);

  return (
    <div
      ref={containerRef}
      role="region"
      aria-label="Map of results"
      className="size-full"
    />
  );
}
