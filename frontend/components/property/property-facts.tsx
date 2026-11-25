import { Panel } from "@/components/property/panel";
import { formatArea, formatPrecision } from "@/lib/format-detail";
import { titleCase } from "@/lib/format";
import type { PropertyDetail } from "@/lib/types";

function buildFacts(property: PropertyDetail): [string, string][] {
  const facts: [string, string | null][] = [
    ["Built area", property.area_m2 ? formatArea(property.area_m2) : null],
    ["Land area", property.land_area ? formatArea(property.land_area) : null],
    ["Bedrooms", property.bedrooms ? String(property.bedrooms) : null],
    [
      "Parking spots",
      property.parking_spots ? String(property.parking_spots) : null,
    ],
    [
      "Occupancy",
      property.occupancy_status ? titleCase(property.occupancy_status) : null,
    ],
    [
      "Location accuracy",
      formatPrecision(property.geocode_precision, property.geocode_confidence),
    ],
  ];
  return facts.filter((fact): fact is [string, string] => fact[1] !== null);
}

export function PropertyFacts({ property }: { property: PropertyDetail }) {
  return (
    <Panel title="Facts">
      <dl className="grid grid-cols-2 gap-4 sm:grid-cols-3">
        {buildFacts(property).map(([label, value]) => (
          <div key={label}>
            <dt className="text-sm text-muted-foreground">{label}</dt>
            <dd className="font-medium">{value}</dd>
          </div>
        ))}
      </dl>
      {property.description && (
        <p className="mt-4 border-t border-input pt-4 text-sm text-muted-foreground">
          {property.description}
        </p>
      )}
    </Panel>
  );
}
