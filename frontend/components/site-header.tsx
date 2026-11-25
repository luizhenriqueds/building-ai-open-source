import { Suspense } from "react";
import { Logo } from "@/components/logo";
import { SearchBar } from "@/components/search/search-bar";

export function SiteHeader() {
  return (
    <header className="z-50 flex shrink-0 flex-wrap items-center gap-x-6 gap-y-2 border-b border-input bg-background px-5 py-3">
      <Logo />
      <Suspense fallback={null}>
        <SearchBar />
      </Suspense>
    </header>
  );
}
