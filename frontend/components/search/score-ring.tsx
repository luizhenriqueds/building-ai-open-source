import type { CSSProperties } from "react";
import { cn } from "@/lib/utils";

type Props = { score: number | null; className?: string };

export function ScoreRing({ score, className }: Props) {
  const label =
    score === null
      ? "No visual score"
      : `Visual score ${Math.round(score)} out of 100`;

  return (
    <div
      role="img"
      aria-label={label}
      style={{ "--p": score ?? 0 } as CSSProperties}
      className={cn(
        "relative grid size-13 place-items-center rounded-full font-mono text-foreground",
        "[background:conic-gradient(var(--primary)_calc(var(--p)*1%),var(--input)_0)]",
        "before:absolute before:inset-1 before:rounded-full before:bg-card before:content-['']",
        className,
      )}
    >
      <b className="relative text-[0.9375rem]">
        {score === null ? "–" : Math.round(score)}
      </b>
    </div>
  );
}
