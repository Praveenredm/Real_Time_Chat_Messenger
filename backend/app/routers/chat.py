from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.websocket.manager import manager
from app.core.security import decode_token

router = APIRouter()

@router.websocket("/ws/chat")
async def chat(ws: WebSocket):
    if not ws.query_params.get("token"):
        await ws.close(code=4003)
        return

    token = ws.query_params.get("token")

    try:
        data = decode_token(token)
        user_id = data.get("user_id")
        username = data.get("sub", f"User {user_id}")
    except Exception:
        await ws.close(code=4003)
        return

    await manager.connect(ws)

    try:
        while True:
            msg = await ws.receive_text()
            # In a real app, you'd fetch the username or store the message
            await manager.broadcast(f"{username}:{msg}")

    except WebSocketDisconnect:
        manager.disconnect(ws)
    except Exception as e:
        print(f"Error: {e}")
        manager.disconnect(ws)
