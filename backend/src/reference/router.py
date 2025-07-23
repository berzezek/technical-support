from fastapi import APIRouter, Depends, HTTPException
from fastapi_crudrouter import SQLAlchemyCRUDRouter
from sqlalchemy.orm import Session

from src.database.db import get_session
from src.reference.models import (
    Lead,
    Task,
    Product,
    Category,
    Author,
    Customer,
    ServiceCenter,
    RepairTypes,
)
from src.reference.schemas import (
    LeadRead,
    LeadCreate,
    LeadUpdate,
    TaskRead,
    TaskCreate,
    TaskUpdate,
    ProductRead,
    ProductCreate,
    ProductUpdate,
    CategoryRead,
    CategoryCreate,
    CategoryUpdate,
    AuthorRead,
    AuthorCreate,
    AuthorUpdate,
    CustomerRead,
    CustomerCreate,
    CustomerUpdate,
    ServiceCenterRead,
    ServiceCenterCreate,
    ServiceCenterUpdate,
    RepairTypeRead,
    RepairTypeCreate,
    RepairTypeUpdate,
)

router = APIRouter()

# 📌 Подключаем каждый CRUD-роут

# === Category ===
router.include_router(
    SQLAlchemyCRUDRouter(
        schema=CategoryRead,
        create_schema=CategoryCreate,
        db_model=Category,
        db=get_session,
        prefix="categories",
    )
)


@router.patch(
    "/categories/{category_id}",
    response_model=CategoryRead,
    tags=["Categories"],
)
def patch_category(
    category_id: int,
    data: CategoryUpdate,
    db: Session = Depends(get_session),
):
    category = db.query(Category).get(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(category, key, value)

    db.commit()
    db.refresh(category)
    return category


# === Product ===
router.include_router(
    SQLAlchemyCRUDRouter(
        schema=ProductRead,
        create_schema=ProductCreate,
        db_model=Product,
        db=get_session,
        prefix="products",
    )
)


@router.patch(
    "/products/{product_id}",
    response_model=ProductRead,
    tags=["Products"],
)
def patch_product(
    product_id: int,
    data: ProductUpdate,
    db: Session = Depends(get_session),
):
    product = db.query(Product).get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product


# === Author ===
router.include_router(
    SQLAlchemyCRUDRouter(
        schema=AuthorRead,
        create_schema=AuthorCreate,
        db_model=Author,
        db=get_session,
        prefix="authors",
    )
)


@router.patch(
    "/authors/{author_id}",
    response_model=AuthorRead,
    tags=["Authors"],
)
def patch_author(
    author_id: int,
    data: AuthorUpdate,
    db: Session = Depends(get_session),
):
    author = db.query(Author).get(author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(author, key, value)

    db.commit()
    db.refresh(author)
    return author


# === Customer ===
router.include_router(
    SQLAlchemyCRUDRouter(
        schema=CustomerRead,
        create_schema=CustomerCreate,
        db_model=Customer,
        db=get_session,
        prefix="customers",
    )
)


@router.patch(
    "/customers/{customer_id}",
    response_model=CustomerRead,
    tags=["Customers"],
)
def patch_customer(
    customer_id: int,
    data: CustomerUpdate,
    db: Session = Depends(get_session),
):
    customer = db.query(Customer).get(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(customer, key, value)

    db.commit()
    db.refresh(customer)
    return customer


# === Service Center ===
router.include_router(
    SQLAlchemyCRUDRouter(
        schema=ServiceCenterRead,
        create_schema=ServiceCenterCreate,
        db_model=ServiceCenter,
        db=get_session,
        prefix="service-centers",
        tags=["Service centers"],
    )
)


@router.patch(
    "/service-centers/{service_center_id}",
    response_model=ServiceCenterRead,
    tags=["Service centers"],
)
def patch_service_center(
    service_center_id: int,
    data: ServiceCenterUpdate,
    db: Session = Depends(get_session),
):
    service_center = db.query(ServiceCenter).get(service_center_id)
    if not service_center:
        raise HTTPException(status_code=404, detail="Not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(service_center, key, value)

    db.commit()
    db.refresh(service_center)
    return service_center


# === Repair Types ===
router.include_router(
    SQLAlchemyCRUDRouter(
        schema=RepairTypeRead,
        create_schema=RepairTypeCreate,
        db_model=RepairTypes,
        db=get_session,
        prefix="repair-types",
        tags=["Repair types"],
    )
)


@router.patch(
    "/repair-types/{repair_type_id}",
    response_model=RepairTypeRead,
    tags=["Repair types"],
)
def patch_repair_type(
    repair_type_id: int,
    data: RepairTypeUpdate,
    db: Session = Depends(get_session),
):
    repair_type = db.query(RepairTypes).get(repair_type_id)
    if not repair_type:
        raise HTTPException(status_code=404, detail="Not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(repair_type, key, value)

    db.commit()
    db.refresh(repair_type)
    return repair_type


# === Lead ===
router.include_router(
    SQLAlchemyCRUDRouter(
        schema=LeadRead,
        create_schema=LeadCreate,
        db_model=Lead,
        db=get_session,
        prefix="leads",
    )
)


@router.patch(
    "/leads/{lead_id}",
    response_model=LeadRead,
    tags=["Leads"],
)
def patch_lead(
    lead_id: int,
    data: LeadUpdate,
    db: Session = Depends(get_session),
):
    lead = db.query(Lead).get(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(lead, key, value)

    db.commit()
    db.refresh(lead)
    return lead


# === Task ===
router.include_router(
    SQLAlchemyCRUDRouter(
        schema=TaskRead,
        create_schema=TaskCreate,
        db_model=Task,
        db=get_session,
        prefix="tasks",
    )
)


@router.patch(
    "/tasks/{task_id}",
    response_model=TaskRead,
    tags=["Tasks"],
)
def patch_task(
    task_id: int,
    data: TaskUpdate,
    db: Session = Depends(get_session),
):
    task = db.query(Task).get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task
