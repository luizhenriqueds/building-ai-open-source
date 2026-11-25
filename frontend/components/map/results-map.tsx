"use client";

import dynamic from "next/dynamic";
import { Skeleton } from "@/components/ui/skeleton";
import type { LeafletMapProps } from "@/components/map/leaflet-map";

// Leaflet touches `window` on import, so it only loads in the browser.
const LeafletMap = dynamic(() => import("@/components/map/leaflet-map"), {
  ssr: false,
  loading: () => <Skeleton className="size-full rounded-none" />,
});

export function ResultsMap(props: LeafletMapProps) {
  return (
    <div className="isolate z-0 h-88 border-t border-input bg-muted lg:h-auto lg:border-t-0 lg:border-l">
      <LeafletMap {...props} />
    </div>
  );
}
