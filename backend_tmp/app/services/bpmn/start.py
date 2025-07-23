from fastapi import HTTPException, status
from app.services.bpmn.initializers import client
from app.services.auth.schemas import AddUser
from app.config import logger
from .config import MAIN_PROCESS


async def main_process(phone: str, user: AddUser) -> dict:
    user_name = user.get("preferred_username", "Unknown User")
    try:
        response = await client.run_process(
            bpmn_process_id=MAIN_PROCESS,
            variables={
                "phone": phone,
                "user_name": user_name,
            },
        )
        logger.info(
            f"▶ Пользователь '{user_name}' запустил процесс '{MAIN_PROCESS}' | phone: {phone} | response: {response}"
        )
        return {
            "message": f"✅ Процесс '{MAIN_PROCESS}' успешно запущен для пользователя '{user_name}' с номером '{phone}'"
        }
    except Exception as e:
        logger.error(
            f"❌ Ошибка при запуске процесса '{MAIN_PROCESS}' для пользователя '{user_name}': {str(e)}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при запуске процесса",
        )
