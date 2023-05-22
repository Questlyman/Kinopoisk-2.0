import pytest
import pytest_mock
from starlette.requests import Request

from server.errors.common_errors import TooManyRequestsError
from server.rate_limits import create_limiter


@pytest.mark.parametrize(
    ["limiter_str", "count_to_fail"],
    [["600/minute", 600], ["10/minute", 10], ["1/hour", 1]],
)
@pytest.mark.asyncio
async def test_limiter_passes(
    limiter_str: str, count_to_fail: int, mocker: pytest_mock.MockerFixture
) -> None:
    limiter = create_limiter(limiter_str)
    mock = mocker.MagicMock(spec=Request)
    mock.client.host = "128.1.1.1"
    mock.url.path = "/path"
    for _ in range(count_to_fail):
        await limiter(mock)
    with pytest.raises(TooManyRequestsError):
        await limiter(mock)
