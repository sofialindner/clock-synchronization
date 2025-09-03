import asyncio
from clock import Clock
import websockets


class Server:
    clients = []
    current_time = 0
    
    def __init__(self):
        self.clock = Clock()
        self.current_time = self.clock.randomize_clock()
        print(f'Server time: {self.clock.seconds_to_hours(self.current_time)}')

    async def start(self):
        async with websockets.serve(self.handler, 'localhost', 8000):
            await asyncio.Future()

    async def connect(self, websocket):
        self.clients.append(websocket)

    async def handler(self, websocket):
        self.clients.append(websocket)
        try:
            await websocket.send('What is your time?')
            response = await websocket.recv()
            websocket.client_time = float(response)
            
            if all(hasattr(c, 'client_time') for c in self.clients):
                await self.berkeley_algorithm() 
        except Exception as e:
            print(f'Server error: {e}')            
        finally:
            self.clients.remove(websocket)

    async def berkeley_algorithm(self):
        if all(hasattr(c, 'client_time') for c in self.clients):

            total_time = self.current_time + sum(c.client_time for c in self.clients)
            self.current_time = total_time / (len(self.clients) + 1)
            for client in self.clients:
                await client.send(str(self.current_time))
            
            print(f'New server time: {self.clock.seconds_to_hours(self.current_time)}')
            
