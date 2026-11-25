import L from "leaflet";
import "leaflet.markercluster";

const PIN =
  "block size-5 rounded-full border-[3px] border-card bg-primary ring-1 ring-input transition-transform";
const PIN_SELECTED = "scale-150 bg-brand-text";
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
