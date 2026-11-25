"use client";

import "leaflet/dist/leaflet.css";
import "leaflet.markercluster/dist/MarkerCluster.css";
import { useRef } from "react";
import { useLeafletMap } from "@/components/map/use-leaflet-map";
import { usePoiMarkers } from "@/components/map/use-poi-markers";
import type { Poi } from "@/lib/types";

export type LeafletPoiMapProps = {
  home: [number, number] | null;
  pois: Poi[];
};

export default function LeafletPoiMap({ home, pois }: LeafletPoiMapProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const view = useLeafletMap(containerRef);
  usePoiMarkers(view, home, pois);

  return (
    <div
      ref={containerRef}
      role="region"
      aria-label="Map of nearby places"
      className="size-full"
    />
  );
}
