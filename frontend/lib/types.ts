export type PropertySummary = {
  property_id: string;
  property_type: string | null;
  uf: string | null;
  city: string | null;
  neighborhood: string | null;
  sale_value: number | null;
  appraised_value: number | null;
  discount: number | null;
  area_m2: number | null;
  bedrooms: number | null;
  lat: number | null;
  lon: number | null;
  visual_score: number | null;
  image_url: string | null;
};

export type FilterOptions = {
  types: string[];
  ufs: string[];
  poi_categories: string[];
};

export type Poi = {
  category: string;
  name: string | null;
  lat: number;
  lon: number;
  dist_m: number;
};

export type VisualDetails = {
  note: string;
  facade: number;
  condition: number;
  standard: number;
  surroundings: number;
  age_class: "new" | "intermediate" | "old" | "unknown";
  age_years_low: number | null;
  age_years_high: number | null;
  is_property_photo: boolean;
};

export type PropertyDetail = PropertySummary & {
  raw_address: string | null;
  parking_spots: number | null;
  geocode_precision: string | null;
  geocode_confidence: number | null;
  visual_age: string | null;
  modality: string | null;
  link: string | null;
  description: string | null;
  land_area: number | null;
  occupancy_status: string | null;
  auction_date: string | null;
  visual_note: string | null;
  visual_details: VisualDetails | null;
  pois: Poi[];
};

export type MapBounds = {
  south: number;
  west: number;
  north: number;
  east: number;
};
