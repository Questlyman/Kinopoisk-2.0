import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from main import app
from server.adapters.database.models import Secret


@pytest.fixture()
def test_client() -> TestClient:
    return TestClient(app)


@pytest.fixture(
    params=[
        [
            b"gAAAAABkayjEITicP6Iv8oquDLX5_qXWGXIlYMc9f_wR6qOg0X3_megJI_0Rd3_4aRuKc2UwFN--s8jVaQGBz9irfK8xXVfXV-T7AMRkC0yYVY1-LmtMoeo=",
            b"some secret data",
            b"strong password",
            b"\x89\x87\x11`\xcc\x05\xf6\x1d\xe1\xd6cen\xf1\xba\xbe",
            "39a8dd55-848e-42bf-b6d9-1c16e8176f76",
        ],
        [
            b"gAAAAABkaynOy-6lkLixg-5LppdVyRQCSsNzhmGiDmWAxwi1r_fmA-qiXbkvT8TykBFjA7TJ1aoZnJj9_JsUlW--fKY5sr7AbJSHVlbyk0Xacrait_5dCm4=",
            b"some even more secret data",
            b"the most strongest password ever",
            b"\xfa\xe3\xb9](\x8f/\x82\x97\x83Yu\xda\x0bh\x0b",
            "de811ac9-e070-4b1c-894a-943a4324b843",
        ],
    ],
)
async def secret_in_db_with_raw_data_and_password(
    session: AsyncSession, request: pytest.FixtureRequest
) -> tuple[Secret, bytes, bytes]:
    secret = Secret(
        id=request.param[4],
        secret_data=request.param[0],
        salt=request.param[3],
    )
    session.add(secret)
    await session.commit()
    await session.refresh(secret)
    return secret, request.param[1], request.param[2]
