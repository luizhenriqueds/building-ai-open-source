import csv
import logging

from pipeline.config import SAMPLE_COLUMNS, SAMPLE_PATH
from pipeline.db import connect

logger = logging.getLogger(__name__)


def build_upsert_sql() -> str:
    """Build the INSERT ... ON CONFLICT statement for the properties table."""
    columns = ", ".join(SAMPLE_COLUMNS)
    placeholders = ", ".join(f"%({column})s" for column in SAMPLE_COLUMNS)
    updates = ", ".join(
        f"{column} = excluded.{column}" for column in SAMPLE_COLUMNS if column != "property_id"
    )
    return (
        f"insert into properties ({columns}) values ({placeholders}) "
        f"on conflict (property_id) do update set {updates}"
    )


def read_sample() -> list[dict]:
    """Read the committed sample CSV, turning empty cells into None."""
    with SAMPLE_PATH.open(newline="", encoding="utf-8") as sample_file:
        return [
            {column: value or None for column, value in row.items()}
            for row in csv.DictReader(sample_file)
        ]


def run() -> None:
    """Upsert the sample properties into Postgres."""
    properties = read_sample()
    with connect() as connection:
        connection.cursor().executemany(build_upsert_sql(), properties)
    logger.info("Loaded %d properties", len(properties))
