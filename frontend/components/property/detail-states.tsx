import Link from "next/link";
import { buttonVariants } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";

export function DetailSkeleton() {
  return (
    <div className="grid gap-4" aria-hidden>
      <Skeleton className="h-24 rounded-xl" />
      <Skeleton className="aspect-video rounded-xl" />
      <Skeleton className="h-40 rounded-xl" />
    </div>
  );
}

export function DetailError({ notFound }: { notFound: boolean }) {
  return (
    <div
      role="alert"
      className="rounded-xl border border-dashed border-input px-4 py-12 text-center"
    >
      <h1 className="text-lg font-medium">
        {notFound ? "Property not found" : "Could not load this property"}
      </h1>
      <p className="mt-1.5 mb-4 text-muted-foreground">
        {notFound
          ? "It may have been removed from the sample."
          : "Make sure the API is running."}
      </p>
      <Link
        href="/"
        className={buttonVariants({ className: "h-10 px-4 font-bold" })}
      >
        Back to search
      </Link>
    </div>
  );
}
