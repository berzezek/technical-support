from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.api.models.author_models import Author
from app.api.schemas.author_schemas import AuthorCreate

class AuthorDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_author(self, author_data: AuthorCreate) -> Author:
        author = Author(**author_data.dict())
        self.session.add(author)
        await self.session.commit()
        await self.session.refresh(author)
        return author

    async def get_all_authors(self):
        result = await self.session.execute(select(Author))
        return result.scalars().all()
