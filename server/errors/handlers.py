from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import Response

from server.errors.base import BaseHTTPError


# to avoid circular import
def init_handlers(app: FastAPI) -> None:
    @app.exception_handler(BaseHTTPError)
    async def handle_base_http_error(
        request: Request, exc: BaseHTTPError  # pylint: disable=W0613
    ) -> Response:
        return Response(
            content=exc.model.dict(),
            status_code=exc.status_code,
            headers=exc.headers,
        )
