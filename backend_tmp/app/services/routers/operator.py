from fastapi import APIRouter, Request, Depends, Body, status
from app.services.auth.auth_dep import get_current_user
from app.services.auth.schemas import AddUser

from app.services.bpmn.user_tasks.operator_tasks import (
    set_lead_info,
    set_task_options,
    set_task_refuse,
)
from app.services.auth import require_roles_any

router = APIRouter()


@router.post("/lead-info", status_code=status.HTTP_201_CREATED)
@require_roles_any(["Operator"])
async def lead_info(
    request: Request,
    user_task: str,
    lead_info: str,
    is_task_needed: bool = True,
    current_user: AddUser = Depends(get_current_user),
):
    """
    Обработка информации о лиде и завершение задачи.
    """
    return await set_lead_info(user_task, lead_info, current_user, is_task_needed)


@router.post("/task_options", status_code=status.HTTP_201_CREATED)
@require_roles_any(["Operator"])
async def task_options(
    request: Request,
    user_task: str,
    task_options: list[str] = Body(..., embed=True),
    current_user: AddUser = Depends(get_current_user),
):
    """
    Установка опций задачи и завершение задачи.
    """
    return await set_task_options(user_task, task_options, current_user)


@router.post("/task_refuse", status_code=status.HTTP_201_CREATED)
@require_roles_any(["Operator"])
async def task_refuse(
    request: Request,
    user_task: str,
    draw_refuse: str,
    current_user: AddUser = Depends(get_current_user),
):
    """
    Отказ от выполнения задачи.
    """
    return await set_task_refuse(user_task, draw_refuse, current_user)
