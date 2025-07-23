from sqlalchemy import Column, Integer, String
from app.dao.database import Base

class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    role = Column(String)
    phone = Column(String)
    description = Column(String)
