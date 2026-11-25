import { formatMoney, propertyPlace, propertyTitle } from "@/lib/format";
import type { PropertySummary } from "@/lib/types";

// Built with DOM nodes (not an HTML string) so listing text can never inject markup.
export function buildPopup(property: PropertySummary): HTMLElement {
  const link = document.createElement("a");
  link.href = `/property/${property.property_id}`;

  const price = document.createElement("strong");
  price.textContent =
    property.sale_value === null ? "" : formatMoney(property.sale_value);

  const description = document.createElement("span");
  description.textContent = `${propertyTitle(property)}, ${propertyPlace(property)}`;

  link.append(price, document.createElement("br"), description);
  return link;
}
