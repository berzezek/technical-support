from datetime import datetime
from typing import Optional, List, Any

from pydantic import BaseModel, Field


# === Category ===
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: int
    products: Optional[List[Any]]

    class Config:
        orm_mode = True


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True


# === Product ===
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    category_id: int


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: int
    category: Optional[CategoryRead]

    class Config:
        orm_mode = True


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None

    class Config:
        from_attributes = True


# === Author ===
class AuthorBase(BaseModel):
    first_name: str
    last_name: str
    role: str
    phone: str
    description: Optional[str] = None


class AuthorCreate(AuthorBase):
    pass


class AuthorRead(AuthorBase):
    id: int

    class Config:
        orm_mode = True


class AuthorUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[str] = None
    phone: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True


# === Customer ===
class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    phone: str
    email: str
    description: Optional[str] = None


class CustomerCreate(CustomerBase):
    pass


class CustomerRead(CustomerBase):
    id: int

    class Config:
        from_attributes = True


class CustomerUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True


# === Service Center ===
class ServiceCenterBase(BaseModel):
    name: str
    address: str
    phone: str
    email: str
    description: Optional[str] = None


class ServiceCenterCreate(ServiceCenterBase):
    pass


class ServiceCenterRead(ServiceCenterBase):
    id: int

    class Config:
        orm_mode = True


class ServiceCenterUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True


# === Repair Type ===
class RepairTypeBase(BaseModel):
    name: str
    price: int
    description: Optional[str] = None


class RepairTypeCreate(RepairTypeBase):
    pass


class RepairTypeRead(RepairTypeBase):
    id: int

    class Config:
        orm_mode = True


class RepairTypeUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[int] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True


# === Task ===
class TaskBase(BaseModel):
    lead_id: int
    description: str
    status: str


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: int

    class Config:
        orm_mode = True


class TaskUpdate(BaseModel):
    description: Optional[str] = None
    status: Optional[str] = None

    class Config:
        from_attributes = True


# === Lead ===
class LeadBase(BaseModel):
    customer_id: int
    author_id: int
    product_id: int
    service_center_id: int
    status: str
    description: Optional[str] = None


class LeadCreate(LeadBase):
    pass


class LeadRead(LeadBase):
    id: int
    created_at: datetime
    updated_at: datetime
    customer: Optional[CustomerRead]
    author: Optional[AuthorRead]
    product: Optional[ProductRead]
    service_center: Optional[ServiceCenterRead]
    tasks: List[TaskRead] = []
    repair_types: List[RepairTypeRead] = []

    class Config:
        orm_mode = True


class LeadUpdate(BaseModel):
    customer_id: Optional[int] = None
    author_id: Optional[int] = None
    product_id: Optional[int] = None
    service_center_id: Optional[int] = None
    status: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True
