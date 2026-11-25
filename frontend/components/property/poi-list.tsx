import { CategoryIcon } from "@/components/property/category-icon";
import { formatCategory } from "@/lib/format";
import { formatDistance } from "@/lib/format-detail";
import type { Poi } from "@/lib/types";

export function PoiList({ pois }: { pois: Poi[] }) {
  return (
    <ul className="grid max-h-112 grid-cols-1 divide-y divide-input overflow-y-auto rounded-lg border border-input">
      {pois.map((poi) => (
        <li
          key={`${poi.category}-${poi.lat}-${poi.lon}`}
          className="grid grid-cols-[auto_minmax(0,1fr)_auto] items-center gap-3 px-3 py-2 text-sm"
        >
          <CategoryIcon
            category={poi.category}
            className="size-4 text-brand-text"
          />
          <span>
            <span className="block truncate font-medium">
              {poi.name ?? formatCategory(poi.category)}
            </span>
            <span className="text-muted-foreground">
              {formatCategory(poi.category)}
            </span>
          </span>
          <span className="shrink-0 font-mono">
            {formatDistance(poi.dist_m)}
          </span>
        </li>
      ))}
    </ul>
  );
}
