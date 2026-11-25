import { BEDROOM_STEPS, RADIUS_OPTIONS_M } from "@/lib/config";
import { formatCategory, formatType } from "@/lib/format";

export type Option = { value: string; label: string };

export const BEDROOM_OPTIONS: Option[] = [
  { value: "0", label: "Any" },
  ...BEDROOM_STEPS.map((count) => ({
    value: String(count),
    label: `${count}+`,
  })),
];

export const RADIUS_OPTIONS: Option[] = RADIUS_OPTIONS_M.map((meters) => ({
  value: String(meters),
  label: `${meters / 1000} km`,
}));

export function buildTypeOptions(types: string[]): Option[] {
  return [
    { value: "", label: "Any type" },
    ...types.map((type) => ({ value: type, label: formatType(type) })),
  ];
}

export function buildStateOptions(ufs: string[]): Option[] {
  return [
    { value: "", label: "Any state" },
    ...ufs.map((uf) => ({ value: uf, label: uf })),
  ];
}

export function buildCategoryOptions(categories: string[]): Option[] {
  return [
    { value: "", label: "Anywhere" },
    ...categories.map((category) => ({
      value: category,
      label: formatCategory(category),
    })),
  ];
}
