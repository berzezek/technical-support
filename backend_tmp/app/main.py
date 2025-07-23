import asyncio
import httpx
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.openapi.utils import get_openapi

from app.services.routers import router as services_router
from app.api.routers import router as api_router
# from app.pages.router import router as pages_router

from app.config import settings
from app.services.auth.keycloak_client import KeycloakClient
from app.services.bpmn.initializers import start_workers, stop_workers

from app.services.polling.operate.services import (
    poll_process_definitions,
    poll_process_instances,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 👉 Создаем и сохраняем shared httpx клиент
    http_client = httpx.AsyncClient()
    app.state.keycloak_client = KeycloakClient(http_client)

    # 👉 Запускаем воркеры
    # await start_ws_poll_worker()
    worker_task = asyncio.create_task(start_workers())
    # process_definitions = asyncio.create_task(poll_process_definitions())
    # process_instances = asyncio.create_task(poll_process_instances())

    # 👉 Подключаем роутеры
    app.include_router(services_router)
    app.include_router(api_router)

    yield

    # 👉 Закрываем httpx клиент
    await http_client.aclose()

    # 👉 Останавливаем воркеры и сервисы
    await stop_workers(worker_task)
    # process_definitions.cancel()
    # process_instances.cancel()
    # await stop_ws_poll_worker()


app = FastAPI(lifespan=lifespan)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="FastAPI",
        version="1.0.0",
        description="Документация с авторизацией через Bearer-токен",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", [{"BearerAuth": []}])
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.exception_handler(HTTPException)
async def auth_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 401:
        return RedirectResponse(
            f"{settings.auth_url}"
            f"?client_id={settings.CLIENT_ID}"
            f"&response_type=code"
            f"&scope=openid"
            f"&redirect_uri={settings.redirect_uri}"
        )
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


origins = [
    "http://localhost:3000",  # Nuxt
    "http://127.0.0.1:3000",
]

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

