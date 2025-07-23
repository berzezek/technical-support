import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.bpmn.polling.service import (
    poll_process_definitions,
    poll_process_instances,
)

from src.database.db import create_all
from src.reference.router import router as reference_router
from src.auth.router import router as auth_router
from src.bpmn.ws import router as websocket_router

from src.config import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ⏳ До старта
    logger.info("🚀 Запуск приложения...")

    # 👉 Запуск поллинга
    process_definitions = asyncio.create_task(poll_process_definitions())
    process_instances = asyncio.create_task(poll_process_instances())

    # 👉 Подключаем роутеры
    app.include_router(reference_router, prefix="/api/v1")
    app.include_router(auth_router, prefix="/api/auth")
    app.include_router(websocket_router, prefix="/bpmn")
    
    # 🏗️ Создание базы данных
    create_all()
    yield
    # 🧹 После завершения
    logger.info("👋 Завершение работы приложения...")
    process_definitions.cancel()
    process_instances.cancel()


app = FastAPI(lifespan=lifespan)

# Настройка CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
