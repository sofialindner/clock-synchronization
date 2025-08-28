from fastapi import FastAPI, WebSocket
from typing import Dict

app = FastAPI()

processes: Dict[int, WebSocket] = {}

@app.websocket("/message/process/{process_id}")
async def chat_websocket(websocket: WebSocket, process_id: int):
    await websocket.accept()
    processes[process_id] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            print(f"[Servidor]: Recebeu de P{process_id} -> {data}")

            for pid, ws in processes.items():
                if pid != process_id:
                    await ws.send_text(data)
    except:
        processes.pop(process_id, None)
        await websocket.close()
