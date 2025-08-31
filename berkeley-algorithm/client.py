import websockets
from clock import Clock


class Client:
    
    current_time = 0

    def __init__(self):
        self.clock = Clock()
        self.current_time = self.clock.randomize_clock()
        print(f'Current client time: {self.clock.seconds_to_hours(self.current_time)}')

    async def connect(self):
        uri = 'ws://localhost:8000'
        async with websockets.connect(uri) as websocket:
            try:
                print("Connected to server")

                await websocket.recv()
                await websocket.send(str(self.current_time))
                response = await websocket.recv()
                self.current_time = float(response)
                print(f'New client time: {self.clock.seconds_to_hours(self.current_time)}')
            except Exception as e:
                print(f'Client error: {e}')