import httpx
from fastapi import WebSocket

from app.services.auth.keycloak_client import KeycloakClient
from app.config import settings, logger


async def get_token() -> str:
    logger.debug("🔐 Получение access_token от Zeebe Authorization Server...")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            settings.ZEEBE_AUTHORIZATION_SERVER_URL,
            data={
                "grant_type": "client_credentials",
                "client_id": settings.ZEEBE_CLIENT_ID,
                "client_secret": settings.ZEEBE_CLIENT_SECRET,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

    if response.status_code != 200:
        logger.error(f"❌ Ошибка получения токена: {response.status_code}")
        logger.error(f"Ответ: {response.text}")
        raise Exception("Не удалось получить access_token")

    token = response.json()["access_token"]
    logger.debug("✅ Токен получен успешно")
    return token


async def fetch_active_tasks(filter_body: dict, token: str) -> list[dict]:
    logger.debug("📥 Запрос активных задач из Tasklist API...")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.CAMUNDA_TASKLIST_BASE_URL}/v1/tasks/search",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            json=filter_body,
        )

    if response.status_code != 200 or not response.text:
        logger.warning(f"❌ Tasklist API вернул ошибку: {response.status_code}")
        logger.debug(f"Ответ: {response.text}")
        return []

    tasks = response.json()
    logger.debug(f"✅ Найдено задач: {len(tasks)}")
    return tasks


def has_common_group(user_groups: list[str], task_groups: list[str]) -> bool:
    return bool(set(user_groups) & set(task_groups))


def filter_tasks_by_groups(tasks: list[dict], user_groups: list[str]) -> list[dict]:
    logger.debug(f"🧮 Фильтрация задач по группам: {user_groups}")
    filtered = [
        task
        for task in tasks
        if has_common_group(user_groups, task.get("candidateGroups", []))
    ]
    logger.debug(f"🔎 Найдено задач после фильтрации: {len(filtered)}")
    return filtered


async def get_token_from_query(websocket: WebSocket) -> str:
    token = websocket.query_params.get("token")
    if not token:
        logger.warning("❌ WebSocket: отсутствует токен")
        await websocket.close(code=1008, reason="Missing token")
        return None
    return token


async def get_current_user_for_ws(websocket: WebSocket) -> dict | None:
    token = websocket.query_params.get("token")
    if not token:
        logger.warning("❌ Отсутствует токен")
        return None

    keycloak: KeycloakClient = websocket.app.state.keycloak_client
    try:
        return await keycloak.get_user_info(token)
    except Exception as e:
        logger.warning(f"❌ Ошибка получения информации о пользователе: {e}")
        return None

async def fetch_active_processes(token: str, filter_body: dict = None) -> list[dict]:
    if filter_body is None:
        filter_body = {"state": "ACTIVE", "pageSize": 100}

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.CAMUNDA_OPERATE_BASE_URL}/v1/process-instances/search",
            json=filter_body,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
        )
        response.raise_for_status()
        return response.json().get("items", [])
