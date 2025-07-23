from pydantic import BaseModel

class AuthorBase(BaseModel):
    first_name: str
    last_name: str
    role: str
    phone: str
    description: str

class AuthorCreate(AuthorBase):
    pass

class AuthorRead(AuthorBase):
    id: int

    class Config:
        orm_mode = True
