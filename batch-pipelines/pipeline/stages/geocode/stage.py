import json
import logging
import math
import time
from collections import Counter

import requests
from sqlalchemy import select

from pipeline.common.config import REQUEST_TIMEOUT_SECONDS
from pipeline.common.db import get_session
from pipeline.common.models import Property
from pipeline.common.schemas import AddressParts, GeocodeResult
from pipeline.stages.geocode.config import (
    EARTH_RADIUS_KM,
    GEOCODE_CACHE_PATH,
    MAX_DISTANCE_FROM_CITY_KM,
    NOMINATIM_INTERVAL_SECONDS,
    NOMINATIM_PARAMS,
    NOMINATIM_URL,
    NOMINATIM_USER_AGENT,
    PLOT_STREET_PATTERN,
    PRECISION_CONFIDENCE,
    STREET_NUMBER_PATTERN,
)

logger = logging.getLogger(__name__)

Point = tuple[float, float]


class Geocoder:
    """Nominatim client with a rate limit and an on-disk cache of every answered query."""

    def __init__(self) -> None:
        self.cache: dict[str, Point | None] = {}
        if GEOCODE_CACHE_PATH.exists():
            self.cache = json.loads(GEOCODE_CACHE_PATH.read_text())
        self.last_request_at = 0.0

    def search(self, query: str) -> Point | None:
        """Return the (lat, lon) of the best match for a query, or None.

        Args:
            query: Free-text address query.
        """
        if query not in self.cache:
            self.cache[query] = self.fetch(query)
        hit = self.cache[query]
        return tuple(hit) if hit else None

    def fetch(self, query: str) -> Point | None:
        """Ask Nominatim at most once per interval; failed requests are not cached.

        Args:
            query: Free-text address query.
        """
        wait = NOMINATIM_INTERVAL_SECONDS - (time.monotonic() - self.last_request_at)
        if wait > 0:
            time.sleep(wait)
        self.last_request_at = time.monotonic()
        try:
            response = requests.get(
                NOMINATIM_URL,
                params={**NOMINATIM_PARAMS, "q": query},
                headers={"User-Agent": NOMINATIM_USER_AGENT},
                timeout=REQUEST_TIMEOUT_SECONDS,
            )
            response.raise_for_status()
        except requests.RequestException as error:
            logger.warning("Nominatim failed for %r (%s)", query, error)
            return None
        results = response.json()
        return (float(results[0]["lat"]), float(results[0]["lon"])) if results else None

    def save(self) -> None:
        """Write the cache to disk."""
        GEOCODE_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        GEOCODE_CACHE_PATH.write_text(json.dumps(self.cache, ensure_ascii=False, indent=0))


def distance_km(first: Point, second: Point) -> float:
    """Return the great-circle distance between two (lat, lon) points.

    Args:
        first: First point.
        second: Second point.
    """
    lat1, lon1, lat2, lon2 = map(math.radians, (*first, *second))
    haversine = (
        math.sin((lat2 - lat1) / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    )
    return 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(haversine))


def parse_address(raw_address: str | None) -> AddressParts:
    """Extract the street and number, dropping plot-style streets and 'S/N' numbers.

    Args:
        raw_address: CAIXA address line.
    """
    match = STREET_NUMBER_PATTERN.match(raw_address or "")
    if not match or PLOT_STREET_PATTERN.match(match["street"].strip()):
        return AddressParts()
    return AddressParts(street=match["street"].strip(), number=match["number"])


def build_ladder(prop: Property) -> list[tuple[str, str]]:
    """Return the (precision, query) attempts from most to least precise.

    Args:
        prop: Property to geocode.
    """
    region = f"{prop.city}, {prop.uf}, Brasil"
    address = parse_address(prop.raw_address)
    street = " ".join(part for part in (address.street, address.number) if part)
    ladder = []
    if street:
        ladder.append(("street", ", ".join(filter(None, (street, prop.neighborhood, region)))))
    if prop.neighborhood:
        ladder.append(("neighborhood", f"{prop.neighborhood}, {region}"))
    ladder.append(("city", region))
    return ladder


def geocode_property(geocoder: Geocoder, prop: Property) -> GeocodeResult | None:
    """Walk the ladder and keep the first hit within range of the city point.

    Args:
        geocoder: Cached Nominatim client.
        prop: Property to geocode.
    """
    ladder = build_ladder(prop)
    city_point = geocoder.search(ladder[-1][1])
    if not city_point:
        return None
    for precision, query in ladder:
        point = geocoder.search(query)
        if point and distance_km(point, city_point) <= MAX_DISTANCE_FROM_CITY_KM:
            lat, lon = point
            return GeocodeResult(
                lat=lat, lon=lon, precision=precision, confidence=PRECISION_CONFIDENCE[precision]
            )
    return None


def apply_result(prop: Property, result: GeocodeResult) -> bool:
    """Store a result unless it would lower the property's existing confidence.

    Args:
        prop: Property row to update.
        result: Geocoding outcome.
    """
    if prop.geocode_confidence is not None and result.confidence <= prop.geocode_confidence:
        return False
    prop.lat, prop.lon = result.lat, result.lon
    prop.geocode_precision, prop.geocode_confidence = result.precision, result.confidence
    return True


def run() -> None:
    """Geocode every property and log how many landed at each precision."""
    geocoder = Geocoder()
    precisions = Counter()
    try:
        with get_session() as session, session.begin():
            for prop in session.scalars(select(Property).order_by(Property.property_id)):
                result = geocode_property(geocoder, prop)
                if result:
                    apply_result(prop, result)
                precisions[result.precision if result else "failed"] += 1
    finally:
        geocoder.save()
    logger.info("Geocoded: %s", dict(precisions))
