import {
  Bus,
  Coffee,
  GraduationCap,
  Hospital,
  Landmark,
  MapPin,
  Pill,
  School,
  ShieldCheck,
  ShoppingBag,
  ShoppingCart,
  TreePine,
  Utensils,
  type LucideIcon,
} from "lucide-react";

const POI_ICONS: Record<string, LucideIcon> = {
  bank: Landmark,
  bus_station: Bus,
  cafe: Coffee,
  hospital: Hospital,
  park: TreePine,
  pharmacy: Pill,
  police: ShieldCheck,
  restaurant: Utensils,
  school: School,
  shopping_center: ShoppingBag,
  supermarket: ShoppingCart,
  university: GraduationCap,
};

export function poiIconFor(category: string): LucideIcon {
  return POI_ICONS[category] ?? MapPin;
}
