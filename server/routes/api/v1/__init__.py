from fastapi import APIRouter

from server.routes.api.v1.private import router as private_router
from server.routes.api.v1.public import router as public_router


router = APIRouter(prefix="/v1")
router.include_router(private_router)
router.include_router(public_router)
