import psycopg

from pipeline.config import DATABASE_URL


def connect() -> psycopg.Connection:
    """Open a Postgres connection that commits when its `with` block exits cleanly."""
    return psycopg.connect(DATABASE_URL)
