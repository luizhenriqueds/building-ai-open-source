import { FilterField } from "@/components/search/filter-field";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import type { Option } from "@/lib/filter-options";
import { cn } from "@/lib/utils";

// Base UI treats an empty string as "no selection", so "any" travels under a sentinel.
const ANY = "any";

type Props = {
  label: string;
  value: string;
  options: Option[];
  onChange: (value: string) => void;
  active: boolean;
  disabled?: boolean;
};

export function FilterSelect({
  label,
  value,
  options,
  onChange,
  active,
  disabled,
}: Props) {
  const items = options.map((option) => ({
    ...option,
    value: option.value || ANY,
  }));

  return (
    <FilterField label={label} active={active}>
      {(labelId) => (
        <Select
          items={items}
          value={value || ANY}
          onValueChange={(next) => onChange(next === ANY ? "" : String(next))}
          disabled={disabled}
        >
          <SelectTrigger
            aria-labelledby={labelId}
            className={cn(
              "w-full bg-card font-normal text-foreground data-[size=default]:h-10",
              active && "border-primary ring-1 ring-primary",
            )}
          >
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            {items.map((item) => (
              <SelectItem key={item.value} value={item.value}>
                {item.label}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      )}
    </FilterField>
  );
}
