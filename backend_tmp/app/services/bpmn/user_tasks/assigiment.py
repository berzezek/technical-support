import httpx
from fastapi import HTTPException

from app.services.bpmn.utils import TokenManager
from app.services.auth.schemas import AddUser
from app.config import settings, logger

token_manager = TokenManager()


async def task_assignment(user_task: str, user: AddUser) -> dict:
    """Назначение задачи пользователю."""
    token = await token_manager.get_token()
    assignee = user.get("email", "unknown")

    url = (
        f"{settings.CAMUNDA_TASKLIST_BASE_URL_V2}/v2/user-tasks/{user_task}/assignment"
    )
    payload = {
        "assignee": assignee,
        "allowOverride": True,
        "action": "claim",
    }
    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)

    if response.status_code == 204:
        logger.info(f"✅ Задача '{user_task}' успешно назначена на '{assignee}'")
        return {"message": f"Task '{user_task}' assigned to '{assignee}'"}

    error_msg = (
        f"❌ Ошибка назначения задачи '{user_task}' пользователю '{assignee}': "
        f"{response.status_code} - {response.text}"
    )
    logger.error(error_msg)
    raise HTTPException(
        status_code=response.status_code,
        detail=f"Failed to assign task: {response.text}",
    )


async def task_unassignment(user_task: str, user: dict) -> dict:
    """Снятие назначения задачи."""
    token = await token_manager.get_token()
    unassignee = "unassigned@system.local"

    url = (
        f"{settings.CAMUNDA_TASKLIST_BASE_URL_V2}/v2/user-tasks/{user_task}/assignment"
    )
    payload = {
        "assignee": unassignee,
        "allowOverride": True,
        "action": "claim",
    }
    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)

    if response.status_code == 204:
        logger.info(
            f"✅ Задача '{user_task}' снята с пользователя '{user.get('name', 'unknown')}' и назначена на '{unassignee}'"
        )
        return {"message": f"Task '{user_task}' unassigned successfully"}

    error_msg = (
        f"❌ Ошибка снятия назначения задачи '{user_task}' пользователем '{user.get('name', 'unknown')}' и назанчения на '{unassignee}': "
        f"{response.status_code} - {response.text}"
    )
    logger.error(error_msg)
    raise HTTPException(
        status_code=response.status_code,
        detail=f"Failed to assign task: {response.text}",
    )
