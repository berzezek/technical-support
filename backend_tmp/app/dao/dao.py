from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from typing import Generic, TypeVar, Type
from pydantic import BaseModel

from app.dao.database import Base
from app.dao.models import User, Lead
from app.dao.schemas import LeadCreate

from app.config import logger

T = TypeVar("T", bound=Base)  # ✅ SQLAlchemy Base


class BaseDAO(Generic[T]):
    model: Type[T] = None

    def __init__(self, session):
        self._session = session
        if not self.model:
            raise ValueError("Модель не указана")

    async def get_or_create(
        self, filters: BaseModel, defaults: BaseModel | None = None
    ):
        filter_dict = filters.model_dump(exclude_unset=True)
        defaults_dict = defaults.model_dump(exclude_unset=True) if defaults else {}

        try:
            stmt = select(self.model).filter_by(**filter_dict)
            result = await self._session.execute(stmt)
            instance = result.scalar_one_or_none()

            if instance:
                logger.info(f"{self.model.__name__} найден: {filter_dict}")
                return instance, False

            new_data = {**filter_dict, **defaults_dict}
            instance = self.model(**new_data)
            self._session.add(instance)
            await self._session.flush()
            logger.info(f"{self.model.__name__} создан: {new_data}")
            return instance, True

        except SQLAlchemyError as e:
            logger.error(f"Ошибка в get_or_create: {e}")
            raise

    async def add(self, values: BaseModel) -> T:
        values_dict = values.model_dump(exclude_unset=True)
        try:
            instance = self.model(**values_dict)
            self._session.add(instance)
            await self._session.flush()
            logger.info(f"{self.model.__name__} добавлен: {values_dict}")
            return instance
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при добавлении {self.model.__name__}: {e}")
            raise

    async def find_one_or_none_by_id(self, entity_id: int) -> T | None:
        stmt = select(self.model).where(self.model.id == entity_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

class UsersDAO(BaseDAO[User]):
    model = User


class LeadsDAO(BaseDAO[Lead]):
    model = Lead

    async def find_all_by_phone(self, phone: str) -> list[Lead]:
        stmt = select(self.model).where(self.model.phone == phone)
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_or_create_by_phone(self, lead_data: LeadCreate):
        """Ищет лида по номеру телефона, если не найден — создаёт"""
        from pydantic import BaseModel

        class LeadPhoneFilter(BaseModel):
            phone: str

        return await self.get_or_create(
            filters=LeadPhoneFilter(phone=lead_data.phone), defaults=lead_data
        )
