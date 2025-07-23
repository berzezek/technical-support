from fastapi import Depends, HTTPException, Request

from src.auth.service import KeycloakClient

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import async_session_maker


async def get_session_with_commit() -> AsyncGenerator[AsyncSession, None]:
    """Асинхронная сессия с автоматическим коммитом."""
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_session_without_commit() -> AsyncGenerator[AsyncSession, None]:
    """Асинхронная сессия без автоматического коммита."""
    async with async_session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()



# ✅ Получаем KeycloakClient из app.state
def get_keycloak_client(request: Request) -> KeycloakClient:
    return request.app.state.keycloak_client


# ✅ Получаем токен из cookie (None, если нет)
async def get_token_from_cookie(request: Request) -> str | None:
    return request.cookies.get("access_token")


async def get_token_from_request(request: Request) -> str | None:
    # 1. Authorization header
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.lower().startswith("bearer "):
        return auth_header[len("Bearer ") :]

    # 2. Cookie fallback
    return request.cookies.get("access_token")


async def get_current_user(
    token: str = Depends(get_token_from_request),
    keycloak: KeycloakClient = Depends(get_keycloak_client),
) -> dict:
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized: No token")

    try:
        return await keycloak.get_user_info(token)
    except HTTPException:
        raise HTTPException(status_code=401, detail="Invalid token")
