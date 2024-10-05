# pylint: disable=W0621,E1101,W0613
import logging
from collections.abc import AsyncIterator, Iterator

import pytest
from loguru import logger
from sqlalchemy.engine import URL, make_url
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.ext.asyncio.session import AsyncSession

from server.adapters.database.models import Base
from server.adapters.database.session import (
    make_async_engine,
    make_async_session_factory,
)
from server.settings import database_settings


@pytest.fixture(scope="session")
def caplog(_caplog: pytest.LogCaptureFixture):  # noqa: F811
    class PropagateHandler(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            logging.getLogger(record.name).handle(record)

    handler_id = logger.add(PropagateHandler(), format="{message} {extra}")
    yield _caplog
    logger.remove(handler_id)


@pytest.fixture(scope="session")
def worker_id() -> str:
    return "bureau_1440_test_task"


@pytest.fixture(scope="session")
def temp_instance_id(worker_id) -> str:
    return f"test_{worker_id}"


@pytest.fixture(scope="session")
def temp_instance_sync_url(session_mocker, temp_instance_id) -> URL:
    """
    Generate the URL to temporary test DB
    """
    instance_url = make_url(database_settings.full_url_sync)
    session_mocker.patch(
        "server.settings.DatabaseSettings.full_url_sync",
        new_callable=session_mocker.PropertyMock,
        return_value=str(instance_url),
    )
    return instance_url


@pytest.fixture(scope="session")
def temp_instance_async_url(session_mocker, temp_instance_id) -> URL:
    """
    Generate the async URL to temporary test DB
    """
    instance_url = make_url(database_settings.full_url_async)
    session_mocker.patch(
        "server.settings.DatabaseSettings.full_url_async",
        new_callable=session_mocker.PropertyMock,
        return_value=str(instance_url),
    )
    return instance_url


@pytest.fixture(scope="session")
def _engine(temp_instance_async_url) -> Iterator[AsyncEngine]:
    engine = make_async_engine(temp_instance_async_url.render_as_string(False))
    yield engine
    engine.sync_engine.dispose()


@pytest.fixture()
async def engine(_engine: AsyncEngine) -> AsyncEngine:
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield _engine

    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture()
async def session(engine) -> AsyncIterator[AsyncSession]:
    async with make_async_session_factory(engine=engine)() as session:
        yield session
