from fastapi import HTTPException, status
from src.bpmn.config import client
from src.bpmn.constants import MAIN_PROCESS
from src.config import logger


async def main_process(phone: str) -> dict:
    try:
        response = await client.run_process(
            bpmn_process_id=MAIN_PROCESS,
            variables={
                "phone": phone,
            },
        )
        logger.info(
            f"▶ Запущен процесс '{MAIN_PROCESS}' | phone: {phone} | response: {response}"
        )
        return {
            "message": f"✅ Процесс '{MAIN_PROCESS}' успешно запущен с номером '{phone}'"
        }
    except Exception as e:
        logger.error(f"❌ Ошибка при запуске процесса '{MAIN_PROCESS}': {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при запуске процесса",
        )
