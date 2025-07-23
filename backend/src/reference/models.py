from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship

from src.database.base import Base


lead_repair_types = Table(
    "lead_repair_types",
    Base.metadata,
    Column("lead_id", ForeignKey("leads.id"), primary_key=True),
    Column("repair_type_id", ForeignKey("repair_types.id"), primary_key=True),
)


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)

    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)

    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="products")

    leads = relationship("Lead", back_populates="product")


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    role = Column(String, index=True)
    phone = Column(String, index=True)
    description = Column(String)

    leads = relationship("Lead", back_populates="author")


class Customer(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    phone = Column(String, index=True)
    email = Column(String, index=True)
    description = Column(String)

    leads = relationship("Lead", back_populates="customer")


class ServiceCenter(Base):
    __tablename__ = "service_centers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String, index=True)
    phone = Column(String, index=True)
    email = Column(String, index=True)
    description = Column(String)

    leads = relationship("Lead", back_populates="service_center")


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("clients.id"))
    author_id = Column(Integer, ForeignKey("authors.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    service_center_id = Column(Integer, ForeignKey("service_centers.id"))

    status = Column(String, index=True)
    description = Column(String)

    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    customer = relationship("Customer", back_populates="leads")
    author = relationship("Author", back_populates="leads")
    product = relationship("Product", back_populates="leads")
    service_center = relationship("ServiceCenter", back_populates="leads")

    tasks = relationship("Task", back_populates="lead")
    repair_types = relationship(
        "RepairTypes", secondary=lead_repair_types, back_populates="leads"
    )


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"))
    description = Column(String, index=True)
    status = Column(String, index=True)

    lead = relationship("Lead", back_populates="tasks")


class RepairTypes(Base):
    __tablename__ = "repair_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Integer, index=True)
    description = Column(String)

    leads = relationship(
        "Lead", secondary=lead_repair_types, back_populates="repair_types"
    )
