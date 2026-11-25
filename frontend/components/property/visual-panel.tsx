import { ExpandableText } from "@/components/property/expandable-text";
import { Panel } from "@/components/property/panel";
import { RatingMeter } from "@/components/property/rating-meter";
import { ScoreRing } from "@/components/search/score-ring";
import { Badge } from "@/components/ui/badge";
import { formatAge } from "@/lib/format-detail";
import type { PropertyDetail } from "@/lib/types";

export function VisualPanel({ property }: { property: PropertyDetail }) {
  const details = property.visual_details;

  return (
    <Panel title="Visual score">
      {!details ? (
        <p className="text-muted-foreground">
          This property has not been scored yet.
        </p>
      ) : (
        <div className="grid gap-4">
          <div className="flex items-center gap-4">
            <ScoreRing score={property.visual_score} />
            <Badge variant="outline">{formatAge(details)}</Badge>
          </div>
          {!details.is_property_photo && (
            <p className="text-sm text-muted-foreground">
              The photo does not show the property, so no score was given.
            </p>
          )}
          <ExpandableText text={details.note} />
          <div className="grid gap-2">
            <RatingMeter label="Facade" value={details.facade} />
            <RatingMeter label="Condition" value={details.condition} />
            <RatingMeter label="Standard" value={details.standard} />
            <RatingMeter label="Surroundings" value={details.surroundings} />
          </div>
          <p className="text-xs text-muted-foreground">
            Estimated by a local vision model from the listing photo.
          </p>
        </div>
      )}
    </Panel>
  );
}
