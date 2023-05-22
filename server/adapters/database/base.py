from __future__ import annotations

from datetime import datetime
from typing import Any, TypeVar, cast
from uuid import uuid4

from sqlalchemy import UUID, Column, DateTime, Executable, MetaData, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import as_declarative, declared_attr
from sqlalchemy.sql.base import ExecutableOption

from server.utils.text import camel_to_snake


T = TypeVar("T", bound="Base")

metadata = MetaData()


@as_declarative(metadata=metadata)
class Base:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = Column(DateTime(timezone=True), index=True, default=datetime.utcnow)
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=datetime.utcnow,
        default=datetime.utcnow,
    )

    @declared_attr
    def __tablename__(cls):  # pylint: disable=no-self-argument
        return camel_to_snake(str(cls.__name__))  # pylint: disable=no-member

    @classmethod
    def get_stmt(cls, *args: ExecutableOption, **kwargs: Any) -> Executable:
        stmt = select(cls).options(*args)
        for key, value in kwargs.items():
            stmt = stmt.where(getattr(cls, key) == value)
        return stmt

    @classmethod
    async def get(
        cls: type[T], session: AsyncSession, *args: ExecutableOption, **kwargs: Any
    ) -> T:
        stmt = cls.get_stmt(*args, **kwargs)
        result = await session.execute(stmt)
        return cast(T, result.scalar_one_or_none())

    @classmethod
    async def get_or_create(
        cls: type[T],
        session: AsyncSession,
        *args: ExecutableOption,
        kwargs_to_request: dict[str, Any] | None = None,
        kwargs_to_create: dict[str, Any] | None = None,
    ) -> T:
        if kwargs_to_request is None:
            kwargs_to_request = {}
        if kwargs_to_create is None:
            kwargs_to_create = {}

        if (obj := await cls.get(session, *args, **kwargs_to_request)) is None:
            obj = cls(**kwargs_to_create)
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
        return obj
