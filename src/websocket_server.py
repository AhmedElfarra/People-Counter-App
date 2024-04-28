from fastapi import FastAPI, WebSocket, APIRouter
from starlette.responses import HTMLResponse
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
router = APIRouter()

# In-memory storage for counts
counts = {"entering": 0, "exiting": 0}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        print(f"Received data: {data}")  # Log received data
        data_dict = json.loads(data)
        counts.update(data_dict)
        await websocket.send_text("Update received")


@router.get("/counts")
async def get_counts():
    return counts

app.include_router(router)
