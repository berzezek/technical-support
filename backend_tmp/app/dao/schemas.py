from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum


class StatusEnum(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class LeadCreate(BaseModel):
    user_id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: str
    status: StatusEnum = StatusEnum.NEW
    description: Optional[str] = None

class LeadRead(BaseModel):
    id: int
    phone: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    description: Optional[str] = None
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = {
        "from_attributes": True,
    }

class LeadUpsert(BaseModel):
    id: Optional[int] = None
    phone: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)