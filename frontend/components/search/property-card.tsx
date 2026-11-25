import Link from "next/link";
import { PropertyPhoto } from "@/components/search/property-photo";
import { ScoreRing } from "@/components/search/score-ring";
import { formatMoney, propertyPlace, propertyTitle } from "@/lib/format";
import type { PropertySummary } from "@/lib/types";

type Props = {
  property: PropertySummary;
  onHover: (propertyId: string | null) => void;
};

function formatFacts(property: PropertySummary): string[] {
  const { area_m2, bedrooms } = property;
  return [
    area_m2 ? `${Math.round(area_m2)} m²` : "",
    bedrooms ? `${bedrooms} ${bedrooms === 1 ? "bedroom" : "bedrooms"}` : "",
  ].filter(Boolean);
}

export function PropertyCard({ property, onHover }: Props) {
  const title = propertyTitle(property);
  const highlight = () => onHover(property.property_id);
  const clear = () => onHover(null);

  return (
    <li onMouseEnter={highlight} onMouseLeave={clear}>
      <Link
        href={`/property/${property.property_id}`}
        onFocus={highlight}
        onBlur={clear}
        className="relative grid grid-cols-[7.5rem_minmax(0,1fr)] overflow-hidden rounded-xl border border-input bg-card transition-colors hover:border-primary sm:grid-cols-[11rem_minmax(0,1fr)]"
      >
        <PropertyPhoto
          imageUrl={property.image_url}
          alt={`Photo of ${title}`}
          discount={property.discount}
        />
        <div className="grid content-center gap-1 py-3.5 pr-18 pl-4">
          <h3 className="text-[1.0625rem] leading-tight font-medium tracking-tight">
            {title}
          </h3>
          <p className="text-sm text-muted-foreground">
            {propertyPlace(property)}
          </p>
          <p className="flex gap-4 text-sm text-muted-foreground">
            {formatFacts(property).map((fact) => (
              <span key={fact}>{fact}</span>
            ))}
          </p>
          {property.sale_value !== null && (
            <p className="mt-1 flex flex-wrap items-baseline gap-x-2.5">
              <strong className="font-mono text-lg">
                {formatMoney(property.sale_value)}
              </strong>
              {property.appraised_value !== null && (
                <small className="text-sm text-muted-foreground">
                  appraised at {formatMoney(property.appraised_value)}
                </small>
              )}
            </p>
          )}
        </div>
        <ScoreRing
          score={property.visual_score}
          className="absolute top-1/2 right-3.5 -translate-y-1/2"
        />
      </Link>
    </li>
  );
}
