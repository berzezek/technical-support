import asyncio
import httpx

from src.auth.service import KeycloakClient
from src.bpmn.polling.connections import broadcast_message

from src.bpmn.polling.schemas import (
    ProcessDefinitionItemSchema,
    ProcessDefinitionSearchFilterSchema,
    ProcessInstanceSearchFilterSchema,
    ProcessInstanceSearchResponseSchema,
)
from src.config import config, logger

# TODO получать токен из логина и пароля
username = config.get("KEYCLOAK_USERNAME")
password = config.get("KEYCLOAK_PASSWORD")

OPERATE_TOKEN = None

# TODO получать токен из логина и пароля
async def set_access_token_by_keycloak(username: str, password: str) -> None:
    """Получение токена доступа через Keycloak."""
    global OPERATE_TOKEN
    keycloak_client = KeycloakClient()
    token_data = await keycloak_client.get_token_by_password(username, password)
    OPERATE_TOKEN = token_data.get("access_token", None)


async def process_definitions_search(
    filter_body: ProcessDefinitionSearchFilterSchema, token: str
) -> ProcessDefinitionItemSchema:
    """Search for process definitions using the provided filter."""
    if not OPERATE_TOKEN:
        await set_access_token_by_keycloak(username, password)
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{config.get('CAMUNDA_OPERATE_BASE_URL')}/v1/process-definitions/search",
            json=filter_body.dict(exclude_none=True),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {OPERATE_TOKEN}",
            },
        )
        response.raise_for_status()
        return ProcessDefinitionItemSchema(**response.json())


async def process_instances_search(
    filter_body: ProcessInstanceSearchFilterSchema, token: str
) -> ProcessInstanceSearchResponseSchema:
    if not OPERATE_TOKEN:
        await set_access_token_by_keycloak(username, password)
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{config.get('CAMUNDA_OPERATE_BASE_URL')}/v1/process-instances/search",
            json=filter_body.dict(exclude_none=True),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {OPERATE_TOKEN}",
            },
        )
        response.raise_for_status()
        return ProcessInstanceSearchResponseSchema(**response.json())


async def poll_process_definitions() -> None:
    """Фоновый воркер: опрашивает Camunda Operate каждые 5 секунд."""
    logger.info("🔁 Запуск воркера process_definitions")

    while True:
        try:
            # 👉 фильтр по bpmnProcessId
            search_filter = ProcessDefinitionSearchFilterSchema(
                filter={"bpmnProcessId": "Process_main", "state": "ACTIVE"}, size=10
            )
            # 👉 Получение токена (замени на свою реализацию, если нужно)
            token = config.get("OPERATE_TOKEN", "")

            # 👉 Получение данных из Operate
            result = await process_definitions_search(search_filter, token)

            await broadcast_message(
                {
                    "type": "process_definitions",
                    "data": result.dict(exclude_none=True),
                }
            )

        except Exception as e:
            logger.error(f"❌ Ошибка опроса процессов: {e}")

        await asyncio.sleep(5)


async def poll_process_instances() -> None:
    """Фоновый воркер: опрашивает Camunda Operate каждые 5 секунд."""
    logger.info("🔁 Запуск воркера process_instances")

    while True:
        try:
            # 👉 фильтр по bpmnProcessId
            search_filter = ProcessInstanceSearchFilterSchema(
                filter={"bpmnProcessId": "Process_main", "state": "ACTIVE"}, size=10
            )
            # 👉 Получение токена (замени на свою реализацию, если нужно)
            token = config.get("OPERATE_TOKEN", "")

            # 👉 Получение данных из Operate
            result = await process_instances_search(search_filter, token)

            await broadcast_message(
                {
                    "type": "process_instances",
                    "data": result.dict(exclude_none=True),
                }
            )

        except Exception as e:
            logger.error(f"❌ Ошибка опроса процессов: {e}")

        await asyncio.sleep(5)
