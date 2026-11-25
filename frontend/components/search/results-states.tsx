import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";

export function ResultsSkeleton() {
  return (
    <ul className="grid gap-3" aria-hidden>
      {[0, 1, 2, 3].map((index) => (
        <li key={index}>
          <Skeleton className="h-36 rounded-xl" />
        </li>
      ))}
    </ul>
  );
}

export function EmptyState({ onReset }: { onReset: () => void }) {
  return (
    <div className="rounded-xl border border-dashed border-input px-4 py-12 text-center">
      <h3 className="text-lg font-medium">No properties match</h3>
      <p className="mt-1.5 mb-4 text-muted-foreground">
        Loosen a filter or try another description.
      </p>
      <Button type="button" className="h-10 px-4 font-bold" onClick={onReset}>
        Clear filters
      </Button>
    </div>
  );
}

export function ErrorState({ message }: { message: string }) {
  return (
    <div
      role="alert"
      className="rounded-xl border border-destructive/40 px-4 py-8 text-center"
    >
      <h3 className="text-lg font-medium text-destructive">
        Could not load properties
      </h3>
      <p className="mt-1.5 text-muted-foreground">
        {message}. Make sure the API is running.
      </p>
    </div>
  );
}

export function OutOfViewState() {
  return (
    <div className="rounded-xl border border-dashed border-input px-4 py-12 text-center">
      <h3 className="text-lg font-medium">No properties in this map area</h3>
      <p className="mt-1.5 text-muted-foreground">
        Zoom out or move the map to see more.
      </p>
    </div>
  );
}
