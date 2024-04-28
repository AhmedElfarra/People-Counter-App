import asyncio
import websockets
import json

class WebSocketClient:
    def __init__(self, uri):
        self.uri = uri

    async def send_counts(self, entering_count, exiting_count):
        async with websockets.connect(self.uri) as websocket:
            counts = {"entering": entering_count, "exiting": exiting_count}
            await websocket.send(json.dumps(counts))

    def update_counts(self, entering_count, exiting_count):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.send_counts(entering_count, exiting_count))
