from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Request

from api import queries
from api.deps import SessionDep
from api.params import SearchParams
from api.schemas import Filters, PoiOut, PropertyCard, PropertyDetail
from pipeline.models import Property
from pipeline.ollama import embed
from prompts.embedding import build_query_prompt

router = APIRouter()


def photo_url(request: Request, image_file: str | None) -> str | None:
    """Return the absolute URL of a property photo, or None.

    Args:
        request: Current request, used to build the URL.
        image_file: Photo file name.
    """
    return str(request.url_for("images", path=image_file)) if image_file else None


@router.get("/properties", response_model=list[PropertyCard])
def search_properties(
    params: Annotated[SearchParams, Query()], request: Request, session: SessionDep
) -> list[PropertyCard]:
    """Search properties by meaning, filters, nearby places and map area.

    Args:
        params: Search filters from the query string.
        request: Current request.
        session: Database session.
    """
    vector = embed([build_query_prompt(params.q)])[0] if params.q else None
    rows = queries.search_properties(session, params, vector)
    return [PropertyCard(**row, image_url=photo_url(request, row["image_file"])) for row in rows]


@router.get("/properties/{property_id}", response_model=PropertyDetail)
def get_property(property_id: str, request: Request, session: SessionDep) -> PropertyDetail:
    """Return one property with its nearby places, nearest first.

    Args:
        property_id: CAIXA property number.
        request: Current request.
        session: Database session.
    """
    item = session.get(Property, property_id)
    if item is None:
        raise HTTPException(404, "Property not found")
    return PropertyDetail.model_validate(item, from_attributes=True).model_copy(
        update={
            "image_url": photo_url(request, item.image_file),
            "pois": [PoiOut(**row) for row in queries.property_pois(session, property_id)],
        }
    )


@router.get("/filters", response_model=Filters)
def get_filters(session: SessionDep) -> Filters:
    """List the values available for the search filters.

    Args:
        session: Database session.
    """
    return Filters(**queries.filter_values(session))
