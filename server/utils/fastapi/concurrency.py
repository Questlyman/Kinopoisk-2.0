from collections.abc import Coroutine
from functools import wraps
from typing import Callable, ParamSpec, TypeVar

from fastapi.concurrency import run_in_threadpool


P = ParamSpec("P")
R = TypeVar("R")


def run_in_threadpool_decorator(
    func: Callable[P, R]
) -> Callable[P, Coroutine[None, None, R]]:
    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        return await run_in_threadpool(func, *args, **kwargs)

    return wrapper
