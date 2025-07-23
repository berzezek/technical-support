from fastapi import WebSocket
from starlette.websockets import WebSocketState
from typing import List
from src.config import logger

active_connections: List[dict] = []

async def connect(websocket: WebSocket, user_id: str = None, group: str = None):
    await websocket.accept()
    active_connections.append({
        "ws": websocket,
        "user_id": user_id,
        "group": group,
    })

async def disconnect(websocket: WebSocket):
    for conn in active_connections:
        if conn["ws"] == websocket:
            active_connections.remove(conn)
            break

async def broadcast_message(message: dict, target_group: str = None, target_user_id: str = None):
    for conn in active_connections:
        ws = conn["ws"]
        if ws.application_state != WebSocketState.CONNECTED:
            continue

        if target_group and conn.get("group") != target_group:
            continue
        if target_user_id and conn.get("user_id") != target_user_id:
            continue

        try:
            await ws.send_json(message)
        except Exception as e:
            logger.warning(f"Failed to send WS message: {e}")
            await disconnect(ws)
