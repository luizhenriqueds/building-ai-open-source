import type { ReactNode } from "react";

type Props = { title: string; children: ReactNode; aside?: ReactNode };

export function Panel({ title, children, aside }: Props) {
  return (
    <section className="rounded-xl border border-input bg-card p-5">
      <div className="mb-4 flex items-center justify-between gap-3">
        <h2 className="text-sm font-semibold tracking-wide text-muted-foreground uppercase">
          {title}
        </h2>
        {aside}
      </div>
      {children}
    </section>
  );
}
