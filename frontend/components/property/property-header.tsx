import { ArrowLeft } from "lucide-react";
import Link from "next/link";
import { Badge } from "@/components/ui/badge";
import { formatDate } from "@/lib/format-detail";
import {
  formatType,
  propertyPlace,
  propertyTitle,
  titleCase,
} from "@/lib/format";
import type { PropertyDetail } from "@/lib/types";

export function PropertyHeader({ property }: { property: PropertyDetail }) {
  return (
    <header className="grid gap-2">
      <Link
        href="/"
        className="inline-flex w-fit items-center gap-1.5 text-sm text-muted-foreground hover:text-foreground"
      >
        <ArrowLeft className="size-4" aria-hidden /> Back to search
      </Link>
      <div className="flex flex-wrap items-center gap-2">
        <Badge variant="secondary">{formatType(property.property_type)}</Badge>
        {property.modality && (
          <Badge variant="outline">{titleCase(property.modality)}</Badge>
        )}
      </div>
      <h1 className="text-2xl font-medium tracking-tight">
        {propertyTitle(property)}
      </h1>
      <p className="text-muted-foreground">
        {property.raw_address
          ? titleCase(property.raw_address)
          : propertyPlace(property)}
      </p>
      <p className="flex flex-wrap gap-x-4 font-mono text-sm text-muted-foreground">
        <span>CAIXA ID {property.property_id}</span>
        {property.auction_date && (
          <span>Auction {formatDate(property.auction_date)}</span>
        )}
      </p>
    </header>
  );
}
