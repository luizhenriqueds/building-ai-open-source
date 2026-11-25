import L from "leaflet";
import { useEffect } from "react";
import { homeIcon, poiIcon } from "@/components/map/marker-icons";
import type { MapView } from "@/components/map/use-leaflet-map";
import { formatDistance } from "@/lib/format-detail";
import { formatCategory } from "@/lib/format";
import type { Poi } from "@/lib/types";

const FIT_PADDING = 0.2;
const FIT_MAX_ZOOM = 16;

// Tooltips take a DOM node so place names can never inject markup.
function tooltipText(text: string): HTMLElement {
  const node = document.createElement("span");
  node.textContent = text;
  return node;
}

function poiLabel(poi: Poi): string {
  const name = poi.name ?? formatCategory(poi.category);
  return `${name} · ${formatDistance(poi.dist_m)}`;
}

export function usePoiMarkers(
  view: MapView | null,
  home: L.LatLngTuple | null,
  pois: Poi[],
) {
  const [homeLat, homeLon] = home ?? [null, null];

  useEffect(() => {
    if (!view) return;
    const layer = L.layerGroup().addTo(view.map);
    const points: L.LatLngTuple[] = [];
    if (homeLat !== null && homeLon !== null) {
      L.marker([homeLat, homeLon], { icon: homeIcon(), zIndexOffset: 1000 })
        .bindTooltip(tooltipText("This property"))
        .addTo(layer);
      points.push([homeLat, homeLon]);
    }
    for (const poi of pois) {
      L.marker([poi.lat, poi.lon], { icon: poiIcon(poi.category) })
        .bindTooltip(tooltipText(poiLabel(poi)))
        .addTo(layer);
      points.push([poi.lat, poi.lon]);
    }
    if (points.length > 0) {
      view.map.fitBounds(L.latLngBounds(points).pad(FIT_PADDING), {
        maxZoom: FIT_MAX_ZOOM,
      });
    }
    return () => {
      layer.remove();
    };
  }, [view, homeLat, homeLon, pois]);
}
