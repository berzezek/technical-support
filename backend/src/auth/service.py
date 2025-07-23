import httpx
from fastapi import HTTPException

from src.config import config, logger


class KeycloakClient:
    def __init__(self, client: httpx.AsyncClient | None = None):
        self.client = client or httpx.AsyncClient()

    async def get_tokens(self, code: str) -> dict:
        """Обмен authorization code на токены"""
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": config.get("REDIRECT_URI"),
            "client_id": config.get("CLIENT_ID"),
            "client_secret": config.get("CLIENT_SECRET"),
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        try:
            response = await self.client.post(
                config.get("TOKEN_URL"), data=data, headers=headers
            )
            if response.status_code != 200:
                raise HTTPException(
                    status_code=401, detail=f"Token request failed: {response.text}"
                )
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=500, detail=f"Token exchange failed: {str(e)}"
            )

    async def get_user_info(self, token: str) -> dict:
        """Получить информацию о пользователе по access_token"""
        headers = {"Authorization": f"Bearer {token}"}
        try:
            response = await self.client.get(config.get("USERINFO_URL"), headers=headers)
            if response.status_code != 200:
                raise HTTPException(
                    status_code=401, detail=f"Invalid access token: {response.text}"
                )
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=500, detail=f"Keycloak request error: {str(e)}"
            )

    async def get_token_by_password(self, username: str, password: str) -> dict:
        logger.debug(f"🔑 Запрос токена для пользователя {username} с паролем {password}")
        data = {
            "grant_type": "password",
            "username": username,
            "password": password,
            "client_id": config.get("CLIENT_ID"),
            "client_secret": config.get("CLIENT_SECRET"),
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        try:
            response = await self.client.post(
                config.get("TOKEN_URL"), data=data, headers=headers
            )
            if response.status_code != 200:
                raise HTTPException(
                    status_code=401, detail=f"Password grant failed: {response.text}"
                )
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=500, detail=f"Token request error: {str(e)}"
            )
