from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from pipeline.common.config import DATABASE_URL

engine = create_engine(DATABASE_URL)


def get_session() -> Session:
    """Open an ORM session; use it as `with get_session() as session, session.begin():`."""
    return Session(engine)
