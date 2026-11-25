import logging
from collections import defaultdict
from collections.abc import Callable

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from pipeline.db import get_session
from pipeline.embed_config import (
    EMBED_BATCH_SIZE,
    SEGMENT_CUTS,
    SEGMENT_LABELS,
    SIZE_CUTS,
    SIZE_LABELS,
)
from pipeline.models import Property, PropertyEmbedding
from pipeline.ollama import embed

logger = logging.getLogger(__name__)


def percentile_rank(value: float, peers: list[float]) -> float:
    """Return the share (0-100) of peers strictly below the value.

    Args:
        value: Value to rank.
        peers: Values of the same property type, including this one.
    """
    return 100 * sum(peer < value for peer in peers) / len(peers)


def label_for(rank: float, cuts: tuple[int, int], labels: tuple[str, str, str]) -> str:
    """Pick the label of the band a percentile falls in.

    Args:
        rank: Percentile, 0-100.
        cuts: Upper bounds of the first two bands.
        labels: One label per band.
    """
    return labels[sum(rank >= cut for cut in cuts)]


def labels_by_property(
    properties: list[Property],
    value_of: Callable[[Property], float | None],
    cuts: tuple[int, int],
    labels: tuple[str, str, str],
) -> dict[str, str]:
    """Label each property by its percentile of a value within its own type.

    Args:
        properties: All properties.
        value_of: Reads the ranked value from a property.
        cuts: Upper bounds of the first two bands.
        labels: One label per band.
    """
    peers_by_type: dict[str, list[float]] = defaultdict(list)
    for item in properties:
        if value_of(item) is not None:
            peers_by_type[item.property_type].append(value_of(item))
    return {
        item.property_id: label_for(
            percentile_rank(value_of(item), peers_by_type[item.property_type]), cuts, labels
        )
        for item in properties
        if value_of(item) is not None
    }


def build_text(item: Property, size: str | None, segment: str | None) -> str:
    """Describe a property in Portuguese; missing parts are skipped.

    Args:
        item: The property.
        size: Size label within its type, if known.
        segment: Price segment label within its type, if known.
    """
    head = item.property_type
    head += f" de porte {size}" if size else ""
    head += f", padrão {segment}" if segment else ""
    location = f"{item.city}-{item.uf}"
    parts = [
        f"{head}.",
        item.area_m2 and f"{item.area_m2:.0f} m² de área construída.",
        item.land_area and f"Terreno de {item.land_area:.0f} m².",
        item.bedrooms and f"{item.bedrooms} quartos.",
        item.parking_spots and f"{item.parking_spots} vaga(s) de garagem.",
        item.occupancy_status and f"Imóvel {item.occupancy_status.lower()}.",
        f"Localizada no bairro {item.neighborhood} em {location}."
        if item.neighborhood
        else f"Localizada em {location}.",
    ]
    return " ".join(part for part in parts if part)


def save_embeddings(session: Session, items: list[Property], vectors: list[list[float]]) -> None:
    """Upsert the vectors and store each embedded text on its property.

    Args:
        session: Open ORM session.
        items: Properties just embedded, with embed_text already set.
        vectors: One vector per property, in the same order.
    """
    rows = [
        {"property_id": item.property_id, "embedding": vector}
        for item, vector in zip(items, vectors, strict=True)
    ]
    statement = insert(PropertyEmbedding)
    session.execute(
        statement.on_conflict_do_update(
            index_elements=[PropertyEmbedding.property_id],
            set_={"embedding": statement.excluded.embedding},
        ),
        rows,
    )


def run() -> None:
    """Embed every property whose description is new or changed."""
    with get_session() as session, session.begin():
        properties = list(session.scalars(select(Property).order_by(Property.property_id)))
        stored_ids = set(session.scalars(select(PropertyEmbedding.property_id)))
        sizes = labels_by_property(properties, lambda item: item.area_m2, SIZE_CUTS, SIZE_LABELS)
        segments = labels_by_property(
            properties, lambda item: item.appraised_value, SEGMENT_CUTS, SEGMENT_LABELS
        )
        pending = []
        for item in properties:
            text = build_text(item, sizes.get(item.property_id), segments.get(item.property_id))
            if text != item.embed_text or item.property_id not in stored_ids:
                item.embed_text = text
                pending.append(item)
        for start in range(0, len(pending), EMBED_BATCH_SIZE):
            batch = pending[start : start + EMBED_BATCH_SIZE]
            save_embeddings(session, batch, embed([item.embed_text for item in batch]))
        logger.info("Embedded %d of %d properties", len(pending), len(properties))
