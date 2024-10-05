from __future__ import annotations

from sqlalchemy.sql.schema import Column
from sqlalchemy.types import LargeBinary
from sqlalchemy_utils import generic_repr

from server.adapters.database.base import Base


@generic_repr("id")
class Secret(Base):
    secret_data = Column(LargeBinary(), unique=False, nullable=False, index=False)
    salt = Column(LargeBinary(), unique=False, nullable=False, index=False)
