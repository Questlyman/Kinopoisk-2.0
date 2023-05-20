import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy import create_engine
from sqlalchemy.engine import URL, Engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from server.settings import database_settings


APP_NAME = "bureau_1440_test_task"


def make_async_engine(
    database_url: str | URL = database_settings.full_url_async,
) -> AsyncEngine:
    return create_async_engine(
        database_url,
        pool_pre_ping=True,
        pool_size=20,
        max_overflow=0,
        connect_args={
            "timeout": database_settings.timeout,
            "server_settings": {
                "statement_timeout": str(database_settings.statement_timeout),
                "application_name": APP_NAME,
            },
        },
    )


def make_sync_engine(database_url: str = database_settings.full_url_sync) -> Engine:
    return create_engine(
        database_url,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=0,
        connect_args={
            "connect_timeout": database_settings.timeout,
            # "application_name": APP_NAME,
            "options": f"-c statement_timeout={database_settings.statement_timeout*1000}",
        },
    )


def make_async_session_factory(
    database_url: str = database_settings.full_url_async,
    engine: AsyncEngine | None = None,
) -> async_sessionmaker[AsyncSession]:
    engine = engine or make_async_engine(database_url)

    return async_sessionmaker(
        engine,
        autoflush=False,
        autocommit=False,
    )


def make_sync_session_factory(
    database_url: str = database_settings.full_url_sync,
    engine: Engine | None = None,
) -> sessionmaker[Session]:  # pylint: disable=unsubscriptable-object
    engine = engine or make_sync_engine(database_url)

    return sessionmaker(
        engine,
        autoflush=False,
        autocommit=False,
    )


def make_async_scoped_session_factory(
    database_url: str = database_settings.full_url_async,
) -> async_scoped_session[AsyncSession]:
    session_factory = make_async_session_factory(database_url)
    return async_scoped_session(session_factory, scopefunc=asyncio.current_task)


def make_sync_scoped_session_factory(
    database_url: str = database_settings.full_url_sync,
) -> scoped_session[Session]:
    session_factory = make_sync_session_factory(database_url)
    return scoped_session(session_factory)


def make_async_scoped_session(
    database_url: str = database_settings.full_url_async,
) -> AsyncSession:
    # noinspection PyShadowingNames
    AsyncSession = make_async_scoped_session_factory(  # pylint: disable=W0621,C0103,
        database_url
    )
    return AsyncSession()


def make_sync_scoped_session(
    database_url: str = database_settings.full_url_sync,
) -> Session:
    ScopedSession = make_sync_scoped_session_factory(  # pylint: disable=C0103,
        database_url
    )
    return ScopedSession()


async_scoped_session_factory = make_async_scoped_session_factory()
async_session_factory = make_async_session_factory()


@asynccontextmanager
async def get_session() -> AsyncIterator[AsyncSession]:
    async with async_scoped_session_factory() as session:
        yield session
