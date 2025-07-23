import time
import jwt
import httpx

from app.config import settings

ZEEBE_AUTHORIZATION_SERVER_URL = settings.ZEEBE_AUTHORIZATION_SERVER_URL
ZEEBE_CLIENT_ID = settings.ZEEBE_CLIENT_ID
ZEEBE_CLIENT_SECRET = settings.ZEEBE_CLIENT_SECRET


class TokenManager:
    def __init__(self):
        self.token = None
        self.exp = 0

    async def get_token(self) -> str:
        if not self.token or time.time() > self.exp - 60:
            await self._refresh_token()
        return self.token

    async def _refresh_token(self):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                ZEEBE_AUTHORIZATION_SERVER_URL,
                data={
                    "grant_type": "client_credentials",
                    "client_id": ZEEBE_CLIENT_ID,
                    "client_secret": ZEEBE_CLIENT_SECRET,
                },
            )

        data = response.json()
        self.token = data["access_token"]

        payload = jwt.decode(self.token, options={"verify_signature": False})
        self.exp = payload["exp"]
