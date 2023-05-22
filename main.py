from fastapi import Depends, FastAPI

from server.errors.base import BaseHTTPError
from server.errors.common_errors import TooManyRequestsError
from server.errors.handlers import init_handlers as init_error_handlers
from server.rate_limits import create_limiter
from server.routes import router


app = FastAPI(
    dependencies=[Depends(create_limiter("600/minute"))],
    responses=BaseHTTPError.generate_responses(TooManyRequestsError),  # type: ignore[arg-type]
)
app.include_router(router)

init_error_handlers(app)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8888, forwarded_allow_ips="*")
