from fastapi import APIRouter

from server.routes.api.v1.public.secret import router as secret_router


router = APIRouter(prefix="/public")
router.include_router(secret_router)
