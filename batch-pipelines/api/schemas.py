from datetime import date

from pydantic import BaseModel


class PropertyCard(BaseModel):
    property_id: str
    property_type: str | None = None
    uf: str | None = None
    city: str | None = None
    neighborhood: str | None = None
    raw_address: str | None = None
    sale_value: float | None = None
    appraised_value: float | None = None
    discount: float | None = None
    area_m2: float | None = None
    bedrooms: int | None = None
    parking_spots: int | None = None
    lat: float | None = None
    lon: float | None = None
    geocode_precision: str | None = None
    visual_score: float | None = None
    visual_age: str | None = None
    similarity: float | None = None
    image_url: str | None = None


class PoiOut(BaseModel):
    category: str
    name: str | None = None
    lat: float
    lon: float
    dist_m: int


class PropertyDetail(PropertyCard):
    modality: str | None = None
    link: str | None = None
    description: str | None = None
    land_area: float | None = None
    occupancy_status: str | None = None
    auction_date: date | None = None
    geocode_confidence: float | None = None
    visual_note: str | None = None
    visual_details: dict | None = None
    pois: list[PoiOut] = []


class Filters(BaseModel):
    types: list[str]
    ufs: list[str]
    poi_categories: list[str]
