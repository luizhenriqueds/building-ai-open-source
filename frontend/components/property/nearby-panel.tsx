"use client";

import { useMemo, useState } from "react";
import { PoiMap } from "@/components/map/poi-map";
import { CategoryChips } from "@/components/property/category-chips";
import { Panel } from "@/components/property/panel";
import { PoiList } from "@/components/property/poi-list";
import type { PropertyDetail } from "@/lib/types";

const RADIUS_LABEL = "within 5 km";

function countByCategory(pois: PropertyDetail["pois"]): [string, number][] {
  const counts = new Map<string, number>();
  for (const poi of pois) {
    counts.set(poi.category, (counts.get(poi.category) ?? 0) + 1);
  }
  return [...counts.entries()];
}

export function NearbyPanel({ property }: { property: PropertyDetail }) {
  const [category, setCategory] = useState<string | null>(null);
  const sorted = useMemo(
    () =>
      [...property.pois].sort((first, second) => first.dist_m - second.dist_m),
    [property.pois],
  );
  const visible = useMemo(
    () => sorted.filter((poi) => !category || poi.category === category),
    [sorted, category],
  );
  const home =
    property.lat !== null && property.lon !== null
      ? ([property.lat, property.lon] as [number, number])
      : null;

  return (
    <Panel title={`Nearby places ${RADIUS_LABEL}`}>
      {sorted.length === 0 ? (
        <p className="text-muted-foreground">No nearby places found.</p>
      ) : (
        <div className="grid gap-4">
          <CategoryChips
            counts={countByCategory(sorted)}
            total={sorted.length}
            selected={category}
            onSelect={setCategory}
          />
          <div className="grid gap-4 md:grid-cols-2">
            <PoiList pois={visible} />
            {home && <PoiMap home={home} pois={visible} />}
          </div>
        </div>
      )}
    </Panel>
  );
}
