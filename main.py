from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.errors.handlers import init_handlers as init_error_handlers
from server.routes import router


app = FastAPI(
    servers=[
        {"url": "https://frontend-drg.site/", "description": "Prod server"},
        {"url": "http://localhost/", "description": "Just local server"},
    ]
)
app.include_router(router, prefix="/api/v1/public")

init_error_handlers(app)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8888, forwarded_allow_ips="*")
