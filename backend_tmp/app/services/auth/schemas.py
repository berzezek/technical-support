from pydantic import BaseModel
from typing import Optional


class SUserId(BaseModel):
    user_id: str


class AddUser(BaseModel):
    id: str
    email: str
    email_verified: bool
    name: str
    preferred_username: str
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    groups: Optional[list[str]] = None


class AddNote(BaseModel):
    title: str
    content: str


class AddNoteWithUserId(AddNote, SUserId):
    pass
