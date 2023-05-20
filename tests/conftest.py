# pylint: disable=W0621,E1101,W0613
import logging
from collections.abc import AsyncIterator, Iterator

import pytest
from loguru import logger
from sqlalchemy.engine import URL, make_url
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.ext.asyncio.session import AsyncSession

from server.adapters.database.models import Base
from server.adapters.database.session import get_session, make_async_engine
from server.settings import database_settings


@pytest.fixture(scope="session")
def caplog(_caplog):  # noqa: F811
    class PropagateHandler(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            logging.getLogger(record.name).handle(record)

    handler_id = logger.add(PropagateHandler(), format="{message} {extra}")
    yield _caplog
    logger.remove(handler_id)


@pytest.fixture(scope="session")
def temp_instance_id(worker_id) -> str:
    return f"test_{worker_id}"


@pytest.fixture(scope="session")
def temp_instance_sync_url(session_mocker, temp_instance_id) -> URL:
    """Сгенерировать путь до временной тестовой БД на основе урлы"""
    instance_url = make_url(database_settings.full_url_sync)
    instance_url = instance_url.set(database=temp_instance_id)
    session_mocker.patch(
        "server.settings.DatabaseSettings.full_url_sync",
        new_callable=session_mocker.PropertyMock,
        return_value=str(instance_url),
    )
    return instance_url


@pytest.fixture(scope="session")
def temp_instance_async_url(session_mocker, temp_instance_id) -> URL:
    """Сгенерировать путь до временной тестовой БД на основе урлы"""
    instance_url = make_url(database_settings.full_url_async)
    instance_url = instance_url.set(database=temp_instance_id)
    session_mocker.patch(
        "server.settings.DatabaseSettings.full_url_async",
        new_callable=session_mocker.PropertyMock,
        return_value=str(instance_url),
    )
    return instance_url


@pytest.fixture(scope="session")
def _engine() -> Iterator[AsyncEngine]:
    engine = make_async_engine()
    yield engine
    engine.sync_engine.dispose()


@pytest.fixture()
async def engine(_engine: AsyncEngine) -> AsyncIterator[AsyncEngine]:
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield _engine
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture()
async def session(engine) -> AsyncIterator[AsyncSession]:
    async with get_session() as session:
        yield session


@pytest.fixture()
async def temp_instance_async_engine(temp_instance_async_url) -> AsyncEngine:
    engine = make_async_engine(
        temp_instance_async_url,
    )
    try:
        yield engine
    finally:
        await engine.dispose()


# declare temp_instance_sync_url and temp_instance_engine
def _temp_instance_setup_clean(temp_instance_sync_url, temp_instance_engine):
    pass
