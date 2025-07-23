from fastapi import APIRouter, WebSocket
from src.bpmn.polling.connections import connect, disconnect
from src.config import logger

router = APIRouter()

@router.websocket("/ws/tasks")
async def websocket_tasks(websocket: WebSocket):
    user_id = websocket.query_params.get("user_id")
    group = websocket.query_params.get("group")

    await connect(websocket, user_id=user_id, group=group)

    try:
        while True:
            await websocket.receive_text()
    except Exception as e:
        logger.warning(f"WebSocket error: {e}")
    finally:
        await disconnect(websocket)
