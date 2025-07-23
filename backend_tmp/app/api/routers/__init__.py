from fastapi import APIRouter

from .author_routers import router as author_router

router = APIRouter(prefix="/api")

router.include_router(author_router)
