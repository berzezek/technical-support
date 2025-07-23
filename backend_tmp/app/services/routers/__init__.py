from fastapi import APIRouter

from app.services.routers.auth_router import router as auth_router
from app.services.routers.process import router as process_router
from app.services.routers.task import router as task_router
from app.services.routers.operator import router as operator_router
from app.services.routers.ws import router as ws_router

router = APIRouter(prefix="/services")
router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(process_router, prefix="/process", tags=["Process"])
router.include_router(task_router, prefix="/task", tags=["Task"])
router.include_router(operator_router, prefix="/operator", tags=["Operator"])
router.include_router(ws_router, tags=["WebSocket"])
