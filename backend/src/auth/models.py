from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database.base import Base


class User(Base):
    __tablename__ = "users"  # обязательно во множественном числе

    id: Mapped[str] = mapped_column(String(36), primary_key=True)  # UUID из Keycloak
    username: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=True)
    full_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    role: Mapped[str] = mapped_column(String(50), default="operator")  # например