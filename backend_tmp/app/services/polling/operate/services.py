import asyncio
import httpx

from app.services.polling.connections import broadcast_message

from app.config import settings, logger
from app.services.polling.operate.schemas import (
    ProcessDefinitionItemSchema,
    ProcessDefinitionSearchFilterSchema,
    ProcessInstanceSearchFilterSchema,
    ProcessInstanceSearchResponseSchema,
)


async def process_definitions_search(
    filter_body: ProcessDefinitionSearchFilterSchema, token: str
) -> ProcessDefinitionItemSchema:
    """Search for process definitions using the provided filter."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.CAMUNDA_OPERATE_BASE_URL}/v1/process-definitions/search",
            json=filter_body.model_dump(exclude_none=True),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
        )
        response.raise_for_status()
        return ProcessDefinitionItemSchema(**response.json())


async def process_instances_search(
    filter_body: ProcessInstanceSearchFilterSchema, token: str
) -> ProcessInstanceSearchResponseSchema:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.CAMUNDA_OPERATE_BASE_URL}/v1/process-instances/search",
            json=filter_body.model_dump(exclude_none=True),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
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
            token = settings.OPERATE_TOKEN

            # 👉 Получение данных из Operate
            result = await process_definitions_search(search_filter, token)

            await broadcast_message(
                {
                    "type": "process_definitions",
                    "data": result.model_dump(exclude_none=True),
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
            token = settings.OPERATE_TOKEN

            # 👉 Получение данных из Operate
            result = await process_instances_search(search_filter, token)

            await broadcast_message(
                {
                    "type": "process_instances",
                    "data": result.model_dump(exclude_none=True),
                }
            )

        except Exception as e:
            logger.error(f"❌ Ошибка опроса процессов: {e}")

        await asyncio.sleep(5)