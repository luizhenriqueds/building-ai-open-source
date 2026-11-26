import json
import logging
import time

import requests
from sqlalchemy import Integer, delete, func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from pipeline.common.db import get_session
from pipeline.common.models import Poi, Property, PropertyPoi
from pipeline.common.schemas import PoiRecord
from pipeline.stages.pois.config import (
    AMENITIES,
    CATEGORY_ALIASES,
    OVERPASS_RETRY_PAUSE_SECONDS,
    OVERPASS_ROUNDS,
    OVERPASS_TIMEOUT_SECONDS,
    OVERPASS_URLS,
    OVERPASS_USER_AGENT,
    POI_RADIUS_M,
    POIS_CACHE_DIR,
    POIS_PER_CATEGORY,
    SELECTORS,
    SHOPS,
)

logger = logging.getLogger(__name__)


def build_query(uf: str) -> str:
    """Build the Overpass QL query for every selector inside a state's area.

    Args:
        uf: State code, matched against the ISO 3166-2 area (BR-<UF>).
    """
    body = "".join(
        f"{kind}{selector}(area.state);"
        for selector in SELECTORS
        for kind in ("node", "way", "relation")
    )
    return f'[out:json][timeout:300];area["ISO3166-2"="BR-{uf}"]->.state;({body});out center tags;'


def post_query(query: str) -> dict:
    """POST a query, trying each Overpass endpoint in turn and retrying the round with a pause.

    Args:
        query: Overpass QL query.
    """
    headers = {"User-Agent": OVERPASS_USER_AGENT}
    for attempt in range(OVERPASS_ROUNDS):
        for url in OVERPASS_URLS:
            try:
                response = requests.post(
                    url, data={"data": query}, headers=headers, timeout=OVERPASS_TIMEOUT_SECONDS
                )
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, ValueError) as error:
                logger.warning("Overpass %s failed: %s", url, error)
        if attempt < OVERPASS_ROUNDS - 1:
            time.sleep(OVERPASS_RETRY_PAUSE_SECONDS)
    raise RuntimeError("All Overpass endpoints failed")


def fetch_elements(uf: str) -> list[dict]:
    """Return the Overpass elements for a state, reading or writing the JSON cache.

    Args:
        uf: State code, used as the cache file name (pois_<UF>.json).
    """
    cache_path = POIS_CACHE_DIR / f"pois_{uf}.json"
    if cache_path.exists():
        return json.loads(cache_path.read_text())
    elements = post_query(build_query(uf))["elements"]
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(elements))
    return elements


def category_of(tags: dict[str, str]) -> str | None:
    """Return the POI category for OSM tags, or None when they are not a wanted place.

    Args:
        tags: OSM tags of an element.
    """
    if tags.get("amenity") in AMENITIES:
        raw_category = tags["amenity"]
    elif tags.get("shop") in SHOPS:
        raw_category = tags["shop"]
    elif tags.get("leisure") == "park":
        raw_category = "park"
    else:
        return None
    return CATEGORY_ALIASES.get(raw_category, raw_category)


def parse_element(element: dict) -> PoiRecord | None:
    """Convert an Overpass element into a POI, or None when it is unwanted or has no position.

    Args:
        element: One Overpass element with tags and a point or center.
    """
    tags = element.get("tags", {})
    category = category_of(tags)
    point = element if "lat" in element else element.get("center")
    if category is None or point is None:
        return None
    return PoiRecord(
        osm_id=f"{element['type']}/{element['id']}",
        category=category,
        name=tags.get("name"),
        lat=point["lat"],
        lon=point["lon"],
    )


def save_pois(session: Session, records: list[PoiRecord]) -> None:
    """Upsert POIs by OSM id.

    Args:
        session: Open ORM session.
        records: POIs to store.
    """
    if not records:
        return
    statement = insert(Poi)
    statement = statement.on_conflict_do_update(
        index_elements=[Poi.osm_id],
        set_={column: statement.excluded[column] for column in ("category", "name", "lat", "lon")},
    )
    session.execute(statement, [record.model_dump() for record in records])


def link_properties(session: Session) -> None:
    """Rebuild property_poi with the nearest POIs per category within the radius.

    Args:
        session: Open ORM session.
    """
    distance = func.st_distance(Property.geom, Poi.geom)
    ranked = (
        select(
            Property.property_id,
            Poi.id.label("poi_id"),
            func.round(distance).cast(Integer).label("dist_m"),
            func.row_number()
            .over(partition_by=[Property.property_id, Poi.category], order_by=distance)
            .label("rank"),
        )
        .select_from(Property)
        .join(Poi, func.st_dwithin(Property.geom, Poi.geom, float(POI_RADIUS_M)))
        .subquery()
    )
    nearest = select(ranked.c.property_id, ranked.c.poi_id, ranked.c.dist_m).where(
        ranked.c.rank <= POIS_PER_CATEGORY
    )
    session.execute(delete(PropertyPoi))
    session.execute(insert(PropertyPoi).from_select(["property_id", "poi_id", "dist_m"], nearest))


def run() -> None:
    """Load POIs for each state with geocoded properties and fill property_poi."""
    with get_session() as session, session.begin():
        located = select(Property.uf).where(Property.lat.is_not(None)).distinct()
        for uf in sorted(session.scalars(located)):
            elements = fetch_elements(uf)
            records = {
                record.osm_id: record for element in elements if (record := parse_element(element))
            }
            save_pois(session, list(records.values()))
            logger.info("%s: %d POIs", uf, len(records))
        link_properties(session)
        total = session.scalar(select(func.count()).select_from(PropertyPoi))
        logger.info("property_poi rows: %d", total)
