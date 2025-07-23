from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.schemas.author_schemas import AuthorCreate, AuthorRead
from app.api.dao.author_dao import AuthorDAO
from app.dao.database import get_session_dep

router = APIRouter(prefix="/authors", tags=["Authors"])

@router.post("/", response_model=AuthorRead)
async def create_author(
    author: AuthorCreate,
    session: AsyncSession = Depends(get_session_dep)
):
    dao = AuthorDAO(session)
    return await dao.create_author(author)

@router.get("/", response_model=list[AuthorRead])
async def get_authors(session: AsyncSession = Depends(get_session_dep)):
    dao = AuthorDAO(session)
    return await dao.get_all_authors()
