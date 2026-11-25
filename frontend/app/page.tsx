import { Suspense } from "react";
import { SearchView } from "@/components/search/search-view";

export default function Home() {
  return (
    <Suspense fallback={null}>
      <SearchView />
    </Suspense>
  );
}
