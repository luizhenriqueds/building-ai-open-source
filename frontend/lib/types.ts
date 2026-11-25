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
