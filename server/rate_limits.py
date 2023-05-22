from typing import Awaitable, Callable

from fastapi.requests import Request
from limits import parse, storage, strategies

from server.errors.common_errors import TooManyRequestsError


# here might be a redis storage, but I suppose in-memory is enough in this certain case
memory_storage = storage.MemoryStorage()
moving_window = strategies.MovingWindowRateLimiter(memory_storage)


def create_limiter(limit: str) -> Callable[[Request], Awaitable[None]]:
    parsed_limit = parse(limit)

    async def limiter(request: Request) -> None:
        client_host_arg = []
        if request.client:
            client_host_arg.append(request.client.host)

        if moving_window.hit(parsed_limit, str(request.url.path), *client_host_arg):
            return
        raise TooManyRequestsError()

    return limiter
