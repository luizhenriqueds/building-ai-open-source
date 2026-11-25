import { CategoryIcon } from "@/components/property/category-icon";
import { Button } from "@/components/ui/button";
import { formatCategory } from "@/lib/format";

type Props = {
  counts: [string, number][];
  total: number;
  selected: string | null;
  onSelect: (category: string | null) => void;
};

export function CategoryChips({ counts, total, selected, onSelect }: Props) {
  const options: [string | null, string, number][] = [
    [null, "All", total],
    ...counts.map(([category, count]): [string, string, number] => [
      category,
      formatCategory(category),
      count,
    ]),
  ];

  return (
    <div className="flex flex-wrap gap-2">
      {options.map(([category, label, count]) => (
        <Button
          key={label}
          type="button"
          size="sm"
          aria-pressed={selected === category}
          variant={selected === category ? "default" : "outline"}
          onClick={() => onSelect(category)}
        >
          {category && <CategoryIcon category={category} />}
          {label} · {count}
        </Button>
      ))}
    </div>
  );
}
