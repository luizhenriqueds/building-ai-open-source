from datetime import date

from sqlalchemy import Date, Integer, Numeric, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


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
