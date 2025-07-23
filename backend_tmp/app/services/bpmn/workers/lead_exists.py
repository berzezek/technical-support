import json

from app.dao.dao import LeadsDAO
from app.dao.database import async_session_maker
from app.dao.schemas import LeadCreate, LeadRead, LeadUpsert
from app.dao.models import Lead

from app.config import logger


async def create_lead_by_phone(phone: str) -> LeadRead:
    """Создаёт лид по номеру телефона и возвращает Pydantic-модель"""
    async with async_session_maker() as session:
        dao = LeadsDAO(session)
        lead_data = LeadCreate(phone=phone)
        lead = await dao.add(lead_data)
        if not lead:
            logger.error(f"Не удалось создать лид для телефона: {phone}")
            raise ValueError("Не удалось создать лид")

        logger.info(f"Лид создан: {lead.id} для телефона: {phone}")

        # Преобразуем в LeadRead
        return json.loads(LeadRead.model_validate(lead).model_dump_json())


async def get_leads_by_phone(phone: str) -> list[Lead]:
    async with async_session_maker() as session:
        dao = LeadsDAO(session)
        return await dao.find_all_by_phone(phone)


def normalize_update_data(data: dict) -> dict:
    """
    Удаляет пустые строки и None, чтобы не затирать поля при обновлении
    """
    return {k: v for k, v in data.items() if v not in ("", None)}


async def create_or_update_lead(data: dict) -> LeadRead:
    async with async_session_maker() as session:
        dao = LeadsDAO(session)

        filtered_data = normalize_update_data(data)
        lead_data = LeadUpsert.model_validate(filtered_data)

        if lead_data.id:
            db_lead = await dao.find_one_or_none_by_id(lead_data.id)
            if db_lead:
                update_data = normalize_update_data(
                    lead_data.model_dump(exclude={"id"}, exclude_unset=True)
                )
                for field, value in update_data.items():
                    setattr(db_lead, field, value)

                await session.flush()
                await session.refresh(db_lead)  # ✅ важно
                session.expunge(db_lead)        # ✅ отсоединяем

                logger.info(f"Лид обновлён: {db_lead.id}")
                return LeadRead.model_validate(db_lead)

        lead = await dao.add(lead_data)
        await session.commit()
        await session.refresh(lead)  # ✅ добавим и тут
        session.expunge(lead)        # ✅ тоже отсоединяем
        logger.info(f"Создан новый лид: {lead.id}")
        return LeadRead.model_validate(lead)


def service_process_lead_exists(worker_instance):
    """Регистрация обработчиков задач Lead Exists"""

    @worker_instance.task(task_type="existing_leads")
    async def existing_leads(phone: str) -> dict:
        logger.info(f"Searching for existing leads with phone: {phone}")

        async with async_session_maker() as session:
            dao = LeadsDAO(session)
            leads = await dao.find_all_by_phone(phone)

        logger.info(f"Found existing leads for phone: {phone} - {len(leads)} leads")

        # Сериализуем datetime через Pydantic -> JSON -> dict
        leads_ui = [
            {
                "label": f"{lead.phone} {lead.first_name or ''} {lead.last_name or ''}".strip(),
                "value": lead.id,
            }
            for lead in leads
        ]
        return {"existing_leads": leads_ui, "candidate_groups": ["operator"]}

    @worker_instance.task(task_type="lead_create")
    async def lead_create(updated_lead: dict) -> dict:
        """Создание нового сервиса по номеру телефона"""
        lead_obj = await create_or_update_lead(updated_lead)
        return {"lead": json.loads(lead_obj.model_dump_json())}
