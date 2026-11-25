"use client";

import { Maximize2, Minimize2 } from "lucide-react";
import dynamic from "next/dynamic";
import { useEffect, useState } from "react";
import type { LeafletPoiMapProps } from "@/components/map/leaflet-poi-map";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { cn } from "@/lib/utils";

const LeafletPoiMap = dynamic(
  () => import("@/components/map/leaflet-poi-map"),
  {
    ssr: false,
    loading: () => <Skeleton className="size-full rounded-none" />,
  },
);

export function PoiMap(props: LeafletPoiMapProps) {
  const [expanded, setExpanded] = useState(false);

  useEffect(() => {
    if (!expanded) return;
    const close = (event: KeyboardEvent) => {
      if (event.key === "Escape") setExpanded(false);
    };
    window.addEventListener("keydown", close);
    return () => window.removeEventListener("keydown", close);
  }, [expanded]);

  const ToggleIcon = expanded ? Minimize2 : Maximize2;

  return (
    <div
      className={cn(
        "isolate overflow-hidden border border-input bg-muted",
        expanded ? "fixed inset-0 z-[2000]" : "relative z-0 h-112 rounded-lg",
      )}
    >
      <LeafletPoiMap {...props} />
      <Button
        type="button"
        size="icon"
        variant="outline"
        aria-label={expanded ? "Exit full screen" : "Expand map"}
        className="absolute top-2.5 right-2.5 z-[1000] bg-card"
        onClick={() => setExpanded(!expanded)}
      >
        <ToggleIcon />
      </Button>
    </div>
  );
}
