"use client";

import type { FormEvent } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useSearchFilters } from "@/hooks/use-search-filters";

export function SearchBar() {
  const { filters, update } = useSearchFilters();

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const query = new FormData(event.currentTarget).get("q");
    update({ q: String(query).trim() });
  }

  return (
    <form
      key={filters.q}
      role="search"
      onSubmit={handleSubmit}
      className="mx-auto flex min-w-0 flex-1 gap-2 max-lg:basis-full max-lg:order-3 lg:max-w-2xl"
    >
      <Input
        name="q"
        type="search"
        autoComplete="off"
        defaultValue={filters.q}
        placeholder="Describe what you want, e.g. bright house with 3 bedrooms near a park"
        aria-label="Search properties"
        className="h-10"
      />
      <Button type="submit" className="h-10 px-4 font-bold">
        Search
      </Button>
    </form>
  );
}
