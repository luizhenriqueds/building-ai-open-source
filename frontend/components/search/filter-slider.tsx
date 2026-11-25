import { useEffect, useState } from "react";
import { FilterField } from "@/components/search/filter-field";
import { Slider } from "@/components/ui/slider";

type Props = {
  label: string;
  value: number;
  min: number;
  max: number;
  step: number;
  readout: (value: number) => string;
  onCommit: (value: number) => void;
  active: boolean;
};

function firstValue(value: number | readonly number[]): number {
  return typeof value === "number" ? value : value[0];
}

export function FilterSlider({
  label,
  value,
  min,
  max,
  step,
  readout,
  onCommit,
  active,
}: Props) {
  const [draft, setDraft] = useState(value);
  useEffect(() => setDraft(value), [value]);

  return (
    <FilterField label={label} active={active} readout={readout(draft)}>
      {(labelId) => (
        <Slider
          aria-labelledby={labelId}
          value={[draft]}
          min={min}
          max={max}
          step={step}
          onValueChange={(next) => setDraft(firstValue(next))}
          onValueCommitted={(next) => onCommit(firstValue(next))}
          className="flex h-10 items-center"
        />
      )}
    </FilterField>
  );
}
