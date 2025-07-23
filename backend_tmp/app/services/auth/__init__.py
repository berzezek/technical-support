from typing import Callable, Awaitable, Any, List
from functools import wraps

from fastapi import Depends, Request, HTTPException
from app.services.auth.keycloak_client import KeycloakClient


def get_keycloak_client(request: Request) -> KeycloakClient:
    return request.app.state.keycloak_client


async def get_token_from_header(request: Request) -> str:
    auth = request.headers.get("Authorization")
    if not auth or not auth.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    return auth[7:]  # Убираем "Bearer "


async def get_current_user(
    token: str = Depends(get_token_from_header),
    keycloak: KeycloakClient = Depends(get_keycloak_client),
) -> dict:
    return await keycloak.get_user_info(token)


def require_roles_any(roles: List[str]):
    def decorator(endpoint_func: Callable[..., Awaitable[Any]]):
        @wraps(endpoint_func)
        async def wrapper(request: Request, *args, **kwargs):
            # 🔐 Извлечение токена
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                raise HTTPException(status_code=401, detail="Authorization header missing")
            token = auth_header.replace("Bearer ", "")

            # 📥 Получение данных пользователя
            client = KeycloakClient()
            user_info = await client.get_user_info(token)
            user_roles = user_info.get("groups", [])
            print(f"User roles: {user_roles}")

            # 🔎 Проверка на наличие хотя бы одной роли
            if not any(role in user_roles for role in roles):
                raise HTTPException(status_code=403, detail="Недостаточно прав")

            return await endpoint_func(request, *args, **kwargs)

        return wrapper
    return decorator