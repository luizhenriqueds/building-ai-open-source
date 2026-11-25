import { PropertyCard } from "@/components/search/property-card";
import {
  EmptyState,
  ErrorState,
  OutOfViewState,
  ResultsSkeleton,
} from "@/components/search/results-states";
import type { PropertySummary } from "@/lib/types";
import { cn } from "@/lib/utils";

type Props = {
  properties?: PropertySummary[];
  totalCount: number;
  loading: boolean;
  error?: string;
  onHover: (propertyId: string | null) => void;
  onReset: () => void;
};

function countLabel({ properties, totalCount, loading, error }: Props): string {
  if (error) return "Something went wrong";
  if (!properties) return loading ? "Loading properties" : "";
  const count = properties.length;
  if (count < totalCount) return `${count} of ${totalCount} in map view`;
  return `${count} ${count === 1 ? "property" : "properties"}`;
}

function ResultsBody(props: Props) {
  const { properties, totalCount, error, loading, onHover, onReset } = props;
  if (error) return <ErrorState message={error} />;
  if (!properties) return <ResultsSkeleton />;
  if (properties.length === 0 && totalCount > 0) return <OutOfViewState />;
  if (properties.length === 0 && !loading)
    return <EmptyState onReset={onReset} />;
  return (
    <ul
      className={cn("grid gap-3 transition-opacity", loading && "opacity-60")}
    >
      {properties.map((property) => (
        <PropertyCard
          key={property.property_id}
          property={property}
          onHover={onHover}
        />
      ))}
    </ul>
  );
}

export function ResultsList(props: Props) {
  return (
    <section className="min-w-0 px-5 pt-4 pb-12 lg:overflow-y-auto">
      <p aria-live="polite" className="mb-3 text-sm text-muted-foreground">
        {countLabel(props)}
      </p>
      <ResultsBody {...props} />
    </section>
  );
}
