"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";

const COLLAPSE_ABOVE_CHARS = 280;

export function ExpandableText({ text }: { text: string }) {
  const [expanded, setExpanded] = useState(false);
  const collapsible = text.length > COLLAPSE_ABOVE_CHARS;

  return (
    <div className="grid justify-items-start gap-1">
      <p
        className={
          collapsible && !expanded ? "line-clamp-3 text-sm" : "text-sm"
        }
      >
        {text}
      </p>
      {collapsible && (
        <Button
          type="button"
          variant="link"
          className="h-auto p-0"
          aria-expanded={expanded}
          onClick={() => setExpanded(!expanded)}
        >
          {expanded ? "Show less" : "Read more"}
        </Button>
      )}
    </div>
  );
}
