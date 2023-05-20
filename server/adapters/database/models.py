from __future__ import annotations

from sqlalchemy.sql.schema import Column
from sqlalchemy.types import Boolean, String
from sqlalchemy_utils import generic_repr

from server.adapters.database.base import Base


@generic_repr("nickname", "disabled", "full_name")
class User(Base):
    nickname = Column(String(length=256), unique=True, nullable=False)
    disabled = Column(Boolean(), default=False, nullable=False)
    full_name = Column(String(length=512), unique=False, nullable=False)
    email = Column(String(length=512), unique=True, nullable=True)
    hashed_password = Column(String(length=256), nullable=False)
