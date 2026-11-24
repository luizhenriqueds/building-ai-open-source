from pydantic import BaseModel, field_validator


class PropertyRecord(BaseModel):
    property_id: str
    property_type: str
    uf: str
    city: str | None = None
    neighborhood: str | None = None
    raw_address: str | None = None
    appraised_value: float | None = None
    sale_value: float | None = None
    discount: float | None = None
    modality: str | None = None
    link: str | None = None
    description: str | None = None
    area_m2: float | None = None
    land_area: float | None = None
    bedrooms: int | None = None
    parking_spots: int | None = None

    @field_validator("*", mode="before")
    @classmethod
    def empty_to_none(cls, value: object) -> object:
        """Treat empty CSV cells as missing values.

        Args:
            value: Raw field value.
        """
        return None if value == "" else value
