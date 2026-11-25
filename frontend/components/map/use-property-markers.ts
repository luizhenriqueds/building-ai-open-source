import L from "leaflet";
import { useEffect, useRef } from "react";
import { pinIcon } from "@/components/map/marker-icons";
import { buildPopup } from "@/components/map/popup";
import {
  BRAZIL_CENTER,
  BRAZIL_ZOOM,
  type MapView,
} from "@/components/map/use-leaflet-map";
import type { PropertySummary } from "@/lib/types";

const FIT_PADDING = 0.2;
const FIT_MAX_ZOOM = 12;

function createMarker(property: PropertySummary, lat: number, lon: number) {
  return L.marker([lat, lon], { icon: pinIcon() }).bindPopup(() =>
    buildPopup(property),
  );
}

export function usePropertyMarkers(
  view: MapView | null,
  properties: PropertySummary[],
  hoveredId: string | null,
) {
  const markers = useRef(new Map<string, L.Marker>());

  useEffect(() => {
    if (!view) return;
    const { map, cluster } = view;
    cluster.clearLayers();
    markers.current.clear();
    for (const property of properties) {
      if (property.lat === null || property.lon === null) continue;
      const marker = createMarker(property, property.lat, property.lon);
      markers.current.set(property.property_id, marker);
      cluster.addLayer(marker);
    }
    if (markers.current.size === 0) {
      map.setView(BRAZIL_CENTER, BRAZIL_ZOOM);
      return;
    }
    map.fitBounds(cluster.getBounds().pad(FIT_PADDING), {
      maxZoom: FIT_MAX_ZOOM,
    });
  }, [view, properties]);

  useEffect(() => {
    const marker = hoveredId ? markers.current.get(hoveredId) : undefined;
    marker?.setIcon(pinIcon(true));
    return () => {
      marker?.setIcon(pinIcon(false));
    };
  }, [hoveredId, properties]);
}
