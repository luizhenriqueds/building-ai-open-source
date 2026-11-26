import logging
from typing import Literal

from pydantic import BaseModel, Field, ValidationError
from requests import RequestException
from sqlalchemy import select

from pipeline.common.db import get_session
from pipeline.common.models import Property
from pipeline.common.ollama import describe_image
from pipeline.stages.crawl.config import IMAGES_DIR
from pipeline.stages.visual.config import SCORE_WEIGHTS
from prompts.visual import INSTRUCT

logger = logging.getLogger(__name__)


class VisualAge(BaseModel):
    is_property_photo: bool
    facade: int = Field(ge=0, le=10)
    condition: int = Field(ge=0, le=10)
    standard: int = Field(ge=0, le=10)
    surroundings: int = Field(ge=0, le=10)
    age_class: Literal["new", "intermediate", "old", "unknown"]
    age_years_low: int | None
    age_years_high: int | None
    note: str


def compute_score(assessment: VisualAge) -> float | None:
    """Return the 0-100 weighted score, or None when the image does not show the property.

    Args:
        assessment: Structured answer from the vision model.
    """
    if not assessment.is_property_photo:
        return None
    weighted = sum(weight * getattr(assessment, name) for name, weight in SCORE_WEIGHTS.items())
    return round(10 * weighted / sum(SCORE_WEIGHTS.values()), 1)


def apply_assessment(item: Property, assessment: VisualAge) -> None:
    """Store the score, age class, note and sub-ratings on the property.

    Args:
        item: The property.
        assessment: Structured answer from the vision model.
    """
    item.visual_score = compute_score(assessment)
    item.visual_age = assessment.age_class
    item.visual_note = assessment.note
    item.visual_details = assessment.model_dump()


def assess(item: Property) -> VisualAge | None:
    """Score one property photo, or return None (logged) when the model fails.

    Args:
        item: Property with an image file.
    """
    image = (IMAGES_DIR / item.image_file).read_bytes()
    try:
        answer = describe_image(image, INSTRUCT, VisualAge.model_json_schema())
        return VisualAge.model_validate_json(answer)
    except (RequestException, ValidationError) as error:
        logger.warning("%s: %s", item.property_id, error)
        return None


def run(limit: int | None = None) -> None:
    """Score every property photo that has not been scored yet, committing one at a time.

    Args:
        limit: Score at most this many properties.
    """
    with get_session() as session:
        pending = select(Property).where(
            Property.image_file.is_not(None), Property.visual_details.is_(None)
        )
        scored = 0
        for item in session.scalars(pending.order_by(Property.property_id).limit(limit)).all():
            assessment = assess(item)
            if assessment:
                apply_assessment(item, assessment)
                session.commit()
                scored += 1
                logger.info("%s: %s (%s)", item.property_id, item.visual_score, item.visual_age)
        logger.info("Scored %d properties", scored)
