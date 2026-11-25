import { ExternalLink } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { buttonVariants } from "@/components/ui/button";
import { formatMoney } from "@/lib/format";
import type { PropertyDetail } from "@/lib/types";

export function PriceCard({ property }: { property: PropertyDetail }) {
  const { sale_value, appraised_value, discount, link } = property;
  const saving =
    sale_value !== null && appraised_value !== null
      ? appraised_value - sale_value
      : null;

  return (
    <aside className="grid gap-3 rounded-xl border border-input bg-card p-5 lg:sticky lg:top-0">
      <p className="text-sm text-muted-foreground">Sale price</p>
      <p className="font-mono text-3xl font-semibold">
        {sale_value === null ? "–" : formatMoney(sale_value)}
      </p>
      {appraised_value !== null && (
        <p className="text-sm text-muted-foreground">
          Appraised at {formatMoney(appraised_value)}
        </p>
      )}
      {discount !== null && discount > 0 && (
        <div className="flex flex-wrap items-center gap-2">
          <Badge className="bg-primary px-2.5 font-semibold text-primary-foreground">
            -{Math.round(discount)}% below appraisal
          </Badge>
          {saving !== null && saving > 0 && (
            <span className="text-sm text-muted-foreground">
              Save {formatMoney(saving)}
            </span>
          )}
        </div>
      )}
      {link && (
        <a
          href={link}
          target="_blank"
          rel="noopener noreferrer"
          className={buttonVariants({ className: "mt-2 h-10 font-bold" })}
        >
          View on CAIXA <ExternalLink className="size-4" aria-hidden />
        </a>
      )}
    </aside>
  );
}
