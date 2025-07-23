from app.config import logger
from app.services.polling.connections import broadcast_message


def notify_service(worker_instance):
    """Регистрация обработчиков задач Notifier"""

    @worker_instance.task(task_type="notify_operator")
    async def notify_operator(phone: str) -> dict:
        logger.info("Notifying operator")
        # TODO Здесь должна быть логика уведомления оператора
        await broadcast_message(
            {"text": f"Новая задача для оператора {phone}"}, target_group="operator"
        )
        return {"candidate_groups": ["operator"]}
