import csv
import logging

from pipeline.common.config import SAMPLE_PATH
from pipeline.common.db import get_session
from pipeline.common.models import Property
from pipeline.common.schemas import PropertyRecord

logger = logging.getLogger(__name__)


def read_sample() -> list[PropertyRecord]:
    """Read and validate the committed sample CSV."""
    with SAMPLE_PATH.open(newline="", encoding="utf-8") as sample_file:
        return [PropertyRecord(**row) for row in csv.DictReader(sample_file)]


def run() -> None:
    """Upsert the sample properties into Postgres."""
    records = read_sample()
    with get_session() as session, session.begin():
        for record in records:
            session.merge(Property(**record.model_dump()))
    logger.info("Loaded %d properties", len(records))
