from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.dao.database import Base


class User(Base):
    __tablename__ = "users"  # обязательно во множественном числе

    id: Mapped[str] = mapped_column(String(36), primary_key=True)  # UUID из Keycloak
    username: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=True)
    full_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    role: Mapped[str] = mapped_column(String(50), default="operator")  # например


class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[str | None] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=True,  # ✅ теперь может быть None
    )
    user: Mapped["User"] = relationship(backref="leads", lazy="selectin")

    first_name: Mapped[str | None] = mapped_column(String(50), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(50), nullable=True)
    email: Mapped[str | None] = mapped_column(String(100), nullable=True)

    phone: Mapped[str] = mapped_column(String(15), nullable=False)

    description: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )  # Optional description
