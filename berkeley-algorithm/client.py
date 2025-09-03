import websockets
from clock import Clock


class Client:
    def __init__(self, id):
        self.id = id
        self.clock = Clock()
        self.current_time = self.clock.randomize_clock()
        print(f"[S{self.id}] - Time: {self.clock.seconds_to_hours(self.current_time)}")

    async def connect(self):
        uri = "ws://localhost:8000"
        async with websockets.connect(uri) as websocket:
            try:
                master_time = float(await websocket.recv())
                offset = self.calculate_offset(master_time)

                await websocket.send(str(offset))
                print(f"[S{self.id}] - Offset: {round(offset / 60, 2)}")

                response = await websocket.recv()

                self.current_time = float(response) + self.current_time
                print(
                    f"[S{self.id}] - New time: {self.clock.seconds_to_hours(self.current_time)}"
                )

                await websocket.send("OK")
            except websockets.ConnectionClosedOK:
                print("Connection closed by master.")
            except Exception as e:
                print(f"Slave error: {e}")

    def calculate_offset(self, master_time):
        return self.current_time - master_time
