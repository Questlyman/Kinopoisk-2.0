from fastapi import APIRouter

from server.routes.api import router as api_router


router = APIRouter()
router.include_router(api_router)
