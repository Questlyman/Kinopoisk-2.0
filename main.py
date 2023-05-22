from fastapi import FastAPI

from server.errors.handlers import init_handlers as init_error_handlers
from server.routes import router


app = FastAPI()
app.include_router(router)

init_error_handlers(app)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8888, forwarded_allow_ips="*")
