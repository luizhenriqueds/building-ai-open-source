"use client";

import {
  DetailError,
  DetailSkeleton,
} from "@/components/property/detail-states";
import { NearbyPanel } from "@/components/property/nearby-panel";
import { PriceCard } from "@/components/property/price-card";
import { PropertyFacts } from "@/components/property/property-facts";
import { PropertyHeader } from "@/components/property/property-header";
import { PropertyHero } from "@/components/property/property-hero";
import { VisualPanel } from "@/components/property/visual-panel";
import { useApiGet } from "@/hooks/use-api-get";
import { propertyTitle } from "@/lib/format";
import type { PropertyDetail } from "@/lib/types";

export function PropertyView({ id }: { id: string }) {
  const { data, loading, error } = useApiGet<PropertyDetail>(
    `/properties/${encodeURIComponent(id)}`,
  );

  return (
    <div className="min-h-0 flex-1 overflow-y-auto">
      <div className="mx-auto grid max-w-6xl gap-5 px-4 py-6 sm:px-6">
        {data ? (
          <>
            <PropertyHeader property={data} />
            <div className="grid items-start gap-5 lg:grid-cols-[minmax(0,1fr)_20rem]">
              <div className="grid gap-5">
                <PropertyHero
                  imageUrl={data.image_url}
                  alt={`Photo of ${propertyTitle(data)}`}
                />
                <PropertyFacts property={data} />
                <VisualPanel property={data} />
                <NearbyPanel property={data} />
              </div>
              <PriceCard property={data} />
            </div>
          </>
        ) : loading ? (
          <DetailSkeleton />
        ) : (
          <DetailError notFound={error?.includes("404") ?? false} />
        )}
      </div>
    </div>
  );
}
