import { useId, type ReactNode } from "react";
import { cn } from "@/lib/utils";

type Props = {
  label: string;
  active: boolean;
  readout?: string;
  children: (labelId: string) => ReactNode;
};

export function FilterField({ label, active, readout, children }: Props) {
  const labelId = useId();
  return (
    <div
      role="group"
      aria-labelledby={labelId}
      className={cn(
        "grid max-w-48 flex-1 basis-32 gap-1 text-sm text-muted-foreground",
        active && "font-semibold text-brand-text",
      )}
    >
      <span id={labelId} className="flex justify-between gap-2">
        {label}
        {readout && (
          <output className="font-normal text-foreground">{readout}</output>
        )}
      </span>
      {children(labelId)}
    </div>
  );
}
