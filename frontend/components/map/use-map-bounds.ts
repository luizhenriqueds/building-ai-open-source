import { useEffect, useRef } from "react";
import type { MapView } from "@/components/map/use-leaflet-map";
import type { MapBounds } from "@/lib/types";

export function useMapBounds(
  view: MapView | null,
  onChange?: (bounds: MapBounds) => void,
) {
  const callback = useRef(onChange);
  useEffect(() => {
    callback.current = onChange;
  }, [onChange]);

  useEffect(() => {
    if (!view) return;
    const { map } = view;
    const report = () => {
      const bounds = map.getBounds();
      callback.current?.({
        south: bounds.getSouth(),
        west: bounds.getWest(),
        north: bounds.getNorth(),
        east: bounds.getEast(),
      });
    };
    report();
    map.on("moveend", report);
    return () => {
      map.off("moveend", report);
    };
  }, [view]);
}
