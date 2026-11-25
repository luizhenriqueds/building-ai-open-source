import { poiIconFor } from "@/lib/poi-icons";

type Props = { category: string; className?: string };

export function CategoryIcon({ category, className = "size-4" }: Props) {
  const Icon = poiIconFor(category);
  return <Icon className={className} aria-hidden />;
}
