import httpx
from fastapi import HTTPException

from app.services.bpmn.utils import TokenManager
from app.services.auth.schemas import AddUser

from app.config import settings, logger

token_manager = TokenManager()


async def set_lead_info(
    user_task: str,
    lead_info: str,
    current_user: AddUser,
    is_task_need: bool = True,
):
    token = await token_manager.get_token()
    user_email = current_user.get("preferred_username", "unknown")

    url = (
        f"{settings.CAMUNDA_TASKLIST_BASE_URL_V2}/v2/user-tasks/{user_task}/completion"
    )
    payload = {
        "variables": {
            "lead_info": lead_info,
            "is_task_need": is_task_need,
            "candidate_users": [user_email],
        }
    }
    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
    if response.status_code == 204:
        logger.info(
            f"✅ User '{user_email}' completed task '{user_task}'. "
            f"Lead Info: {lead_info}. Is task needed next: {is_task_need}"
        )
        return {
            "message": f"User task '{user_task}' completed successfully by {user_email}"
        }
    else:
        logger.error(
            f"❌ Failed to complete task '{user_task}' by user '{user_email}'. "
            f"Status: {response.status_code}, Response: {response.text}"
        )
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Failed to complete task '{user_task}': {response.text}",
        )


async def set_task_options(user_task: str, draw_refuse: str, current_user: AddUser):
    token = await token_manager.get_token()
    user_email = current_user.get("preferred_username", "unknown")
    url = (
        f"{settings.CAMUNDA_TASKLIST_BASE_URL_V2}/v2/user-tasks/{user_task}/completion"
    )
    payload = {"variables": {"draw_refuse": draw_refuse}}
    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)

    if response.status_code == 204:
        logger.info(
            f"✅ User '{user_email}' completed task '{user_task}' "
            f"with options: {draw_refuse}"
        )
        return {
            "message": f"User task '{user_task}' completed successfully by {user_email}"
        }
    else:
        logger.error(
            f"❌ Failed to complete task '{user_task}' by user '{user_email}'. "
            f"Status: {response.status_code}, Response: {response.text}"
        )
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Failed to complete task '{user_task}': {response.text}",
        )


async def set_task_refuse(user_task: str, draw_refuse: dict, current_user: AddUser):
    token = await token_manager.get_token()
    user_email = current_user.get("preferred_username", "unknown")
    url = (
        f"{settings.CAMUNDA_TASKLIST_BASE_URL_V2}/v2/user-tasks/{user_task}/completion"
    )
    payload = {"variables": {"draw_refuse": draw_refuse}}
    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)

    if response.status_code == 204:
        logger.info(
            f"✅ User '{user_email}' completed task '{user_task}' with draw_refuse: {draw_refuse}"
        )
        return {
            "message": f"User task '{user_task}' completed successfully by {user_email}"
        }

    logger.error(
        f"❌ Failed to complete task '{user_task}' by user '{user_email}'. "
        f"Status: {response.status_code}, Response: {response.text}"
    )
    raise HTTPException(
        status_code=response.status_code,
        detail=f"Failed to complete task '{user_task}': {response.text}",
    )
