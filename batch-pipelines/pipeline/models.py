from datetime import date

from pgvector.sqlalchemy import HALFVEC
from sqlalchemy import Computed, Date, Float, ForeignKey, Integer, Numeric, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import UserDefinedType


class Base(DeclarativeBase):
    pass


class Geography(UserDefinedType):
    """PostGIS geography(Point, 4326); only used in SQL expressions, never loaded."""

    cache_ok = True

    def get_col_spec(self, **kw: object) -> str:
        """Return the column type DDL.

        Args:
            kw: Unused compiler options.
        """
        return "geography(Point,4326)"


class Property(Base):
    __tablename__ = "properties"

    property_id: Mapped[str] = mapped_column(Text, primary_key=True)
    property_type: Mapped[str | None] = mapped_column(Text)
    uf: Mapped[str | None] = mapped_column(Text)
    city: Mapped[str | None] = mapped_column(Text)
    neighborhood: Mapped[str | None] = mapped_column(Text)
    raw_address: Mapped[str | None] = mapped_column(Text)
    appraised_value: Mapped[float | None] = mapped_column(Numeric(asdecimal=False))
    sale_value: Mapped[float | None] = mapped_column(Numeric(asdecimal=False))
    discount: Mapped[float | None] = mapped_column(Numeric(asdecimal=False))
    modality: Mapped[str | None] = mapped_column(Text)
    link: Mapped[str | None] = mapped_column(Text)
    description: Mapped[str | None] = mapped_column(Text)
    area_m2: Mapped[float | None] = mapped_column(Numeric(asdecimal=False))
    land_area: Mapped[float | None] = mapped_column(Numeric(asdecimal=False))
    bedrooms: Mapped[int | None] = mapped_column(Integer)
    parking_spots: Mapped[int | None] = mapped_column(Integer)
    occupancy_status: Mapped[str | None] = mapped_column(Text)
    auction_date: Mapped[date | None] = mapped_column(Date)
    image_file: Mapped[str | None] = mapped_column(Text)
    lat: Mapped[float | None] = mapped_column(Float)
    lon: Mapped[float | None] = mapped_column(Float)
    geocode_precision: Mapped[str | None] = mapped_column(Text)
    geocode_confidence: Mapped[float | None] = mapped_column(Float)
    geom: Mapped[str | None] = mapped_column(
        Geography,
        Computed("case when lat is not null then st_makepoint(lon,lat)::geography end"),
        deferred=True,
    )
    visual_score: Mapped[float | None] = mapped_column(Float)
    visual_age: Mapped[str | None] = mapped_column(Text)
    visual_note: Mapped[str | None] = mapped_column(Text)
    visual_details: Mapped[dict | None] = mapped_column(JSONB)
    embed_text: Mapped[str | None] = mapped_column(Text)


class Poi(Base):
    __tablename__ = "pois"

    id: Mapped[int] = mapped_column(primary_key=True)
    osm_id: Mapped[str] = mapped_column(Text, unique=True)
    category: Mapped[str] = mapped_column(Text)
    name: Mapped[str | None] = mapped_column(Text)
    lat: Mapped[float] = mapped_column(Float)
    lon: Mapped[float] = mapped_column(Float)
    geom: Mapped[str] = mapped_column(
        Geography, Computed("st_makepoint(lon,lat)::geography"), deferred=True
    )


class PropertyPoi(Base):
    __tablename__ = "property_poi"

    property_id: Mapped[str] = mapped_column(ForeignKey("properties.property_id"), primary_key=True)
    poi_id: Mapped[int] = mapped_column(ForeignKey("pois.id"), primary_key=True)
    dist_m: Mapped[int] = mapped_column(Integer)


class PropertyEmbedding(Base):
    __tablename__ = "property_embeddings"

    property_id: Mapped[str] = mapped_column(ForeignKey("properties.property_id"), primary_key=True)
    embedding: Mapped[list[float]] = mapped_column(HALFVEC(1024))
