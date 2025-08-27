import asyncio
import sys
import websockets


class Process:
    def __init__(self, id: int):
        self.id = id
        self.logical_clock = 0

    async def connect(self):
        uri = f"ws://localhost:8000/message/process/{self.id}"
        async with websockets.connect(uri) as websocket:
            self.websocket = websocket

            asyncio.create_task(self.receive_message())

            while True:
                await asyncio.sleep(5)
                self.internal_event()
                await self.send_message("Mensagem periódica")

    def internal_event(self):
        self.logical_clock += 1
        print(f"[P{self.id}]: Evento interno. Relógio: {self.logical_clock}")

    async def send_message(self, message: str):
        self.logical_clock += 1
        msg = f"[Mensagem de P{self.id}]: {message}. Relógio: {self.logical_clock}"
        await self.websocket.send(msg)

    async def receive_message(self):
        async for message in self.websocket:
            clock = str(message).split("Relógio: ")
            self.logical_clock = max(self.logical_clock, int(clock[1])) + 1
            print(f"{message} | Relógio: {self.logical_clock}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        id = sys.argv[1]
        p = Process(int(id))
        asyncio.run(p.connect())
