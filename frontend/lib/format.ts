import { MAX_PRICE, MAX_VISUAL_SCORE_FILTER, TYPE_LABELS } from "@/lib/config";
import type { PropertySummary } from "@/lib/types";

const moneyFormat = new Intl.NumberFormat("pt-BR", {
  style: "currency",
  currency: "BRL",
  maximumFractionDigits: 0,
});

export function formatMoney(value: number): string {
  return moneyFormat.format(value);
}

export function formatMaxPrice(value: number): string {
  return value >= MAX_PRICE ? "any" : `≤ ${formatMoney(value)}`;
}

export function formatMinScore(value: number): string {
  return value > 0 && value <= MAX_VISUAL_SCORE_FILTER ? `≥ ${value}` : "any";
}

export function titleCase(text: string): string {
  return text
    .toLowerCase()
    .replace(/(^|\s)\S/g, (letter) => letter.toUpperCase());
}

export function formatType(type: string | null): string {
  return type ? (TYPE_LABELS[type] ?? type) : "Property";
}

export function formatCategory(category: string): string {
  const text = category.replace(/_/g, " ");
  return text.charAt(0).toUpperCase() + text.slice(1);
}

export function propertyTitle(property: PropertySummary): string {
  const place = property.neighborhood ?? property.city;
  return place
    ? `${formatType(property.property_type)} in ${titleCase(place)}`
    : formatType(property.property_type);
}

export function propertyPlace(property: PropertySummary): string {
  const region = [property.city && titleCase(property.city), property.uf]
    .filter(Boolean)
    .join("/");
  return [property.neighborhood && titleCase(property.neighborhood), region]
    .filter(Boolean)
    .join(", ");
}
