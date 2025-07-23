from fastapi import APIRouter, Depends
from app.services.auth.auth_dep import get_current_user
from app.services.bpmn.start import main_process
from app.services.auth.schemas import AddUser

router = APIRouter()

@router.get("/start-main-process")
async def start_main_process(phone: str, user: AddUser = Depends(get_current_user)) -> dict:
    return await main_process(phone, user)
