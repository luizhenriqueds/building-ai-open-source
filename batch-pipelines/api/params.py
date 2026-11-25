from pydantic import BaseModel, Field, field_validator

BBOX_PARTS = 4


class SearchParams(BaseModel):
    """Query parameters of GET /properties."""

    q: str | None = None
    property_type: str | None = Field(None, alias="type")
    uf: str | None = None
    max_price: float | None = None
    min_bedrooms: int | None = None
    min_visual_score: float | None = None
    poi_cat: str | None = None
    poi_radius_m: int = 2000
    bbox: str | None = Field(None, description="minLon,minLat,maxLon,maxLat")

    @field_validator("bbox")
    @classmethod
    def check_bbox(cls, value: str | None) -> str | None:
        """Require four comma-separated numbers.

        Args:
            value: Raw query value.
        """
        if value is not None and len(parse_numbers(value)) != BBOX_PARTS:
            raise ValueError("bbox must be minLon,minLat,maxLon,maxLat")
        return value

    @property
    def bbox_values(self) -> list[float] | None:
        """The bounding box as numbers, or None when not given."""
        return parse_numbers(self.bbox) if self.bbox else None


def parse_numbers(text: str) -> list[float]:
    """Split a comma-separated string into floats.

    Args:
        text: Comma-separated numbers.
    """
    return [float(part) for part in text.split(",")]
