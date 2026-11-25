from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from pipeline.db import get_session


def get_db() -> Iterator[Session]:
    """Yield a database session for one request."""
    with get_session() as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
