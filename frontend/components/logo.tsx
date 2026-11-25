import { Gavel } from "lucide-react";
import Link from "next/link";

export function Logo() {
  return (
    <Link
      href="/"
      aria-label="BidRank home"
      className="flex items-center gap-2 font-medium tracking-tight whitespace-nowrap"
    >
      <span className="grid size-7 place-items-center rounded-md bg-primary text-primary-foreground">
        <Gavel className="size-4" aria-hidden />
      </span>
      BidRank
    </Link>
  );
}
