from typing import Any

from pgvector.sqlalchemy import HALFVEC
from sqlalchemy import ARRAY, Float, Integer, Numeric, Text, cast, func, literal, select
from sqlalchemy.orm import Session
from sqlalchemy.types import TypeEngine

from api.params import SearchParams
from api.schemas import PoiOut, PropertyCard
from pipeline.models import Poi, Property

CARD_COLUMNS = (*(name for name in PropertyCard.model_fields if name != "image_url"), "image_file")
POI_COLUMNS = tuple(PoiOut.model_fields)
EMBEDDING_TYPE = HALFVEC(1024)
BBOX_TYPE = ARRAY(Float(53))


def typed(value: object, sql_type: TypeEngine) -> Any:
    """Bind a value with an explicit SQL type, so NULLs match the function signature.

    Args:
        value: Python value, possibly None.
        sql_type: SQL type to cast to.
    """
    return cast(literal(value, sql_type), sql_type)


def search_properties(
    session: Session, params: SearchParams, vector: list[float] | None
) -> list[dict]:
    """Call the search_properties SQL function and return the matching cards.

    Args:
        session: Database session.
        params: Validated search filters.
        vector: Query embedding, or None for no semantic ranking.
    """
    results = func.search_properties(
        typed(vector, EMBEDDING_TYPE),
        typed(params.property_type, Text),
        typed(params.uf, Text),
        typed(params.max_price, Numeric),
        typed(params.min_bedrooms, Integer),
        typed(params.min_visual_score, Float(24)),
        typed(params.poi_cat, Text),
        params.poi_radius_m,
        typed(params.bbox_values, BBOX_TYPE),
    ).table_valued(*CARD_COLUMNS)
    return list(session.execute(select(results)).mappings())


def property_pois(session: Session, property_id: str) -> list[dict]:
    """Call the property_pois SQL function: nearby places, nearest first.

    Args:
        session: Database session.
        property_id: CAIXA property number.
    """
    nearby = func.property_pois(property_id).table_valued(*POI_COLUMNS)
    return list(session.execute(select(nearby)).mappings())


def distinct_values(session: Session, column: Any) -> list[str]:
    """Return the sorted distinct values of a column.

    Args:
        session: Database session.
        column: ORM column to read.
    """
    return list(session.scalars(select(column).distinct().order_by(column)))


def filter_values(session: Session) -> dict[str, list[str]]:
    """List the values behind the search filters.

    Args:
        session: Database session.
    """
    return {
        "types": distinct_values(session, Property.property_type),
        "ufs": distinct_values(session, Property.uf),
        "poi_categories": distinct_values(session, Poi.category),
    }
