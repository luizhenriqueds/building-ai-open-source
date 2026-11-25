"use client";

import "leaflet/dist/leaflet.css";
import "leaflet.markercluster/dist/MarkerCluster.css";
import { useRef } from "react";
import { useLeafletMap } from "@/components/map/use-leaflet-map";
import { usePropertyMarkers } from "@/components/map/use-property-markers";
import type { PropertySummary } from "@/lib/types";

export type LeafletMapProps = {
  properties: PropertySummary[];
  hoveredId: string | null;
};

export default function LeafletMap({ properties, hoveredId }: LeafletMapProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const view = useLeafletMap(containerRef);
  usePropertyMarkers(view, properties, hoveredId);

  return (
    <div
      ref={containerRef}
      role="region"
      aria-label="Map of results"
      className="size-full"
    />
  );
}
