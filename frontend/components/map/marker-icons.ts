import L from "leaflet";
import "leaflet.markercluster";
import { House, type LucideIcon } from "lucide-react";
import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { poiIconFor } from "@/lib/poi-icons";

const PIN =
  "block size-5 rounded-full border-[3px] border-card bg-primary ring-1 ring-input transition-transform";
const PIN_SELECTED = "scale-150 bg-brand-text";
const POI_PIN =
  "grid size-[1.625rem] place-items-center rounded-full border-2 border-primary/60 bg-card text-brand-text";
const HOME_PIN =
  "grid size-9 place-items-center rounded-full border-[3px] border-card bg-primary text-primary-foreground ring-1 ring-input";
const CLUSTER =
  "grid size-[2.4rem] place-items-center rounded-full border-[3px] border-card bg-primary font-extrabold text-primary-foreground ring-1 ring-input";

export function pinIcon(selected = false): L.DivIcon {
  return L.divIcon({
    className: "",
    html: `<span class="${PIN} ${selected ? PIN_SELECTED : ""}"></span>`,
    iconSize: [22, 22],
    iconAnchor: [11, 11],
  });
}

export function clusterIcon(cluster: L.MarkerCluster): L.DivIcon {
  return L.divIcon({
    className: "",
    html: `<span class="${CLUSTER}">${cluster.getChildCount()}</span>`,
    iconSize: [38, 38],
  });
}

function iconMarkup(icon: LucideIcon, size: number): string {
  return renderToStaticMarkup(createElement(icon, { size, strokeWidth: 2.25 }));
}

export function poiIcon(category: string): L.DivIcon {
  return L.divIcon({
    className: "",
    html: `<span class="${POI_PIN}">${iconMarkup(poiIconFor(category), 14)}</span>`,
    iconSize: [26, 26],
    iconAnchor: [13, 13],
  });
}

export function homeIcon(): L.DivIcon {
  return L.divIcon({
    className: "",
    html: `<span class="${HOME_PIN}">${iconMarkup(House, 20)}</span>`,
    iconSize: [36, 36],
    iconAnchor: [18, 18],
  });
}
