import L from "leaflet";
import "leaflet.markercluster";
import { useEffect, useState, type RefObject } from "react";
import { clusterIcon } from "@/components/map/marker-icons";

const TILES_URL = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
export const BRAZIL_CENTER: L.LatLngTuple = [-15, -50];
export const BRAZIL_ZOOM = 4;

export type MapView = { map: L.Map; cluster: L.MarkerClusterGroup };

export function useLeafletMap(containerRef: RefObject<HTMLDivElement | null>) {
  const [view, setView] = useState<MapView | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;
    const map = L.map(containerRef.current).setView(BRAZIL_CENTER, BRAZIL_ZOOM);
    L.tileLayer(TILES_URL, { attribution: "© OpenStreetMap" }).addTo(map);
    const cluster = L.markerClusterGroup({ iconCreateFunction: clusterIcon });
    map.addLayer(cluster);
    setView({ map, cluster });
    const resizeObserver = new ResizeObserver(() => map.invalidateSize());
    resizeObserver.observe(containerRef.current);
    return () => {
      resizeObserver.disconnect();
      map.remove();
      setView(null);
    };
  }, [containerRef]);

  return view;
}
